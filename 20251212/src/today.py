def today(time):
    time = time # 임시
    def wake_up(time):
        information = {
            "시간" : time,
            "설명" : "학원가기 적절한 시간"
        }
        return information
    
    def wash_body(shampoo, bodywash, toothbrush):
        body_parts = {
            "샴푸" : shampoo,
            "바디워시" : bodywash,
            "양치" : toothbrush,
        }

        return body_parts
    
    def take_clothes(상의, 하의, 신발):
        clothes = {
            "상의" : 상의,
            "하의" : 하의,
            "신발" : 신발,
        }

        return clothes

    total = [wake_up(time), wash_body("케라시스", "도브", "죽염"), take_clothes("검은색 옷","검은색 바지","검은색 컨버스")]
    return total

print(today("7시"))
print(today("8시"))
print(today("9시"))

