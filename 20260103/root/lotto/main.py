import tkinter as tk
from app import LottoApp # 단일 앱 테스트

if __name__ == "__main__": 
    # 메인에서는 앱 실행만 담당하도록 제한
    root = tk.Tk()  # 루트 윈도우 생성
    app = LottoApp(root) # 앱 인스턴스 생성
    root.mainloop() # 루트 동작
