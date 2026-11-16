
import WebGUI
import HAL
import Frequency
import cv2
import time

#Parametros del controlador PID
Kp = 0.012
Ki = 0.00005
Kd = 0.008

#Parametros para reducir la velocidad cuando el coche se aleja del centro de la linea
#para evitar que se salga en las curvas
MAX_SPEED = 12
MIN_SPEED = 4
SPEED_REDUCTION = 0.04

#Velocidad que puede alcanzar el coche cuando detecta una recta
STRAIGHT_SPEED = 16

#Variables del controlador, necesitamos almacenar informacion entre iteraciones para calcular
#las componentes integral y derivativa
previous_error = 0.0
integral = 0.0
previous_time = time.monotonic()

while True:

    #Capturar la imagen de la camara el coche mediante getImage()
    img = HAL.getImage()

    if img is None:
        HAL.setV(0)
        HAL.setW(0)
        continue

    #Convertir la imagen a HSV, para facilitar la deteccion del color rojo
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Creamos dos mascaras para combinarlas y detectar mejor la linea roja
    mask1 = cv2.inRange(hsv, (0, 125, 125), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 125, 125), (179, 255, 255))

    #Generar una mascara donde los pixeles que cumplen el rango de color aparecen en blanco
    red_mask = cv2.bitwise_or(mask1, mask2)

    #Calcular centro horizontal de la imagen
    height, width = red_mask.shape
    center = width / 2

    #Dividir la imagen en dos regiones para analizar la linea roja
    #La zona cercana se utiliza para controlar la direccion del coche
    near_roi = red_mask[int(height * 0.65):, :]
    M = cv2.moments(near_roi)

    #La zona lejana se utiliza para detectar si el coche se encuentra en una recta
    far_roi = red_mask[int(height * 0.40):int(height * 0.60), :]
    Mf = cv2.moments(far_roi)

    #Calcular el tiempo entre iteraciones. El PID debe tener en cuenta el tiempo transcurrido
    #entre actualizacion, porque la frecuencia de ejecucion puede variar
    current_time = time.monotonic()
    dt = max(current_time - previous_time, 0.001)
    previous_time = current_time

    if M["m00"] > 0:
        cX = M["m10"] / M["m00"]

        #Calcular el error respecto al centro
        error = center - cX

        #Componente proporcional
        P = Kp * error

        #Componente integral
        integral += error * dt
        integral = max(-100, min(100, integral))
        I = Ki * integral

        #Componente derivativa
        derivative = (error - previous_error) / dt
        D = Kd * derivative

        #Salida del controlador PID
        angular_velocity = P + I + D

        #Limitar la velocidad angular, evitamos velocidades angulares superiores a 3 o inferiores
        #a -3
        angular_velocity = max(-3, min(3, angular_velocity))

        #Reducir la velocidad cuando aumenta el error
        speed = MAX_SPEED - abs(error) * SPEED_REDUCTION
        speed = max(MIN_SPEED, speed)

        #Comprobar si la linea roja tambien aparece en la zona lejana
        if Mf["m00"] > 0:
            far_x = Mf["m10"] / Mf["m00"]

            #Si la linea esta centrada en ambas regiones, consideramos que es una recta
            if abs(error) < 20 and abs(far_x - cX) < 20:
                speed = STRAIGHT_SPEED

        HAL.setV(speed)
        HAL.setW(angular_velocity)

        #Guardar el error para la siguiente iteracion
        previous_error = error

    else:
        #Si no detecta la linea, se detiene el coche
        HAL.setV(0)
        HAL.setW(0)

        integral = 0
        previous_error = 0

    WebGUI.showImage(red_mask)
