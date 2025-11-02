# Treasure Duel 🏴‍☠️

A turn-based strategy game showcasing artificial intelligence algorithms including minimax, alpha-beta pruning, and fuzzy logic evaluation.

## 🎮 Game Description

Treasure Duel is played on a square grid where treasures are randomly placed. The human player starts at the top-left corner while the AI agent begins at the bottom-right corner. Players take turns moving one step at a time (up, down, left, or right) to collect treasures and increase their score. The game ends when all treasures are collected, and the player with the higher score wins.

### Key Features
- **Strategic Gameplay**: Plan your moves carefully to collect valuable treasures
- **Negative Treasures**: Some cells contain negative values - beware!
- **AI Opponent**: Advanced AI using minimax with alpha-beta pruning
- **Fuzzy Logic**: Sophisticated evaluation function considering multiple factors
- **Two Interfaces**: Console-based and graphical (pygame) interfaces

## 🎯 Game Rules

- Play on a configurable grid (default 4×4)
- Human starts at (0,0), AI starts at (n-1,n-1)
- Take turns moving one step (up, down, left, or right)
- Cannot move outside grid boundaries
- Cannot revisit cells
- Collect treasures to increase your score
- Some treasures have negative values!
- Game ends when all treasures are collected
- Winner is the player with the higher score

## 🧠 AI Algorithms

### Minimax Algorithm
The AI uses the minimax algorithm to simulate possible moves by both players, choosing the move that maximizes its advantage while assuming the human will play optimally.

### Alpha-Beta Pruning
Enhances minimax by pruning branches of the game tree that cannot affect the outcome, making AI decision-making more efficient.

### Fuzzy Logic Evaluation
The evaluation function considers multiple factors:
- **Distance to nearest treasure** (closer is better)
- **Current score difference** between AI and human
- **Mobility** (number of available moves)
- **Treasure values** within reach

## 🚀 Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Play

### Console Mode
```bash
python main.py --mode console
```

### GUI Mode (Default)
```bash
python main.py
```

### Command Line Options
```bash
python main.py --help
```

Available options:
- `--mode {console,gui}`: Choose interface (default: gui)
- `--grid-size N`: Size of the game grid (default: 4)
- `--treasures N`: Number of treasures to place (default: 5)
- `--depth N`: AI search depth (default: 4)
- `--treasure-range MIN MAX`: Treasure value range (default: -3 10)

### Examples
```bash
# Quick 3x3 game with GUI
python main.py --grid-size 3 --treasures 3

# Deep AI analysis in console
python main.py --mode console --depth 6 --grid-size 5

# High-stakes game with more treasures
python main.py --treasures 8 --treasure-range -5 15
```

## 🎨 Game Interface

### Console Interface
- Text-based grid display
- Numbered move selection
- Clear score tracking
- Turn indicators

### GUI Interface
- Visual grid with color coding
- Click to move
- Real-time score display
- Press 'R' to restart
- Green cells show legal moves
- Gold circles for positive treasures
- Red circles for negative treasures

## 🏗️ Project Structure

```
treasure_duel/
├── game/                    # Core game logic
│   ├── state.py            # Game state management
│   ├── rules.py            # Move generation and validation
│   ├── engine.py           # AI algorithms (minimax, alpha-beta)
│   ├── heuristic.py        # Evaluation functions with fuzzy logic
│   └── main.py             # Console game interface
├── ui/                     # User interfaces
│   └── game_ui.py          # Pygame graphical interface
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Technical Details

### Game State
The `GameState` class manages:
- Player positions and scores
- Treasure locations and values
- Visited cells tracking
- Turn management

### AI Engine
- **Transposition Table**: Caches evaluated positions for efficiency
- **Move Ordering**: Prioritizes promising moves for better pruning
- **Iterative Deepening**: Can be extended for time-limited searches

### Evaluation Function
Combines multiple heuristics using fuzzy logic:
- Score difference (weight: 0.5)
- Distance to nearest treasure (weight: 0.25)
- Opponent's distance to treasure (weight: -0.15)
- Mobility advantage (weight: 0.1)

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Test core game logic
python test_game.py

# Test GUI components
python test_gui.py
```

## 🎯 Strategy Tips

1. **Plan Ahead**: Consider the AI's possible responses
2. **Value Assessment**: Weigh treasure values against distance
3. **Mobility**: Maintain multiple move options
4. **Blocking**: Sometimes it's better to deny the AI access to treasures
5. **Risk Management**: Be cautious around negative treasures

## 🔮 Future Enhancements

- **Iterative Deepening**: Time-limited AI searches
- **Opening Book**: Precomputed opening strategies
- **Difficulty Levels**: Adjustable AI strength
- **Tournament Mode**: Multiple games with statistics
- **Network Play**: Online multiplayer support

## 📚 Educational Value

This project demonstrates:
- **Search Algorithms**: Minimax and alpha-beta pruning
- **Heuristic Design**: Multi-factor evaluation functions
- **Fuzzy Logic**: Soft decision boundaries
- **Game Theory**: Adversarial search strategies
- **Software Architecture**: Modular design patterns

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest new features
- Improve the AI algorithms
- Add new game modes
- Enhance the user interface

## 📄 License

This project is open source and available under the MIT License.

---

**Enjoy your treasure hunting adventure! 🏴‍☠️✨**
