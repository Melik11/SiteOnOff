from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Читаем параметр ?status= из URL
        query = parse_qs(urlparse(self.path).query)
        status = query.get('status', [''])[0].lower()

        # Определяем цвет и текст
        if status == 'on':
            css_class, text = 'on', 'ON'
        elif status == 'off':
            css_class, text = 'off', 'OFF'
        else:
            css_class, text = 'unknown', 'Не задано'

        # Формируем HTML
        html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Статус</title>
            <style>
                body {{ font-family: sans-serif; text-align: center; padding: 50px; }}
                .badge {{ padding: 20px 40px; border-radius: 50px; font-size: 20px; color: white; }}
                .on {{ background: #10b981; }}
                .off {{ background: #ef4444; }}
                .unknown {{ background: #64748b; }}
            </style>
        </head>
        <body>
            <h1>Статус системы</h1>
            <div class="badge {css_class}">{text}</div>
        </body>
        </html>"""

        # Отправляем ответ браузеру
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


if __name__ == '__main__':
    port = 8000
    print(f"Сервер запущен: http://localhost:{port}")
    print("Откройте в браузере:")
    print(f"  http://localhost:{port}/?status=on")
    print(f"  http://localhost:{port}/?status=off")

    HTTPServer(('localhost', port), StatusHandler).serve_forever()
