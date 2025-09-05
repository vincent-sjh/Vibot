import sys
import time
import random
import os

class SnakeGame:
    def __init__(self, size=10):
        self.size = size
        self.reset()

    def reset(self):
        self.snake = [(self.size // 2, self.size // 2)]
        self.direction = 'd'  # Start moving right
        self.food = self.spawn_food()
        self.alive = True
        self.score = 0
        self.pending_direction = None
        self.pending_direction = None

    def spawn_food(self):
        attempts = 0
        while attempts < 100:  # Prevent infinite loop
            pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if pos not in self.snake:
                return pos
            attempts += 1
        # If can't find empty spot, return a random position (shouldn't happen in normal game)
        return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

    def change_direction(self, d):
        if d in 'wasd':
            # Prevent reverse direction
            if (d == 'w' and self.direction != 's') or \
               (d == 's' and self.direction != 'w') or \
               (d == 'a' and self.direction != 'd') or \
               (d == 'd' and self.direction != 'a'):
                self.pending_direction = d

    def move(self):
        # Apply pending direction change
        if self.pending_direction:
            self.direction = self.pending_direction
            self.pending_direction = None
            
        head = self.snake[0]
        if self.direction == 'w':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 's':
            new_head = (head[0] + 1, head[1])
        elif self.direction == 'a':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'd':
            new_head = (head[0], head[1] + 1)
        else:
            new_head = head

        # Check collision
        if (new_head[0] < 0 or new_head[0] >= self.size or
            new_head[1] < 0 or new_head[1] >= self.size or
            new_head in self.snake):
            self.alive = False
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        # Simple clear screen using os.system
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Game title with ASCII art
        print("🐍 " + "=" * (self.size + 10) + " 🐍")
        print("   🎮 VIBOT GLUTTONOUS SNAKE GAME 🎮")
        print("🐍 " + "=" * (self.size + 10) + " 🐍")
        print()
        
        # Score and status
        print(f"📊 Score: {self.score}   🍎 Food eaten: {self.score}   🐍 Length: {len(self.snake)}")
        print(f" Legend: ^ v < > = Snake Head   ● = Snake Body   @ = Food")
        print()
        
        board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        
        # Place snake body and head
        for i, (y, x) in enumerate(self.snake):
            if 0 <= y < self.size and 0 <= x < self.size:
                if i == 0:  # Head
                    # Direction-based head symbols using consistent characters
                    if self.direction == 'w':
                        board[y][x] = '^'
                    elif self.direction == 's':
                        board[y][x] = 'v'
                    elif self.direction == 'a':
                        board[y][x] = '<'
                    elif self.direction == 'd':
                        board[y][x] = '>'
                else:  # Body
                    board[y][x] = '●'
        
        # Place food
        fy, fx = self.food
        if 0 <= fy < self.size and 0 <= fx < self.size:
            board[fy][fx] = '@'
        
        # Draw border with proper alignment
        print('    ╔' + '═' * (self.size * 2) + '╗')
        for i, row in enumerate(board):
            row_str = '    ║'
            for cell in row:
                if cell == ' ':
                    row_str += '  '
                elif cell in ['^', 'v', '<', '>']:
                    row_str += cell + ' '
                elif cell == '●':
                    row_str += '●' + ' '
                elif cell == '@':  # Food
                    row_str += '@' + ' '
                else:
                    row_str += cell + ' '
            row_str += '║'
            print(row_str)
        print('    ╚' + '═' * (self.size * 2) + '╝')
        
        print()
        # Game tips
        if self.score == 0:
            print("💡 Tip: Eat the apple 🍎 to grow and increase your score!")
        elif self.score < 5:
            print("🌟 Great start! Keep eating to grow longer!")
        elif self.score < 10:
            print("🔥 You're on fire! Watch out for walls and your tail!")
        else:
            print("🏆 Snake Master! You're doing amazing!")
        
        print()

    def run(self):
        import threading
        import queue
        import time
        
        while True:  # 外层循环支持重开游戏
            # Reset game state
            self.reset()
            
            # Show welcome screen (不清屏)
            self.welcome_screen()
            
            # 游戏开始前先清屏一次，然后开始游戏循环
            print("\n🎮 Game starting...")
            time.sleep(0.2)  # 给用户0.2秒时间看到开始信息

            # Input queue for handling user input
            input_queue = queue.Queue()
            
            # 使用更简单的方法：只在游戏进行时处理输入
            # Initial draw
            self.draw()
            
            game_ended = False
            try:
                while self.alive:
                    # 使用非阻塞输入检查
                    import select
                    import sys
                    
                    # 检查是否有输入可用（非阻塞）
                    if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                        try:
                            char = sys.stdin.readline().strip().lower()
                            #print(f"DEBUG: Main loop received input: '{char}'")
                            if char == 'q':
                                #print("DEBUG: Quitting game from main loop")
                                game_ended = True
                                break
                            elif char in 'wasd':
                                #print(f"DEBUG: Changing direction to: {char}")
                                self.change_direction(char)
                        except:
                            pass
                    
                    # Move snake automatically
                    self.move()
                    
                    if self.alive:
                        self.draw()  # 只在游戏进行时清屏重绘
                    else:
                        #print("DEBUG: Game over detected, showing game over screen")
                        # 游戏结束时直接显示结束界面
                        time.sleep(0.2)
                        self.game_over_screen()
                        
                        # 重开选择 - 现在没有输入线程冲突
                        #print("DEBUG: Calling get_restart_choice...")
                        restart_choice = self.get_restart_choice()
                        #print(f"DEBUG: get_restart_choice returned: {restart_choice}")
                        if restart_choice == 'restart':
                            print("🎮 Restarting game...\n")
                            time.sleep(0.2)
                            break  # 跳出内层循环，重开游戏
                        else:
                            game_ended = True
                            break

                    time.sleep(0.25)  # 自动移动间隔

            except KeyboardInterrupt:
                # Ctrl+C 退出
                #print("DEBUG: KeyboardInterrupt caught")
                self.game_over_screen()
                game_ended = True
            
            if game_ended:
                #print("DEBUG: Exiting game completely")
                break  # 退出外层循环，结束程序
    
    def get_restart_choice(self):
        """独立的重开选择函数，避免输入冲突"""
        #print("DEBUG: Entering get_restart_choice function")
        while True:
            print("🔄 Press C + ENTER to restart, or Q + ENTER to quit:")
            try:
                #print("DEBUG: Waiting for restart choice input...")
                choice = input().lower().strip()
                #print(f"DEBUG: Received restart choice: '{choice}'")
                if choice == 'c':
                    #print("DEBUG: Returning 'restart'")
                    return 'restart'
                elif choice == 'q':
                    #print("DEBUG: Returning 'quit'")
                    return 'quit'
                else:
                    #print(f"DEBUG: Invalid choice '{choice}', asking again")
                    print("Invalid input! Press C to restart or Q to quit.")
            except Exception as e:
                #print(f"DEBUG: Exception in get_restart_choice: {e}")
                return 'quit'
            except:
                return 'quit'
        
    def game_over_screen(self):
        # 游戏结束时清屏
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print()
        print("💀 " + "=" * 50 + " 💀")
        print("                    🎮 GAME OVER 🎮")
        print("💀 " + "=" * 50 + " 💀")
        print()
        
        # Score evaluation
        if self.score == 0:
            print("😅 Better luck next time! Every master was once a beginner.")
            rank = "Beginner Snake"
            emoji = "🐣"
        elif self.score < 5:
            print("👍 Not bad for a start! Practice makes perfect!")
            rank = "Amateur Snake"
            emoji = "🐍"
        elif self.score < 10:
            print("🌟 Good job! You're getting the hang of it!")
            rank = "Skilled Snake"
            emoji = "⭐"
        elif self.score < 20:
            print("🔥 Excellent! You're a natural at this!")
            rank = "Expert Snake"
            emoji = "🔥"
        else:
            print("🏆 AMAZING! You're a true Snake Master!")
            rank = "Snake Legend"
            emoji = "👑"
        
        print()
        print(f"    {emoji} Final Score: {self.score}")
        print(f"    🏅 Rank: {rank}")
        print(f"    🐍 Snake Length: {len(self.snake)}")
        print(f"    🍎 Apples Eaten: {self.score}")
        print()
        
        # ASCII snake art with proper alignment
        print("    ╔═══════════════════════════════════╗")
        print("    ║                                   ║")
        print("    ║        Thanks for playing!        ║")
        print("    ║                                   ║")
        print("    ║    🐍 VIBOT Snake Game v1.0 🐍    ║")
        print("    ║                                   ║")
        print("    ╚═══════════════════════════════════╝")
        print()
        
        
        print("🚀 Want to play again? Press C + ENTER")
        print("❌ Want to quit?       Press Q + ENTER")
        print("🎮 Try a bigger map with: vibot -g --map-size 15")
        print()

    def welcome_screen(self):
        # 不清屏，保留之前的命令行结果
        
        print()
        print("🐍 " + "=" * 60 + " 🐍")
        print("                🎮 WELCOME TO VIBOT SNAKE GAME! 🎮")
        print("🐍 " + "=" * 60 + " 🐍")
        print()
        
        print("🎯 OBJECTIVE:")
        print("   Eat the apples 🍎 to grow your snake and increase your score!")
        print("   Avoid hitting walls or your own tail!")
        print()
        
        print("🎮 CONTROLS:")
        print("   W + ENTER = Move Up    ⬆️")
        print("   A + ENTER = Move Left  ⬅️") 
        print("   S + ENTER = Move Down  ⬇️")
        print("   D + ENTER = Move Right ➡️")
        print("   C + ENTER = Start Game 🔄")
        print("   Q + ENTER = Quit Game  ❌")

        print("   🐍 Snake moves automatically every 0.4 seconds!")
        print()
        
        print(f"🗺️  MAP SIZE: {self.size} x {self.size}")
        print()
        
        print("🐍 Ready to start? Press ENTER to begin...")
        input()  # Wait for user to press enter


def main(size=10):
    game = SnakeGame(size)
    game.run()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Play Snake Game')
    parser.add_argument('--size', '-s', type=int, default=10, help='Map size (default 10)')
    args = parser.parse_args()
    main(args.size)
