import tkinter as tk
from app import App # 클래스 이름 미정

if __name__ == "__main__": 
    # 메인에서는 앱 실행만 담당하도록 제한
    root = tk.Tk()  # 루트 윈도우 생성
    app = App(root) # 앱 인스턴스 생성
    root.mainloop() # 루트 동작
