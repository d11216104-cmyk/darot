import random

# ----- Card / Deck -----
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def build_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]

def shuffle_deck(deck, seed=None):
    rng = random.Random(seed)
    rng.shuffle(deck)
    return rng

def card_value(rank):
    if rank == "A":
        return 1.0
    if rank in ["J", "Q", "K"]:
        return 0.5
    return float(rank)  # "2".."10"

def hand_value(hand):
    return sum(card_value(rank) for rank, _ in hand)

def format_hand(hand):
    return " ".join([f"{rank}{suit}" for rank, suit in hand])

# ----- Game Logic -----
LIMIT = 10.5

def draw(deck):
    return deck.pop()

def outcome(player, dealer):
    p = hand_value(player)
    d = hand_value(dealer)

    if p > LIMIT:
        return "玩家爆了(>10.5)，玩家輸"
    if d > LIMIT:
        return "莊家爆了(>10.5)，玩家贏"

    if p > d:
        return "玩家點數較大，玩家贏"
    if p < d:
        return "莊家點數較大，玩家輸"
    return "平手"

def main():
    print("=== 撲克牌 十點半(10.5) ===")
    seed_text = input("輸入洗牌種子(可空白，留空=隨機)：").strip()
    seed = int(seed_text) if seed_text else None

    deck = build_deck()
    rng = shuffle_deck(deck, seed=seed)

    player = [draw(deck)]
    dealer = [draw(deck)]

    print("\n--- 發牌 ---")
    print(f"玩家：{format_hand(player)}  | 點數：{hand_value(player)}")
    print(f"莊家：{format_hand([dealer[0]])}  | 點數：? (暗牌)")

    # Player turn
    while True:
        p_val = hand_value(player)
        if p_val > LIMIT:
            break

        cmd = input("\n玩家要牌嗎？(h=要牌 / s=停牌)：").strip().lower()
        if cmd == "h":
            player.append(draw(deck))
            print(f"玩家：{format_hand(player)}  | 點數：{hand_value(player)}")
        elif cmd == "s":
            break
        else:
            print("請輸入 h 或 s")

    # Dealer turn
    print("\n--- 莊家回合 ---")
    print(f"莊家亮牌：{format_hand(dealer)}  | 點數：{hand_value(dealer)}")

    # Simple dealer policy: hit if < 8, stand otherwise (adjust as you like)
    while hand_value(player) <= LIMIT and hand_value(dealer) < 8:
        dealer.append(draw(deck))
        print(f"莊家要牌：{format_hand(dealer)}  | 點數：{hand_value(dealer)}")

    print("\n--- 結算 ---")
    print(f"玩家：{format_hand(player)}  | 點數：{hand_value(player)}")
    print(f"莊家：{format_hand(dealer)}  | 點數：{hand_value(dealer)}")
    print(outcome(player, dealer))

if __name__ == "__main__":
    main()
