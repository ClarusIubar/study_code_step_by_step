from datetime import datetime

class TemplateRenderer:
    @staticmethod
    def render_index(header, main, footer, index, user_name="홍길동"):
        # 1. 데이터 준비
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 2. 본문 내용 채우기
        filled_index = index.replace("__USER_NAME__", user_name).replace("__TIME__", current_time)
        
        # 3. 전체 레이아웃 조립
        rendered_header = header.replace("__TITLE__", "홈페이지")
        rendered_main = main.replace("{content}", filled_index)
        
        return rendered_header + rendered_main + footer