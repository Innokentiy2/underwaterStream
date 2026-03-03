from http.server import BaseHTTPRequestHandler, HTTPServer
from frame_source import generate_frame

PORT = 7123

PAGE = """\
<html>
<head><meta charset="utf-8"><title>Underwater demo</title></head>
<body>
<h1>Underwater module (prototype)</h1>
<p>Кадр обновляется по кнопке (потом здесь будет видео).</p>
<img src="/frame.jpg" width="640" height="480" />
<br>
<a href="/">Обновить кадр</a>
</body>
</html>
"""
PAGE_BYTES = PAGE.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PAGE_BYTES)))
            self.end_headers()
            self.wfile.write(PAGE_BYTES)

        elif self.path == "/frame.jpg":
            frame = generate_frame()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Content-Length", str(len(frame)))
            self.end_headers()
            self.wfile.write(frame)

        else:
            self.send_error(404)


if __name__ == "__main__":
    with HTTPServer(("", PORT), Handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

