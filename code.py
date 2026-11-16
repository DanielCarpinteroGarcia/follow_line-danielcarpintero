
import WebGUI
import HAL
import Frequency
import cv2
import time

#Parametros del controlador PID
Kp = 0.012
Ki = 0.00005
Kd = 0.001

#Parametros para reducir la velocidad cuando el coche se aleja del centro de la linea
#para evitar que se salga en las curvas
MAX_SPEED = 12
MIN_SPEED = 3
SPEED_REDUCTION = 0.04

#Variables del controlador, necesitamos almacenar informacion entre iteraciones para calcular
#las componentes integral y derivativa
previous_error = 0.0
integral = 0.0
previous_time = time.monotonic()
filtered_derivative = 0.0

#Variables para registrar las estadisticas de velocidad
last_report = time.monotonic()
speed_sum = 0.0
speed_samples = 0
slow_samples = 0

while True:
    Frequency.tick()

    #Capturar la imagen de la camara del coche mediante getImage()
    img = HAL.getImage()

    if img is None:
        HAL.setV(0)
        HAL.setW(0)
        continue

    #Convertir la imagen a HSV, para facilitar la deteccion del color rojo
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Generar una mascara donde los pixeles que cumplen el rango de color aparecen en blanco
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))

    #Calcular el centroide de la mascara
    M = cv2.moments(red_mask)

    #Calcular centro horizontal de la imagen
    height, width = red_mask.shape
    center = width / 2

    #Calcular el tiempo entre iteraciones
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

        #Suavizar la derivada para evitar oscilaciones
        filtered_derivative = (
            0.8 * filtered_derivative
            + 0.2 * derivative
        )

        D = Kd * filtered_derivative

        #Salida del controlador PID
        angular_velocity = P + I + D

        #Limito la velocidad angular para evitar giros excesivos
        angular_velocity = max(-3, min(3, angular_velocity))

        #Reducir la velocidad cuando aumenta el error
        speed = MAX_SPEED - abs(error) * SPEED_REDUCTION
        speed = max(MIN_SPEED, speed)

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
        filtered_derivative = 0.0
        speed = 0

    #Guardar los valores para calcular la velocidad media
    speed_sum += speed
    speed_samples += 1

    #Contar las iteraciones con velocidad inferior a 8
    if speed < 8:
        slow_samples += 1

    #Mostrar las estadisticas cada 15 segundos
    if current_time - last_report >= 15:
        avg_speed = speed_sum / max(speed_samples, 1)
        slow_pct = 100 * slow_samples / max(speed_samples, 1)

        print(
            f"Velocidad media ordenada: {avg_speed:.2f}"
            f" | Iteraciones lentas: {slow_pct:.1f}%"
        )

        last_report = current_time

    WebGUI.showImage(red_mask)
