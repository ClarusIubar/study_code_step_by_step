import asyncio
from pyscript import document, window
from pyodide.ffi import create_proxy
from service.vendingmachine import VendingMachineService

async def init_admin():
    if hasattr(window, "__VM_ADMIN_READY__"): return
    window.__VM_ADMIN_READY__ = True

    await asyncio.sleep(0.3)
    try:
        with open("products.json", "r", encoding="utf-8") as f: data = f.read()
    except: data = "{}"
    
    vm = VendingMachineService(data)

    def update_admin_ui():
        document.querySelector("#revenue-display").innerText = f"{vm.total_revenue}원"
        for p in vm.products.get_all():
            el = document.querySelector(f"#stock-{p.id}")
            if el:
                el.innerText = f"재고: {p.stock}/10"
                el.style.color = "#ff4444" if p.stock <= 0 else "#0f0"

    def handle_admin_click(e):
        target = e.target.closest(".refill-btn")
        if target:
            p_id = int(target.getAttribute("data-id"))
            success, msg = vm.refill_one(p_id)
            document.querySelector("#log-bar").innerText = f"> {msg}"
            update_admin_ui()

    grid = document.querySelector("#admin-grid")
    html = [f"<div class='admin-item'><small>Slot {p.id}</small><br><b>{p.name[:5]}</b><br><span id='stock-{p.id}'>재고: {p.stock}/10</span><br><button class='refill-btn' data-id='{p.id}'>보충 +1</button></div>" for p in vm.products.get_all()]
    grid.innerHTML = "".join(html)
    grid.onclick = create_proxy(handle_admin_click)

    def handle_collect(e):
        amt = vm.collect_revenue()
        document.querySelector("#log-bar").innerText = f"> {amt}원 회수 완료"
        update_admin_ui()

    document.querySelector("#collect-btn").onclick = create_proxy(handle_collect)
    update_admin_ui()

asyncio.ensure_future(init_admin())