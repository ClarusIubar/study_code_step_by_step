from pyscript import document

class VendingMachine:
    def __init__(self):
        self.selected_item = None
        self.wishes = []

    def select_item(self, name):
        self.selected_item = name
        self.update_display(f"{name} 선택됨")

    def pay(self, method):
        if not self.selected_item:
            self.update_display("먼저 제품을 선택하세요.")
            return
        
        result = f"{self.selected_item} -> {method} 결제 완료"
        self.selected_item = None
        self.update_display(result)

    def add_wish(self, title):
        if not title.strip():
            return
        self.wishes.append(title)
        self.update_display(f"건의: {title}")
        return self.wishes

    def update_display(self, message):
        document.querySelector("#display-log").innerText = f"상태: {message}"