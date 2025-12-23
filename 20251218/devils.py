import tkinter as tk
import math
import random

GAME = {
    "width": 1200,
    "height": 800,
    "state": "BOOTING",
    "frame_count": 0,
    
    "player": {
        "x": 400, "y": 400,
        "hp": 100, "max_hp": 100,
        "mp": 100, "max_mp": 100,
        "loc": 0,
    },
    
    "monsters": [],
    "bullets": [],
    "keys_pressed": set(),
    
    "spells": {
        "CLEAN": ["root", "sudo", "rm", "rf", "delete", "force", "kill"],
        "RESTORE": ["git", "checkout", "undo", "revert", "reset", "head"],
        "SCAN": ["grep", "find", "search", "list", "ls", "dir"]
    },
    
    "current_spell_type": None
}

def init_game():
    global root, canvas, entry, log_text, heap_bar, stack_bar, status_text
    
    root = tk.Tk()
    root.title("SYSTEM_305_PROCEDURAL_EDITION (No Class)")
    
    canvas = tk.Canvas(root, width=GAME["width"], height=GAME["height"], bg="#0d1117", highlightthickness=0)
    canvas.pack()
    
    canvas.create_rectangle(820, 30, 1170, 770, fill="#161b22", outline="#30363d")
    docs = (
        "### PROCEDURAL_API (v1.0)\n"
        "---------------------------\n"
        "NO CLASS, JUST FUNCTION.\n\n"
        "[ MOVEMENT ]\n"
        " Arrow Keys (Up, Down..)\n\n"
        "[ BASIC ATTACK ]\n"
        " Space Bar\n\n"
        "[ MAGIC TERMINAL ]\n"
        " 1. Ctrl+Shift+P -> CLEAN\n"
        " 2. Ctrl+Z       -> RESTORE\n"
        " 3. Ctrl+F       -> SCAN\n\n"
        "[ HOW TO USE ]\n"
        " 터미널이 열리면 연상되는\n"
        " 단어를 콤마로 구분해 입력.\n"
        " 예: sudo, rm, force...\n"
        "---------------------------\n"
        "TARGET: GONG_WOOK_JAE\n"
        "STATUS: WAITING..."
    )
    canvas.create_text(840, 50, text=docs, fill="#7ee787", font=("Consolas", 10), anchor="nw")
    
    GAME["player"]["id"] = canvas.create_rectangle(0,0,20,20, fill="#58a6ff", outline="white")
    
    canvas.create_text(50, 730, text="HEAP (HP)", fill="#ff7b72", font=("Consolas", 10))
    heap_bar = canvas.create_rectangle(120, 725, 420, 740, fill="#ff7b72")
    
    canvas.create_text(50, 760, text="STACK (MP)", fill="#79c0ff", font=("Consolas", 10))
    stack_bar = canvas.create_rectangle(120, 755, 420, 770, fill="#79c0ff")
    
    log_text = canvas.create_text(400, 680, text="> SYSTEM READY...", fill="#7ee787", font=("Consolas", 11))
    status_text = canvas.create_text(30, 30, text="", fill="#8b949e", font=("Consolas", 12), anchor="nw")

    entry = tk.Entry(root, bg="#0d1117", fg="#7ee787", font=("Consolas", 14), insertbackground="white", borderwidth=0)
    GAME["entry_window"] = canvas.create_window(150, 600, window=entry, width=500, state="hidden")
    
    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)
    entry.bind("<Return>", execute_terminal)

    GAME["state"] = "PLAYING"
    game_loop()
    root.mainloop()

def on_key_press(e):
    if GAME["state"] == "TERMINAL_INPUT": return

    key = e.keysym
    GAME["keys_pressed"].add(key)
    
    keys = GAME["keys_pressed"]
    ctrl = "Control_L" in keys or "Control_R" in keys
    shift = "Shift_L" in keys or "Shift_R" in keys
    
    if key == "space":
        fire_bullet("BASIC", 1.0)
    
    elif ctrl and shift and key.upper() == "P": open_terminal("CLEAN")
    elif ctrl and key.upper() == "Z": open_terminal("RESTORE")
    elif ctrl and key.upper() == "F": open_terminal("SCAN")

def on_key_release(e):
    if e.keysym in GAME["keys_pressed"]:
        GAME["keys_pressed"].remove(e.keysym)

def open_terminal(spell_type):
    GAME["state"] = "TERMINAL_INPUT"
    GAME["current_spell_type"] = spell_type
    
    canvas.itemconfigure(GAME["entry_window"], state="normal")
    entry.delete(0, tk.END)
    entry.focus_set()
    
    write_log(f"INPUT MODE: {spell_type} 관련 명령어를 입력하세요...", "#d29922")

def execute_terminal(e):
    user_input = entry.get().lower()
    words = user_input.replace(" ", "").split(",")
    
    score = 0
    target_words = GAME["spells"][GAME["current_spell_type"]]
    
    for w in words:
        if w in target_words:
            score += 1
    
    power = 1.0 + (score * 0.5)
    cast_spell(GAME["current_spell_type"], power)
    
    entry.delete(0, tk.END)
    canvas.itemconfigure(GAME["entry_window"], state="hidden")
    canvas.focus_set()
    GAME["state"] = "PLAYING"

def cast_spell(spell_type, power):
    mp_cost = 30
    if GAME["player"]["mp"] < mp_cost:
        write_log("ERROR: 스택 메모리(MP)가 부족합니다!", "#ff7b72")
        return
        
    GAME["player"]["mp"] -= mp_cost
    write_log(f"EXECUTE: {spell_type} (Power x{power:.1f})", "#a5d6ff")
    
    px, py = GAME["player"]["x"], GAME["player"]["y"]
    
    if spell_type == "CLEAN":
        radius = 150 * power
        eff = canvas.create_oval(px-radius, py-radius, px+radius, py+radius, outline="#ff7b72", width=3)
        root.after(200, lambda: canvas.delete(eff))
        
        for m in GAME["monsters"][:]:
            dist = math.sqrt((px - m["x"])**2 + (py - m["y"])**2)
            if dist < radius:
                damage_monster(m, 100 * power)

    elif spell_type == "RESTORE":
        heal = 30 * power
        GAME["player"]["hp"] = min(GAME["player"]["max_hp"], GAME["player"]["hp"] + heal)
        write_log(f"SYSTEM: 힙 메모리 {heal:.0f} 복구 완료", "#7ee787")

    elif spell_type == "SCAN":
        if len(GAME["monsters"]) > 0:
            target = GAME["monsters"][0]
            fire_bullet("TRACKING", power, target)

def fire_bullet(b_type, power, target=None):
    px, py = GAME["player"]["x"], GAME["player"]["y"]
    
    vx, vy = 0, 0
    color = "#ffffff"
    
    if b_type == "BASIC":
        if "Left" in GAME["keys_pressed"]: vx = -15
        elif "Right" in GAME["keys_pressed"]: vx = 15
        elif "Up" in GAME["keys_pressed"]: vy = -15
        elif "Down" in GAME["keys_pressed"]: vy = 15
        else: vx = 15
        color = "#7ee787"
        
    elif b_type == "TRACKING" and target:
        angle = math.atan2(target["y"] - py, target["x"] - px)
        speed = 20
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        color = "#a5d6ff"

    bullet = {
        "id": canvas.create_oval(px-5, py-5, px+5, py+5, fill=color),
        "x": px, "y": py,
        "vx": vx, "vy": vy,
        "damage": 20 * power
    }
    GAME["bullets"].append(bullet)

def spawn_monster():
    if len(GAME["monsters"]) < 10:
        mx = random.randint(50, 750)
        my = random.randint(50, 750)
        
        is_boss = (GAME["player"]["loc"] > 500) and (not any(m.get("is_boss") for m in GAME["monsters"]))
        
        if is_boss:
            name = "DAEMON_GONG"
            color = "#ff0000"
            hp = 2000
            size = 40
            write_log("WARNING: 치명적 데몬 '공욱재' 감지!", "#ff0000")
        else:
            name = random.choice(["BUG", "ERROR", "LEAK"])
            color = "#d29922"
            hp = 50
            size = 15
            
        monster = {
            "id": canvas.create_rectangle(mx-size, my-size, mx+size, my+size, fill=color),
            "text_id": canvas.create_text(mx, my-20, text=name, fill="white", font=("Consolas", 8)),
            "x": mx, "y": my,
            "hp": hp,
            "is_boss": is_boss,
            "size": size
        }
        GAME["monsters"].append(monster)

def damage_monster(monster, dmg):
    monster["hp"] -= dmg
    if monster["hp"] <= 0:
        canvas.delete(monster["id"])
        canvas.delete(monster["text_id"])
        if monster in GAME["monsters"]:
            GAME["monsters"].remove(monster)
        
        GAME["player"]["loc"] += 50
        write_log(f"DEBUGGED: {dmg:.0f} Damage!", "#7ee787")

def write_log(msg, color):
    canvas.itemconfigure(log_text, text=f"> {msg}", fill=color)

def game_loop():
    if GAME["state"] == "PLAYING":
        
        speed = 5
        if "Up" in GAME["keys_pressed"] and GAME["player"]["y"] > 20: GAME["player"]["y"] -= speed
        if "Down" in GAME["keys_pressed"] and GAME["player"]["y"] < 780: GAME["player"]["y"] += speed
        if "Left" in GAME["keys_pressed"] and GAME["player"]["x"] > 20: GAME["player"]["x"] -= speed
        if "Right" in GAME["keys_pressed"] and GAME["player"]["x"] < 800: GAME["player"]["x"] += speed
        
        px, py = GAME["player"]["x"], GAME["player"]["y"]
        canvas.coords(GAME["player"]["id"], px-15, py-15, px+15, py+15)
        
        for b in GAME["bullets"][:]:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
            canvas.coords(b["id"], b["x"]-5, b["y"]-5, b["x"]+5, b["y"]+5)
            
            if not (0 < b["x"] < GAME["width"] and 0 < b["y"] < GAME["height"]):
                canvas.delete(b["id"])
                GAME["bullets"].remove(b)
                continue
                
            for m in GAME["monsters"]:
                dist = math.sqrt((b["x"] - m["x"])**2 + (b["y"] - m["y"])**2)
                if dist < m["size"] + 5:
                    damage_monster(m, b["damage"])
                    canvas.delete(b["id"])
                    if b in GAME["bullets"]: GAME["bullets"].remove(b)
                    break

        for m in GAME["monsters"]:
            dx = px - m["x"]
            dy = py - m["y"]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                m["x"] += (dx/dist) * 2
                m["y"] += (dy/dist) * 2
            
            canvas.coords(m["id"], m["x"]-m["size"], m["y"]-m["size"], m["x"]+m["size"], m["y"]+m["size"])
            canvas.coords(m["text_id"], m["x"], m["y"]-m["size"]-10)
            
            if dist < m["size"] + 15:
                GAME["player"]["hp"] -= 0.5

        GAME["frame_count"] += 1
        if GAME["frame_count"] % 100 == 0:
            spawn_monster()
        if GAME["player"]["mp"] < 100:
            GAME["player"]["mp"] += 0.1
            
        hp_ratio = GAME["player"]["hp"] / GAME["player"]["max_hp"]
        canvas.coords(heap_bar, 120, 725, 120 + (300 * max(0, hp_ratio)), 740)
        
        mp_ratio = GAME["player"]["mp"] / GAME["player"]["max_mp"]
        canvas.coords(stack_bar, 120, 755, 120 + (300 * max(0, mp_ratio)), 770)
        
        status_msg = f"LOC(EXP): {GAME['player']['loc']} | PROCESSES: {len(GAME['monsters'])}"
        canvas.itemconfigure(status_text, text=status_msg)

    root.after(16, game_loop)

if __name__ == "__main__":
    init_game()