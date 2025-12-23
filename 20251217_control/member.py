# from collections import ChainMap

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

# members_view = ChainMap(*members)
# print(members_view) # chainmap(dict)
# print(members_view.maps) # json style # symbolic access without first list index

# print(type(members_view)) # collections.chainmap
# print(type(members_view.maps)) #list

# ## **시나리오: 이번 주 주말 정모 준비**
# 당신은 이 동호회의 **운영진(총무)**입니다. 이번 주말 맛집 모임을 위해 아래 업무들을 처리해주세요.

# ### **[업무 1] 회장님 취향 파악**
print(members[0]["favorite"])

# 회원 명부 **가장 맨 앞**에 있는 사람이 우리 동호회 회장님입니다. 회장님이 누구인지, 그리고 회식 메뉴 선정을 위해 **가장 좋아하는 음식**이 무엇인지 확인해주세요.

# ### **[업무 2] 신입 회원 챙기기**
# 명부 **맨 뒤**에 있는 사람은 가장 최근에 가입한 신입 회원입니다. 낯설어하지 않게 챙겨줘야 하니, 누군지 확인하고 **어디 사는지(거주지)** 파악해두세요. (회원이 늘어나도 항상 마지막 사람을 가리키도록 코드를 짜야 편합니다.)

print(members[len(members) - 1]["address"])

# ### **[업무 3] 주소록 업데이트**

# **세 번째** 멤버가 최근에 직장을 옮기면서 이사를 갔다고 합니다. 회비 고지서 발송을 위해 주소를 **"제주도 서귀포시"**로 변경해주세요.

members[2]["address"] = "제주도 서귀포시"
print(members[2]["address"])

# ### **[업무 4] 식성 정보 수정**

# **다섯 번째** 멤버랑 톡을 했는데, 이제 편식을 안 하기로 했답니다. 싫어하는 음식 정보를 **"없음"**으로 쿨하게 지워주세요(수정해주세요).

members[4]["dislike"] = ""
print(members[4]["dislike"])

# ### **[업무 5] 고문관님 초대**

# 우리 모임의 정신적 지주인 **"공욱재"** 님이 뒤늦게 합류하기로 했습니다. 명부 **맨 마지막**에 공욱재 님의 정보를 추가해주세요.

# (정보: 35세, 서울시 영등포구, 아이스아메리카노 선호, 따뜻한파인애플 극혐)

members.append( {
    "name" : "공욱재",
    "age" : 35,
    "address" : "서울시 영등포구",
    "favorite" : "아이스아메리카노",
    "dislike" : "따뜻한파인애플"
} )

print(members[-1])

# ### **[업무 6] 식당 예약 인원 확정**

# 공욱재 님까지 오신다니 이제 인원은 확정되었습니다. 식당에 "몇 명 예약할게요"라고 말해야 할까요? 현재 명부에 있는 인원이 **총 몇 명**인지 계산해주세요.

print(len(members))

# ### **[업무 7] 네임택(Name Tag) 제작**

# 모임 장소에서 서로 이름을 부르기 쉽게 네임택을 만들려고 합니다. 명부를 쭉 훑으면서 모든 멤버의 **이름**만 순서대로 출력해주세요.

for i, item in enumerate(members):
    print(members[i]["name"][1:])

# ### **[업무 8] 서울 '벙개' 멤버 모집**
# 이번 주 평일 저녁에 서울에서 급하게 번개 모임(벙개)을 하려고 합니다. 집에 가기 편하게 주소에 **"서울"**이 들어가는 멤버들만 따로 추려서, **이름**과 **동네(주소)**를 뽑아주세요.

# print(members[0]["address"])

# print("서울시 마포구".split(' ')[0]) ## 좀 고급지게 써보고 싶어짐

extract_member_soeul = []
for i, item in enumerate(members):
    if members[i]["address"].__contains__("서울"):
        extract_member_soeul.append( [members[i]["name"], members[i]["address"]] )

print(extract_member_soeul)

# ### **[업무 9] 메뉴 선정 "오이" 주의보**

# 이번 정모 식당의 밑반찬에 '오이무침'이 나온다고 합니다. 큰일 날 수 있으니, 전체 멤버를 확인해서 싫어하는 음식이 **"오이"**인 사람을 찾아내고, 그 멤버에게 "오이 주의!!"라고 알려주세요.

def send_message_to_memeber():
    extract_hate_cucumber = [] 
    for i, item in enumerate(members):
        if members[i]["dislike"] == "오이":
            extract_hate_cucumber.append(members[i]["name"])
    for i in extract_hate_cucumber:
        print(f"{i}님, 오이 주의!!")

send_message_to_memeber()

# ### **[업무 10] '형님/누님' 테이블 편성**

# 술맛을 좀 아는 30대 이상끼리 테이블을 따로 잡으려고 합니다. 전체 멤버 중 나이가 **30세 이상**인 사람들의 **이름**만 골라서 **`senior_table`**이라는 리스트에 따로 담아주세요.

senior_table = []
for i, item in enumerate(members):
    if members[i]["age"] >= 30:
        senior_table.append(members[i]["name"])

print(senior_table)