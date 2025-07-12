# E-Card Game

A custom online 1v1 card game inspired by Kaiji, featuring three card types: Emperor, Citizen, and Slave.

## Features

- **Simple Authentication**: Local storage-based user system
- **Real-time Matchmaking**: Find opponents instantly
- **Card Game**: Emperor > Citizen > Slave > Emperor
- **Elo System**: Track your ranking
- **Leaderboard**: See top players

## Quick Start

### 🚀 Deploy Online (Recommended)
For online multiplayer like chess.com:

1. **Deploy to Render** (Free & Easy):
   - Go to [render.com](https://render.com)
   - Connect your GitHub repo
   - Deploy automatically
   - Get your URL like: `https://e-card-game.onrender.com`

2. **Or use other services**:
   - Railway: [railway.app](https://railway.app)
   - Heroku: [heroku.com](https://heroku.com)
   - Vercel: [vercel.com](https://vercel.com)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions!

### 🖥️ Local Development
For testing on your computer:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py

# Open browser to http://localhost:5000
```

### Play the Game
1. Open your browser to your deployed URL (or localhost for testing)
2. Sign up or sign in
3. Click "START GAME" to find an opponent
4. Play your cards and compete!

## Game Rules

- **Emperor** beats **Citizen**
- **Citizen** beats **Slave**  
- **Slave** beats **Emperor**
- Each player has 5 cards: 1 Emperor, 3 Citizens, 1 Slave
- Play 5 rounds, highest score wins!

## File Structure

```
E-Card/
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── setup.py           # Setup script
├── templates/
│   └── index.html     # Game frontend
└── data/              # Game data storage (auto-created)
    ├── users.json     # User accounts
    ├── matches.json   # Active matches
    └── waiting.json   # Players waiting for matches
```

## API Endpoints

- `GET /` - Game homepage
- `POST /api/join-match` - Join or create a match
- `GET /api/check-match/<user_id>` - Check for active match
- `POST /api/play-card` - Play a card
- `GET /api/game-state/<match_id>` - Get current game state
- `POST /api/leave-match` - Leave current match
- `POST /api/cleanup` - Clean up expired data

## Troubleshooting

- **Connection failed**: Make sure the Flask server is running on port 5000
- **No opponents found**: Try refreshing or wait for another player
- **Game not updating**: Check browser console for errors

## Development

The game uses:
- **Backend**: Flask with JSON file storage
- **Frontend**: HTML/CSS/JavaScript
- **Authentication**: LocalStorage-based
- **Real-time**: Polling-based updates

Enjoy playing E-Card! 🎮 