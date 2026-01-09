import asyncio
from pyscript import document
from pyodide.ffi import create_proxy
from logic import VendingMachine
from memo import MemoManager

async def init_system():
    await asyncio.sleep(0.3)
    try:
        with open("products.json", "r", encoding="utf-8") as f: data = f.read()
    except: data = "{}"
    
    vm = VendingMachine(data)
    mm = MemoManager()
    dispensed_items = []

    def update_ui():
        document.querySelector("#balance-display").innerText = f"{vm.balance}원"
        for i in range(1, 37):
            el = document.querySelector(f"#item-{i}")
            if el and i in vm.products:
                p = vm.products[i]
                if vm.balance >= p['price'] and p['stock'] > 0: el.classList.add("on")
                else: el.classList.remove("on")
        document.querySelector("#take-btn").style.display = "block" if dispensed_items else "none"

    # 메모 직접 클릭 로직
    def on_memo_grid_select(idx):
        memos = mm.read_memos()
        document.querySelector("#memo-id").value = str(idx)
        document.querySelector("#memo-title").value = memos.get(idx, "")
        document.querySelector("#memo-title").focus()

    def refresh_memos():
        grid = document.querySelector("#memo-grid")
        grid.innerHTML = ""
        memos = mm.read_memos()
        for i in range(1, 10):
            div = document.createElement("div")
            div.className = "memo-sticker"
            if i in memos:
                div.innerHTML = f"<b>{i}</b><br>{memos[i]}"
                div.style.background = "#fff9c4"
            else:
                div.innerHTML = f"<span style='color:#ccc'>{i}</span>"
                div.style.background = "#fafafa"
            div.onclick = create_proxy(lambda e, idx=i: on_memo_grid_select(idx))
            grid.appendChild(div)

    def handle_memo(op):
        try:
            mid = int(document.querySelector("#memo-id").value)
            if mid <= 0:
                document.querySelector("#log-bar").innerText = "> 오류: ID는 1 이상의 숫자만 가능합니다."
                return
            txt = document.querySelector("#memo-title").value
            if op == "C": mm.create_memo(mid, txt)
            elif op == "U": mm.update_memo(mid, txt)
            elif op == "D": mm.delete_memo(mid)
            refresh_memos()
            document.querySelector("#memo-id").value = ""
            document.querySelector("#memo-title").value = ""
        except:
            document.querySelector("#log-bar").innerText = "> 오류: 올바른 ID와 내용을 입력하세요."

    # 자판기 로직
    def on_confirm(e):
        code = document.querySelector("#code-input").value
        product, msg = vm.purchase(code)
        document.querySelector("#log-bar").innerText = f"> {msg}"
        if product:
            dispensed_items.append(product)
            render_out()
            update_ui()

    def render_out():
        lst = document.querySelector("#product-list")
        lst.innerHTML = ""
        for item in dispensed_items:
            img = document.createElement("img")
            img.src = item['image']
            lst.appendChild(img)

    async def on_card(e):
        document.querySelector("#log-bar").innerText = "> 카드 인증 중..."
        await asyncio.sleep(1.0)
        vm.balance = 20000
        vm.payment_locked = "CARD"
        update_ui()

    # 리스너 등록
    document.querySelector("#cash-btn").onclick = create_proxy(lambda e: (vm.insert_cash(1000), update_ui()))
    document.querySelector("#card-btn").onclick = create_proxy(on_card)
    document.querySelector("#confirm-btn").onclick = create_proxy(on_confirm)
    document.querySelector("#return-btn").onclick = create_proxy(lambda e: (vm.reset_system(), update_ui()))
    document.querySelector("#take-btn").onclick = create_proxy(lambda e: (vm.reset_system(), dispensed_items.clear(), render_out(), update_ui()))
    
    document.querySelector("#m-create").onclick = create_proxy(lambda e: handle_memo("C"))
    document.querySelector("#m-update").onclick = create_proxy(lambda e: handle_memo("U"))
    document.querySelector("#m-delete").onclick = create_proxy(lambda e: handle_memo("D"))

    # 상품 그리드 생성
    grid = document.querySelector("#product-grid")
    for i in range(1, 37):
        p = vm.products[i]
        div = document.createElement("div")
        div.id = f"item-{i}"
        div.className = "grid-item"
        div.innerHTML = f"<img src='{p['image']}' onerror='this.src=\"https://img.icons8.com/color/48/error.png\"'><br><b>{i}</b><br><small>{p['price']}원</small>"
        div.onclick = create_proxy(lambda e, idx=i: setattr(document.querySelector("#code-input"), 'value', str(idx)))
        grid.appendChild(div)

    refresh_memos()
    update_ui()