import cv2
from PIL import Image

origin_cv = cv2.imread('timetable3.jpg')

origin_width = origin_cv.shape[1]

resized_cv = cv2.resize(origin_cv, (964, 1440))

full_image = resized_cv[int(52*resized_cv.shape[1]/origin_width):,int(52*resized_cv.shape[1]/origin_width):]

width = full_image.shape[1] // 5

cropped_images = {'월':[], '화':[], '수':[], '목':[], '금':[]}

day = ['월','화','수','목','금']

for i in range(5):
    if i == 0:
        image_cv = full_image[:,i*width:(i+1)*width+5]
    else:
        image_cv = full_image[:,i*width-5:(i+1)*width+5]
    # curr = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    # curr.show()

    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (7, 7), 0)
    edges = cv2.Canny(blurred_image, 50, 130)

    dilated_edges = cv2.dilate(edges, None, iterations=2)

    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w > 50 and h > 50:
            cropped_image = image_cv[y:y+h, x:x+w]
            cropped_images[day[i]].append([Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)),y])

for today in day:
    for i in range(len(cropped_images[today])):
        cropped_images[today][i][0].show()        
