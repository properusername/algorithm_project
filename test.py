import cv2
import numpy as np
from PIL import Image

# 이미지 로드 및 크기 조정
origin_cv = cv2.imread('timetable.jpg')
origin_width = origin_cv.shape[1]
resized_cv = cv2.resize(origin_cv, (964, 1440))
full_image = resized_cv[int(52 * resized_cv.shape[1] / origin_width):, int(52 * resized_cv.shape[1] / origin_width):]

# 요일별로 이미지를 저장할 딕셔너리
cropped_images = {'월': [], '화': [], '수': [], '목': [], '금': []}
day = ['월', '화', '수', '목', '금']
width = full_image.shape[1] // 5

# 요일별로 이미지를 분할하여 처리
for i in range(5):
    if i == 0:
        image_cv = full_image[:, i * width:(i + 1) * width + 5]
    else:
        image_cv = full_image[:, i * width - 5:(i + 1) * width + 5]

    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)

    # 파란색과 보라색 마스크 생성
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_purple = np.array([130, 100, 100])
    upper_purple = np.array([160, 255, 255])
    purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # 각 색상 마스크를 팽창하여 블록을 더 명확히
    blue_mask = cv2.dilate(blue_mask, np.ones((3, 3), np.uint8), iterations=2)
    purple_mask = cv2.dilate(purple_mask, np.ones((3, 3), np.uint8), iterations=2)

    # 파란색과 보라색 윤곽선 찾기
    contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_purple, _ = cv2.findContours(purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 파란색 윤곽선에 따라 이미지 잘라내기
    for contour in contours_blue:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:
            cropped_image = image_cv[y:y+h, x:x+w]
            cropped_images[day[i]].append([Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)), y])

    # 보라색 윤곽선에 따라 이미지 잘라내기
    for contour in contours_purple:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:
            cropped_image = image_cv[y:y+h, x:x+w]
            cropped_images[day[i]].append([Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)), y])

# 결과 확인: 요일별로 잘라낸 이미지를 표시
for today in day:
    for i in range(len(cropped_images[today])):
        cropped_images[today][i][0].show()
