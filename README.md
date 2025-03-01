# ✨ WP Plugin Scanner ✨

## 📝 Descripción
🚀 Este proyecto contiene el script `wp_plugin_scanner.py` que permite escanear y analizar los plugins de un sitio de WordPress en busca de posibles vulnerabilidades. 🔍

## 📦 Requisitos
Para ejecutar este script, necesitarás tener instalado Python 3 y las siguientes dependencias:

1. 📦 `requests` - Para hacer peticiones HTTP.
2. 📦 `argparse` - Para la gestión de argumentos en la línea de comandos.
3. 🕒 `time` - Para gestionar tiempos y hacer pausas entre las peticiones.
4. 🎲 `random` (uniform) - Para generar pausas aleatorias entre peticiones.
5. 🧵 `concurrent.futures` - Para ejecutar tareas concurrentes utilizando hilos.
6. 🖥️ `tqdm` - Para mostrar una barra de progreso mientras se ejecuta el escaneo.
7. 🎨 `colorama` - Para colorear el texto de la salida del script.

## 🚀 Instalación
1. Clona el repositorio o descarga los archivos del proyecto.
2. Instala las dependencias utilizando pip:
```bash
pip install -r requirements.txt
```

## 🔧 Uso
Para ejecutar el script, usa el siguiente comando:
```bash
python wp_plugin_scanner.py -u <url_objetivo> -w <ruta_wordlist>
```

### Ejemplo
```bash
python wp_plugin_scanner.py -u http://example.com -w plugins.txt
```

## 🛠️ Contribución
Si deseas contribuir a este proyecto, por favor abre un pull request con las mejoras o correcciones. 💡

## 📝 Licencia
Este proyecto está licenciado bajo la Licencia MIT. 🖤

## 🎨 Decoración
Para más detalles, consulta la documentación o si tienes dudas, no dudes en abrir un issue. 🐞

¡Gracias por usar el escáner de plugins de WordPress! 🌟
