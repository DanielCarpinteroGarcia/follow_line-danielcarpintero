# Follow Line

El objetivo es conseguir que un coche autónomo siga una línea roja y complete una vuelta al circuito en el menor tiempo posible, sin salirse de la pista.

## Funcionamiento

El programa obtiene las imágenes de la cámara del coche y utiliza OpenCV para detectar la línea roja mediante máscaras HSV. A partir de esta detección, calcula la posición de la línea respecto al centro de la imagen y corrige la dirección utilizando un **controlador PID**.

El controlador tiene tres componentes:

- **P (Proporcional):** corrige la dirección según la distancia entre la línea y el centro de la imagen.
- **I (Integral):** acumula los errores para corregir desviaciones mantenidas.
- **D (Derivativa):** tiene en cuenta cómo cambia el error para mejorar la estabilidad.

Los parámetros utilizados son Kp = 0.012, Ki = 0.00005 y Kd = 0.008.

Además de controlar la dirección, el programa ajusta la velocidad dependiendo de la posición de la línea y de si detecta una recta o una curva.

## Evolución del código

Durante el desarrollo se han realizado varias modificaciones para mejorar el seguimiento de la línea y reducir el tiempo necesario para completar una vuelta.

### 1. Primer controlador proporcional

Inicialmente, el programa detectaba la línea roja mediante una máscara HSV y calculaba su centro utilizando `cv2.moments()`.

La dirección se corregía con un controlador proporcional sencillo, multiplicando el error por una constante.

El principal problema era que el coche circulaba demasiado rápido y no conseguía seguir correctamente las curvas, por lo que terminaba saliéndose de la pista.

### 2. Mejora de la detección del rojo

Se sustituyó la máscara inicial por dos máscaras HSV que permiten detectar mejor los diferentes tonos de rojo.

También se modificó el cálculo del centro de la imagen, que inicialmente tenía un valor fijo de 320 píxeles, para obtenerlo directamente a partir de sus dimensiones.

### 3. Implementación del controlador PID

Se sustituyó el controlador proporcional por un PID completo, incorporando las componentes integral y derivativa.

También se empezó a calcular el tiempo transcurrido entre iteraciones y se limitó la velocidad angular para evitar correcciones demasiado bruscas.

Aunque el control de dirección mejoró, todavía era necesario ajustar la velocidad para afrontar las curvas.

### 4. Velocidad adaptativa

Se introdujo una velocidad variable dependiendo del error respecto al centro de la línea.

De esta manera, cuando el coche se encuentra centrado puede circular más rápido, mientras que cuando aumenta la desviación reduce su velocidad para intentar corregir la trayectoria sin salirse.

### 5. Regiones de interés y detección de rectas

Se dividió la imagen en dos zonas:

- **Zona cercana:** se utiliza para detectar la posición de la línea y calcular el error del PID.
- **Zona lejana:** permite comprobar si la línea continúa aproximadamente recta y decidir cuándo aumentar la velocidad.

Esta modificación permite aprovechar mejor los tramos rectos sin tener que mantener una velocidad elevada durante todo el circuito.

### 6. Aceleración progresiva

Se modificó el control de velocidad para evitar aceleraciones bruscas.

Cuando el coche puede aumentar su velocidad, lo hace progresivamente. En cambio, cuando necesita reducirla para afrontar una curva, la reducción se aplica inmediatamente.

También se fueron ajustando los parámetros de velocidad mediante diferentes pruebas en el simulador.

### 7. Estadísticas de rendimiento

Finalmente, se añadieron estadísticas que muestran en la consola la velocidad media ordenada y el porcentaje de iteraciones en las que el coche circula a una velocidad inferior a 8.

Esto permite analizar el comportamiento del controlador y comprobar si el coche está aprovechando realmente las velocidades configuradas.

## Resultados

Durante el desarrollo se han probado distintas configuraciones para mejorar el tiempo de vuelta.

| Prueba | Tiempo |
|---|---|
| Primera vuelta completada | 260 s |
| Primera mejora | 204 s |
| Segunda mejora | 198,42 s |
| Mejor vuelta registrada | 167,81 s |

Se ha conseguido reducir considerablemente el tiempo respecto a las primeras pruebas, aunque no siempre aumentar la velocidad ha permitido obtener mejores resultados.

En el repositorio también se incluyen capturas de pantalla de las ejecuciones.

## Ejecución

Para ejecutar el proyecto se necesita Robotics Academy (Unibotics) y el backend de robótica.

El backend se inicia con Docker:

```bash
docker run --rm -it -p 6080-6090:6080-6090 -p 7163:7163 jderobot/robotics-backend:latest
```

Después se abre el ejercicio **Follow Line**, se selecciona la conexión `Local ROS2 (Robotics Backend)` y se ejecuta el código de `code.py`.

## Conclusión

La principal dificultad de la práctica ha sido encontrar un equilibrio entre la velocidad y la precisión en las curvas.

A lo largo del desarrollo se ha pasado de un controlador proporcional bastante sencillo, que no conseguía completar el circuito, a un controlador PID con detección de rectas y velocidad adaptativa.

Las distintas modificaciones han permitido mejorar progresivamente el comportamiento del coche y reducir el tiempo de vuelta, comprobando que no basta con aumentar la velocidad, sino que también es importante detectar correctamente la línea y adaptar el movimiento a cada tramo del circuito.