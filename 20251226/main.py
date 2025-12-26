# 어차피 글은 다 str처리 할 거니까 신경끄기.

class Board():
    def __init__(self, msg):
        self.msg = msg

    def create_board(self):
        open (self.msg, 'w', encoding='utf-8').close()
        return NotImplemented

    def read_board(self):
        open (self.msg, 'r', encoding='utf-8').read()
        return NotImplemented
    
    def update_board(self):
        open (self.msg, 'a', encoding='utf-8').write(self.msg)
        return NotImplemented
    
    def delete_board(self):
        del self.msg
        return NotImplemented