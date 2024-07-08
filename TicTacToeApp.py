import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeApp:
    def __init__(self,root):
        self.root=root
        self.root.title("TIC-TAC-TOE")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.scores = {"Player X": 0, "Player O": 0, "Draws": 0}
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.ai_enabled = messagebox.askyesno("AI Opponent", "Do you want to play against the AI?")

    def create_widgets(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(self.root, text=" ", font=("Arial", 24), width=5, height=2,
                                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                self.buttons[row][col].grid(row=row, column=col)

        self.reset_button = tk.Button(self.root, text="Restart", font=("Arial", 18), command=self.reset_game)
        self.reset_button.grid(row=3, column=0, columnspan=3)

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 14))
        self.score_label.grid(row=4, column=0, columnspan=3)

    def get_score_text(self):
        return f"Player X: {self.scores['Player X']} | Player O: {self.scores['Player O']} | Draws: {self.scores['Draws']}"

    def on_button_click(self, row, col):
        if self.buttons[row][col]["text"] == " ":
            if self.current_player == "X":
                self.make_move(row, col, "X")
                if self.ai_enabled:
                    self.current_player = "O"
                    self.root.after(500, self.ai_move)
                else:
                    self.current_player = "O"
            elif self.current_player == "O" and not self.ai_enabled:
                self.make_move(row, col, "O")
                self.current_player = "X"

    def make_move(self, row, col, player):
        self.buttons[row][col]["text"] = player
        self.board[row][col] = player
        if self.check_winner(player):
            self.end_game(f"Player {player} wins!")
        elif self.check_draw():
            self.end_game("It's a draw!")

    def ai_move(self):
        row, col = self.get_best_move()
        self.make_move(row, col, "O")
        self.current_player = "X"

    def get_best_move(self):
        best_score = -float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for row in self.board:
            if all(s == player for s in row):
                return True
        for col in range(3):
            if all(row[col] == player for row in self.board):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def end_game(self, message):
        if "wins" in message:
            winner = "Player X" if "X" in message else "Player O"
            self.scores[winner] += 1
        else:
            self.scores["Draws"] += 1
        messagebox.showinfo("Game Over", message)
        self.score_label.config(text=self.get_score_text())
        self.reset_game()

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = " "


def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


