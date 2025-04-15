
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
 #### 활용한 Calibration 결과 
#####  Camera Matrix (내부 파라미터)

| 파라미터 | 설명 | 값 |
|----------|------|-----|
| fx       | 초점 거리 (x 방향) | 819.1333 |
| fy       | 초점 거리 (y 방향) | 787.4159 |
| cx       | 주점의 x 좌표      | 459.2465 |
| cy       | 주점의 y 좌표      | 363.4292 |

#####  Distortion Coefficients (왜곡 계수)

`[k1, k2, p1, p2, k3]`

| 계수 | 설명            | 값         |
|------|-----------------|-------------|
| k1   | 반경 왜곡 계수 1 |  0.3516623  |
| k2   | 반경 왜곡 계수 2 | -2.1880383  |
| p1   | 접선 왜곡 계수 1 |  0.0009509  |
| p2   | 접선 왜곡 계수 2 | -0.0473972  |
| k3   | 반경 왜곡 계수 3 |  6.3331162  |

---

- 출력 영상: `Floating_YDH.avi` 

### 2. 주요 처리 단계

1. `calibration_result.npz` 파일에서 카메라 내부 파라미터(`mtx`)와 왜곡 계수(`dist`)를 불러옵니다. 이는 3D → 2D 투영 및 카메라 자세 추정을 위한 필수 요소입니다.

2. `cv2.findChessboardCorners`를 사용하여 입력된 영상에서 체스보드의 코너를 검출합니다. 이후 `cv2.cornerSubPix`를 이용해 코너 위치를 서브픽셀 수준으로 보정합니다.

3. 검출된 코너점(`imagePoints`)과 체스보드 상의 실제 3D 위치(`objectPoints`)를 대응시켜 `cv2.solvePnP()`로 카메라의 회전 벡터(`rvec`)와 이동 벡터(`tvec`)를 추정합니다. 이를 통해 카메라의 3차원 공간상 위치와 방향(pose)을 계산합니다.

4. Y, D, H 문자 각각을 3D 좌표계 상에서 선분의 집합으로 정의합니다. 각 점은 실제 공간에 존재하는 물체처럼 적절한 위치와 크기로 설정됩니다.

5. 정의된 3D 문자 좌표를 `cv2.projectPoints()`로 영상 좌표계로 투영합니다. 이때 내부 파라미터(`mtx`)와 외부 파라미터(`rvec`, `tvec`)를 사용하여 각 점을 현재 프레임 상의 2D 위치로 변환합니다.

6. `cv2.line()`을 사용하여 투영된 2D 점들을 선분으로 연결해 문자를 영상 위에 시각화합니다. Y, D, H는 각각 노랑, 주황, 보라로 구분됩니다.

7. 최종적으로 `cv2.VideoWriter()`를 이용하여 AR 텍스트가 표시된 각 프레임을 하나의 영상(`Floating_YDH.avi`)으로 저장합니다.

---

## AR " Y D H " 표시 결과 demo
> Result


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
