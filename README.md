# Follow Line

El objetivo es conseguir que un coche autónomo siga una línea roja y complete una vuelta al circuito en el menor tiempo posible, sin salirse de la pista.

## Funcionamiento

El programa obtiene las imágenes de la cámara del coche y utiliza OpenCV para detectar la línea roja mediante máscaras HSV.

A partir de la posición de la línea, se calcula el error respecto al centro de la imagen y se utiliza un **controlador PID** para corregir la dirección.

Los parámetros utilizados son:

- Kp = 0.012
- Ki = 0.00005
- Kd = 0.008

También se han añadido algunas mejoras:

- **Velocidad adaptativa:** el coche reduce la velocidad cuando se aleja del centro de la línea.
- **Detección de rectas:** se utilizan dos zonas de la imagen para identificar cuándo puede acelerar.
- **Aceleración progresiva:** se evitan cambios bruscos de velocidad.
- **Estadísticas:** se muestra la velocidad media ordenada y el porcentaje de iteraciones a baja velocidad.

## Resultados

Durante el desarrollo se han probado distintas configuraciones para mejorar el tiempo de vuelta.

| Prueba | Tiempo |
|---|---|
| Primera vuelta completada | 260 s |
| Primera mejora | 204 s |
| Segunda mejora | 198,42 s |
| Mejor vuelta registrada | 167,81 s |

En el repositorio también se incluyen capturas de pantalla de las ejecuciones.

## Ejecución

Para ejecutar el proyecto se necesita Robotics Academy (Unibotics) y el backend de robótica.

El backend se inicia con Docker:

```bash
docker run --rm -it -p 6080-6090:6080-6090 -p 7163:7163 jderobot/robotics-backend:latest
```

Después se abre el ejercicio **Follow Line**, se selecciona la conexión `Local ROS2 (Robotics Backend)` y se ejecuta el código de `code.py`.

## Conclusión

La principal dificultad ha sido encontrar un equilibrio entre la velocidad y la precisión en las curvas.

Se ha conseguido mejorar el seguimiento de la línea pasando de un controlador proporcional sencillo a un PID con velocidad adaptativa, reduciendo considerablemente el tiempo necesario para completar el circuito.