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
    dispensed_items = []

    def update_ui():
        """잔액 및 상품 상태 동기화"""
        document.querySelector("#balance-display").innerText = f"{vm.balance}원"
        for p in vm.products.get_all():
            el = document.querySelector(f"#item-{p.id}")
            if el:
                if vm.balance >= p.price and p.stock > 0: el.classList.add("on")
                else: el.classList.remove("on")
        document.querySelector("#take-btn").style.display = "block" if dispensed_items else "none"

    def refresh_memos():
        """메모지 다이렉트 편집 및 ID 상호 반응 로직"""
        grid = document.querySelector("#memo-grid")
        grid.innerHTML = "" # 중복 생성 방지
        
        for m in vm.memos.get_all():
            container = document.createElement("div")
            container.className = "memo-sticker"
            container.style.background = "#fff9c4" if m.title else "#fafafa"
            
            # 1. 스티커 클릭 시 상단 ID 입력창 동기화
            def make_click_handler(mid, parent):
                def on_click(e):
                    document.querySelector("#memo-id").value = str(mid)
                    # 이미 에디터에 포커스가 있는 경우는 제외하고 에디터로 포커스 이동
                    if e.target.className != "memo-body":
                        parent.querySelector(".memo-body").focus()
                return on_click
            
            container.onclick = create_proxy(make_click_handler(m.id, container))
            
            # ID 라벨
            id_tag = document.createElement("b")
            id_tag.innerText = str(m.id)
            container.appendChild(id_tag)
            
            # 2. 다이렉트 편집 영역
            editor = document.createElement("div")
            editor.className = "memo-body"
            editor.contentEditable = "true"
            editor.innerText = m.title
            editor.style.flex = "1"
            editor.style.outline = "none"
            
            # 입력 시 데이터 모델에 즉시 반영
            def make_input_handler(mid, el, parent):
                def on_input(e):
                    memo = vm.memos.find_by_id(mid)
                    memo.title = el.innerText
                    parent.style.background = "#fff9c4" if memo.title else "#fafafa"
                return on_input
            
            editor.oninput = create_proxy(make_input_handler(m.id, editor, container))
            container.appendChild(editor)
            grid.appendChild(container)

    async def on_card(e):
        document.querySelector("#log-bar").innerText = "> 카드 승인 중..."
        await asyncio.sleep(1.0)
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
        except: pass

    def render_out():
        lst = document.querySelector("#product-list")
        lst.innerHTML = ""
        for item in dispensed_items:
            img = document.createElement("img")
            img.src = item.image; img.style.margin = "5px"; lst.appendChild(img)

    # 초기 상품 그리드 생성 (중복 차단)
    grid = document.querySelector("#product-grid")
    grid.innerHTML = "" 
    for p in vm.products.get_all():
        div = document.createElement("div")
        div.id = f"item-{p.id}"; div.className = "grid-item"
        div.innerHTML = f"<img src='{p.image}' onerror='this.src=\"https://img.icons8.com/color/48/error.png\"'><br><b>{p.id}</b><br><small>{p.price}원</small>"
        div.onclick = create_proxy(lambda e, idx=p.id: setattr(document.querySelector("#code-input"), 'value', str(idx)))
        grid.appendChild(div)

    # 리스너 등록
    document.querySelector("#cash-btn").onclick = create_proxy(lambda e: (vm.insert_cash(1000), update_ui()))
    document.querySelector("#card-btn").onclick = create_proxy(on_card)
    document.querySelector("#confirm-btn").onclick = create_proxy(on_confirm)
    document.querySelector("#return-btn").onclick = create_proxy(lambda e: (vm.reset_system(), update_ui()))
    document.querySelector("#take-btn").onclick = create_proxy(lambda e: (
        vm.reset_system(), dispensed_items.clear(), render_out(), update_ui()
    ))

    refresh_memos()
    update_ui()

asyncio.ensure_future(init_system())