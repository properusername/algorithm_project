import cv2
import numpy as np
from PIL import Image
import pytesseract

# 이미지 로드
origin_cv = cv2.imread('timetable4.jpg')
width = origin_cv.shape[1]

#이미지 왼쪽만 자르기
new_cv = origin_cv[:,:int(width*0.1)]

# cv2.imshow("d",new_cv)
# cv2.waitKey()

# pytesseract를 이용하여 이미지에서 텍스트 인식
gray = cv2.cvtColor(new_cv, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]

# 시간 텍스트 추출
custom_config = r'--oem 3 --psm 6'
text_data = pytesseract.image_to_data(thresh, config=custom_config, output_type=pytesseract.Output.DICT)

# y 좌표로 정렬된 시간 텍스트의 위치 찾기
count = 0
time_y_positions = []
for i, text in enumerate(text_data['text']):
    if text.strip().isdigit() and int(text) >= 9 and int(text) <= 12 and count < 2:  #좌표 얻기
        time_y_positions.append(text_data['top'][i])
        count+=1

# 시간당 픽셀 간격 계산
if len(time_y_positions) > 1:
    PIXELS_PER_HOUR = abs(time_y_positions[1]-time_y_positions[0])
else:
    PIXELS_PER_HOUR = 100  # 기본값으로 설정

# 시작 시간 설정
START_HOUR = 9

print(time_y_positions)
#print(PIXELS_PER_HOUR)
