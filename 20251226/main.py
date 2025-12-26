import os
# 어차피 글은 다 str처리 할 거니까 신경끄기.

class Board():
    def __init__(self, file_name):
        self.file_name = file_name

    def create_board(self):
        open (self.file_name, 'w', encoding='utf-8').close()

    def read_board(self):
        return open (self.file_name, 'r', encoding='utf-8').read()

    def update_board(self, content):
        return open (self.file_name, 'a', encoding='utf-8').write(content)

    def delete_board(self):
        os.remove(self.file_name)

if __name__ == "__main__":

    # 파일 생성 및 초기화
    board = Board("board.txt")
    # board.create_board() # 그냥 빈 파일 생성

    # msg = input("메세지를 입력하세요: ")
    # board.update_board(msg + "\n")

    print(board.read_board()) # 파일 읽기

    # board.delete_board() # 파일 삭제