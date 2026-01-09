class MemoManager:
    def __init__(self):
        self.memos = {i: "" for i in range(1, 10)} # 미리 가용 영역을 할당.

    # 혹시 모르니 id(배열을 직접 맵핑)하고 제목만 입력하게 한다. 제목과 내용이 분리된 형태가 아닌 포스트잇 형태의 메모.
    def create_memo(self, id, title): 
        if id in self.memos:
            self.memos[id] = title
            return title
        return None

    # 고정 할당된 영역에 상시 표시
    def read_memos(self):
        return self.memos

    def update_memo(self, id, title):
        if id in self.memos:
            self.memos[id] = title
            return title
        return None

    def delete_memo(self, id):
        if id in self.memos:
            self.memos[id] = "" # 빈 문자열로 바꾼다. # 영역 내의 문자들을 지울 뿐.
            return True
        return False

# def create_memo():
#     return NotImplementedError

# def read_memo():
#     return NotImplementedError

# def update_memo():
#     return NotImplementedError

# def delete_memo():
#     return NotImplementedError


## ---- ##
# 기본형 : id(배열id) - title(제목)

# * create 
# input (id, title)
# output (title)

# * read
# 상시 출력 상태

# * update
# input(id, title)
# output (title)

# * delete 
# input(id)