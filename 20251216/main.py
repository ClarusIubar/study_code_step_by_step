weight = 0

for i in range(100):
    weight = (weight + 1)
    na = f"내 몸무게는 {weight}kg입니다."
    print(na)
    if weight == 50:
        print("나는 미남이지롱!")
