a = ["김수빈", "고경명", "박의천", "유효현", "김민우", "이세한"]
b = ["김동찬", "정승훈", "박지수", "송우인", "신재혁", "손예진", "김노현", "전민권"]

# length_a = len(a)
# length_b = len(b)

if len(a) > len(b):
    print(f"{a}그룹이 {b}그룹보다 많다.")
elif len(a) < len(b):
    print(f"{b}그룹이 {a}그룹보다 많다.")
else:
    print(f"두 그룹의 숫자는 같습니다.")

# 더 세련된 방법은 없을까?
# 더 짧게 쓸 수 있는 방법은?

if len(a) > len(b):
    print(f"a그룹이 {len(a) - len(b)}명 더 많습니다.")
elif len(a) < len(b):
    print(f"b그룹이 {len(b) - len(a)}명 더 많습니다.")
else:
    print(f"두 그룹의 숫자는 같습니다.")

# len함수는 어떻게 구현할 수 있을까?

# number = 0
# for i in a:
#     number += 1

# print(number)

def count_list(input:list) -> int:
    number = 0
    for i in input:
        number += 1
    return number

if count_list(a) > count_list(b):
    print(f"a그룹이 {count_list(a) - count_list(b)}명 더 많아요.")
elif count_list(a) < count_list(b):
    print(f"b그룹이 {count_list(b) - count_list(a)}명 더 많아요")
else:
    print(f"두 그룹의 숫자는 같습니다.")

# 또 뭐가 있을까? print를 literal로 쓰지 않는 방법.

# count함수는 만들었어.
# 비교 함수 return -> big_one
# 프린트 함수

def compare_number(*count:int) -> list:
    # 두 개의 비교수가 튜플로 들어오지만, 그 값이 리스트와 매치가 안된다.
    # 그래서 억지로 리스트를 맵핑하는 작업이 필요하니까 번거로운 과정이 들어간다.
    # 어차피 return을 해당 변수와 함께 주는거면 input을 int로만 받으면 안 되었지. 
    # 그러네 들어가는 매개변수의 형태가 다른 것은 쉽게 호환이 안된다.
    return

def last_member(input:list) -> str:
    name = input[-1]
    return name

# 여기에 프린트하는 함수를 연결해서 쓰려면? 독립적? 종속적?
# 이래서 클래스를 쓰나? 그래야 그 클래스 안의 변수를 공통으로 사용할 수 있으니까?
# 클래스를 사용안하면 waterfall형태로 중첩함수를 쓸 수 밖에 없나?
print(last_member(a))

# 클래스
# 클래스 변수 (list_a, list_b)
# 메서드 count(a, b)
# 메서드 comparison(a, b)
# 메서드 last(a, b)
# 메서드 print(result)

# 너무 구조적으로만 생각하나?

class ListComparison:
    def __init__(self, list1:list, list2:list):
        if not isinstance(list1,list) or not isinstance(list2, list):
            raise TypeError("리스트가 아닌데유?")
        
        self.list1 = list1
        self.list2 = list2

    def compare_length_lists(self) -> None:
        len1 = len(self.list1)
        len2 = len(self.list2)

        if len1 > len2:
            print(f"1번째 리스트가 {len1-len2}개 더 많습니다.")
        elif len1 < len2:
            print(f"2번째 리스트가 {len2-len1}개 더 많습니다.")
        else:
            print("두 리스트의 개수가 같습니다.")
        return None

ListComparison(a,b).compare_length_lists()