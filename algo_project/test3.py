import cv2
import numpy as np
from PIL import Image

# 1. 이미지 로드 및 크기 조정
origin_cv = cv2.imread('timetable4.jpg')
print(origin_cv.shape)

resized_cv = cv2.resize(origin_cv, (962, 1440))
full_image = resized_cv[52:, 52:]  # 여백 제거

# 2. 요일별로 강의 칸을 저장할 딕셔너리 생성
cropped_images = {'월': [], '화': [], '수': [], '목': [], '금': []}
day = ['월', '화', '수', '목', '금']

# 3. 각 요일에 해당하는 열을 순회하며 강의 칸 추출
for i in range(5):
    image_cv = full_image[:, i * 182:(i + 1) * 182]  # 각 요일 열 분리

    # 4. RGB -> HSV 변환
    hsv_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)

    # 5. 흰색 범위 정의 (H=무의미, S=0~50, V=200~255)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 50, 255])

    # 6. 흰색 마스크 생성 및 반전 (흰색 제외)
    mask = cv2.inRange(hsv_image, lower_white, upper_white)
    non_white_mask = cv2.bitwise_not(mask)

    # 7. Dilate로 경계 강화
    dilated = cv2.dilate(non_white_mask, None, iterations=2)

    # 8. 윤곽선 검출
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 9. 윤곽선을 통해 강의 칸 이미지 자르기
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # 일정 크기 이상의 윤곽만 처리
        if w > 50 and h > 50:
            cropped_image = image_cv[y:y+h, x:x+w]
            # 자른 이미지와 y좌표를 저장
            cropped_images[day[i]].append([Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)), y])

# 10. 특정 요일(목요일)의 첫 번째 강의 이미지 출력+

for today in day:
    cropped_images[today][0][0].show()
