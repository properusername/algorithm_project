import cv2
import numpy as np
from PIL import Image
import pytesseract
import re

class TimetableExtractor:
    def __init__(self, image_file):
        # 시간표 이미지
        self.image_file = cv2.imread(image_file)
        self.width = self.image_file.shape[1]

        # 요일별로 이미지를 저장할 딕셔너리
        self.cropped_images = {'월': [], '화': [], '수': [], '목': [], '금': []}
        self.days = ['월', '화', '수', '목', '금'] #딕셔너리 저장을 도울 리스트

        # 색상 범위 정의(HSV)
        self.color_ranges = {
            "파랑": ([100, 100, 100], [130, 255, 255]),     
            "보라": ([130, 100, 100], [160, 255, 255]),      
            "주황": ([10, 100, 150], [19, 255, 255]),         
            "연두": ([40, 100, 100], [70, 255, 255]),        
            "빨강": ([0, 100, 100], [9, 255, 255]),         
            "노랑": ([20, 100, 100], [39, 255, 255]),        
            "청록": ([80, 100, 100], [100, 255, 255])  
        }

        self.result = [] #최종 데이터 저장 리스트
        self.time_dict = {}  # 시간 매핑 딕셔너리

    # 각 색상 윤곽 추출 함수
    def getlectrue(self):
        hsv = cv2.cvtColor(self.image_file, cv2.COLOR_BGR2HSV)

        for color_name, (lower, upper) in self.color_ranges.items():
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
                    cropped_image = self.image_file[y:y+h, x:x+w]
                    self.cropped_images[self.days[int(x/self.width*5)]].append([Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)), y, y+h]) # int(x/widht*5)로 x값에 따라 들어갈 요일을 결정

    def show_extracted_images(self):
        # 추출된 이미지 보여주기
        for day in self.days:
            for i, (image, _,_) in enumerate(self.cropped_images[day]):
                print(self.cropped_images[day][i][2])
                #image.show()

    # 이미지에서 시간 당 픽셀 구하는 함수
    def get_pixel_per_hour(self):
        left_image = self.image_file[:,:int(self.width*0.1)]

        # pytesseract를 이용하여 이미지에서 텍스트 인식
        gray = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]

        # 시간 텍스트 추출
        custom_config = r'--oem 3 --psm 6'
        text_data = pytesseract.image_to_data(thresh, config=custom_config, output_type=pytesseract.Output.DICT)

        # y 좌표로 정렬된 시간 텍스트의 위치 찾기(예외처리 필요)
        count = 0
        time_y_positions = []
        for i, text in enumerate(text_data['text']):
            if text.strip().isdigit() and int(text) >= 9 and int(text) <= 12 and count < 2:  #좌표 얻기
                time_y_positions.append(text_data['top'][i])
                count+=1

        return abs(time_y_positions[1]-time_y_positions[0]), time_y_positions[0]
    
    # 타임 딕셔너리에 데이터 추가 함수
    def get_time_dictionary(self):
        # 픽셀 당 시간 변환 비율과 시작 픽셀 위치 가져오기
        pixel_per_hour, start_y_position = self.get_pixel_per_hour()

        # 1시간당 픽셀 수를 기준으로 15분 간격 시간값 계산
        time_interval = 15  # 15분 간격
        intervals_per_hour = 60 // time_interval
        pixels_per_interval = pixel_per_hour / intervals_per_hour

        # 시간 계산
        current_y_position = start_y_position
        current_hour = 9
        current_minute = 0

        while current_hour < 24:
            time_str = f"{current_hour:02}{current_minute:02}"
            self.time_dict[int(current_y_position)] = time_str

            # 15분 증가
            current_minute += time_interval
            if current_minute == 60:
                current_minute = 0
                current_hour += 1

            # 다음 y 위치
            current_y_position += pixels_per_interval

    # 각 요일에 대해 강의 시작/종료 시간과 강의명 저장
    def save_lecture_data(self):
        # 시간 변환 딕셔너리가 비어 있으면 생성
        if not self.time_dict:
            self.get_time_dictionary()

        # 각 요일에 대해 강의 시작/종료 시간 저장
        for day in self.days:
            for image, y, y_end in self.cropped_images[day]:
                # 강의명 추출 (이미지 전처리) -> 인식률 높이기 위해 개선 필요
                # 이미지를 흑백으로 변환
                gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                
                # 텍스트 강조: 흰색 텍스트를 검은 배경으로 반전
                _, inverted = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

                # OCR 수행 (한국어 인식 활성화)
                text = pytesseract.image_to_string(inverted, config='--psm 6 -l kor').strip()
                
                # 가장 가까운 시작 시간 및 종료 시간 찾기
                start_y = min(self.time_dict.keys(), key=lambda key: abs(key - y))
                end_y = min(self.time_dict.keys(), key=lambda key: abs(key - y_end))
                
                # 시작 시간과 종료 시간을 문자열로
                start_time = self.time_dict[start_y]
                end_time = self.time_dict[end_y]

                text = text.replace('\n','')
                text = text.replace(' ','')
                match = re.search(r'\d',text)

                course_name = text
                course_number = ''

                if match:
                    course_name = text[:match.start()]  # 숫자 이전 부분
                    course_number = text[match.start():]  # 숫자 이후 부분

                # 각 요일별로 시작/종료 시간과 강의명 추가
                self.result.append([day, course_name, start_time, end_time, course_number])

test = TimetableExtractor('../images/timetable.jpg')
test.getlectrue()
#test.show_extracted_images()
test.get_time_dictionary()
test.save_lecture_data()
print(test.result)
