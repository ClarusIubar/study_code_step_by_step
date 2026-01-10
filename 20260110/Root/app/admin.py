import asyncio
import json
from pyscript import document
from pyodide.ffi import create_proxy
from service.vendingmachine import VendingMachineService

async def init_admin():
    await asyncio.sleep(0.3)
    
    try:
        with open("products.json", "r", encoding="utf-8") as f: data = f.read()
    except: data = "{}"
    
    vm = VendingMachineService(data)

    def update_admin_ui():
        """수익금 및 각 슬롯 재고 현황을 화면에 매핑"""
        document.querySelector("#revenue-display").innerText = f"{vm.total_revenue}원"
        for p in vm.products.get_all():
            stock_el = document.querySelector(f"#stock-{p.id}")
            if stock_el:
                stock_el.innerText = f"재고: {p.stock}/10"
                stock_el.style.color = "#ff4444" if p.stock <= 0 else "#0f0"

    def handle_refill(p_id):
        """재고 보충 처리 및 UI 동기화"""
        success, msg = vm.refill_one(p_id)
        document.querySelector("#log-bar").innerText = f"> {msg}"
        update_admin_ui()

    def handle_collect(e):
        """수익금 회수 처리 및 UI 동기화"""
        amount = vm.collect_revenue()
        document.querySelector("#log-bar").innerText = f"> 수익금 {amount}원 회수 완료 (금고 초기화)"
        update_admin_ui()

    # 1. 관리자용 그리드 생성
    grid = document.querySelector("#admin-grid")
    grid.innerHTML = ""
    for p in vm.products.get_all():
        div = document.createElement("div")
        div.className = "admin-item"
        div.innerHTML = f"""
            <small>Slot {p.id}</small><br>
            <b style='font-size:11px; display:block; margin:5px 0;'>{p.name}</b>
            <span id='stock-{p.id}' style='font-size:12px; font-weight:bold;'>재고: {p.stock}/10</span><br>
            <button class='refill-btn' id='refill-{p.id}'>보충 +1</button>
        """
        grid.appendChild(div)
        
        # 클로저 이슈 방지를 위한 핸들러 생성 함수
        def make_handler(pid):
            return create_proxy(lambda e: handle_refill(pid))
        
        document.querySelector(f"#refill-{p.id}").onclick = make_handler(p.id)

    # 2. 전액 회수 버튼 바인딩
    document.querySelector("#collect-btn").onclick = create_proxy(handle_collect)

    # 3. 초기 데이터 반영 (LocalStorage 복구 데이터 포함)
    update_admin_ui()

# 실행 예약
asyncio.ensure_future(init_admin())