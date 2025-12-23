a = ["김수빈", "고경명"] 
b = ["박의천", "유효현", "김민우", "이세한"]
c = ["김동찬", "정승훈", "박지수", "송우인", "신재혁", "손예진", "김노현", "전민권"]
d = {"이름" : "이상학", "age":36}
e = 13
f = "공욱재"
g = (1984, "응답하라")
h = ''

class ListComparison:
    def __init__(self, *args:list):
        self.lists = [] # 초기화

        for i, item in enumerate(args):
            if not isinstance(item, list):
                raise TypeError(f"{i + 1}번째 요소가 리스트가 아닌데유?")
            elif item == None: # 방어적으로 설계하려고 넣은 것이지만, 이미 위에서 걸러지기 때문에 -->
                raise ValueError("값을 주셔야 처리를 하죠!")
            else:
                self.lists.append(item) # list써서 오류(keyword는 사용 지양)
        # print(self.lists) # [[  ], [   ]] 다중리스트

    def comparison_list_length(self:list) -> None:
        container = []

        if len(self.lists) < 2:
            print("두 개 이상을 줘야 비교를 하죠? ㅎㅎ")
            return # 잘못되면 빠져나와야함. 안그러면, 아래의 로직을 실행함.
        
        else:
            for i, item in enumerate(self.lists):
                container.append( (i, item, len(item)) )
        
        index, item, length = max(container, key=lambda x: x[2]) # container의 요소의 3번째끼리 비교하라.
        # print(index, item, length)
        print(f"{index + 1}번째 리스트가 {length}개로 가장 큽니다.")

# ListComparison(a,b,c)
ListComparison(a).comparison_list_length() # 두 개 이상을 줘야 비교를 하죠? ㅎㅎ
ListComparison(a,b).comparison_list_length() # 2번째 리스트가 4개로 가장 큽니다.
ListComparison(a,b,c).comparison_list_length() # 3번째 리스트가 8개로 가장 큽니다.

# 의도적으로 에러 발생시키기
# ListComparison(a,b,c,d).comparison_list_length() # TypeError: 4번째 요소가 리스트가 아닌데유?
# ListComparison(d,e,f,g).comparison_list_length() # TypeError: 1번째 요소가 리스트가 아닌데유? 
    # 오류를 일으키는 첫 순간에 error일으키고 종료, 모든 오류들을 일일히 다 표현해주지는 않음.
# ListComparison(h).comparison_list_length() # 1번째 요소가 리스트가 아닌데유? <--
    # 순차적으로 실행하다가 에러를 만나면 하위의 논리를 실행하지 않고 종료하기 때문에, 하나씩 확인해야했다.



# 클래스가 진가를 발휘하려면, 같은 데이터를 가지고 여러개의 기능을 사용할 수 있도록 구현해야 한다.
# flatten해서 sorted하게 해야하나? 아니면 flatten과 sorted를 별도로 만들어야 하나?
# flatten했는데, 중복이 있다면 제거해야 할까?

# 대화를 하다보니 어떤 게 파이써닉(흠 그냥 괜찮으면 가져다 붙이는 말처럼 보이는데)한가의 답안지를 얻어봄.
# def comparison_list_length_pythonic(self):
        
#     if len(self.lists) < 2:
#         print("두 개 이상을 줘야 비교를 하죠? ㅎㅎ")
#         return
        
#     # 1. 가장 긴 리스트 객체를 한 줄로 찾습니다.
#     longest_list = max(self.lists, key=len) 
    
#     # 2. 가장 짧은 리스트 객체를 한 줄로 찾습니다.
#     shortest_list = min(self.lists, key=len) 
    
#     # 3. 인덱스 찾기: 리스트 객체가 self.lists의 몇 번째에 있는지 찾습니다.
#     max_index = self.lists.index(longest_list)
#     min_index = self.lists.index(shortest_list)
    
#     max_length = len(longest_list)
#     min_length = len(shortest_list)

#     print(f"🥇 가장 긴 리스트: {max_index + 1}번째, 길이: {max_length}개")
#     print(f"🤏 가장 짧은 리스트: {min_index + 1}번째, 길이: {min_length}개")

# 아, 너무 재밌다! 이런 게 나의 심장을 뛰게 하지!
# pandas, numpy 데이터 핸들링을 선조들이 만들어 둠에 감사하십시오!

# import pandas as pd

# # 1. 데이터 준비 (Pandas에 전달할 리스트 목록)
# list_data = [a, b, c] # d, e, f, g, h는 리스트가 아니므로 제외하고 유효한 데이터만 사용

# def compare_lists_pandas(input_lists):
#     """
#     Pandas DataFrame을 사용하여 리스트들의 길이를 비교하는 함수.
#     """
#     if len(input_lists) < 2:
#         print("두 개 이상을 줘야 비교를 하죠? ㅎㅎ")
#         return

#     # 1. DataFrame 생성: 리스트들을 'List' 열에 담고, 인덱스를 'Index'로 사용
#     # Index는 0, 1, 2, ...
#     df = pd.DataFrame({'List': input_lists})

#     # 2. 'Length' 열 추가: 각 리스트에 파이썬 내장 len() 함수를 적용 (핵심!)
#     df['Length'] = df['List'].apply(len)

#     # 3. 가장 긴 리스트 찾기
#     # idxmax()는 특정 열에서 최대값을 가진 행의 인덱스(여기서는 0, 1, 2)를 반환합니다.
#     max_index_in_df = df['Length'].idxmax()
    
#     # 4. 결과 추출
#     longest_list_row = df.loc[max_index_in_df]
#     length = longest_list_row['Length']
    
#     # 5. 출력 (원래 코드의 'index + 1'에 맞춰 1을 더해줌)
#     print(f"🥇 Pandas 버전: {max_index_in_df + 1}번째 리스트가 {length}개로 가장 큽니다.")

# # --- 실행 ---

# compare_lists_pandas(list_data) 
# # 결과: 3번째 리스트가 8개로 가장 큽니다.