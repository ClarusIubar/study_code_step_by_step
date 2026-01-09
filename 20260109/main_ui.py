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
    dispensed_items = [] # 토출구에 쌓인 상품 리스트

    def update_ui():
        """잔액 및 상품 가용성 실시간 업데이트"""
        document.querySelector("#balance-display").innerText = f"{vm.balance}원"
        
        # 6x6 그리드 하이라이트 (잔액 내 구매 가능 상품만 ON)
        for i in range(1, 37):
            el = document.querySelector(f"#item-{i}")
            if el and i in vm.products:
                p = vm.products[i]
                if vm.balance >= p['price'] and p['stock'] > 0:
                    el.classList.add("on")
                else:
                    el.classList.remove("on")
        
        # 수령 버튼 노출 제어
        take_btn = document.querySelector("#take-btn")
        take_btn.style.display = "block" if dispensed_items else "none"

    def refresh_memos():
        grid = document.querySelector("#memo-grid")
        grid.innerHTML = ""
        memos = mm.read_memos()
        for i in range(1, 10):
            div = document.createElement("div")
            div.className = "memo-sticker"
            if i in memos: div.innerHTML = f"<b>{i}</b><br>{memos[i]}"
            else: div.innerHTML = f"<span style='color:#ccc'>{i}</span>"
            grid.appendChild(div)

    async def on_card(e):
        document.querySelector("#log-bar").innerText = "> 카드 승인 중..."
        await asyncio.sleep(1.0)
        vm.balance = 20000
        vm.payment_locked = "CARD"
        document.querySelector("#log-bar").innerText = "> 카드 승인 완료. 상품을 선택하세요."
        update_ui()

    def on_confirm(e):
        """다중 구매 로직: 구매 후에도 추가 구매 가능"""
        code = document.querySelector("#code-input").value
        product, msg = vm.purchase(code)
        document.querySelector("#log-bar").innerText = f"> {msg}"
        
        if product:
            dispensed_items.append(product)
            render_output_slot()
            document.querySelector("#code-input").value = ""
            update_ui() # 잔액이 남았다면 다른 상품 하이라이트 유지

    def render_output_slot():
        """토출구에 구매한 상품들을 나열"""
        out_div = document.querySelector("#product-list")
        out_div.innerHTML = ""
        for item in dispensed_items:
            img = document.createElement("img")
            img.src = item['image']
            img.style.cssText = "height:60px; margin:5px;"
            out_div.appendChild(img)

    def on_take(e):
        """명시적 수령: 상품 수거 및 잔액 반환 (초기화)"""
        if not dispensed_items: return
        
        change = vm.reset_system()
        dispensed_items.clear()
        render_output_slot()
        document.querySelector("#log-bar").innerText = f"> 상품 수령 완료 및 잔돈 {change}원 반환"
        update_ui()

    def on_return(e):
        """변심 시 반환"""
        change = vm.reset_system()
        document.querySelector("#log-bar").innerText = f"> 반환 완료: {change}원"
        update_ui()

    # 리스너 등록 (비약 없음)
    document.querySelector("#cash-btn").onclick = create_proxy(lambda e: (vm.insert_cash(1000), update_ui()))
    document.querySelector("#card-btn").onclick = create_proxy(on_card)
    document.querySelector("#confirm-btn").onclick = create_proxy(on_confirm)
    document.querySelector("#return-btn").onclick = create_proxy(on_return)
    document.querySelector("#take-btn").onclick = create_proxy(on_take)
    
    # 메모 CRUD
    def memo_cmd(op):
        try:
            mid = int(document.querySelector("#memo-id").value)
            txt = document.querySelector("#memo-title").value
            if op == "C": mm.create_memo(mid, txt)
            elif op == "U": mm.update_memo(mid, txt)
            elif op == "D": mm.delete_memo(mid)
            refresh_memos()
        except: pass

    document.querySelector("#m-create").onclick = create_proxy(lambda e: memo_cmd("C"))
    document.querySelector("#m-update").onclick = create_proxy(lambda e: memo_cmd("U"))
    document.querySelector("#m-delete").onclick = create_proxy(lambda e: memo_cmd("D"))

    # 그리드 초기화
    grid = document.querySelector("#product-grid")
    grid.innerHTML = ""
    for i in range(1, 37):
        p = vm.products[i]
        div = document.createElement("div")
        div.id = f"item-{i}"
        div.className = "grid-item"
        div.innerHTML = f"<img src='{p['image']}' onerror='this.src=\"https://img.icons8.com/color/48/error.png\"'><br><b>{i}</b><br><small>{p['price']}원</small>"
        div.onclick = create_proxy(lambda e, idx=i: (document.querySelector("#code-input").focus(), setattr(document.querySelector("#code-input"), 'value', str(idx))))
        grid.appendChild(div)

    refresh_memos()
    update_ui()