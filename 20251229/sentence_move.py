import tkinter as tk

# 클래스
root = tk.Tk()
root.title("저리가")
root.geometry("500x500")

# 캔버스
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# 객체할당
text_id = canvas.create_text(200, 200, text="저리가", font=("Arial", 20), fill="blue")

def move_text(event):
    # move 함수로 글자 움직이기
    if event.keysym == 'Up':    canvas.move(text_id, 0, -10)
    if event.keysym == 'Down':  canvas.move(text_id, 0, 10)
    if event.keysym == 'Left':  canvas.move(text_id, -10, 0)
    if event.keysym == 'Right': canvas.move(text_id, 10, 0)

# bind하면 조작도 가능하구나, 어떻게 움직일지 할당해주면 이동이 가능하네.
root.bind("<Key>", move_text) 
root.mainloop()