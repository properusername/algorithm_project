import cv2
import numpy as np
from PIL import Image

# 이미지 로드 및 크기 조정
origin_cv = cv2.imread('timetable.jpg')

# 요일별로 이미지를 저장할 딕셔너리
cropped_images = {'월': [], '화': [], '수': [], '목': [], '금': []}
day = ['월', '화', '수', '목', '금']
width = origin_cv.shape[1]

# 색상 범위 정의
color_ranges = {
    "파랑": ([100, 100, 100], [130, 255, 255]),     
    "보라": ([130, 100, 100], [160, 255, 255]),      
    "주황": ([10, 100, 150], [19, 255, 255]),         
    "연두": ([40, 100, 100], [70, 255, 255]),        
    "빨강": ([0, 100, 100], [9, 255, 255]),         
    "노랑": ([20, 100, 100], [39, 255, 255]),        
    "청록": ([80, 100, 100], [100, 255, 255])        
}

# BGR에서 HSV로 변환
hsv = cv2.cvtColor(origin_cv, cv2.COLOR_BGR2HSV)

# 각 색상에 대해 마스크 생성 및 윤곽선 찾기
for color_name, (lower, upper) in color_ranges.items():
    lower = np.array(lower)
    upper = np.array(upper)

    # 색상 마스크 생성
    mask = cv2.inRange(hsv, lower, upper)

    # 마스크를 팽창하여 블록을 더 명확히
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    # 윤곽선 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 윤곽선에 따라 이미지 잘라내기
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # 일정 크기 이상일 때만 잘라냄 (작은 잡음 제거)
        if w > 50 and h > 50:
            cropped_image = origin_cv[y:y+h, x:x+w]
            cropped_images[day[int(x/width*5)]].append([Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)), y]) # int(x/widht*5)로 x값에 따라 들어갈 요일을 결정

# for i in range(len(cropped_images)):
#     cropped_images[i][0].show()
#     print(cropped_images[i][1])

#추출된 각 요일의 이미지 확인
for today in day:
    for i in range(len(cropped_images[today])):
        cropped_images[today][i][0].show()

        