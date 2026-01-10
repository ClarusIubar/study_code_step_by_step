import asyncio
from pyscript import document, window
from pyodide.ffi import create_proxy
from service.vendingmachine import VendingMachineService

async def init_system():
    # [방어] 싱글톤 가드: 상태 분리 현상 원천 차단
    if hasattr(window, "__VM_SYSTEM_READY__"): return
    window.__VM_SYSTEM_READY__ = True

    await asyncio.sleep(0.3)
    try:
        with open("products.json", "r", encoding="utf-8") as f: data = f.read()
    except: data = "{}"
    
    vm = VendingMachineService(data)
    window.__VM_INSTANCE__ = vm
    dispensed_items = []

    def set_status(msg: str):
        """[중앙 집중형 로그 제어] 모든 상태 변화 시 하단 바 갱신"""
        document.querySelector("#log-bar").innerText = f"> {msg}"

    def update_ui():
        document.querySelector("#balance-display").innerText = f"{vm.balance}원"
        for p in vm.products.get_all():
            el = document.querySelector(f"#item-{p.id}")
            if el:
                if vm.balance >= p.price and p.stock > 0: el.classList.add("on")
                else: el.classList.remove("on")
        document.querySelector("#take-btn").style.display = "block" if dispensed_items else "none"

    def handle_key(e):
        val = e.target.getAttribute("data-val")
        inp = document.querySelector("#code-input")
        if inp.value == "00": inp.value = ""
        if len(inp.value) < 2: inp.value += val
        set_status("번호 입력 중...") # 상태 바 갱신을 통해 이전 에러 메시지 제거

    def on_confirm(e):
        """[입력 정합성 강화] 명령 종료 시 입력창 무조건 리셋"""
        inp = document.querySelector("#code-input")
        try:
            val_str = inp.value.strip()
            if not val_str or val_str == "00":
                set_status("제품 번호를 입력하세요.")
                return
            
            p, msg = vm.purchase(int(val_str))
            set_status(msg) # 결과 출력
            if p:
                dispensed_items.append(p)
                render_out(); update_ui()
            
            # [수정] 성공/실패 여부와 관계없이 입력창을 초기화하여 '33' 입력을 방지
            inp.value = "00"
        except Exception as err:
            set_status(f"오류: {err}")
            inp.value = "00"

    def handle_cash(e):
        amt = int(e.target.getAttribute("data-amt"))
        success, msg = vm.insert_cash(amt)
        set_status(msg); update_ui()

    async def on_card(e):
        set_status("카드 통신 중..."); await asyncio.sleep(0.8)
        success, msg = vm.tag_card()
        set_status(msg); update_ui()

    def render_out():
        lst = document.querySelector("#product-list"); lst.innerHTML = ""
        for item in dispensed_items:
            img = document.createElement("img"); img.src = item.image
            img.onerror = create_proxy(lambda e: setattr(e.target, 'src', "https://img.icons8.com/color/48/error.png"))
            lst.appendChild(img)

    def refresh_memos():
        grid = document.querySelector("#memo-grid"); grid.innerHTML = ""
        for m in vm.memos.get_all():
            sticker = document.createElement("div"); sticker.className = "memo-sticker"
            sticker.style.background = "#fff9c4" if m.title else "#fafafa"
            sticker.innerHTML = f"<div class='memo-id-label'>{m.id}</div><div contentEditable='true' class='memo-editor'>{m.title}</div>"
            def make_input_handler(target_m, el, parent):
                def on_input(e): target_m.title = el.innerText; parent.style.background = "#fff9c4" if target_m.title else "#fafafa"; vm.save_state()
                return on_input
            editor = sticker.querySelector(".memo-editor")
            editor.oninput = create_proxy(make_input_handler(m, editor, sticker))
            grid.appendChild(sticker)

    # 이벤트 바인딩
    for btn in document.querySelectorAll(".key-btn[data-val]"): btn.onclick = create_proxy(handle_key)
    document.querySelector("#key-clr").onclick = create_proxy(lambda e: (setattr(document.querySelector("#code-input"), 'value', '00'), set_status("입력 초기화")))
    document.querySelector("#confirm-btn").onclick = create_proxy(on_confirm)
    for btn in document.querySelectorAll(".btn-cash"): btn.onclick = create_proxy(handle_cash)
    document.querySelector("#card-btn").onclick = create_proxy(on_card)
    document.querySelector("#return-btn").onclick = create_proxy(lambda e: (vm.reset_system(), set_status("반환 완료"), update_ui()))
    document.querySelector("#take-btn").onclick = create_proxy(lambda e: (vm.reset_system(), dispensed_items.clear(), render_out(), update_ui(), set_status("시스템 가동 준비 완료")))

    p_grid = document.querySelector("#product-grid"); p_grid.innerHTML = ""
    for p in vm.products.get_all():
        div = document.createElement("div"); div.id = f"item-{p.id}"; div.className = "grid-item"
        div.innerHTML = f"<img src='{p.image}' onerror='this.src=\"https://img.icons8.com/color/48/error.png\"'><br><b>{p.id}</b><br><small>{p.price}원</small>"
        div.onclick = create_proxy(lambda e, idx=p.id: (setattr(document.querySelector("#code-input"), 'value', str(idx)), set_status(f"{idx}번 상품 선택됨")))
        p_grid.appendChild(div)

    refresh_memos(); update_ui()

asyncio.ensure_future(init_system())