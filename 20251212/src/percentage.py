# percentage.py

def calculate_percentage(part, whole):
    """
    'whole'에서 'part'가 차지하는 비율을 퍼센테이지(%)로 계산합니다.

    Args:
        part (float 또는 int): 부분 값
        whole (float 또는 int): 전체 값 (0이 될 수 없습니다)

    Returns:
        float: 백분율 값
    """
    if whole == 0:
        # 0으로 나누는 것을 방지
        raise ValueError("전체 값(whole)은 0이 될 수 없습니다.")
    
    # (부분 / 전체) * 100
    percentage = (part / whole) * 100
    return percentage

def calculate_part_from_percentage(whole, percent):
    """
    'whole' 값의 'percent' 퍼센트(%)에 해당하는 부분을 계산합니다.

    Args:
        whole (float 또는 int): 전체 값
        percent (float 또는 int): 퍼센테이지 값

    Returns:
        float: 부분 값
    """
    # 전체 * (퍼센트 / 100)
    part = whole * (percent / 100)
    return part

# 이 모듈의 간단한 사용 예시
if __name__ == "__main__":
    print(f"100에서 20이 차지하는 비율: {calculate_percentage(20, 100)}%")
    print(f"500의 15%는 얼마?: {calculate_part_from_percentage(500, 15)}")