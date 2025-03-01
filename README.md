# ✨ WP Plugin Scanner ✨

## 📝 Descripción
🚀 Este proyecto contiene el script `wp_plugin_scanner.py` que permite escanear y analizar los plugins de un sitio de WordPress en busca de posibles vulnerabilidades. 🔍

## 📦 Requisitos
Para ejecutar este script, necesitarás tener instalado Python 3 y las siguientes dependencias:

1. 📦 requests
2. 📦 BeautifulSoup4
3. 🧰 (Cualquier otra librería que tu script use)

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

## 📝 Licencia
Este proyecto está licenciado bajo la [Licencia](LICENSE) MIT. 🖤
