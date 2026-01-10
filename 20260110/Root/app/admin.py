import asyncio
from pyscript import document, window
from pyodide.ffi import create_proxy
from service.vendingmachine import VendingMachineService

async def init_admin():
    # [방어] 이중 실행 방지 가드
    if hasattr(window, "__VM_ADMIN_INITIALIZED__"): return
    window.__VM_ADMIN_INITIALIZED__ = True

    await asyncio.sleep(0.3)
    try:
        with open("products.json", "r", encoding="utf-8") as f: data = f.read()
    except: data = "{}"
    
    vm = VendingMachineService(data)

    def update_admin_ui():
        document.querySelector("#revenue-display").innerText = f"{vm.total_revenue}원"
        for p in vm.products.get_all():
            stock_el = document.querySelector(f"#stock-{p.id}")
            if stock_el:
                stock_el.innerText = f"재고: {p.stock}/10"
                stock_el.style.color = "#ff4444" if p.stock <= 0 else "#0f0"

    def handle_refill(p_id):
        success, msg = vm.refill_one(p_id)
        document.querySelector("#log-bar").innerText = f"> {msg}"; update_admin_ui()

    def handle_collect(e):
        amount = vm.collect_revenue()
        document.querySelector("#log-bar").innerText = f"> {amount}원 회수 완료"; update_admin_ui()

    # 관리자 그리드 생성
    grid = document.querySelector("#admin-grid"); grid.innerHTML = ""
    for p in vm.products.get_all():
        div = document.createElement("div"); div.className = "admin-item"
        div.innerHTML = f"""
            <small>Slot {p.id}</small><br>
            <b style='font-size:10px;'>{p.name}</b><br>
            <span id='stock-{p.id}'>재고: {p.stock}/10</span><br>
            <button class='refill-btn'>보충 +1</button>
        """
        grid.appendChild(div)
        div.querySelector(".refill-btn").onclick = create_proxy(lambda e, idx=p.id: handle_refill(idx))

    document.querySelector("#collect-btn").onclick = create_proxy(handle_collect)
    update_admin_ui()

asyncio.ensure_future(init_admin())