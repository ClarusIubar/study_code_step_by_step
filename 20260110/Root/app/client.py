import asyncio
from pyscript import document
from pyodide.ffi import create_proxy
from service.vendingmachine import VendingMachineService

async def init_system():
    # DOM 안정화 대기
    await asyncio.sleep(0.3)
    
    try:
        with open("products.json", "r", encoding="utf-8") as f: data = f.read()
    except: data = "{}"
    
    vm = VendingMachineService(data)
    dispensed_items = [] # 토출구 배열

    def update_ui():
        """잔액 및 상품 활성화 상태 실시간 동기화"""
        document.querySelector("#balance-display").innerText = f"{vm.balance}원"
        for p in vm.products.get_all():
            el = document.querySelector(f"#item-{p.id}")
            if el:
                if vm.balance >= p.price and p.stock > 0: el.classList.add("on")
                else: el.classList.remove("on")
        document.querySelector("#take-btn").style.display = "block" if dispensed_items else "none"

    # --- [숫자 키패드 핸들러] ---
    def handle_key(e):
        val = e.target.getAttribute("data-val")
        inp = document.querySelector("#code-input")
        if len(inp.value) < 2: inp.value += val

    def clear_key(e): document.querySelector("#code-input").value = ""

    # --- [결제 시스템 핸들러] ---
    def handle_cash(e):
        amt = int(e.target.getAttribute("data-amt"))
        success, msg = vm.insert_cash(amt)
        document.querySelector("#log-bar").innerText = f"> {msg}"
        update_ui()

    async def on_card(e):
        document.querySelector("#log-bar").innerText = "> 카드 통신 시도 중..."
        await asyncio.sleep(0.8)
        success, msg = vm.tag_card()
        document.querySelector("#log-bar").innerText = f"> {msg}"
        update_ui()

    def on_confirm(e):
        try:
            val = document.querySelector("#code-input").value
            p, msg = vm.purchase(int(val))
            document.querySelector("#log-bar").innerText = f"> {msg}"
            if p:
                dispensed_items.append(p)
                render_out(); update_ui()
                document.querySelector("#code-input").value = ""
        except: pass

    def render_out():
        lst = document.querySelector("#product-list")
        lst.innerHTML = ""
        for item in dispensed_items:
            img = document.createElement("img")
            img.src = item.image; img.style.margin = "3px"
            img.onerror = create_proxy(lambda e: setattr(e.target, 'src', "https://img.icons8.com/color/48/error.png"))
            lst.appendChild(img)

    # --- [메모 CRUD 및 다이렉트 편집 핸들러] ---
    def refresh_memos():
        """1x9 압축 메모지 렌더링 (ID 및 클릭 동기화 복원)"""
        grid = document.querySelector("#memo-grid")
        grid.innerHTML = "" # 중복 방지
        for m in vm.memos.get_all():
            sticker = document.createElement("div")
            sticker.className = "memo-sticker"
            sticker.style.background = "#fff9c4" if m.title else "#fafafa"
            
            # 1. ID 라벨 생성 (v27.1 누락 복구)
            id_lbl = document.createElement("div")
            id_lbl.className = "memo-id-label"; id_lbl.innerText = str(m.id)
            sticker.appendChild(id_lbl)
            
            # 2. 다이렉트 편집 영역
            editor = document.createElement("div")
            editor.contentEditable = "true"; editor.innerText = m.title
            editor.style.outline = "none"; editor.style.width = "100%"; editor.style.flex = "1"
            
            # 스티커 클릭 시 상단 입력창으로 ID 채우기
            def make_click_handler(mid):
                def on_click(e): document.querySelector("#memo-id").value = str(mid)
                return on_click
            sticker.onclick = create_proxy(make_click_handler(m.id))
            
            # 타이핑 시 데이터 동기화
            def make_input_handler(mid, el, parent):
                def on_input(e):
                    memo = vm.memos.find_by_id(mid)
                    memo.title = el.innerText
                    parent.style.background = "#fff9c4" if memo.title else "#fafafa"
                return on_input
            editor.oninput = create_proxy(make_input_handler(m.id, editor, sticker))
            sticker.appendChild(editor); grid.appendChild(sticker)

    def handle_memo(op):
        """상단 버튼(생성/수정/삭제) 연동 로직"""
        try:
            mid = int(document.querySelector("#memo-id").value)
            txt = document.querySelector("#memo-title").value
            m = vm.memos.find_by_id(mid)
            if m:
                if op == "D": m.title = ""
                else: m.title = txt
                refresh_memos() # 명시적 UI 갱신
                document.querySelector("#memo-id").value = ""
                document.querySelector("#memo-title").value = ""
        except: pass

    # --- [초기화 및 리스너 등록] ---
    
    # 1. 상품 그리드 생성 (6x6)
    p_grid = document.querySelector("#product-grid")
    p_grid.innerHTML = ""
    for p in vm.products.get_all():
        div = document.createElement("div")
        div.id = f"item-{p.id}"; div.className = "grid-item"
        div.innerHTML = f"<img src='{p.image}' onerror='this.src=\"https://img.icons8.com/color/48/error.png\"'><br><b>{p.id}</b><br><small>{p.price}원</small>"
        div.onclick = create_proxy(lambda e, idx=p.id: setattr(document.querySelector("#code-input"), 'value', str(idx)))
        p_grid.appendChild(div)

    # 2. 모든 버튼 리스너 바인딩 (생략 제로)
    for btn in document.querySelectorAll(".key-btn[data-val]"):
        btn.onclick = create_proxy(handle_key)
    document.querySelector("#key-clr").onclick = create_proxy(clear_key)
    for btn in document.querySelectorAll(".btn-cash"):
        btn.onclick = create_proxy(handle_cash)
        
    document.querySelector("#card-btn").onclick = create_proxy(on_card)
    document.querySelector("#confirm-btn").onclick = create_proxy(on_confirm)
    document.querySelector("#return-btn").onclick = create_proxy(lambda e: (vm.reset_system(), update_ui()))
    document.querySelector("#take-btn").onclick = create_proxy(lambda e: (vm.reset_system(), dispensed_items.clear(), render_out(), update_ui()))
    
    # 메모 버튼 리스너
    document.querySelector("#m-create").onclick = create_proxy(lambda e: handle_memo("C"))
    document.querySelector("#m-update").onclick = create_proxy(lambda e: handle_memo("U"))
    document.querySelector("#m-delete").onclick = create_proxy(lambda e: handle_memo("D"))

    refresh_memos()
    update_ui()

asyncio.ensure_future(init_system())