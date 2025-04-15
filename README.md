
# Floating Mark
### it is an AR program that projects colorful 3D letters floating above a chessboard using camera pose estimation.

**Floating_ar_chessboard.py** 
-> 카메라 캘리브레이션 결과를 이용하여, 체스보드 영상 위에 Y, D, H 문자를 3차원 공간에 띄우는 증강현실(AR) 프로그램입니다.

---

## Intro.
 OpenCV를 활용하여, 
 camera calibration 프로그램을 통해 얻은 **calibration reslut.npz**을 활용하였습니다. 
- calibration reslut.npz에서 **내부 파라미터(mtx)** 와 **왜곡 계수(dist)** 얻기 
- **체스보드의 코너 검출**을 통해 카메라의 **자세(Pose)** 를 추정
- 추정된 pose 바탕으로 **Y, D, H**를 서로 다른 색으로 **영상 상에 투영**하는 증강현실(ar) 구현

---

## 프로그램 구조

### 1. 사용한 데이터
- 입력 영상: `checkboard2.mp4`
  <-- 나의 카메라를 이용해 얻은 영상.
  

https://github.com/user-attachments/assets/2ae9bf73-e7b1-4da5-8042-e2783aa5c46c


- 캘리브레이션 결과: `calibration_result.npz`
- 출력 영상: `Floating_YDH.avi` 

### 2. 주요 처리 단계
1. `calibration_result.npz` 파일에서 mtx, dist 불러오기
2. `cv2.findChessboardCorners`로 체스보드의 코너 검출
3. `cv2.solvePnP()`로 카메라 자세 추정
4. 3D 좌표계 상의 Y, D, H 문자 정의
5. `cv2.projectPoints()`로 3D → 2D 투영
6. `cv2.line()`으로 각 문자 그리기 (색상: 노랑, 주황, 보라)
7. `cv2.VideoWriter()`로 결과 영상 저장

---

## AR " Y D H " 표시 결과 demo
> Before

https://github.com/user-attachments/assets/8b2b4dc7-07e9-418d-b93e-4dc3d2b24036

> After


https://github.com/user-attachments/assets/3926d8a8-273f-4ead-b036-d3937695d465


---

## 실행
```bash
python Floating_ar_chessboard.py
```

###  +( 전체 폴더 구성)
```
.
├── README.md
├── Floating_ar_chessboard.py
├── cvdata/
│   ├── checkboard2.mp4
│   └── Floating_YDH.avi
│   └── calibration_result.npz
│   └── Floating_YDH.mp4

```

---
