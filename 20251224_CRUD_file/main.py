import os
import shutil
import random
import time
import sys
from engine import Card, SUITS, RANKS, is_playable, get_hand_details, get_filename_from_card, get_card_from_filename

class FileOneCardGame:
    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), "game_data")
        self.paths = {
            'deck': os.path.join(self.base_dir, "deck"),
            'table': os.path.join(self.base_dir, "table"),
            'human': os.path.join(self.base_dir, "players", "human"),
            'computer': os.path.join(self.base_dir, "players", "computer")
        }
        self.table_counter = 0
        self.game_running = True
        self.setup_environment()

    def setup_environment(self):
        """초기 폴더 트리 생성 및 덱 초기화 (Reset 시에도 호출됨)"""
        print("시스템 초기화 중...")
        self.table_counter = 0
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)
        
        for path in self.paths.values():
            os.makedirs(path, exist_ok=True)

        deck = [Card(s, r) for s in SUITS for r in RANKS]
        random.shuffle(deck)

        for card in deck:
            filename = get_filename_from_card(card)
            filepath = os.path.join(self.paths['deck'], filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"[{card.suit} {card.rank}]")

        # 윈도우 보안: 덱 폴더 숨김 처리
        os.system(f'attrib +h "{self.paths["deck"]}"')

    def move_to_table(self, src_path, filename):
        """순번을 붙여 테이블로 이동 (물리적 순서 보장)"""
        self.table_counter += 1
        new_filename = f"{self.table_counter:04d}_{filename}"
        shutil.move(
            os.path.join(src_path, filename),
            os.path.join(self.paths['table'], new_filename)
        )

    def draw_card(self, player_key, count=1):
        for _ in range(count):
            try:
                deck_files = os.listdir(self.paths['deck'])
                if not deck_files:
                    self.recycle_discard_pile()
                    deck_files = os.listdir(self.paths['deck'])
                    if not deck_files: return

                target = random.choice(deck_files)
                if player_key == 'table':
                    self.move_to_table(self.paths['deck'], target)
                else:
                    shutil.move(
                        os.path.join(self.paths['deck'], target),
                        os.path.join(self.paths[player_key], target)
                    )
            except Exception:
                break

    def recycle_discard_pile(self):
        table_files = sorted(os.listdir(self.paths['table']))
        if len(table_files) <= 1: return
        
        for f in table_files[:-1]:
            original_name = "_".join(f.split("_")[1:])
            shutil.move(
                os.path.join(self.paths['table'], f),
                os.path.join(self.paths['deck'], original_name)
            )

    def get_top_card(self):
        table_files = sorted(os.listdir(self.paths['table']))
        if not table_files: return None
        top_filename = table_files[-1]
        actual_card_name = "_".join(top_filename.split("_")[1:])
        return get_card_from_filename(actual_card_name)

    def clear_screen(self):
        os.system('cls')

    def check_winner(self):
        if not os.listdir(self.paths['human']): return "사용자"
        if not os.listdir(self.paths['computer']): return "컴퓨터"
        return None

    def start(self):
        """메인 게임 루프"""
        while self.game_running:
            # 게임 시작 전 초기 배분
            self.draw_card('human', 7)
            self.draw_card('computer', 7)
            self.draw_card('table', 1)

            while True:
                winner = self.check_winner()
                if winner:
                    self.clear_screen()
                    print(f"\n🏆 축하합니다! {winner}가 승리했습니다!")
                    input("\n엔터를 누르면 메인 메뉴로 돌아갑니다...")
                    break
                
                # 사용자 턴에서 exit/reset 신호를 받음
                signal = self.human_turn()
                
                if signal == "RESET":
                    self.setup_environment()
                    break # 내부 루프 탈출 후 초기 배분부터 다시 시작
                elif signal == "EXIT":
                    self.game_running = False
                    break
                
                if self.check_winner(): continue
                self.computer_turn()
            
            if not self.game_running:
                self.clear_screen()
                print("\n게임을 종료합니다. 이용해 주셔서 감사합니다!")
                sys.exit()

    def human_turn(self):
        while True:
            self.clear_screen()
            top_card = self.get_top_card()
            hand = get_hand_details(self.paths['human'])
            
            print(f"================ ONE CARD (FILE CRUD) ================")
            print(f" 현재 바닥 카드:  >> [ {top_card.suit} {top_card.rank} ] <<")
            print(f"======================================================")
            print(f"당신의 패 (남은 장수: {len(hand)}):")
            
            for i, (fname, card) in enumerate(hand, 1):
                can_play = is_playable(card, top_card)
                status = "★" if can_play else " "
                print(f"  {i}. {status} {card.suit}_{card.rank}")
            
            print(f"------------------------------------------------------")
            print(f"  0. 덱에서 뽑기  |  reset. 게임 재시작  |  exit. 종료")
            print(f"------------------------------------------------------")
            
            user_input = input("\n명령어 또는 카드 번호를 입력하세요: ").strip().lower()
            
            if user_input == 'exit':
                return "EXIT"
            if user_input == 'reset':
                return "RESET"
            if not user_input:
                continue
            
            try:
                choices = list(map(int, user_input.split()))
                if 0 in choices:
                    self.draw_card('human')
                    return "CONTINUE"
                
                selected_cards = [hand[idx-1] for idx in choices if 1 <= idx <= len(hand)]
                if not selected_cards or len(selected_cards) != len(choices):
                    print("잘못된 번호입니다."); time.sleep(0.8); continue

                first_card = selected_cards[0][1]
                all_same_rank = all(c[1].rank == first_card.rank for c in selected_cards)
                
                if is_playable(first_card, top_card) and all_same_rank:
                    for fname, card in selected_cards:
                        self.move_to_table(self.paths['human'], fname)
                    return "CONTINUE"
                else:
                    print("규칙 오류! (첫 카드 매칭 & 동일 숫자 필수)"); time.sleep(1.2)
            except ValueError:
                print("숫자나 지정된 명령어만 입력 가능합니다."); time.sleep(0.8)

    def computer_turn(self):
        self.clear_screen()
        print("컴퓨터가 생각 중입니다...")
        time.sleep(0.8)
        
        top_card = self.get_top_card()
        hand = get_hand_details(self.paths['computer'])
        
        playable_groups = {}
        for fname, card in hand:
            if is_playable(card, top_card):
                rank = card.rank
                if rank not in playable_groups:
                    playable_groups[rank] = [h for h in hand if h[1].rank == rank]
        
        if playable_groups:
            best_rank = max(playable_groups, key=lambda r: len(playable_groups[r]))
            for fname, card in playable_groups[best_rank]:
                self.move_to_table(self.paths['computer'], fname)
        else:
            self.draw_card('computer')
        time.sleep(0.8)

if __name__ == "__main__":
    game = FileOneCardGame()
    game.start()