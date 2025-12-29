import tkinter as tk
from PIL import Image, ImageTk

# 1. 원본 사각형 이미지 생성
img_org = Image.new("RGBA", (100, 100), "blue")
angle = 0

def update():
    global angle, tk_img
    angle += 5
    
    # 2. 추상화된 회전 함수 사용 (수학 공식 필요 없음)
    rotated = img_org.rotate(angle, expand=True) # 각도만 넣으면 끝 # 회전을 변경할 수 있음.
    
    # 3. 킨터용으로 변환 및 렌더링
    tk_img = ImageTk.PhotoImage(rotated)
    canvas.delete("all") # 잔상 제거
    canvas.create_image(200, 200, image=tk_img)
    
    # 4. 루프 제어 (50ms 마다 실행)
    root.after(50, update)

if __name__ == "__main__":

    root = tk.Tk()
    root.title("돌리고 돌리고")
    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()

    update()
    root.mainloop()