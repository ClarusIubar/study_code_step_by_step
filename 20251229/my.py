import tkinter as tk

root = tk.Tk()
root.title("자유를 찾아서")
root.geometry("400x300")

# 1. 도화지(Canvas) 만들기
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# 2. 네모 그리기 (왼쪽위 x, y, 오른쪽아래 x, y)
# canvas.create_rectangle(50, 50, 150, 150, fill="blue", outline="black")

for i in range(4):
    i *= 50 #하드코딩 오지네.
    canvas.create_rectangle(50+i, 50+i, 150+i, 150+i, fill="blue", outline="black")

# # 3. 원 그리기 (네모 안에 꽉 차는 타원을 그린다고 생각하면 됨)
# canvas.create_oval(200, 50, 300, 150, fill="red")

# # 4. 선 그리기
# canvas.create_line(0, 0, 400, 300, fill="green", width=3)


# button = tk.Button(root, text="클릭하세요")
# button.pack(pady=20) # 여백을 줍니다.

# 실행
root.mainloop()