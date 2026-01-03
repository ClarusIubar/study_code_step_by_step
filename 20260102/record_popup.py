# record_popup.py
import tkinter as tk
from delete_check_popup import DeleteCheckPopup

class RecordViewPopup(tk.Toplevel):
    def __init__(self, root, storage): # storage 객체를 주입받음
        super().__init__(root)
        self.storage = storage
        self.title("전체 저장 기록 조회")
        
        # 위치 정합성 (부모 중앙 배치)
        self._align_to_center(root)
        
        # UI 그리기 시작
        self.render_list()

    def _align_to_center(self, root):
        self.update_idletasks()
        w, h = 450, 350
        px, py = root.winfo_rootx(), root.winfo_rooty()
        pw, ph = root.winfo_width(), root.winfo_height()
        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")    

    def render_list(self):
        """저장소의 데이터를 기반으로 리스트를 렌더링 (삭제 후 재호출 가능)"""
        # 기존에 그려진 위젯이 있다면 모두 제거 (새로고침 효과)
        for widget in self.winfo_children():
            widget.destroy()

        # 상단 타이틀
        tk.Label(self, text="[ 로또 추출 이력 ]", font=("Arial", 12, "bold"), pady=10).pack()
        
        # storage에서 데이터 읽기
        all_records = self.storage.read_all()
        
        if not all_records:
            tk.Label(self, text="저장된 데이터가 없습니다.", font=("Arial", 11), pady=50, fg="gray").pack()
        else:
            for record in all_records:
                row_frame = tk.Frame(self)
                row_frame.pack(fill="x", padx=20, pady=2)
                
                # 가독성을 위해 변수명 명확히 분리
                record_id = record['id']
                lotto_numbers = record['numbers']
                created_date = record['date']
                
                display_text = f"ID:{record_id:02d} | {lotto_numbers} | {created_date}"
                tk.Label(row_frame, text=display_text, font=("Consolas", 9)).pack(side="left")
                
                # 삭제 버튼: lambda를 통해 해당 ID를 박제
                tk.Button(
                    row_frame, 
                    text="X", 
                    fg="red", 
                    command=lambda target_id=record_id: self.handle_delete(target_id)
                ).pack(side="right")
        
        # 하단 닫기 버튼
        tk.Button(self, text="닫기", width=10, command=self.destroy).pack(pady=15)

    def handle_delete(self, target_id):
        """바로 삭제하지 않고, 재확인 팝업을 먼저 띄움"""
        DeleteCheckPopup(
            root=self, 
            record_id=target_id, 
            on_confirm=self._execute_actual_delete # 확인 시 실행될 진짜 삭제 함수
        )

    def _execute_actual_delete(self, record_id):
        """사용자가 '예'를 눌렀을 때만 호출되는 최종 삭제 단계"""
        self.storage.delete_by_id(record_id)
        self.render_list() # 리스트 갱신

