class MemoManager:
    def __init__(self):
        self.memos = {i: "" for i in range(1, 10)}

    def create_memo(self, mid, title):
        if mid in self.memos:
            self.memos[mid] = title
            return title
        return None

    def read_memos(self):
        return self.memos

    def update_memo(self, mid, title):
        if mid in self.memos:
            self.memos[mid] = title
            return title
        return None

    def delete_memo(self, mid):
        if mid in self.memos:
            self.memos[mid] = ""
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