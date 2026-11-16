# Follow Line

El objetivo es conseguir que un coche autónomo siga una línea roja y complete una vuelta al circuito en el menor tiempo posible, sin salirse de la pista.

## Funcionamiento

El programa obtiene las imágenes de la cámara del coche y utiliza OpenCV para detectar la línea roja mediante una máscara HSV. A partir de esta detección, calcula la posición de la línea respecto al centro de la imagen y corrige la dirección utilizando un **controlador PID**.

El controlador tiene tres componentes:

- **P (Proporcional):** corrige la dirección según la distancia entre la línea y el centro de la imagen.
- **I (Integral):** acumula los errores para corregir desviaciones mantenidas.
- **D (Derivativa):** tiene en cuenta cómo cambia el error para mejorar la estabilidad.

Los parámetros utilizados son:

- Kp = 0.012
- Ki = 0.00005
- Kd = 0.001

Además, se utiliza un filtro para suavizar la componente derivativa y reducir las oscilaciones.

La velocidad del coche también se adapta al error. Actualmente se utiliza una velocidad máxima de 12, una mínima de 3 y un factor de reducción de 0.04. Cuando aumenta la desviación respecto a la línea, el coche reduce su velocidad para intentar afrontar mejor las curvas.

## Evolución del código

Durante el desarrollo se han realizado varias modificaciones para mejorar el seguimiento de la línea y reducir el tiempo de vuelta.

### 1. Primer controlador proporcional

Inicialmente se detectaba la línea roja mediante una máscara HSV y se calculaba su centro utilizando `cv2.moments()`.

La dirección se corregía multiplicando el error por una constante. El problema era que el coche circulaba demasiado rápido y se salía en las curvas.

### 2. Mejora de la detección del rojo

Se probaron dos máscaras HSV para detectar diferentes tonos de rojo. También se modificó el cálculo del centro de la imagen, sustituyendo el valor fijo de 320 píxeles por uno calculado a partir de sus dimensiones.

### 3. Implementación del controlador PID

Se incorporaron las componentes integral y derivativa al controlador proporcional.

También se comenzó a calcular el tiempo entre iteraciones y a limitar la velocidad angular para evitar correcciones excesivas.

### 4. Velocidad adaptativa

Se introdujo una velocidad variable según el error horizontal.

De esta forma, el coche reduce la velocidad cuando se aleja del centro de la línea y puede circular más rápido cuando está mejor alineado.

### 5. Regiones de interés y detección de rectas

Se dividió la imagen en dos zonas: una cercana para calcular el error y otra lejana para detectar posibles rectas.

Esto permitía aumentar la velocidad en determinados tramos del circuito.

### 6. Aceleración progresiva

Se añadió una aceleración gradual para evitar aumentos bruscos de velocidad, manteniendo una reducción inmediata cuando el coche necesitaba afrontar una curva.

### 7. Estadísticas de rendimiento

Se incorporaron estadísticas que muestran en la consola la velocidad media ordenada y el porcentaje de iteraciones con velocidad inferior a 8.

Estos datos ayudan a comprobar cuánto se aprovechan las velocidades configuradas.

### 8. Simplificación del controlador PID

Tras varias pruebas, se comprobó que el coche seguía presentando oscilaciones y que añadir más funcionalidades no siempre mejoraba los resultados.

Por ello, se realizaron los siguientes cambios:

- Se redujo Kd de 0.008 a 0.001.
- Se añadió un filtro a la componente derivativa.
- Se volvió a utilizar el centroide de toda la imagen.
- Se eliminaron la detección de rectas y la aceleración progresiva.
- Se ajustaron las velocidades y se incorporó `Frequency.tick()`.

Con esta versión se consiguió completar una vuelta en aproximadamente **115 segundos**.

### 9. Optimización de la velocidad

Finalmente, se realizaron nuevas pruebas modificando únicamente los parámetros de velocidad, manteniendo el PID anterior.

Se aumentó la velocidad máxima hasta 12 y se redujo el factor `SPEED_REDUCTION` de 0.05 a 0.04.

Con ello, el coche reduce menos la velocidad cuando detecta pequeñas desviaciones de la línea, lo que permite mantener una velocidad mayor durante parte del recorrido.

Esta configuración ha permitido mejorar el tiempo hasta aproximadamente **104 segundos**, siendo el mejor resultado registrado hasta el momento.

## Resultados

| Prueba | Tiempo |
|---|---|
| Primera vuelta completada | 260 s |
| Primera mejora | 204 s |
| Segunda mejora | 198,42 s |
| Versión con detección de rectas | 167,81 s |
| PID simplificado | 115 s |
| Optimización de velocidad | **104 s** |

Respecto a la primera vuelta completada, se ha reducido el tiempo aproximadamente un **60 %**.

En el repositorio también se incluyen capturas de pantalla de las ejecuciones.

## Ejecución

Para ejecutar el proyecto se necesita Robotics Academy (Unibotics) y el backend de robótica.

El backend se inicia mediante Docker:

```bash
docker run --rm -it -p 6080-6090:6080-6090 -p 7163:7163 jderobot/robotics-backend:latest
```

Después se abre el ejercicio **Follow Line**, se selecciona la conexión `Local ROS2 (Robotics Backend)` y se ejecuta el código de `code.py`.

## Conclusión

La principal dificultad ha sido encontrar un equilibrio entre la velocidad y la estabilidad del coche.

Durante el desarrollo se han probado diferentes soluciones, desde un controlador proporcional sencillo hasta un PID con detección de rectas y aceleración progresiva.

Finalmente, se ha conseguido un mejor resultado simplificando el controlador, suavizando la componente derivativa y ajustando la velocidad en función del error.

Con la última configuración se ha logrado completar una vuelta en aproximadamente **104 segundos**, mejorando considerablemente los resultados iniciales.