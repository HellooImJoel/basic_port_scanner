# Escáner de Puertos Simple en Python

Un proyecto educativo que demuestra los principios fundamentales detrás de herramientas profesionales de exploración de redes como Nmap, implementado completamente en Python.

## Tabla de Contenidos

1. [Propósito del Proyecto](#propósito-del-proyecto)
2. [Fundamentos Teóricos](#fundamentos-teóricos)
3. [Características Principales](#características-principales)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Guía de Uso](#guía-de-uso)
6. [Arquitectura del Código](#arquitectura-del-código)
7. [Análisis Técnico Detallado](#análisis-técnico-detallado)
8. [Comparación con Nmap](#comparación-con-nmap)
9. [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)
10. [Uso Ético y Legal](#uso-ético-y-legal)
11. [Extensiones Propuestas](#extensiones-propuestas)

## Propósito del Proyecto

Este proyecto nace con el objetivo de desmitificar el funcionamiento interno de las herramientas de exploración de redes, específicamente replicando las funcionalidades básicas de Nmap a través de una implementación educativa en Python. 

La idea central es que los conceptos detrás de herramientas aparentemente complejas como Nmap son, en realidad, aplicaciones elegantes de principios fundamentales de redes. Al construir nuestra propia versión simplificada, podemos comprender no solo cómo funcionan estas herramientas, sino también por qué funcionan de esa manera específica.

Imagina que Nmap es como un automóvil moderno con todas las características avanzadas. Nuestro proyecto es como construir un automóvil básico que te enseña los principios fundamentales de la combustión interna, la transmisión y la dirección. Aunque nuestro "automóvil" no tendrá todas las características del modelo profesional, te dará una comprensión profunda de cómo funcionan los componentes esenciales.

## Fundamentos Teóricos

### ¿Qué es un Escaneo de Puertos?

Para entender completamente qué hace nuestro escáner, necesitamos empezar por los conceptos básicos de redes. En el mundo de las comunicaciones de red, un puerto es conceptualmente similar a los canales de televisión o las frecuencias de radio. Así como diferentes estaciones de radio transmiten en diferentes frecuencias, diferentes servicios de red operan en diferentes puertos.

Cuando tu navegador web se conecta a un sitio web, no solo se conecta a la dirección IP del servidor, sino específicamente al puerto 80 (para HTTP) o 443 (para HTTPS). Es como si estuvieras llamando a una empresa grande y necesitaras marcar una extensión específica para llegar al departamento correcto.

### El Protocolo TCP y las Conexiones de Red

Nuestro escáner utiliza el protocolo TCP (Transmission Control Protocol), que es uno de los protocolos fundamentales de Internet. TCP es como un servicio de entrega confiable: antes de enviar datos, establece una "conversación" con el destino para asegurarse de que está listo para recibir información.

Este proceso de establecimiento de conexión es lo que aprovechamos para determinar si un puerto está abierto. Cuando intentamos conectarnos a un puerto específico, pueden ocurrir tres escenarios principales:

**Puerto Abierto**: El servicio en el puerto responde positivamente, estableciendo una conexión completa. Es como tocar una puerta y que alguien la abra y te invite a pasar.

**Puerto Cerrado**: El sistema objetivo responde, pero indica que no hay ningún servicio escuchando en ese puerto. Es como tocar una puerta y que alguien te diga desde adentro que ese no es el departamento correcto.

**Puerto Filtrado**: No recibimos respuesta alguna, lo que generalmente indica que un firewall o sistema de filtrado está bloqueando nuestra solicitud. Es como tocar una puerta y no obtener respuesta alguna, sin saber si hay alguien adentro o si la puerta está bloqueada.

### Concurrencia y Optimización de Rendimiento

Una de las características que hace efectivas a las herramientas profesionales de escaneo es su capacidad para examinar múltiples puertos simultáneamente. Si tuviéramos que escanear 1000 puertos uno por uno, esperando la respuesta de cada uno antes de continuar con el siguiente, el proceso sería extremadamente lento.

Nuestro escáner implementa concurrencia utilizando múltiples hilos de ejecución. Piensa en esto como tener varios asistentes trabajando en paralelo: mientras uno está verificando el puerto 80, otro puede estar verificando el puerto 443, y un tercero puede estar examinando el puerto 22. Esta paralelización puede reducir dramáticamente el tiempo total de escaneo.

## Características Principales

### Escaneo de Puertos TCP

La funcionalidad central de nuestro escáner es la capacidad de determinar qué puertos TCP están abiertos en un sistema objetivo. Implementamos esto creando conexiones socket individuales a cada puerto que queremos examinar.

El proceso es elegantemente simple pero técnicamente sofisticado: para cada puerto, creamos un nuevo socket TCP, configuramos un tiempo límite apropiado para evitar esperas indefinidas, intentamos establecer una conexión, e interpretamos el resultado para determinar el estado del puerto.

### Identificación Básica de Servicios

Una vez que identificamos un puerto abierto, nuestro escáner intenta proporcionar información contextual sobre qué servicio podría estar ejecutándose en ese puerto. Mantenemos un diccionario interno de asociaciones comunes entre números de puerto y servicios conocidos.

Es importante entender que esta identificación es probabilística y se basa en convenciones estándar, no en análisis profundo del servicio. Por ejemplo, si encontramos el puerto 80 abierto, asumimos que probablemente es un servidor web HTTP, aunque técnicamente cualquier servicio podría configurarse para usar ese puerto.

### Verificación de Disponibilidad del Host

Antes de comenzar un escaneo extensivo de puertos, nuestro escáner implementa una verificación básica de disponibilidad del host objetivo. Esto previene que malgastemos tiempo escaneando un sistema que no está respondiendo a ninguna comunicación de red.

Nuestra implementación de "ping" es diferente del ping tradicional ICMP. En su lugar, intentamos establecer conexiones TCP a puertos comúnmente disponibles como 80 y 443. Esta aproximación es más confiable en entornos donde el ICMP podría estar bloqueado por firewalls.

### Flexibilidad en la Especificación de Puertos

El escáner acepta múltiples formatos para especificar qué puertos examinar, proporcionando flexibilidad según las necesidades del usuario. Puedes especificar un rango continuo de puertos, una lista de puertos específicos, o un puerto individual.

Esta flexibilidad es crucial porque diferentes situaciones requieren diferentes estrategias de escaneo. Un administrador de sistema podría querer verificar solo los puertos de servicios críticos, mientras que un auditor de seguridad podría necesitar un escaneo más exhaustivo.

## Instalación y Configuración

### Requisitos del Sistema

Este proyecto está diseñado para ser completamente autocontenido, utilizando únicamente bibliotecas que vienen incluidas con Python 3.6 o superior. Esta decisión de diseño garantiza que el código pueda ejecutarse en prácticamente cualquier sistema que tenga Python instalado, sin necesidad de gestionar dependencias externas.

Las bibliotecas utilizadas incluyen `socket` para comunicaciones de red, `threading` y `concurrent.futures` para manejo de concurrencia, `argparse` para procesamiento de argumentos de línea de comandos, y `datetime` para registro de tiempo de ejecución.

### Instalación

```bash
# Clona o descarga el archivo basic_port_scanner.py
# No se requieren instalaciones adicionales si tienes Python 3.6+

# Verifica tu versión de Python
python3 --version

# Otorga permisos de ejecución (en sistemas Unix/Linux)
chmod +x basic_port_scanner.py
```

### Configuración Opcional

Aunque el escáner funciona sin configuración adicional, hay algunos aspectos del sistema que pueden afectar su comportamiento:

**Límites de Descriptores de Archivo**: En sistemas Unix/Linux, el número máximo de conexiones simultáneas puede estar limitado por la configuración de descriptores de archivo del sistema. Si planeas usar un número muy alto de hilos, podrías necesitar ajustar estos límites.

**Configuración de Firewall**: Si estás ejecutando el escáner en un sistema con firewall activo, asegúrate de que permite conexiones TCP salientes a los puertos que planeas escanear.

## Guía de Uso

### Sintaxis Básica

```bash
python3 scanner.py [host] [opciones]
```

### Ejemplos Prácticos

**Escaneo básico de un sitio web:**
```bash
python3 scanner.py google.com
```
Este comando escaneará los primeros 100 puertos del servidor de Google, lo cual es útil para obtener una vista general rápida de los servicios disponibles públicamente.

**Escaneo de un rango específico de puertos:**
```bash
python3 scanner.py 192.168.1.1 -p 1-1000
```
Este ejemplo escanea los primeros 1000 puertos de un router doméstico típico, útil para auditoria de seguridad en redes domésticas.

**Escaneo de puertos específicos:**
```bash
python3 scanner.py localhost -p 22,80,443,3389,5432
```
Aquí estamos verificando servicios específicos en el sistema local: SSH, HTTP, HTTPS, RDP, y PostgreSQL.

**Escaneo con configuración personalizada:**
```bash
python3 scanner.py example.com -p 1-5000 --timeout 2 --threads 100
```
Este comando aumenta tanto el timeout como el número de hilos para un escaneo más exhaustivo pero potencialmente más lento.

### Interpretación de Resultados

El escáner proporciona salida estructurada que incluye información sobre cada puerto abierto encontrado. La salida típica incluye el número de puerto, el servicio identificado (basado en convenciones estándar), y el estado confirmado.

Cuando el escáner reporta un puerto como "abierto," significa que logró establecer una conexión TCP completa con ese puerto. Esto es una indicación muy confiable de que hay un servicio activo escuchando en ese puerto.

Los puertos reportados como "filtrados" son aquellos donde nuestra solicitud de conexión no recibió respuesta dentro del tiempo límite configurado. Esto generalmente indica la presencia de un firewall o sistema de filtrado de red.

## Arquitectura del Código

### Estructura de Clases

El código está organizado alrededor de una clase principal `SimplePortScanner` que encapsula toda la funcionalidad de escaneo. Esta aproximación orientada a objetos facilita la organización del código y permite una fácil extensión de funcionalidades.

La clase mantiene estado interno sobre el host objetivo, configuración de tiempo límite, y resultados de escaneo. Esto permite que diferentes métodos de la clase trabajen con información compartida de manera coherente.

### Métodos Principales

**`__init__(self, target_host, timeout=1)`**: El constructor de la clase se encarga de la configuración inicial y validación. Uno de los aspectos más importantes es la resolución de nombres DNS, convirtiendo nombres de host como "google.com" en direcciones IP numéricas que pueden ser usadas para conexiones de red.

**`scan_port(self, port)`**: Este es el corazón técnico del escáner. Crea un socket TCP, configura el tiempo límite, intenta establecer una conexión, e interpreta los resultados. La implementación utiliza un context manager (`with` statement) para garantizar que los sockets se cierren apropiadamente, evitando leaks de recursos.

**`scan_range(self, start_port, end_port, max_threads=50)`**: Coordina el escaneo de múltiples puertos utilizando un pool de hilos. Esta función demuestra cómo la concurrencia puede ser manejada de manera elegante en Python utilizando `ThreadPoolExecutor`.

**`get_service_name(self, port)`**: Proporciona identificación básica de servicios basada en un diccionario interno de asociaciones puerto-servicio. Esta función podría ser extendida para incluir más servicios o para realizar identificación más sofisticada.

**`ping_host(self)`**: Implementa una verificación básica de disponibilidad del host. A diferencia del ping ICMP tradicional, utiliza intentos de conexión TCP a puertos comunes, lo que es más confiable en entornos de red modernos donde ICMP podría estar bloqueado.

### Manejo de Concurrencia

La implementación de concurrencia es uno de los aspectos más sofisticados del código. Utilizamos `ThreadPoolExecutor` de la biblioteca `concurrent.futures`, que proporciona una interfaz de alto nivel para ejecutar código en paralelo.

El número de hilos concurrentes es configurable, lo que permite balancear entre velocidad de escaneo y uso de recursos del sistema. Demasiados hilos pueden sobrecargar el sistema objetivo o resultar en limitación por parte de firewalls, mientras que muy pocos hilos harán el escaneo innecesariamente lento.

### Procesamiento de Argumentos

El script utiliza `argparse` para proporcionar una interfaz de línea de comandos profesional. Esto incluye ayuda automática, validación de argumentos, y mensajes de error informativos.

La flexibilidad en la especificación de puertos se maneja a través de lógica de parsing que puede interpretar rangos, listas, o puertos individuales. Este parsing demuestra cómo hacer interfaces de usuario flexibles y amigables.

## Análisis Técnico Detallado

### Comunicación de Red a Bajo Nivel

En el nivel más fundamental, nuestro escáner utiliza la interfaz de sockets de Berkeley, que es el estándar de facto para programación de red en sistemas Unix-like y Windows. Cuando creamos un socket con `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`, estamos especificando que queremos usar IPv4 (`AF_INET`) y TCP (`SOCK_STREAM`).

El método `connect_ex()` es particularmente interesante desde una perspectiva técnica. A diferencia del método `connect()` estándar, que lanza una excepción cuando la conexión falla, `connect_ex()` devuelve un código de error numérico. Esto nos permite distinguir entre diferentes tipos de fallas de conexión sin tener que manejar múltiples tipos de excepciones.

### Gestión de Timeouts y Recursos

La configuración de timeout es crítica para el rendimiento del escáner. Un timeout demasiado corto puede resultar en falsos negativos, donde puertos abiertos son reportados como cerrados debido a latencia de red o carga del servidor. Un timeout demasiado largo hace que el escaneo sea innecesariamente lento.

Nuestro valor por defecto de 1 segundo representa un balance razonable para la mayoría de escenarios de red local, pero puede necesitar ajuste para redes de alta latencia o sistemas sobrecargados.

El uso de context managers (`with` statements) para manejo de sockets garantiza que los recursos de red se liberen apropiadamente, incluso si ocurren errores durante el escaneo. Esto previene leaks de descriptores de archivo que podrían agotar los recursos del sistema.

### Paralelización y Rendimiento

La paralelización en nuestro escáner utiliza threading en lugar de multiprocessing. Esta decisión está basada en la naturaleza I/O-bound de las operaciones de red. Cuando un hilo está esperando una respuesta de red, otros hilos pueden estar trabajando productivamente, maximizando la utilización de recursos.

Python's Global Interpreter Lock (GIL) normalmente limitaría la efectividad del threading para operaciones CPU-intensive, pero las operaciones de red liberan el GIL, permitiendo paralelización efectiva.

### Identificación de Servicios

Nuestra aproximación a la identificación de servicios es simplista pero efectiva para casos básicos. Mantenemos un diccionario de asociaciones puerto-servicio basado en asignaciones estándar de IANA (Internet Assigned Numbers Authority).

Una implementación más sofisticada podría incluir "banner grabbing", donde enviamos solicitudes específicas a puertos abiertos y analizamos las respuestas para identificar servicios y versiones específicas. Esto requeriría conocimiento específico de protocolos individuales pero proporcionaría información mucho más detallada.

## Comparación con Nmap

### Similitudes Fundamentales

Nuestro escáner comparte varios principios fundamentales con Nmap. Ambos utilizan sockets TCP para establecer conexiones, ambos pueden operar en múltiples puertos simultáneamente, y ambos interpretan las respuestas de conexión para determinar el estado de los puertos.

La estructura básica de "enviar solicitud, esperar respuesta, interpretar resultado" es idéntica entre ambas herramientas. Esta similitud demuestra que los conceptos fundamentales de exploración de red son consistentes independientemente de la complejidad de la implementación.

### Diferencias en Sofisticación

Nmap implementa docenas de técnicas de escaneo diferentes, cada una optimizada para escenarios específicos o para evadir diferentes tipos de sistemas de detección. Nuestro escáner utiliza únicamente TCP connect scanning, que es la técnica más básica pero también la más detectable.

**Técnicas de Escaneo Avanzadas**: Nmap puede realizar SYN scanning (half-open scanning), que es más sigiloso pero requiere privilegios de administrador. También puede realizar UDP scanning, que es técnicamente más complejo debido a la naturaleza sin conexión del protocolo UDP.

**Detección de Sistema Operativo**: Nmap puede identificar sistemas operativos analizando características específicas de cómo diferentes sistemas implementan el stack TCP/IP. Esta "fingerprinting" requiere una base de datos extensa de firmas de sistemas y algoritmos sofisticados de análisis.

**Evasión y Stealth**: Nmap incluye numerosas técnicas para evitar detección por sistemas de seguridad, incluyendo fragmentación de paquetes, timing personalizado, y uso de direcciones de origen falsificadas.

**Scripting Engine**: Nmap incluye un motor de scripting completo (NSE - Nmap Scripting Engine) que permite automatizar tareas complejas de auditoría de seguridad más allá del simple escaneo de puertos.

### Diferencias en Base de Datos de Servicios

Nmap mantiene una base de datos exhaustiva de servicios conocidos, incluyendo no solo asociaciones puerto-servicio, sino también firmas específicas que permiten identificar versiones exactas de software. Nuestra implementación utiliza una lista básica de servicios comunes.

Esta diferencia es significativa en auditorías de seguridad profesionales, donde conocer la versión exacta de un servicio puede ser crucial para identificar vulnerabilidades específicas.

## Limitaciones y Consideraciones

### Limitaciones Técnicas

**Detección por Sistemas de Seguridad**: Nuestro escáner utiliza TCP connect scanning, que establece conexiones completas. Esto significa que cada conexión será registrada en logs del sistema objetivo, haciendo el escaneo fácilmente detectable.

**Falta de Soporte para UDP**: Muchos servicios importantes utilizan UDP en lugar de TCP (como DNS, DHCP, y SNMP). Nuestro escáner no puede detectar estos servicios porque no implementa escaneo UDP.

**Identificación Limitada de Servicios**: La identificación de servicios se basa únicamente en números de puerto, lo que puede ser inexacto. Servicios pueden ejecutarse en puertos no estándar, y puertos estándar pueden ser utilizados por servicios diferentes.

**Rendimiento en Redes de Alta Latencia**: El diseño actual asume latencias de red relativamente bajas. En redes satelitales o conexiones intercontinentales, los timeouts pueden necesitar ajustes significativos.

### Consideraciones de Seguridad

**Firma de Tráfico**: El patrón de tráfico generado por nuestro escáner es distintivo y puede ser fácilmente identificado por sistemas de detección de intrusiones (IDS/IPS).

**Rate Limiting**: Algunos sistemas implementan rate limiting que puede bloquear o retardar conexiones que llegan demasiado rápidamente. Nuestro escáner no implementa mecanismos para detectar o adaptarse a estas medidas.

**Logs de Auditoría**: Cada conexión exitosa será registrada en los logs del sistema objetivo, potencialmente alertando a administradores sobre la actividad de escaneo.

### Limitaciones de Portabilidad

Aunque Python es multiplataforma, algunos aspectos del comportamiento de red pueden variar entre sistemas operativos. Windows, macOS, y Linux pueden tener diferencias sutiles en cómo manejan sockets, timeouts, y límites de recursos.

## Uso Ético y Legal

### Principios de Uso Responsable

El poder de las herramientas de exploración de red viene acompañado de responsabilidades significativas. Estas herramientas pueden proporcionar información valiosa para la seguridad y administración de sistemas, pero también pueden ser utilizadas con propósitos maliciosos.

**Autorización Explícita**: Nunca utilices el escáner en sistemas que no posees o para los cuales no tienes autorización explícita por escrito. Esto incluye redes corporativas, sistemas gubernamentales, o cualquier infraestructura de terceros.

**Entornos de Prueba**: Para aprendizaje y experimentación, utiliza siempre entornos controlados. Esto puede incluir tu propia red doméstica, máquinas virtuales que configures específicamente para pruebas, o laboratorios de seguridad diseñados para educación.

**Transparencia y Documentación**: Si estás utilizando el escáner en un contexto profesional legítimo, mantén documentación clara de qué sistemas estás escaneando, cuándo, y por qué. Esta documentación puede ser crucial si surgen preguntas sobre la actividad de red.

### Implicaciones Legales

Las leyes relacionadas con la exploración de redes varían significativamente entre jurisdicciones, pero generalmente incluyen principios similares. El acceso no autorizado a sistemas informáticos es ilegal en la mayoría de países, y el escaneo de puertos puede ser interpretado como un primer paso hacia acceso no autorizado.

**Leyes de Acceso No Autorizado**: En muchas jurisdicciones, incluso el simple acto de escanear puertos en sistemas ajenos puede constituir una violación de leyes de acceso no autorizado, especialmente si se puede demostrar intención maliciosa.

**Términos de Servicio**: Muchos proveedores de servicios de Internet y servicios en la nube tienen términos de servicio que prohíben explícitamente el escaneo de puertos, incluso en tus propios sistemas hospedados.

**Contexto Profesional**: En contextos profesionales legítimos, como auditorías de seguridad autorizadas, asegúrate de tener contratos claros que especifiquen el alcance del trabajo y las actividades autorizadas.

### Detección y Respuesta

Es importante entender que la actividad de escaneo de puertos es fácilmente detectable por sistemas de monitoreo modernos. Administradores de sistemas experimentados pueden identificar patrones de escaneo en logs de red y pueden responder con medidas que incluyen bloqueo de IP, investigación de seguridad, o incluso acción legal.

Esta detectabilidad no es una limitación de nuestro escáner específicamente, sino una característica inherente de TCP connect scanning. Incluso herramientas profesionales como Nmap dejan rastros similares cuando utilizan este método de escaneo.

## Extensiones Propuestas

### Mejoras de Core Functionality

**Implementación de Escaneo UDP**: Agregar capacidades de escaneo UDP expandiría significativamente la utilidad del escáner. UDP scanning es técnicamente más desafiante porque UDP es un protocolo sin conexión, requiriendo técnicas diferentes para determinar si los puertos están abiertos.

**Banner Grabbing Básico**: Implementar capacidades básicas de banner grabbing permitiría obtener información más detallada sobre servicios identificados. Esto involucraría enviar solicitudes específicas de protocolo y analizar las respuestas.

**Detección de Filtrado**: Mejorar la capacidad de distinguir entre puertos cerrados y filtrados utilizando técnicas más sofisticadas de análisis de respuestas y timing.

### Mejoras de Rendimiento

**Escaneo Adaptativo**: Implementar algoritmos que ajusten automáticamente el número de hilos y timeouts basándose en las características de la red objetivo y la capacidad del sistema local.

**Optimización de Rangos**: Desarrollar heurísticas para escanear rangos de puertos de manera más eficiente, potencialmente saltando rangos que probablemente no contengan servicios activos.

**Caching de Resultados**: Implementar un sistema de cache que recuerde resultados de escaneos anteriores para evitar trabajo redundante en escaneos repetidos.

### Características de Usabilidad

**Salida Estructurada**: Agregar capacidades para generar salida en formatos estructurados como JSON o XML, facilitando la integración con otras herramientas.

**Perfiles de Escaneo**: Crear perfiles predefinidos para diferentes tipos de escaneo (escaneo rápido, escaneo completo, escaneo de servicios web, etc.).

**Interfaz Gráfica**: Desarrollar una interfaz gráfica simple que haga la herramienta más accesible para usuarios no técnicos.

### Características de Seguridad

**Randomización de Timing**: Implementar variación aleatoria en el timing de conexiones para hacer el escaneo menos detectable por sistemas de monitoreo.

**Proxy Support**: Agregar capacidad de realizar escaneos a través de proxies para adicionar una capa de anonimato.

**Evasión Básica**: Implementar técnicas básicas de evasión como fragmentación de conexiones o uso de direcciones de origen variables.

### Análisis y Reporting

**Detección de Vulnerabilidades Básicas**: Implementar verificaciones básicas para vulnerabilidades comunes basadas en servicios y versiones identificadas.

**Reporting Avanzado**: Desarrollar capacidades de generación de reportes que incluyan visualizaciones de datos y análisis de tendencias.

**Integración con Bases de Datos**: Agregar capacidades para almacenar y consultar resultados de escaneo en bases de datos para análisis histórico.

---

## Conclusión

Este proyecto demuestra que los principios fundamentales detrás de herramientas sofisticadas como Nmap son accesibles y comprensibles. Aunque esta implementación es necesariamente más simple que herramientas profesionales, proporciona una base sólida para entender cómo funcionan estas herramientas y cómo pueden ser extendidas.

La diferencia entre una herramienta educativa como esta y una herramienta profesional como Nmap no está en los principios fundamentales, sino en la profundidad de implementación, la amplitud de características, y años de refinamiento y optimización. Entender estos principios fundamentales es el primer paso para apreciar completamente la sofisticación de las herramientas profesionales.

Más importante aún, este proyecto subraya la importancia del uso responsable y ético de herramientas de exploración de red. Con gran poder viene gran responsabilidad, y las capacidades de estas herramientas deben ser utilizadas siempre con consideración cuidadosa de las implicaciones éticas y legales.

## Licencia y Contribuciones

Este proyecto está diseñado para propósitos educativos. Se encourage la experimentación y modificación del código para fines de aprendizaje, siempre dentro del contexto de uso ético y legal.

Las contribuciones que mejoren la claridad educativa del código o que agreguen características que demuestren principios importantes de seguridad de redes son bienvenidas.