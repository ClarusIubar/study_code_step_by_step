import os
from collections import namedtuple

# 1. 카드 데이터 구조 정의
Card = namedtuple('Card', ['suit', 'rank'])

SUITS = ['Spade', 'Heart', 'Diamond', 'Club']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def get_card_from_filename(filename):
    """파일명(Heart_A.txt)을 Card 객체로 변환 (Read)"""
    name = filename.replace('.txt', '')
    try:
        suit, rank = name.split('_')
        return Card(suit, rank)
    except ValueError:
        return None

def get_filename_from_card(card):
    """Card 객체를 파일명으로 변환"""
    return f"{card.suit}_{card.rank}.txt"

def is_playable(card, top_card):
    """원카드 매칭 룰: 문양이나 숫자가 같으면 제출 가능"""
    if not top_card: return True  # 시작 시 예외 처리
    return card.suit == top_card.suit or card.rank == top_card.rank

def get_hand_details(player_path):
    """플레이어 폴더 내의 파일들을 Card 객체 리스트로 반환 (Read)"""
    files = [f for f in os.listdir(player_path) if f.endswith('.txt')]
    hand = []
    for f in files:
        card = get_card_from_filename(f)
        if card:
            hand.append((f, card)) # (파일명, 카드객체) 튜플 반환
    return hand