import os
# 어차피 글은 다 str처리 할 거니까 신경끄기.

class Board():
    def __init__(self, file_name):
        self.file_name = file_name

    def create_board(self):
        if os.path.exists(self.file_name):
            print("파일이 이미 존재합니다.")
            pass
        else:
            open (self.file_name, 'w', encoding='utf-8').close()

    def read_board(self):
        # print()같은 것을 쓰지 않으면, 내용이 불러들어오지 않으니까 메서드 내에서 동작하게 하고 싶어.
        return open (self.file_name, 'r', encoding='utf-8').read()

    def update_board(self, content):
        return open (self.file_name, 'a', encoding='utf-8').write(content + "\n")

    def delete_board(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print("파일이 존재하지 않습니다.")

if __name__ == "__main__":

    # 파일 생성 및 초기화
    board = Board("board.txt")
    # board.create_board() # 그냥 빈 파일 생성

    # msg = input("메세지를 입력하세요: ")
    # board.update_board(msg)

    # print(board.read_board()) # 파일 읽기

    board.delete_board("test.txt") # 파일 삭제