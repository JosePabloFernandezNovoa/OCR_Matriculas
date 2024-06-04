import re
import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
placa = []

image = cv2.imread('./imagenes/coche3.jpg')
cv2.imshow('Image', image)
cv2.moveWindow('Image', 45, 10)
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray, (2, 2))
cv2.imshow('Escala Grises', gray)
cv2.moveWindow('Escala Grises', 45, 10)
cv2.waitKey(0)

canny = cv2.Canny(gray, 20, 150)
kernel = np.ones((1, 1), np.uint8)
canny = cv2.dilate(canny, kernel, iterations=1)
cv2.imshow('Binarizado', canny)
cv2.moveWindow('Binarizado', 45, 10)
cv2.waitKey(0)

# _,cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image,cnts,-1,(0,255,0),2)

for c in cnts:
    area = cv2.contourArea(c)

    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0.07 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)

    if len(approx)==4:
        aspect_ratio = float(w)/h
        if aspect_ratio>=2.4:
            print('aspect_ratio= ', aspect_ratio)

            placa = gray[y:y + h, x:x + w]
            text = pytesseract.image_to_string(placa, config='--psm 13')
            print('PLACA: ', text)

            texto_limpio = re.sub(r'[^A-Z0-9]', '', text)

            expresion_regular = re.compile(r'^[A-Z0-9]+$')
            if expresion_regular.match(texto_limpio):
                if len(texto_limpio)>5 and len(texto_limpio)<9:
                    print("-----------------------")
                    print('PLACA: ', texto_limpio)
                    print("-----------------------")
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(image, texto_limpio, (x - 20, y - 10), 1, 2.2, (0, 255, 0), 3)

                """cv2.imshow('PLACA', placa)
                cv2.moveWindow('PLACA', 780, 10)"""


cv2.imshow('Image', image)
cv2.moveWindow('Image', 45, 10)
cv2.waitKey(0)