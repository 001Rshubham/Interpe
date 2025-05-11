import tkinter as tk
from tkinter import messagebox
import random
import copy

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe Menu")
        self.mode = tk.StringVar(value="Human vs Human")
        self.difficulty = tk.StringVar(value="Easy")

        tk.Label(master, text="Choose Mode:").pack()
        tk.OptionMenu(master, self.mode, "Human vs Human", "Human vs Computer").pack()

        tk.Label(master, text="AI Difficulty:").pack()
        tk.OptionMenu(master, self.difficulty, "Easy", "Normal", "Hard").pack()

        tk.Button(master, text="Start Game", command=self.start_game).pack(pady=10)

    def start_game(self):
        self.new_window = tk.Toplevel(self.master)
        GameBoard(self.new_window, self.mode.get(), self.difficulty.get())

class GameBoard:
    def __init__(self, root, mode, difficulty):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.mode = mode
        self.difficulty = difficulty
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=('Helvetica', 32), width=5, height=2,
                                command=lambda row=i, col=j: self.make_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def make_move(self, row, col):
        if self.board[row][col] != "":
            return

        if self.mode == "Human vs Human" or self.current_player == "X":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.reset_game()
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
                return
            self.current_player = "O" if self.current_player == "X" else "X"

        if self.mode == "Human vs Computer" and self.current_player == "O":
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.difficulty == "Easy":
            move = self.get_random_move()
        elif self.difficulty == "Normal":
            move = self.get_normal_ai_move()
        else:  # Hard
            move = self.get_best_move()

        if move:
            row, col = move
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")
            if self.check_winner("O"):
                messagebox.showinfo("Game Over", "Computer (O) wins!")
                self.reset_game()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "X"

    def get_random_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(empty) if empty else None

    def get_normal_ai_move(self):
        # Win if possible
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        return (i, j)
                    self.board[i][j] = ""
        # Block if X can win
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
        # Else random
        return self.get_random_move()

    def get_best_move(self):
        best_score = -float('inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def minimax(self, is_max):
        if self.check_winner("O"):
            return 1
        elif self.check_winner("X"):
            return -1
        elif self.is_draw():
            return 0

        if is_max:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        best = max(best, self.minimax(False))
                        self.board[i][j] = ""
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        best = min(best, self.minimax(True))
                        self.board[i][j] = ""
            return best

    def check_winner(self, player):
        win_lines = (
            self.board,
            zip(*self.board),
            [[self.board[i][i] for i in range(3)]],
            [[self.board[i][2-i] for i in range(3)]]
        )
        for line_group in win_lines:
            for line in line_group:
                if all(cell == player for cell in line):
                    return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for row in self.buttons:
            for btn in row:
                btn.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
