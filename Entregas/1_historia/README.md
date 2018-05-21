# Historia de los Sistemas Operativos

## La década de 1940
A finales de la década de 1940, con lo que se podría considerar la aparición de la primera generación de computadoras en el mundo, se accedía directamente a la consola de la computadora desde la cual se actuaba sobre una serie de micro interruptores que permitían introducir directamente el programa en la memoria de la computadora.

## La década de 1950 (Sistema Batch)
A principios de los años 50 con el objeto de facilitar la interacción entre persona y computadora, los sistemas operativos hacen una aparición discreta y bastante simple, con conceptos tales como el monitor residente, el proceso por lotes y el almacenamiento temporal.

### Monitor residente
Su funcionamiento era bastante simple, se limitaba a cargar programas a la memoria, leyéndolos de una cinta o de tarjetas perforadas, y ejecutarlos. El problema era encontrar una forma de optimizar el tiempo entre la retirada de un trabajo y el montaje del siguiente.
El primer Sistema Operativo de la historia fue creado en 1956 para un ordenador IBM 704, y básicamente lo único que hacía era comenzar la ejecución de un programa cuando el anterior terminaba.

### Almacenamiento temporal
Su objetivo era disminuir el tiempo de carga de los programas, haciendo simultánea la carga del programa o la salida de datos con la ejecución de la siguiente tarea. Para ello se utilizaban dos técnicas, el buffering y el spooling.

## La década de 1960
En los años 60 se produjeron cambios notorios en varios campos de la informática, con la aparición del circuito integrado la mayoría orientados a seguir incrementando el potencial de los ordenadores. Para ello se utilizaban técnicas de lo más diversas.

### Multiprogramación
En un sistema "multiprogramado" la memoria principal alberga a más de un programa de usuario. La CPU ejecuta instrucciones de un programa, cuando el que se encuentra en ejecución realiza una operación de E/S; en lugar de esperar a que termine la operación de E/S, se pasa a ejecutar otro programa. Si éste realiza, a su vez, otra operación de E/S, se mandan las órdenes oportunas al controlador, y pasa a ejecutarse otro. De esta forma es posible, teniendo almacenado un conjunto adecuado de tareas en cada momento, utilizar de manera óptima los recursos disponibles.

### Tiempo compartido
En este punto tenemos un sistema que hace buen uso de la electrónica disponible, pero adolece la falta de interactividad; para conseguirla debe convertirse en un sistema multiusuario, en el cual existen varios usuarios con un terminal en línea, utilizando el modo de operación de tiempo compartido. En estos sistemas igual que en la multiprogramación. Pero, a diferencia de ésta, cuando un programa lleva cierto tiempo ejecutándose el sistema operativo lo detiene para que se ejecute otra aplicación.

### Tiempo real
Estos sistemas se usan en entornos donde se deben aceptar y procesar en tiempos muy breves un gran número de sucesos, en su mayoría externos al ordenador. Si el sistema no respeta las restricciones de tiempo en las que las operaciones deben entregar su resultado se dice que ha fallado. El tiempo de respuesta a su vez debe servir para resolver el problema o hecho planteado. El procesamiento de archivos se hace de una forma continua, pues se procesa el archivo antes de que entre el siguiente, sus primeros usos fueron y siguen siendo en telecomunicaciones.

### Multiprocesador
Diseño que no se encuentran en ordenadores monoprocesador. Estos problemas derivan del hecho de que dos programas pueden ejecutarse simultáneamente y, potencialmente, pueden interferirse entre sí. Concretamente, en lo que se refiere a las lecturas y escrituras en memoria. Existen dos arquitecturas que resuelven estos problemas:

La arquitectura NUMA, donde cada procesador tiene acceso y control exclusivo a una parte de la memoria. La arquitectura SMP, donde todos los procesadores comparten toda la memoria. Esta última debe lidiar con el problema de la coherencia de caché. Cada microprocesador cuenta con su propia memoria caché local. De manera que cuando un microprocesador escribe en una dirección de memoria, lo hace únicamente sobre su copia local en caché. Si otro microprocesador tiene almacenada la misma dirección de memoria en su caché, resultará que trabaja con una copia obsoleta del dato almacenado.
Para que un multiprocesador opere correctamente necesita un sistema operativo especialmente diseñado para ello. La mayoría de los sistemas operativos actuales poseen esta capacidad.

## La década de 1970
### Sistemas operativos desarrollados
Además del Atlas Supervisor y el OS/360, los años 1970 marcaron el inicio de UNIX, a mediados de los 60 aparece Multics, sistema operativo multiusuario - multitarea desarrollado por los laboratorios Bell de AT&T y Unix, convirtiéndolo en uno de los pocos SO escritos en un lenguaje de alto nivel. En el campo de la programación lógica se dio a luz la primera implementación de Prolog, y en la revolucionaria orientación a objetos, Smalltalk.

### Inconvenientes de los Sistemas operativos
Se trataba de sistemas grandes, complejos y costosos, pues antes no se había construido nada similar y muchos de los proyectos desarrollados terminaron con costos muy por encima del presupuesto y mucho después de lo que se marcaba como fecha de la finalización. Además, aunque formaban una capa entre el hardware y el usuario, éste debía conocer un complejo lenguaje de control para realizar sus trabajos. Otro de los inconvenientes es el gran consumo de recursos que ocasionaban, debido a los grandes espacios de memoria principal y secundaria ocupados, así como el tiempo de procesador consumido. Es por esto que se intentó hacer hincapié en mejorar las técnicas ya existentes de multiprogramación y tiempo compartidos .

### Sistemas operativos desarrollados
* MULTICS (Multiplexed Information and Computing Service)
* BDOS (Basic Disk Operating System): Traductor de las instrucciones en llamadas a la BIOS.
* CP/M: (Control Program for Microcomputers) fue un sistema operativo desarrollado por Gary Kildall para el microprocesador Intel 8080 (los Intel 8085 y Zilog Z80 podían ejecutar directamente el código del 8080, aunque lo normal era que se entregara el código recompilado para el microprocesador de la máquina). Se trataba del sistema operativo más popular entre las computadoras personales en los años 70. Aunque fue modificado para ejecutarse en un IBM PC, el hecho que IBM eligiera MS-DOS, al fracasar las negociaciones con Digital Research, hizo que el uso de CP/M disminuyera hasta hacerlo desaparecer. CP/M originalmente significaba Control Program/Monitor. Más tarde fue renombrado a Control Program for Microcomputers. En la época, la barra inclinada (/) tenía el significado de "diseñado para". No obstante, Gary Kildall redefinió el significado del acrónimo poco después. CP/M se convirtió en un estándar de industria para los primeros micro-ordenadores.
El hecho de que, años después, IBM eligiera para sus PC a MS-DOS supuso su mayor fracaso, por lo que acabó desapareciendo.

## La década de 1980
Con la creación de los circuitos LSI (integración a gran escala), chips que contenían miles de transistores en un centímetro cuadrado de silicio, empezó el auge de los ordenadores personales. En éstos se dejó un poco de lado el rendimiento y se buscó más que el sistema operativo fuera amigable, surgiendo menús, e interfaces gráficas. Esto reducía la rapidez de las aplicaciones, pero se volvían más prácticos y simples para los usuarios. En esta época, siguieron utilizándose lenguajes ya existentes, como Smalltalk o C, y nacieron otros nuevos, de los cuales se podrían destacar: C++ y Eiffel dentro del paradigma de la orientación a objetos, y Haskell y Miranda en el campo de la programación declarativa. Un avance importante que se estableció a mediados de la década de 1980 fue el desarrollo de redes de computadoras personales que corrían sistemas operativos en red y sistemas operativos distribuidos. En esta escena, dos sistemas operativos eran los mayoritarios: MS-DOS (Micro Soft Disk Operating System), escrito por Microsoft para IBM PC y otras computadoras que utilizaban la CPU Intel 8088 y sus sucesores, y UNIX, que dominaba en los ordenadores personales que hacían uso del Motorola 68000.

### SunOS
SunOS fue la versión del sistema operativo derivado de Unix y BSD desarrollado por Sun Microsystems para sus estaciones de trabajo y servidores hasta el principio de los años 1990. Ésta estaba basada en los UNIX BSD con algunos añadidos de los System V UNIX en versiones posteriores.
SunOS 1.0 estaba basada básicamente en BSD 4.1 y se publicó en 1982. SunOS 2.0, que salió en 1985, usaba BSD 4.2 como una base e introducía una capa de sistema de ficheros virtual (VFS) y el protocolo NFS. SunOS 3.0 coincidía con el lanzamiento de la serie Sun-3 en 1986 e incorporaba varias utilidades de System V. SunOS 4.0, que salió en 1989, migró a la base de BSD 4.3, introdujo un nuevo sistema de memoria virtual, enlazamiento dinámico y una implementación de la arquitectura System V STREAMS I/O.

### MS-DOS
En 1981 Microsoft compró un sistema operativo llamado QDOS que, tras realizar unas pocas modificaciones, se convirtió en la primera versión de MS-DOS (Micro Soft Disk Operating System). A partir de aquí se sucedieron una serie de cambios hasta llegar a la versión 7.1, versión 8 en Windows Milenium, a partir de la cual MS-DOS dejó de existir como un componente del Sistema Operativo.

En 1983, con la aparición de los ordenadores MSX, se realizó una adaptación para este sistema que utilizaba el procesador Z-80 llamada MSX-DOS. Era un cruce entre la versión MS-DOS 1.25 y CP/M. En 1988, una vez que Microsoft se desvinculó de proyecto, ASCII Corporation publicó la versión MSX-DOS 2.0 que añadió, entre otras cosas, soporte para el uso de directorios.

### Macintosh
El lanzamiento oficial del ordenador Macintosh en enero de 1984, al precio de US $1,995 (después cambiado a $2,495 dólares)[1]. Incluía su sistema operativo Mac OS cuya características novedosas era una GUI (Graphic User Interface), Multitareas y Mouse. Provocó diferentes reacciones entre los usuarios acostumbrados a la línea de comandos y algunos tachando el uso del Mouse como juguete.

### AmigaOS
AmigaOS es el nombre que recibe el conjunto de la familia de gestores de ventanas y ROMs que incluían por defecto los ordenadores personales Commodore Amiga como sistema operativo. Fue desarrollado originalmente por Commodore International, e inicialmente presentado en 1985 junto con el Amiga 1000.

### OS/2
OS/2 es un sistema operativo de IBM que intentó suceder a DOS como sistema operativo de las computadoras personales. Se desarrolló inicialmente de manera conjunta entre Microsoft e IBM, hasta que la primera decidió seguir su camino con su Windows e IBM se ocupó en solitario de OS/2.
OS/2 ya no es comercializado por IBM, y el soporte estándar de IBM para OS / 2 se suspendió el 31 de diciembre de 2006. Se ha mantenido desde entonces con relativamente pocas nuevas características bajo el nombre eComStation.

## La década de 1990
### BeOS
BeOS es un sistema operativo para PC desarrollado por Be Incorporated en 1990, orientado principalmente a proveer alto rendimiento en aplicaciones multimedia. A pesar de la creencia común fomentada por la inclusión de la interfaz de comandos Bash en el sistema operativo, el diseño de BeOS no estaba basado en UNIX.
Originalmente (1995-1996) el sistema operativo se corría sobre su propio hardware, conocido como BeBox. Más tarde (1997) fue extendido a la plataforma PowerPC y finalmente (1998) se añadió compatibilidad con procesadores x86.

### GNU/Linux
Este sistema al parecer es una versión mejorada de Unix, basado en el estándar POSIX, un sistema que en principio trabajaba en modo comandos. Hoy en día dispone de Ventanas, gracias a un servidor gráfico y a gestores de ventanas como KDE, GNOME entre muchos. Recientemente GNU/Linux dispone de un aplicativo que convierte las ventanas en un entorno 3D como por ejemplo Beryl o Compiz. Lo que permite utilizar Linux de una forma visual atractiva.
Existen muchas distribuciones actuales de Gnu/Linux (Debian, Fedora, Ubuntu, Slackware, etc.) donde todas ellas tienen en común que ocupan el mismo núcleo Linux. Dentro de las cualidades de Gnu/Linux se puede caracterizar el hecho de que la navegación a través de la web es sin riegos de ser afectada por virus, esto debido al sistema de permisos implementado, el cual no deja correr ninguna aplicación sin los permisos necesarios, permisos que son otorgados por el usuario. A esto se suma que los virus que vienen en dispositivos desmontables tampoco afectan al sistema, debido al mismo sistema de permisos.

### Solaris
Solaris es un sistema operativo de tipo Unix desarrollado desde 1992 inicialmente por Sun Microsystems y actualmente por Oracle Corporation como sucesor de SunOS. Es un sistema certificado oficialmente como versión de Unix. Funciona en arquitecturas SPARC y x86 para servidores y estaciones de trabajo.

### Microsoft Windows NT
Windows NT es una familia de sistemas operativos producidos por Microsoft, de la cual la primera versión fue publicada en julio de 1993.
Previamente a la aparición del famoso Windows 95 la empresa Microsoft concibió una nueva línea de sistemas operativos orientados a estaciones de trabajo y servidor de red. Un sistema operativo con interfaz gráfica propia, estable y con características similares a los sistemas de red UNIX. Las letras NT provienen de la designación del producto como "Tecnología Nueva" (New Technology).
Las versiones publicadas de este sistema son: 3.1, 3.5, 3.51 y 4.0. Además, Windows NT se distribuía en dos versiones, dependiendo de la utilidad que se le fuera a dar: Workstation para ser utilizado como estación de trabajo y Server para ser utilizado como servidor.

### FreeBSD
FreeBSD es un sistema operativo multiusuario, capaz de efectuar multitarea con apropiación y multiproceso en plataformas compatibles con múltiples procesadores; el funcionamiento de FreeBSD está inspirado en la variante 4.4 BSD-Lite de UNIX. Aunque FreeBSD no puede ser propiamente llamado UNIX, al no haber adquirido la debida licencia de The Open Group, FreeBSD sí está hecho para ser compatible con la norma POSIX, al igual que varios otros sistemas "clones de UNIX".
El sistema FreeBSD incluye el núcleo, la estructura de ficheros del sistema, bibliotecas de la API de C, y algunas utilidades básicas. La versión 6.14​ trajo importantes mejoras como mayor apoyo para dispositivos Bluetooth y controladores para tarjetas de sonido y red.
La versión 7.0, lanzada el 27 de febrero de 2008, incluye compatibilidad con el sistema de archivos ZFS de Sun y a la arquitectura ARM, entre otras novedades.

### Microsoft Windows
Windows es el nombre de una familia de sistemas operativos desarrollados y vendidos por Microsoft basado en MS-DOS. Windows nunca fue realmente un Sistema Operativo con verdadero entorno gráfico hasta Windows 95. Hasta la versión 3.11 Windows fue un entorno de escritorio para MS-DOS.
Windows 95 es un sistema operativo con interfaz gráfica de usuario híbrido de entre 16 y 32 bits. Fue lanzado al mercado el 24 de agosto de 1995 por la empresa de software Microsoft con notable éxito de ventas. Durante su desarrollo se conoció como Windows 4 o por el nombre clave Chicago. Esta serie de Windows terminó con Windows Me.

### ReactOS
ReactOS (React Operating System) es un sistema operativo de código abierto destinado a lograr la compatibilidad binaria con aplicaciones de software y controladores de dispositivos hechos para Microsoft Windows NT versiones 5.x en adelante (Windows XP y sus sucesores).
En 1996 un grupo de programadores y desarrolladores de software libre comenzaron un proyecto llamado FreeWin95 el cual consistía en implementar un clon de Windows 95. El proyecto estuvo bajo discusión por el diseño del sistema ya habiendo desarrollado la capa compatible con MS-DOS, pero lamentablemente esta fue una situación que no se completó. Para 1997 el proyecto no había lanzado ninguna versión, por lo que los miembros de éste, coordinados por Jason Filby, pudieron revivirlo. Se decidió cambiar el núcleo del sistema compatible con MS-DOS y de ahora en adelante basarlo en uno compatible con Windows NT, y así el proyecto pudo seguir adelante con el nombre actual de ReactOS, que comenzó en febrero de 1998, desarrollando las bases del kernel y algunos drivers básicos.

### FreeDOS
FreeDOS es un proyecto que aspira a crear un sistema operativo libre que sea totalmente compatible con las aplicaciones y los controladores de MS-DOS.
El programa ya ha alcanzado un alto grado de madurez y tiene algunas características que no existían en MS-DOS. Algunos comandos de FreeDOS son idénticos o mejores que sus equivalentes de MS-DOS, pero aún faltan algunos del sistema operativo original.
El intérprete de línea de comandos usado por FreeDOS se llama FreeCOM.

## La década de 2000
### SymbOS
SymbOS es un sistema operativo desarrollado originalmente en 2001 para los ordenadores Amstrad CPC. Se trata de un sistema operativo gráfico con una estética e interfaz similar a Windows 95. A pesar de la baja potencia que desarrollan estos ordenadores, alrededor de 4MHz, está minuciosamente optimizado para el hardware en el cuál funciona, por lo que el rendimiento es más que aceptable.
Debido a su cuidada programación modular, ha sido migrado posteriormente a los ordenadores MSX, Amstrad PCW y Enterprise 128 que, con versiones adaptadas y recompiladas en cada caso, son capaces de ejecutar las mismas aplicaciones sin modificación alguna.
Aunque parezca un sistema obsoleto, existe una extensa comunidad implicada en el proyecto. Los programadores originales continúan actualizando y dando soporte al sistema en la actualidad.
SymbOS es un claro ejemplo de software optimizado, de tal manera que con un mínimo hardware se obtienen prestaciones similares a otros grandes sistemas operativos actuales. Esto lo convierte en el antagonista de los modernos sistemas operativos, que derrochan la mayor parte de los recursos apoyándose en la alta potencia del hardware actual.

### MorphOS
MorphOS es un sistema operativo, en parte propietario y en parte de código abierto, producido para ordenadores basados en los procesadores PowerPC (PPC). El sistema operativo en sí es propietario, pero muchas de sus bibliotecas y otros componentes son de código abierto, como Ambient (la interfaz del escritorio). La mariposa azul es el logo característico de este sistema operativo. Está basado en el Micronúcleo de Quark.

### Darwin
Darwin es el sistema que subyace en Mac OS X, cuya primera versión final salió en el año 2001 para funcionar en computadoras Macintosh.
Integra el micronúcleo XNU y servicios de sistema operativo de tipo UNIX basados en BSD 4.4 (en particular FreeBSD) que proporcionan una estabilidad y un rendimiento mayor que el de versiones anteriores de Mac OS. Se trata de una evolución del sistema operativo NEXTSTEP (basado en Mach 2.5 y código BSD 4.3) desarrollado por NeXT en 1989 comprado por Apple Computer en diciembre de 1996.
Darwin proporciona al Mac OS X prestaciones modernas, como la memoria protegida, la multitarea por desalojo o expulsiva, la gestión avanzada de memoria y el multiproceso simétrico.

### Mac OS
mac OS, antes llamado Mac OS X, es un sistema operativo basado en Unix, desarrollado, comercializado y vendido por Apple Inc.
La primera versión del sistema fue Mac OS X Server 1.0 en 1999, y en cuanto al escritorio, fue Mac OS X v10.0 «Cheetah» (publicada el 24 de marzo de 2001).
La variante para servidores, Mac OS X Server, es arquitectónicamente idéntica a su contraparte para escritorio, además de incluir herramientas para administrar grupos de trabajo y proveer acceso a los servicios de red. Estas herramientas incluyen un servidor de correo, un servidor Samba, un servidor LDAP y un servidor de dominio entre otros.

### Haiku
Haiku es un sistema operativo de código abierto actualmente en desarrollo que se centra específicamente en la informática personal y multimedia. Inspirado por BeOS (Be Operating System), Haiku aspira a convertirse en un sistema rápido, eficiente, fácil de usar y fácil de aprender, sin descuidar su potencia para los usuarios de todos los niveles.

### OpenSolaris
OpenSolaris fue un sistema operativo libre publicado en 2005 a partir de la versión privativa de Solaris de Sun Microsystems, ahora parte de Oracle Corporation. OpenSolaris es también el nombre de un proyecto iniciado en 2005 por Sun para construir y desarrollar una comunidad de usuarios alrededor de las tecnologías del sistema operativo del mismo nombre. Después de la adquisición de Sun Microsystems, en agosto de 2010, Oracle decidió interrumpir la publicación y distribución de OpenSolaris, así como su modelo de desarrollo, basado en la disponibilidad de versiones de desarrollo compiladas cada dos semanas y versiones estables cada seis meses. Sin embargo, los términos de su licencia libre no han sido modificados, por lo que el código fuente afectado por ella será publicado cuando Oracle publique nuevas versiones de Solaris.

## La década de 2010
### IllumOS
Illumos es un proyecto de software libre derivado de OpenSolaris. Fue anunciado por conferencia web desde Nueva York el 3 de agosto de 2010. El nombre del proyecto es un neologismo procedente del latín "Illum" (la luz) y de "OS" (operating system, sistema operativo).
Se trata del código base a partir del cual cualquiera podrá crear su propia distribución de software basada en el sistema operativo OpenSolaris. Pero Illumos no es una distribución, ni una bifurcación (fork), al menos por el momento, en la medida que no pretende separarse del tronco principal, sino un derivado de la "consolidación" OS/Net (más conocida como ON), que consiste básicamente en el código fuente del kernel (SunOS), los drivers, los servicios de red, las bibliotecas del sistema y los comandos básicos del sistema operativo.

### OpenIndiana
OpenIndiana es un sistema operativo tipo Unix liberado como software libre y de código abierto. Es una bifurcación de OpenSolaris concebida después de la compra de Sun Microsystems por parte de Oracle y tiene como objetivo continuar con el desarrollo y la distribución del código base de OpenSolaris. El proyecto opera bajo el patrocinio de la Illumos Foundation (Fundación Illumos). El objetivo declarado del proyecto es convertirse en la distribución de OpenSolaris de facto instalada en servidores de producción donde se requieren soluciones de seguridad y errores de forma gratuita.