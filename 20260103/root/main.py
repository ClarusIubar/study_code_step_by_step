import tkinter as tk
import sys
import os
import argparse
from lotto.app import LottoApp
from acidrain.app import AcidRainApp

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="nothing")
    parser.add_argument(
        '--game', 
        type=str, 
        default='lotto', 
        choices=['lotto', 'acidrain'],
        help="실행할 게임을 선택하세요: lotto 또는 acidrain (기본값: lotto)"
    )
    
    args = parser.parse_args()

    # 2. Tkinter 루트 생성
    root = tk.Tk() # 루트 윈도우 생성

    # 3. 인자에 따른 앱 주입 (Dependency Injection)
    if args.game == 'lotto':
        print("[System] 로또 번호 생성기를 실행합니다.")
        LottoApp(root) # 앱 인스턴스 생성
    elif args.game == 'acidrain':
        print("[System] 산성비 게임을 실행합니다.")
        AcidRainApp(root) # 앱 인스턴스 생성
    else:
        # choices 제한으로 인해 실제로 도달할 가능성은 낮지만 안전장치로 둠
        print(f"[Error] 알 수 없는 게임입니다: {args.game}")
        sys.exit(1)

    root.mainloop() # 루트 동작

if __name__ == "__main__": 
    main()