# 기준 기온
# 기온이 0보다 높으면 걸어가고, 기온이 0보다 낮으면 버스를 탄다.

temperature = 0

def how_to_goto_greenart(temperature):
    if temperature >= 0:
        walk()
    else:
        take_bus()



# 스위치를 on에 두면 불을켜고, off에 두면 끈다.

isOn = 1 # True
def state_bulb(isOn):
    if isOn == True:
        Turn_On()
    else:
        Turn_Off()



# 돈을 넣는다. # 카드를 넣는다.
# 돈을 넣으면 해당 돈을 Max로 한 제품만 불을 켠다.
# 제품을 선택하면, 
# Max - price 차액만큼, 잔금과 제품을 준다.

# 카드를 넣으면 모든 제품에 불을 켠다.
# 제품을 선택하면, 결제처리를 진행
# 잔고가 부족하면 error, 잔고가 충분하면,
# 음료가 나온다.

