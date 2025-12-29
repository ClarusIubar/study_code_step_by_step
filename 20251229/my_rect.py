import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def update():
    global angle, tk_img
    angle += 5
    # (150, 150)은 사각형 꼭짓점이 있는 도화지의 '중앙'입니다.
    rotated = img_org.rotate(angle, center=(150, 150))
    
    tk_img = ImageTk.PhotoImage(rotated) # 돌아가는 이미지를 위해서 PIL
    canvas.delete("all") # 잔상제거 효과가 있대
    canvas.create_image(200, 200, image=tk_img) # 생성된 이미지로 랜더링 이미지 형성 
    root.after(50, update) # update함수를 시간마다 호출함

if __name__ == "__main__":
    # tk module
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()
    root.title("꼭지점 돌리기")

    # 도화지는 넉넉하게 300
    img_org = Image.new("RGBA", (300, 300), (0,0,0,0))
    # 도화지 위에 100짜리 사각형을 (150, 150) 꼭짓점에서 시작하게 그림
    ImageDraw.Draw(img_org).rectangle([150, 150, 250, 250], fill="blue") # 네모의 좌표를 일단 지정

    angle = 0 # 초기값 할당
    update()
    root.mainloop()