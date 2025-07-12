from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import uuid
import time
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# Data storage files
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
MATCHES_FILE = os.path.join(DATA_DIR, 'matches.json')
WAITING_FILE = os.path.join(DATA_DIR, 'waiting.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize data files if they don't exist
def init_data_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(MATCHES_FILE):
        with open(MATCHES_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(WAITING_FILE):
        with open(WAITING_FILE, 'w') as f:
            json.dump([], f)

# Load data from JSON files
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return []

# Save data to JSON files
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Game logic
def get_initial_game_state():
    return {
        "player1": {
            "hand": ["Emperor", "Citizen", "Citizen", "Citizen", "Slave"],
            "played": [],
            "score": 0
        },
        "player2": {
            "hand": ["Emperor", "Citizen", "Citizen", "Citizen", "Slave"],
            "played": [],
            "score": 0
        },
        "current_turn": 1,
        "max_turns": 5,
        "history": []
    }

def get_card_winner(card1, card2):
    if card1 == card2:
        return "tie"
    
    rules = {
        "Emperor": ["Citizen"],
        "Citizen": ["Slave"],
        "Slave": ["Emperor"]
    }
    
    if card2 in rules.get(card1, []):
        return "player1"
    else:
        return "player2"

# API Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/join-match', methods=['POST'])
def join_match():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    
    if not user_id or not username:
        return jsonify({"error": "Missing user_id or username"}), 400
    
    # Load waiting players
    waiting_players = load_data(WAITING_FILE)
    
    # Remove expired waiting players (older than 5 minutes)
    current_time = time.time()
    waiting_players = [p for p in waiting_players if current_time - p.get('timestamp', 0) < 300]
    
    if waiting_players:
        # Join existing match
        waiting_player = waiting_players[0]
        
        # Create match
        match_id = str(uuid.uuid4())
        match = {
            "id": match_id,
            "player1_id": waiting_player['user_id'],
            "player2_id": user_id,
            "player1_username": waiting_player['username'],
            "player2_username": username,
            "status": "playing",
            "game_state": get_initial_game_state(),
            "created_at": datetime.now().isoformat()
        }
        
        # Save match
        matches = load_data(MATCHES_FILE)
        matches.append(match)
        save_data(MATCHES_FILE, matches)
        
        # Remove from waiting
        waiting_players.pop(0)
        save_data(WAITING_FILE, waiting_players)
        
        return jsonify({
            "match_id": match_id,
            "status": "joined",
            "player1": waiting_player['username'],
            "player2": username
        })
    
    else:
        # Join waiting list
        waiting_player = {
            "user_id": user_id,
            "username": username,
            "timestamp": current_time
        }
        
        waiting_players.append(waiting_player)
        save_data(WAITING_FILE, waiting_players)
        
        return jsonify({
            "status": "waiting",
            "message": "Waiting for opponent..."
        })

@app.route('/api/check-match/<user_id>')
def check_match(user_id):
    # Check if user is in a match
    matches = load_data(MATCHES_FILE)
    
    for match in matches:
        if match['player1_id'] == user_id or match['player2_id'] == user_id:
            if match['status'] == 'playing':
                return jsonify({
                    "found": True,
                    "match": match
                })
    
    return jsonify({"found": False})

@app.route('/api/play-card', methods=['POST'])
def play_card():
    data = request.json
    match_id = data.get('match_id')
    user_id = data.get('user_id')
    card = data.get('card')
    
    if not all([match_id, user_id, card]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Load matches
    matches = load_data(MATCHES_FILE)
    
    # Find match
    match = None
    for m in matches:
        if m['id'] == match_id:
            match = m
            break
    
    if not match:
        return jsonify({"error": "Match not found"}), 404
    
    # Determine player
    is_player1 = match['player1_id'] == user_id
    player_key = "player1" if is_player1 else "player2"
    
    # Check if card is available
    game_state = match['game_state']
    player_hand = game_state[player_key]['hand']
    
    if card not in player_hand:
        return jsonify({"error": "Card not in hand"}), 400
    
    # Play card
    player_hand.remove(card)
    game_state[player_key]['played'].append(card)
    
    # Check if both players have played
    if len(game_state['player1']['played']) > 0 and len(game_state['player2']['played']) > 0:
        # Both have played - resolve round
        card1 = game_state['player1']['played'][-1]
        card2 = game_state['player2']['played'][-1]
        winner = get_card_winner(card1, card2)
        
        # Update scores
        if winner == "player1":
            game_state['player1']['score'] += 1
        elif winner == "player2":
            game_state['player2']['score'] += 1
        
        # Add to history
        game_state['history'].append({
            "turn": game_state['current_turn'],
            "player1_card": card1,
            "player2_card": card2,
            "winner": winner
        })
        
        # Advance turn
        game_state['current_turn'] += 1
        
        # Check if game is over
        if game_state['current_turn'] > game_state['max_turns']:
            match['status'] = 'finished'
    
    # Save updated match
    for i, m in enumerate(matches):
        if m['id'] == match_id:
            matches[i] = match
            break
    
    save_data(MATCHES_FILE, matches)
    
    return jsonify({
        "success": True,
        "game_state": game_state,
        "match_status": match['status']
    })

@app.route('/api/game-state/<match_id>')
def get_game_state(match_id):
    matches = load_data(MATCHES_FILE)
    
    for match in matches:
        if match['id'] == match_id:
            return jsonify(match)
    
    return jsonify({"error": "Match not found"}), 404

@app.route('/api/leave-match', methods=['POST'])
def leave_match():
    data = request.json
    match_id = data.get('match_id')
    user_id = data.get('user_id')
    
    if not match_id or not user_id:
        return jsonify({"error": "Missing match_id or user_id"}), 400
    
    # Remove from matches
    matches = load_data(MATCHES_FILE)
    matches = [m for m in matches if m['id'] != match_id]
    save_data(MATCHES_FILE, matches)
    
    # Remove from waiting
    waiting_players = load_data(WAITING_FILE)
    waiting_players = [w for w in waiting_players if w['user_id'] != user_id]
    save_data(WAITING_FILE, waiting_players)
    
    return jsonify({"success": True})

@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """Clean up expired waiting players"""
    waiting_players = load_data(WAITING_FILE)
    current_time = time.time()
    
    # Remove players waiting more than 5 minutes
    waiting_players = [p for p in waiting_players if current_time - p.get('timestamp', 0) < 300]
    save_data(WAITING_FILE, waiting_players)
    
    return jsonify({"cleaned": len(waiting_players)})

# Initialize data files on startup
init_data_files()

# Initialize data files
init_data_files()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
