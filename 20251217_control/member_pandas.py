import pandas as pd

members = [
    {"name": "김수빈", "age": 24, "address": "서울시 마포구", "favorite": "마라탕", "dislike": "오이"},
    {"name": "고경명", "age": 29, "address": "경기도 성남시", "favorite": "냉삼", "dislike": "가지무침"},
    {"name": "박의천", "age": 26, "address": "서울시 강남구", "favorite": "오마카세", "dislike": "고수"},
    {"name": "유효현", "age": 31, "address": "경기도 수원시", "favorite": "치맥", "dislike": "브로콜리"},
    {"name": "김민우", "age": 22, "address": "인천시 부평구", "favorite": "하와이안피자", "dislike": "당근"},
    {"name": "이세한", "age": 27, "address": "서울시 송파구", "favorite": "수제버거", "dislike": "민트초코"},
    {"name": "김재형", "age": 33, "address": "경기도 용인시", "favorite": "돼지김치구이", "dislike": "생굴"},
    {"name": "김동찬", "age": 30, "address": "경기도 고양시", "favorite": "돈카츠", "dislike": "버섯"},
    {"name": "정승훈", "age": 28, "address": "서울시 관악구", "favorite": "로제파스타", "dislike": "순대간"},
    {"name": "박지수", "age": 23, "address": "경기도 안양시", "favorite": "불족발", "dislike": "번데기"},
    {"name": "송우인", "age": 32, "address": "서울시 영등포구", "favorite": "매운갈비찜", "dislike": "홍어"},
    {"name": "신재혁", "age": 29, "address": "인천시 연수구", "favorite": "돈코츠라멘", "dislike": "파인애플"},
    {"name": "손예진", "age": 24, "address": "서울시 종로구", "favorite": "타코", "dislike": "곱창"},
    {"name": "김노현", "age": 27, "address": "경기도 부천시", "favorite": "바지락칼국수", "dislike": "닭발"},
    {"name": "전민권", "age": 34, "address": "서울시 강동구", "favorite": "얼큰순대국", "dislike": "회"}
]

df = pd.DataFrame(members)

# [업무 1] 회장님 취향 파악
# 명부 가장 맨 앞(index 0)에 있는 회장님의 이름과 가장 좋아하는 음식을 확인하세요.
president = df.iloc[0][["name","favorite"]]
print(president)

# [업무 2] 신입 회원 챙기기
# 명부 맨 뒤에 있는 신입 회원의 이름과 거주지를 파악하세요. (데이터가 늘어나도 항상 마지막을 가리켜야 함)

newbie = df.iloc[-1][["name","address"]]
print(newbie)

# [업무 3] 주소록 업데이트
# 세 번째 멤버의 주소를 "제주도 서귀포시"로 변경하세요.

df.loc[3-1,"address"] = "제주도 서귀포시" # 왜 iloc[][]는 안되고, loc[ , ]은 update가 될까?
print(df.iloc[3-1])

# [업무 4] 식성 정보 수정
# 다섯 번째 멤버의 싫어하는 음식 정보를 "없음"으로 수정하세요.

df.loc[5-1, "dislike"] = ""
print(df.iloc[5-1])

# [업무 5] 신규 인원 추가
# 새로운 멤버(공욱재, 35세, 서울시 영등포구, 선호: 아이스아메리카노, 불호: 따뜻한파인애플)를 명부 맨 마지막에 추가하세요.

new_member = {
    "name" : "공욱재",
    "age" : 35,
    "address" : "서울시 영등포구", 
    "favorite" : "아이스아메리카노",
    "dislike" : "따뜻한파인애플"
}

df = pd.concat([df, pd.DataFrame([new_member])], ignore_index=True) ## 문법 숙달 필요! 
# 첫번째 인덱스에 concat되는 두개의 데이터프레임을 []로 감싸야함.
print(df.iloc[-1][:])

# [업무 6] 식당 예약 인원 확정
# 현재 명부에 등록된 전체 회원이 총 몇 명인지 계산하세요.

print(len(df))

# [업무 7] 네임택 제작
# 모든 멤버의 이름만 순서대로 출력하세요.
print(df.loc[:,"name"])

# [업무 8] 서울 '벙개' 멤버 모집
# 주소에 "서울"이 포함된 멤버들만 추출하여 이름과 주소를 확인하세요.
sliced = df.loc[ df.loc[:,"address"].str.contains("서울"), "name":"address" ]
print(sliced)

# [업무 9] 메뉴 선정 "오이" 주의보
# 싫어하는 음식에 "오이"가 포함된 멤버를 찾아 그들에게 "오이 주의!!"라는 메시지를 출력하세요.

member_hate_cucumber = df.loc[ df.loc[:,"dislike"]=="오이", "name"].tolist()

for i in member_hate_cucumber:
    print(f"{i}님 오이 주의!!")

# [업무 10] '형님/누님' 테이블 편성
# 나이가 30세 이상인 멤버들의 이름만 골라 senior_table이라는 별도의 리스트를 만드세요.

senior_table = df.loc[ df.loc[:,"age"] >= 30, "name"].tolist()
print(senior_table)