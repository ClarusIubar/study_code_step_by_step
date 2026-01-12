from http.server import HTTPServer, BaseHTTPRequestHandler
from renderer import TemplateRenderer
import json

class SSRHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. 파일 읽기
            with open("header.html", "r", encoding="utf-8") as f: 
                header = f.read()
            with open("main.html", "r", encoding="utf-8") as f: 
                main = f.read()
            with open("footer.html", "r", encoding="utf-8") as f: 
                footer = f.read()
            with open("index.html", "r", encoding="utf-8") as f: 
                index = f.read()
            with open("config.json", "r", encoding="utf-8") as f: 
                config_data = json.load(f)

            # 2. 렌더러를 통한 HTML 생성 (로직 분리)
            full_html = TemplateRenderer.render_index(header, main, footer, index, config_data["name"])

            # 3. 전송
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(full_html.encode("utf-8"))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server Error: {e}".encode("utf-8"))

print("서버 실행 중: http://localhost:8080")
HTTPServer(('localhost', 8080), SSRHandler).serve_forever()