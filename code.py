
import WebGUI
import HAL
import Frequency
import cv2

# Enter sequential code!

linearVelocity = 12
err = 0

while True:
    HAL.setV(linearVelocity)

    #Capturar la imagen de la camara el coche mediante getImage()
    img = HAL.getImage()
    WebGUI.showImage(img)

    #Convertir la imagen a HSV, para facilitar la deteccion del color rojo
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Creamos dos mascaras para combinarlas y detectar mejor la linea roja
    mask1 = cv2.inRange(hsv, (0, 125, 125), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 125, 125), (179, 255, 255))

    #Generar una mascara donde los pixeles que cumplen el rango de color aparecen en blanco
    red_mask = cv2.bitwise_or(mask1, mask2)
    
    #Calcular el centroide de la máscara
    M = cv2.moments(red_mask)
    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]    
        cY = M["m01"] / M["m00"]   
    else:
        cX, cY = 0, 0

    #Calcular centro horizontal de la imagen
    height, width = red_mask.shape
    center = width / 2

    if cX > 0:
        #Calcular el error horizontal entre el centro de la camara y la linea detectada
        err = center - cX

        #Controlar la direccion aplicando una correcion proporcional al error
        HAL.setV(20)
        HAL.setW(0.01 * err)

    WebGUI.showImage(red_mask)
