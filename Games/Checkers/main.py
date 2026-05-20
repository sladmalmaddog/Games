import tkinter as tk
from tkinter import messagebox


class Checkers:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Checkers")
        self.root.resizable(False, False)
        self.root.configure(bg="#fafaf9")

        tk.Label(self.root, text="Checkers", font=("Segoe UI", 22, "bold"), bg="#fafaf9", fg="#292524").pack(pady=(12, 2))
        self.status = tk.Label(self.root, text="", font=("Segoe UI", 11), bg="#fafaf9", fg="#44403c")
        self.status.pack(pady=(0, 8))

        self.frame = tk.Frame(self.root, bg="#292524", padx=3, pady=3)
        self.frame.pack()
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                button = tk.Button(
                    self.frame,
                    width=4,
                    height=2,
                    font=("Consolas", 16, "bold"),
                    command=lambda r=row, c=col: self.click(r, c),
                )
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

        tk.Button(
            self.root,
            text="New Game",
            font=("Segoe UI", 11, "bold"),
            bg="#57534e",
            fg="white",
            activebackground="#44403c",
            activeforeground="white",
            command=self.reset,
        ).pack(pady=12)

        self.reset()

    def reset(self):
        self.board = [["" for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = "b"
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = "r"
        self.turn = "r"
        self.selected = None
        self.game_over = False
        self.draw()

    def click(self, row, col):
        if self.game_over or (row + col) % 2 == 0:
            return

        piece = self.board[row][col]
        if self.selected is None:
            if piece and piece.lower() == self.turn:
                self.selected = (row, col)
                self.draw()
            return

        sr, sc = self.selected
        moves = self.valid_moves(sr, sc)
        if (row, col) in moves:
            captured = moves[(row, col)]
            self.board[row][col] = self.board[sr][sc]
            self.board[sr][sc] = ""
            if captured:
                cr, cc = captured
                self.board[cr][cc] = ""
            if self.board[row][col] == "r" and row == 0:
                self.board[row][col] = "R"
            if self.board[row][col] == "b" and row == 7:
                self.board[row][col] = "B"
            self.turn = "b" if self.turn == "r" else "r"
            self.selected = None
            self.check_win()
        elif piece and piece.lower() == self.turn:
            self.selected = (row, col)
        else:
            self.selected = None
        self.draw()

    def directions_for(self, piece):
        if piece == "r":
            return [(-1, -1), (-1, 1)]
        if piece == "b":
            return [(1, -1), (1, 1)]
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def valid_moves(self, row, col):
        piece = self.board[row][col]
        moves = {}
        if not piece:
            return moves
        for dr, dc in self.directions_for(piece):
            nr, nc = row + dr, col + dc
            if self.inside(nr, nc) and not self.board[nr][nc]:
                moves[(nr, nc)] = None
            jump_r, jump_c = row + dr * 2, col + dc * 2
            if self.inside(jump_r, jump_c) and not self.board[jump_r][jump_c]:
                middle = self.board[nr][nc] if self.inside(nr, nc) else ""
                if middle and middle.lower() != piece.lower():
                    moves[(jump_r, jump_c)] = (nr, nc)
        return moves

    def inside(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def check_win(self):
        red = any(piece.lower() == "r" for row in self.board for piece in row)
        black = any(piece.lower() == "b" for row in self.board for piece in row)
        if not red or not black:
            self.game_over = True
            winner = "Red" if red else "Black"
            self.status.config(text=f"{winner} wins!")
            messagebox.showinfo("Checkers", f"{winner} wins!")

    def draw(self):
        for row in range(8):
            for col in range(8):
                light = "#f0d9b5"
                dark = "#7c2d12"
                bg = light if (row + col) % 2 == 0 else dark
                if self.selected == (row, col):
                    bg = "#fde047"
                piece = self.board[row][col]
                text = ""
                fg = "#111827"
                if piece:
                    text = piece.upper()
                    fg = "#dc2626" if piece.lower() == "r" else "#111827"
                self.buttons[row][col].config(text=text, bg=bg, activebackground=bg, fg=fg)
        if not self.game_over:
            name = "Red" if self.turn == "r" else "Black"
            self.status.config(text=f"{name} to move.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Checkers().run()

