# record_popup.py
import tkinter as tk
from base_popup import BasePopup
from delete_check_popup import DeleteCheckPopup

class RecordViewPopup(BasePopup):
    def __init__(self, root, storage):
        # [주의] 부모의 __init__ 내에서 _build_ui가 호출되므로 
        # storage를 부모 호출보다 먼저 할당해야 에러가 나지 않음
        self.storage = storage 
        super().__init__(root, "전체 저장 기록 조회", width=450, height=350)

    def _build_ui(self):
        """추상 메서드 구현: 리스트 렌더링 시작"""
        self.render_list()

    def render_list(self):
        """데이터를 읽어와 화면에 표시 (새로고침 기능 포함)"""
        # 기존 위젯 소거 (Refresh)
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="[ 로또 추출 이력 ]", font=("Arial", 12, "bold"), pady=10).pack()
        
        all_records = self.storage.read_all()
        
        if not all_records:
            tk.Label(self, text="저장된 데이터가 없습니다.", pady=50, fg="gray").pack()
        else:
            for record in all_records:
                row_frame = tk.Frame(self)
                row_frame.pack(fill="x", padx=20, pady=2)
                
                # 변수명 명확화 (record 사용)
                record_id = record['id']
                nums = record['numbers']
                date = record['date']
                
                text = f"ID:{record_id:02d} | {nums} | {date}"
                tk.Label(row_frame, text=text, font=("Consolas", 9)).pack(side="left")
                
                # 개별 삭제 버튼
                tk.Button(row_frame, text="X", fg="red", 
                          command=lambda target_id=record_id: self.request_delete(target_id)).pack(side="right")
        
        tk.Button(self, text="닫기", width=10, command=self.destroy).pack(pady=15, side="bottom")

    def request_delete(self, target_id):
        """확인 팝업 요청"""
        DeleteCheckPopup(root=self, record_id=target_id, on_confirm=self.execute_delete)

    def execute_delete(self, record_id):
        """최종 삭제 및 화면 갱신"""
        self.storage.delete_by_id(record_id)
        self.render_list()