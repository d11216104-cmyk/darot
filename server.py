from flask import Flask, render_template, request, session, redirect, url_for
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ----- Card / Deck -----
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def build_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]

def shuffle_deck(deck, seed=None):
    rng = random.Random(seed)
    rng.shuffle(deck)

def card_value(rank):
    if rank == "A":
        return 1.0
    if rank in ["J", "Q", "K"]:
        return 0.5
    return float(rank)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    seed_text = request.form.get('seed', '').strip()
    seed = None
    if seed_text:
        try:
            seed = int(seed_text)
        except ValueError:
            pass
    
    # Initialize game state
    deck = build_deck()
    shuffle_deck(deck, seed=seed)
    
    player = [draw(deck)]
    dealer = [draw(deck)]
    
    session['deck'] = deck
    session['player'] = player
    session['dealer'] = dealer
    session['game_over'] = False
    session['dealer_turn'] = False
    
    return redirect(url_for('game'))

@app.route('/game')
def game():
    if 'player' not in session:
        return redirect(url_for('index'))
    
    player = session['player']
    dealer = session['dealer']
    game_over = session.get('game_over', False)
    dealer_turn = session.get('dealer_turn', False)
    
    player_value = hand_value(player)
    dealer_value = hand_value(dealer) if dealer_turn or game_over else None
    
    result = None
    if game_over:
        result = outcome(player, dealer)
    
    return render_template('game.html', 
                         player=player,
                         dealer=dealer,
                         player_value=player_value,
                         dealer_value=dealer_value,
                         game_over=game_over,
                         dealer_turn=dealer_turn,
                         result=result,
                         LIMIT=LIMIT)

@app.route('/hit', methods=['POST'])
def hit():
    if 'player' not in session or session.get('game_over'):
        return redirect(url_for('index'))
    
    deck = session['deck']
    player = session['player']
    
    player.append(draw(deck))
    session['deck'] = deck
    session['player'] = player
    
    # Check if player busted
    if hand_value(player) > LIMIT:
        session['dealer_turn'] = True
        session['game_over'] = True
    
    return redirect(url_for('game'))

@app.route('/stand', methods=['POST'])
def stand():
    if 'player' not in session or session.get('game_over'):
        return redirect(url_for('index'))
    
    session['dealer_turn'] = True
    
    deck = session['deck']
    player = session['player']
    dealer = session['dealer']
    
    # Dealer's turn: hit if < 8
    while hand_value(player) <= LIMIT and hand_value(dealer) < 8:
        dealer.append(draw(deck))
    
    session['deck'] = deck
    session['dealer'] = dealer
    session['game_over'] = True
    
    return redirect(url_for('game'))

@app.route('/new_game')
def new_game():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # WARNING: Debug mode is enabled for development only
    # In production, set debug=False and use a production WSGI server
    app.run(debug=True, host='0.0.0.0', port=5000)
