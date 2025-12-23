light_on = True # 상태

for i in range(1000):
    print(light_on)
    if light_on == True:
        light_on = False
    else:
        light_on = True

