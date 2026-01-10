import asyncio
from pyscript import document, window
from pyodide.ffi import create_proxy
from service.vendingmachine import VendingMachineService

async def init_system():
    if hasattr(window, "__VM_CLIENT_READY__"): return
    window.__VM_CLIENT_READY__ = True

    await asyncio.sleep(0.3)
    try:
        with open("products.json", "r", encoding="utf-8") as f: data = f.read()
    except: data = "{}"
    
    vm = VendingMachineService(data)
    dispensed_items = []

    def set_status(msg: str): document.querySelector("#log-bar").innerText = f"> {msg}"

    def update_ui():
        document.querySelector("#balance-display").innerText = f"{vm.balance}원"
        for p in vm.products.get_all():
            el = document.querySelector(f"#item-{p.id}")
            if el:
                if vm.balance >= p.price and p.stock > 0: el.classList.add("on")
                else: el.classList.remove("on")
        document.querySelector("#take-btn").style.display = "block" if dispensed_items else "none"

    def on_confirm(e):
        inp = document.querySelector("#code-input")
        try:
            val_str = inp.value.strip()
            if not val_str or val_str == "00": return set_status("번호를 입력하세요.")
            p, msg = vm.purchase(int(val_str)); set_status(msg)
            if p: dispensed_items.append(p); render_out(); update_ui()
            inp.value = "00"
        except Exception as err: set_status(f"오류: {err}"); inp.value = "00"

    def render_out():
        """[수정] 토출구 상품 시인성 강화"""
        lst = document.querySelector("#product-list"); lst.innerHTML = ""
        for item in dispensed_items:
            div = document.createElement("div")
            div.className = "dispensed-item-label"
            div.innerText = item.name
            lst.appendChild(div)

    def handle_grid_click(e):
        target = e.target.closest(".grid-item")
        if target:
            p_id = target.getAttribute("data-id")
            document.querySelector("#code-input").value = p_id
            set_status(f"{p_id}번 상품 선택됨")

    def handle_key(e):
        val = e.target.getAttribute("data-val")
        inp = document.querySelector("#code-input")
        if inp.value == "00": inp.value = ""
        if len(inp.value) < 2: inp.value += val

    def handle_cash(e):
        amt = int(e.target.getAttribute("data-amt"))
        success, msg = vm.insert_cash(amt); set_status(msg); update_ui()

    async def handle_card(e):
        set_status("카드 통신 중..."); await asyncio.sleep(0.5)
        success, msg = vm.tag_card(); set_status(msg); update_ui()

    # [복구] 메모 CRUD 핸들러
    def refresh_memos():
        grid = document.querySelector("#memo-grid"); grid.innerHTML = ""
        for m in vm.memos.get_all():
            s = document.createElement("div"); s.className = "memo-sticker"
            s.innerHTML = f"<div class='memo-id-label'>{m.id}</div><div class='memo-editor'>{m.title}</div>"
            grid.appendChild(s)

    def on_m_create(e):
        mid = document.querySelector("#memo-id").value
        mtitle = document.querySelector("#memo-title").value
        if mid and mtitle:
            memo = vm._repository.find_by_id(type(vm.memos[0]), int(mid))
            if memo: memo.title = mtitle; vm.save_state(); refresh_memos(); set_status(f"{mid}번 메모 생성됨")

    def on_m_update(e):
        mid = document.querySelector("#memo-id").value
        mtitle = document.querySelector("#memo-title").value
        if mid:
            memo = vm._repository.find_by_id(type(vm.memos[0]), int(mid))
            if memo: memo.title = mtitle; vm.save_state(); refresh_memos(); set_status(f"{mid}번 메모 수정됨")

    def on_m_delete(e):
        mid = document.querySelector("#memo-id").value
        if mid:
            memo = vm._repository.find_by_id(type(vm.memos[0]), int(mid))
            if memo: memo.title = ""; vm.save_state(); refresh_memos(); set_status(f"{mid}번 메모 삭제됨")

    # 버튼들 바인딩
    for btn in document.querySelectorAll(".key-btn[data-val]"): btn.onclick = create_proxy(handle_key)
    document.querySelector("#key-clr").onclick = create_proxy(lambda e: setattr(document.querySelector("#code-input"), 'value', '00'))
    document.querySelector("#confirm-btn").onclick = create_proxy(on_confirm)
    for btn in document.querySelectorAll(".btn-cash"): btn.onclick = create_proxy(handle_cash)
    document.querySelector("#card-btn").onclick = create_proxy(handle_card)
    document.querySelector("#return-btn").onclick = create_proxy(lambda e: (vm.reset_system(), update_ui(), set_status("반환 완료")))
    document.querySelector("#take-btn").onclick = create_proxy(lambda e: (vm.reset_system(), dispensed_items.clear(), render_out(), update_ui(), set_status("준비 완료")))

    # 메모 CRUD 버튼 바인딩
    document.querySelector("#m-create").onclick = create_proxy(on_m_create)
    document.querySelector("#m-update").onclick = create_proxy(on_m_update)
    document.querySelector("#m-delete").onclick = create_proxy(on_m_delete)

    p_grid = document.querySelector("#product-grid")
    html = [f"<div id='item-{p.id}' class='grid-item' data-id='{p.id}'><div class='product-card'>{p.name[:4]}</div><b>{p.id}번</b><br><small>{p.price}원</small></div>" for p in vm.products.get_all()]
    p_grid.innerHTML = "".join(html)
    p_grid.onclick = create_proxy(handle_grid_click)

    refresh_memos(); update_ui()

asyncio.ensure_future(init_system())