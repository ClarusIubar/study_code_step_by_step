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
        # 어떤 파일을 업데이터 할 건지 정하고, 내용을 추가하게 할래.
        # 매개변수에 파일인지 내용인지 구분하게 해서 헷갈리지 않게 할래.
        return open (self.file_name, 'a', encoding='utf-8').write(content)

    def delete_board(self):
        # 어떤 것을 삭제할 건지 정하고, 그 파일을 삭제하게 할래.
        # 테스트 케이스에 파일이름을 할당하게 하고 싶지 않아. 그건 리터럴이야.
        # 최소한 사람이 어떤 파일을 삭제하는지 직접 입력하게 할래.
        # 근데 있지도 않은 것을 삭제하게 하면 에러가 나니까 방어하고 싶어.
        os.remove(self.file_name)

if __name__ == "__main__":

    # 파일 생성 및 초기화
    board = Board("board.txt")
    board.create_board() # 그냥 빈 파일 생성

    # msg = input("메세지를 입력하세요: ")
    # board.update_board(msg + "\n")

    # print(board.read_board()) # 파일 읽기

    # board.delete_board() # 파일 삭제