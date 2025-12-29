import tkinter as tk
import math

root = tk.Tk()
root.title("수열 별찍기 풍차")

canvas = tk.Canvas(root, width=600, height=600, bg="#1a1a1a") # 배경을 어둡게
canvas.pack()

angle = 0

def draw_windmill():
    global angle
    canvas.delete("all")
    
    cx, cy = 300, 300 # 중심점
    
    # 4개의 날개 방향 (0도, 90도, 180도, 270도)
    for wing_angle in [0, 90, 180, 270]:
        base_rad = math.radians(angle + wing_angle)
        
        # --- [수열 별찍기 로직] ---
        for i in range(1, 6): # 1단부터 5단까지 (세로 거리)
            dist_step = i * 25 # 중심에서 얼마나 멀어지는지
            
            for j in range(i): # 각 단마다 별 개수를 늘림 (가로 너비)
                # j(개수)에 따라 옆으로 퍼지는 간격 계산
                offset = (j - (i-1)/2) * 20 
                
                # 회전 변환 (수학적 역치를 넘는 지점!)
                # 원래 위치(dist_step, offset)를 각도만큼 회전시킨 좌표
                final_x = cx + dist_step * math.cos(base_rad) - offset * math.sin(base_rad)
                final_y = cy + dist_step * math.sin(base_rad) + offset * math.cos(base_rad)
                
                # 별 렌더링
                canvas.create_text(final_x, final_y, text="*", fill="yellow", font=("Arial", 12))
    
    angle += 3 # 회전 속도
    root.after(30, draw_windmill)

draw_windmill()
root.mainloop()