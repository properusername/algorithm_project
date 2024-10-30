import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 로드 및 전처리
image_path = 'timetable_pastel.jpg'
image = Image.open(image_path)
image = image.convert('L')  # 그레이스케일로 변환
image = ImageEnhance.Contrast(image).enhance(2)  # 대비 향상
image = image.filter(ImageFilter.SHARPEN)  # 이미지 선명하게

# 요일별로 나눌 이미지 좌표 설정 (이미지의 크기에 맞게 수정 필요)
image_width, image_height = image.size
column_width = image_width // 5  # 요일 칸이 5개라고 가정

# 요일별 텍스트 저장용
days_text = {}

# '월', '화', '수', '목', '금' 순서로 요일을 리스트에 정의
days = ["월", "화", "수", "목", "금"]

# 각 요일 칸에 대해 OCR 수행
for i, day in enumerate(days):
    # 좌우 좌표 계산
    if i == 0:
        left = i * column_width + 50
        right = (i + 1) * column_width + 50
    else:
        left = i * column_width + 44
        right = (i + 1) * column_width + 44
    day_image = image.crop((left, 0, right, image_height))  # 해당 요일의 영역 자르기
    
    # OCR 수행
    text = pytesseract.image_to_string(day_image, lang='kor')
    
    # 요일별로 텍스트 저장
    days_text[day] = text.strip()

# 결과 출력
for day, text in days_text.items():
    print(f"{day}:\n{text}\n")
