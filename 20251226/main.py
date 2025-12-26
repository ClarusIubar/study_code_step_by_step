import os

# * 텍스트 파일 CRUD 클래스
class Board():
    def __init__(self, file_name):
        self.file_name = file_name

    # * 윈도우에 새 파일 만들기
    def create_board(self): 
        if os.path.exists(self.file_name):
            print("파일이 이미 존재합니다.")
            pass
        else:
            open (self.file_name, 'w', encoding='utf-8').close()

    # * 선택한 파일 읽기
    def read_board(self, file_name):
        if not os.path.exists(file_name):  
            print("파일이 존재하지 않습니다.")
            return
        else:
            text = open (file_name, 'r', encoding='utf-8').read().strip()
            print(text)

    # * 선택한 파일에 글 추가하기
    def update_board(self, content, file_name=None):
        target_file = file_name if file_name is not None else self.file_name

        if not os.path.exists(target_file):
            print(f"[{target_file}] 파일이 존재하지 않습니다.")
            return
        else:
            open (target_file, 'a', encoding='utf-8').write(content + "\n")

    # * 선택한 파일 삭제하기
    def delete_board(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print("파일이 존재하지 않습니다.")

# * 테스트 코드
if __name__ == "__main__":

    # 파일 생성 및 초기화
    board = Board("board.txt")
    # board.create_board() # 그냥 빈 파일 생성

    msg = input("메세지를 입력하세요: ")
    board.update_board(msg)
    board.update_board(msg, "test.txt")

    # board.read_board("board.txt") # 파일 읽기

    # board.delete_board("test.txt") # 파일 삭제