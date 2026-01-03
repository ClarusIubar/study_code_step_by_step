# base_popup.py
import tkinter as tk
from abc import ABC, abstractmethod

class BasePopup(tk.Toplevel, ABC): # ABC를 함께 상속받아 추상 클래스로 지정
    def __init__(self, root, title, width=300, height=200):
        super().__init__(root)
        self.withdraw() 
        self.title(title)
        self.width = width
        self.height = height

        self._align_to_center(root)
        
        # 여기서 호출되는 _build_ui는 이제 반드시 오버라이드되어 있어야 함
        self._build_ui() 

        self.transient(root)
        self.grab_set()
        self.deiconify()

    def _align_to_center(self, root):
        self.update_idletasks()
        px, py = root.winfo_rootx(), root.winfo_rooty()
        pw, ph = root.winfo_width(), root.winfo_height()
        
        x = px + (pw // 2) - (self.width // 2)
        y = py + (ph // 2) - (self.height // 2)
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    @abstractmethod
    def _build_ui(self):
        """
        이 메서드는 추상 메서드입니다.
        자식 클래스에서 이를 구현하지 않으면 객체 생성이 불가능합니다.
        """
        # notimplemented error따위로 소극적인 방어를 하게 둘 수는 없지.
        # 자식에서 오버라이딩 하지 않으면 객체 생성 시에 type error를 발생시켜야지.
        pass