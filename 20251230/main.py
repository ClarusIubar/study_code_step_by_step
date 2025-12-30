import tkinter as tk

# 왜 굳이 tk라는 메서드를 호출했을까?
root = tk.Tk()
# 왜 매개변수 자리에 = 할당연산자가 있는거지?
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20)

# canvas = tk.Canvas
# canvas.create_text()
# 왜 메서드 이름이 loop라는 뜻이 담겨 있을까?
root.mainloop()