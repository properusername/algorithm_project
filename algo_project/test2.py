import cv2
from PIL import Image

origin_cv = cv2.imread('timetable2.jpg')

print(origin_cv.shape)

resized_cv = cv2.resize(origin_cv, (962, 1440))

full_image = resized_cv[52:,52:]

cropped_images = {'월':[], '화':[], '수':[], '목':[], '금':[]}

day = ['월','화','수','목','금']

for i in range(5):
    image_cv = full_image[:,i*182:(i+1)*182]
    # curr = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    # curr.show()

    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)

    dilated_edges = cv2.dilate(edges, None, iterations=2)

    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w > 50 and h > 50:
            cropped_image = image_cv[y:y+h, x:x+w]
            cropped_images[day[i]].append([Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)),y])

cropped_images['월'][0][0].show()