## Pelea de personajes

### General
Al ejecutar el programa, este pedirá 3 parámetros:
1. Dirección de correo a la que se enviará un resumen de la batalla. Presionar ENTER para no enviar correo.
2. Tiempo de espera después de imprimir un bloque. Está en segundos y admite valores decimales positivos incluyendo el 0. Presionar ENTER para control manual, donde se imprimirá el siguiente bloque apretando ENTER.
3. Número de peleas a imprimir. Admite valoress enteros del 0 hacia arriba. Presionar ENTER para imprimir las 5 peleas.

### Batalla
En cada batalla se enfrentan 2 equipos de 5 integrantes cada uno: Equipo azul a la izquierda y equipo rojo a la derecha.
Así, se juntan dos oponentes aleatoriamente y se simulan las 5 peleas consecutivamente.
Finalmente, el equipo que cuente con más victorias gana la batalla.

### Turno
Cada turno representa la ejecución de un ataque.
En consola se muestra una línea con la siguiente información:
- En la columna del que recibe el ataque se muestra su HP restante.
- En la columna del atacante se muestra el ataque usado y el daño causado.

### Supuestos y observaciones
- Los Health Points son indivisibles, por lo que el daño de los ataques se redondea al entero superior.
- No se usa la URL de superheroesapi.com, porque arroja error.
- Se usa un valor distinto de AS para cada stat (incluyendo HP).
- Se usan los stats reales para calcular el HP.

### Desarrollo y ejecución
#### Desarrollado y probado en Python 3.10.6 & macOS 12.5
#### Ejecución
``` python3 src/main.py ```
#### Dependencias
``` pip3 install requests email-validator ```
#### Ideas propuestas
- Habilitar la opción de usar los stats base para calcular los HP, así el FB no tendrá tanto impacto en el desarrollo de la pelea.
- Tratar de que las peleas consistan de oponentes con FB similar para que sean más interesantes.
