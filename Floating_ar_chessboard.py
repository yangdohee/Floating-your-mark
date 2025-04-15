import cv2
import numpy as np

# 저번 과제의 캘리브레이션 결과 불러와 활용용
data = np.load('calibration_result.npz')
mtx = data['mtx']
dist = data['dist']

# 체스보드 설정 
chessboard_size = (10, 7)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# 영상 불러오기 (checkboard2.mp4)
cap = cv2.VideoCapture("C:/Users/dideh/OneDrive/cvdata/checkboard2.mp4")
if not cap.isOpened():
    print("[ERROR] 영상 열기 실패")
    exit()

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 결과 영상 저장 
out = cv2.VideoWriter('Floating_YDH.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (w, h))

# 글자별 색상 설정
colors = {
    'Y': (0, 255, 255),   # 노랑
    'D': (0, 165, 255),   # 주황
    'H': (255, 0, 255)    # 보라
}

# 글자별 중심 보정값 (오른쪽으로 너무 치우친 글자는 음수 보정)
centering_offsets = {
    'Y': 0.0,
    'D': 0.0,
    'H': -0.25  # H를 살짝 왼쪽으로 이동
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if found:
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
                                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

        ret, rvec, tvec = cv2.solvePnP(objp, corners2, mtx, dist)

        base_x, base_y, base_z = 3, 3, -1
        spacing = 1.1  # spacing을 약간 줄여 전체 압축
        scale = 1.0

        letters = {
            'Y': [
                [0, 0, 0], [0.5, 0.5, 0],
                [1.0, 0, 0], [0.5, 0.5, 0],
                [0.5, 0.5, 0], [0.5, 1.0, 0]
            ],
            'D': [
                [0.0, 0, 0], [0.0, 1.0, 0],
                [0.0, 0, 0], [0.5, 0.2, 0],
                [0.5, 0.2, 0], [0.5, 0.8, 0],
                [0.5, 0.8, 0], [0.0, 1.0, 0]
            ],
            'H': [
                [0.0, 0, 0], [0.0, 1.0, 0],
                [0.0, 0.5, 0], [0.5, 0.5, 0],
                [0.5, 0, 0], [0.5, 1.0, 0]
            ]
        }

        for idx, char in enumerate(['Y', 'D', 'H']):
            pts = letters[char]
            offset = base_x + idx * spacing + centering_offsets[char]
            pts3d = np.array([
                [offset + scale * x, base_y + scale * y, base_z + scale * z] for x, y, z in pts
            ], dtype=np.float32)

            imgpts, _ = cv2.projectPoints(pts3d, rvec, tvec, mtx, dist)
            imgpts = np.int32(imgpts).reshape(-1, 2)

            for i in range(0, len(imgpts), 2):
                frame = cv2.line(frame, tuple(imgpts[i]), tuple(imgpts[i+1]), colors[char], 8)

    out.write(frame)

cap.release()
out.release()
print("[INFO] Y D H (AR) 표시 완료 → Floating_YDH.avi")