import asyncio
import json
from pyscript import document
from pyodide.ffi import create_proxy
from service.vendingmachine import VendingMachineService

async def init_admin():
    await asyncio.sleep(0.3)
    try:
        with open("products.json", "r", encoding="utf-8") as f: 
            data = f.read()
    except Exception as e:
        document.querySelector("#log-bar").innerText = f"> 파일 로드 실패: {e}"
        data = "{}"
    
    vm = VendingMachineService(data)
    
    if not vm.products.get_all():
        document.querySelector("#log-bar").innerText = "> 경고: 제품 데이터가 비어있습니다."

    def update_admin_ui():
        """수익금 및 각 슬롯 재고 현황 업데이트"""
        document.querySelector("#revenue-display").innerText = f"{vm.total_revenue}원"
        for p in vm.products.get_all():
            stock_el = document.querySelector(f"#stock-{p.id}")
            if stock_el:
                stock_el.innerText = f"재고: {p.stock}/10"
                # 품절 시 시각적 경고
                stock_el.style.color = "#ff4444" if p.stock <= 0 else "#0f0"

    def handle_refill(p_id):
        """개별 상품 보충"""
        success, msg = vm.refill_one(p_id)
        document.querySelector("#log-bar").innerText = f"> {msg}"
        update_admin_ui()

    def handle_collect(e):
        """매출액 회수"""
        amount = vm.collect_revenue()
        document.querySelector("#log-bar").innerText = f"> 수익금 {amount}원이 회수되었습니다. (금고 비움)"
        update_admin_ui()

    # 1. 관리자 그리드 (뒷면) 생성
    grid = document.querySelector("#admin-grid")
    grid.innerHTML = ""
    for p in vm.products.get_all():
        div = document.createElement("div")
        div.className = "admin-item"
        div.innerHTML = f"""
            <small>Slot {p.id}</small><br>
            <b style='font-size:10px;'>{p.name}</b><br>
            <span id='stock-{p.id}' style='font-size:11px;'>재고: {p.stock}/10</span><br>
            <button class='refill-btn' id='refill-{p.id}'>보충 +1</button>
        """
        grid.appendChild(div)
        
        # 보충 버튼 리스너 바인딩
        def make_refill_handler(pid):
            return lambda e: handle_refill(pid)
        document.querySelector(f"#refill-{p.id}").onclick = create_proxy(make_refill_handler(p.id))

    # 2. 전액 회수 리스너
    document.querySelector("#collect-btn").onclick = create_proxy(handle_collect)

    update_admin_ui()

asyncio.ensure_future(init_admin())