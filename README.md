# Follow Line

El objetivo es conseguir que un coche autónomo siga una línea roja y complete una vuelta al circuito en el menor tiempo posible, sin salirse de la pista.

## Funcionamiento

El programa obtiene las imágenes de la cámara del coche y utiliza OpenCV para detectar la línea roja mediante una máscara HSV. A partir de esta detección, calcula la posición de la línea respecto al centro de la imagen y corrige la dirección utilizando un **controlador PID**.

El controlador tiene tres componentes:

- **P (Proporcional):** corrige la dirección según la distancia entre la línea y el centro de la imagen.
- **I (Integral):** acumula los errores para corregir desviaciones mantenidas.
- **D (Derivativa):** tiene en cuenta cómo cambia el error para mejorar la estabilidad.

Los parámetros utilizados en la versión actual son:

- Kp = 0.012
- Ki = 0.00005
- Kd = 0.001

Además, se ha añadido un filtro a la componente derivativa para suavizar las correcciones y reducir las oscilaciones del coche.

La velocidad también se adapta al error: cuanto más se aleja la línea del centro de la imagen, más se reduce la velocidad. Actualmente se utiliza una velocidad máxima de 10 y una mínima de 3.

## Evolución del código

Durante el desarrollo se han realizado varias modificaciones para mejorar el seguimiento de la línea y reducir el tiempo necesario para completar una vuelta.

### 1. Primer controlador proporcional

Inicialmente, el programa detectaba la línea roja mediante una máscara HSV y calculaba su centro utilizando `cv2.moments()`.

La dirección se corregía con un controlador proporcional sencillo, multiplicando el error por una constante.

El principal problema era que el coche circulaba demasiado rápido y no conseguía seguir correctamente las curvas, por lo que terminaba saliéndose de la pista.

### 2. Mejora de la detección del rojo

Se sustituyó la máscara inicial por dos máscaras HSV para detectar mejor los diferentes tonos de rojo.

También se modificó el cálculo del centro de la imagen, que inicialmente tenía un valor fijo de 320 píxeles, para obtenerlo directamente a partir de sus dimensiones.

### 3. Implementación del controlador PID

Se sustituyó el controlador proporcional por un PID completo, incorporando las componentes integral y derivativa.

También se empezó a calcular el tiempo transcurrido entre iteraciones y se limitó la velocidad angular para evitar correcciones excesivas.

Aunque el control de dirección mejoró, todavía era necesario ajustar la velocidad para afrontar las curvas.

### 4. Velocidad adaptativa

Se introdujo una velocidad variable dependiendo del error respecto al centro de la línea.

De esta manera, cuando el coche se encuentra centrado puede circular más rápido, mientras que cuando aumenta la desviación reduce su velocidad para intentar corregir la trayectoria sin salirse.

### 5. Regiones de interés y detección de rectas

Se dividió la imagen en dos zonas:

- **Zona cercana:** se utilizaba para detectar la posición de la línea y calcular el error del PID.
- **Zona lejana:** permitía comprobar si la línea continuaba aproximadamente recta y decidir cuándo aumentar la velocidad.

Con esta modificación se intentó aprovechar mejor los tramos rectos del circuito.

### 6. Aceleración progresiva

Se modificó el control de velocidad para evitar aceleraciones bruscas.

Cuando el coche podía aumentar su velocidad, lo hacía progresivamente. En cambio, cuando necesitaba reducirla para afrontar una curva, la reducción se aplicaba inmediatamente.

También se fueron ajustando los parámetros de velocidad mediante diferentes pruebas en el simulador.

### 7. Estadísticas de rendimiento

Se añadieron estadísticas que muestran en la consola la velocidad media ordenada y el porcentaje de iteraciones en las que el coche circula a una velocidad inferior a 8.

Esto permite analizar el comportamiento del controlador y comprobar si el coche está aprovechando realmente las velocidades configuradas.

### 8. Simplificación y mejora del controlador PID

Después de realizar varias pruebas, se observó que el coche seguía teniendo oscilaciones y que añadir más funcionalidades no siempre mejoraba los tiempos.

Por ello, se decidió volver a una versión más sencilla y realizar los siguientes cambios:

- Se redujo **Kd de 0.008 a 0.001** para disminuir la influencia de la componente derivativa.
- Se añadió un filtro a la derivada para suavizar los cambios de dirección.
- Se volvió a calcular el centroide utilizando toda la imagen, eliminando las regiones de interés.
- Se eliminaron la detección de rectas y la aceleración progresiva.
- Se ajustaron las velocidades a un máximo de 10 y un mínimo de 3.
- Se incorporó `Frequency.tick()` para regular la frecuencia del bucle.

Con estos cambios se consiguió un comportamiento más estable y se redujo el tiempo de vuelta hasta aproximadamente **115 segundos**.

Esta es la versión que se utiliza actualmente, manteniendo también las estadísticas de rendimiento.

## Resultados

Durante el desarrollo se han probado distintas configuraciones para mejorar el tiempo de vuelta.

| Prueba | Tiempo |
|---|---|
| Primera vuelta completada | 260 s |
| Primera mejora | 204 s |
| Segunda mejora | 198,42 s |
| Versión anterior | 167,81 s |
| Versión actual | **115 s** |

Se ha conseguido reducir el tiempo de vuelta aproximadamente un **56 %** respecto a la primera vuelta completada.

Las pruebas también han demostrado que aumentar la velocidad o añadir más funcionalidades no siempre mejora el resultado. En este caso, simplificar el controlador y reducir las oscilaciones ha permitido obtener un tiempo considerablemente mejor.

En el repositorio se incluyen capturas de pantalla de las ejecuciones.

## Ejecución

Para ejecutar el proyecto se necesita Robotics Academy (Unibotics) y el backend de robótica.

El backend se inicia con Docker:

```bash
docker run --rm -it -p 6080-6090:6080-6090 -p 7163:7163 jderobot/robotics-backend:latest
```

Después se abre el ejercicio **Follow Line**, se selecciona la conexión `Local ROS2 (Robotics Backend)` y se ejecuta el código de `code.py`.

## Conclusión

La principal dificultad de la práctica ha sido encontrar un equilibrio entre la velocidad y la precisión en las curvas.

A lo largo del desarrollo se ha pasado de un controlador proporcional sencillo, que no conseguía completar el circuito, a un controlador PID con velocidad adaptativa.

Se han probado diferentes mejoras, como la detección de rectas y la aceleración progresiva, pero finalmente se ha comprobado que una solución más sencilla, con la componente derivativa suavizada y unas velocidades adecuadas, ofrece mejores resultados en nuestras pruebas.

Con la última versión se ha conseguido completar una vuelta en aproximadamente **115 segundos**, mejorando considerablemente los resultados iniciales.