#!/usr/bin/env python3
"""
Treasure Duel - Main Entry Point

A turn-based strategy game showcasing AI algorithms including minimax,
alpha-beta pruning, and fuzzy logic evaluation.

Usage:
    python main.py [--mode console|gui] [--grid-size N] [--treasures N] [--depth N]

Examples:
    python main.py                    # GUI mode with default settings
    python main.py --mode console     # Console mode
    python main.py --mode gui --grid-size 5 --treasures 8 --depth 6
"""

import argparse
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Treasure Duel - AI Strategy Game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Game Modes:
  console    Text-based interface in terminal
  gui        Graphical interface using pygame (default)

Game Rules:
  - Play on a grid where treasures are randomly placed
  - Human starts at top-left, AI starts at bottom-right
  - Take turns moving one step (up/down/left/right)
  - Collect treasures to increase your score
  - Some treasures have negative values!
  - Game ends when all treasures are collected
  - Player with highest score wins

AI Features:
  - Minimax algorithm with alpha-beta pruning
  - Fuzzy logic evaluation function
  - Transposition table for efficiency
  - Move ordering for better pruning
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['console', 'gui'], 
        default='gui',
        help='Game interface mode (default: gui)'
    )
    
    parser.add_argument(
        '--grid-size', 
        type=int, 
        default=4,
        help='Size of the game grid (default: 4)'
    )
    
    parser.add_argument(
        '--treasures', 
        type=int, 
        default=5,
        help='Number of treasures to place (default: 5)'
    )
    
    parser.add_argument(
        '--depth', 
        type=int, 
        default=4,
        help='AI search depth (default: 4)'
    )
    
    parser.add_argument(
        '--treasure-range',
        nargs=2,
        type=int,
        default=[-3, 10],
        help='Treasure value range (default: -3 10)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.grid_size < 3:
        print("Error: Grid size must be at least 3")
        sys.exit(1)
    
    if args.treasures < 1:
        print("Error: Must have at least 1 treasure")
        sys.exit(1)
    
    if args.depth < 1:
        print("Error: AI depth must be at least 1")
        sys.exit(1)
    
    max_treasures = args.grid_size * args.grid_size - 2  # Exclude starting positions
    if args.treasures > max_treasures:
        print(f"Error: Too many treasures. Maximum for {args.grid_size}x{args.grid_size} grid is {max_treasures}")
        sys.exit(1)
    
    try:
        if args.mode == 'console':
            from game.main import play_game
            print("Starting Treasure Duel in console mode...")
            play_game(
                grid_size=args.grid_size,
                num_treasures=args.treasures,
                ai_depth=args.depth,
                mode='human_vs_ai'
            )
        else:  # gui mode
            from ui.game_ui import PygameUI
            print("Starting Treasure Duel in GUI mode...")
            ui = PygameUI(
                grid_size=args.grid_size,
                num_treasures=args.treasures,
                ai_depth=args.depth
            )
            ui.run()
            
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please install required packages: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
