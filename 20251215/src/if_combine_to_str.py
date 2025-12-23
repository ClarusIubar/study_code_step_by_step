# 강한 언어인 파이썬의 숫자와 문자열을 자바처럼 문자열로 합치는 함수 만들기

def combine_all_to_str(*args) -> str:

    string_elements = map(str, args) # 1. map(str, args): (1, 'two', 3.0) -> ('1', 'two', '3.0')
    final_string = ''.join(string_elements) # 2. ''.join(...): 모든 문자열 요소를 공백 없이 하나로 합칩니다.
    
    return final_string

# --- 실행 예시 ---
result1 = combine_all_to_str(10, 'hello', 3.14, ['a', 'b'])
result2 = combine_all_to_str(1, 2, 3) 

print(f"결과 1: {result1}") # 출력: 결과 1: 10hello3.14['a', 'b']
print(f"결과 2: {result2}") # 출력: 결과 2: 123




def combine_with_separator(*args, separator: str = ', ') -> str:
    
    string_elements = map(str, args) # 모든 요소를 문자열로 변환
    final_string = separator.join(string_elements)   # 구분자(separator)를 사용하여 결합
    
    return final_string

result3 = combine_with_separator(10, 'apple', 2024, separator=' - ')
print(f"결과 3: {result3}") # 출력: 결과 3: 10 - apple - 2024



def combine_str_extended(*args) -> str:

    all_elements = [] # 객체 초기화

    for item in args:
        # 각 item에 대해 패턴 매칭 시작
        match item:
            # Case 1: item이 List 타입인 경우 (리스트 해부)
            case list(elements): # match에 지정한 값을 알아서 인자로 전달 함.
                stringified_elements = map(str, elements) # 리스트 내부 요소(elements)를 개별적으로 처리
                all_elements.extend(stringified_elements) # map(str, elements)로 각 요소를 문자열로 변환한 후 all_elements에 확장

            # Case 2: item이 정수(int) 타입인 경우
            case int(x):
                all_elements.append(str(x))

            # Case 3 (와일드카드): 위의 모든 패턴에 해당하지 않는 경우 (str, float 등)
            case _:
                all_elements.append(str(item))

    return "".join(all_elements) # 최종적으로 모든 요소를 하나의 문자열로 결합

# --- 실행 예시 ---
# 입력: 1 (int), [2, 3] (list), 'four' (str), 5.5 (float)
result = combine_str_extended(1, [2, 3], 'four', 5.5)
print(f"결과 4: {result}") # 출력: 결과: 123four5.5 




def combine_str_isinstance(*args) -> str:
    all_elements = []
    
    for item in args:
        if isinstance(item, list):
            all_elements.extend(map(str, item)) # item이 리스트면, 내부 요소를 문자열로 변환 후 확장(extend)
        else:
            all_elements.append(str(item)) # 리스트가 아니면, 해당 요소를 문자열로 변환 후 추가(append)
            
    return "".join(all_elements)

result_isinstance = combine_str_isinstance(1, [2, 3], 'four', 5.5) # 출력: 결과: 123four5.5
print(f"결과 5: {result_isinstance}")