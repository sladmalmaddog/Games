import tkinter as tk
from tkinter import messagebox


PIECES = {
    "wk": "\u2654",
    "wq": "\u2655",
    "wr": "\u2656",
    "wb": "\u2657",
    "wn": "\u2658",
    "wp": "\u2659",
    "bk": "\u265a",
    "bq": "\u265b",
    "br": "\u265c",
    "bb": "\u265d",
    "bn": "\u265e",
    "bp": "\u265f",
}


class Chess:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f4")

        tk.Label(self.root, text="Chess", font=("Segoe UI", 22, "bold"), bg="#f5f5f4", fg="#292524").pack(pady=(12, 2))
        self.status = tk.Label(self.root, text="", font=("Segoe UI", 11), bg="#f5f5f4", fg="#44403c")
        self.status.pack(pady=(0, 8))

        self.frame = tk.Frame(self.root, bg="#292524", padx=3, pady=3)
        self.frame.pack()
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                button = tk.Button(
                    self.frame,
                    width=3,
                    height=1,
                    font=("Segoe UI Symbol", 24),
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
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp"] * 8,
            [""] * 8,
            [""] * 8,
            [""] * 8,
            [""] * 8,
            ["wp"] * 8,
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]
        self.turn = "w"
        self.selected = None
        self.game_over = False
        self.draw()

    def click(self, row, col):
        if self.game_over:
            return
        piece = self.board[row][col]
        if self.selected is None:
            if piece and piece[0] == self.turn:
                self.selected = (row, col)
                self.draw()
            return

        start = self.selected
        if start == (row, col):
            self.selected = None
            self.draw()
            return

        if piece and piece[0] == self.turn:
            self.selected = (row, col)
            self.draw()
            return

        if self.valid_move(start, (row, col)):
            self.move_piece(start, (row, col))
        else:
            self.status.config(text="That piece cannot move there.")
        self.selected = None
        self.draw()

    def move_piece(self, start, end):
        sr, sc = start
        er, ec = end
        moving = self.board[sr][sc]
        captured = self.board[er][ec]
        self.board[er][ec] = moving
        self.board[sr][sc] = ""
        if moving[1] == "p" and er in (0, 7):
            self.board[er][ec] = moving[0] + "q"
        if captured.endswith("k"):
            self.game_over = True
            winner = "White" if self.turn == "w" else "Black"
            self.status.config(text=f"{winner} wins by capturing the king.")
            messagebox.showinfo("Chess", f"{winner} wins!")
            return
        self.turn = "b" if self.turn == "w" else "w"

    def valid_move(self, start, end):
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]
        target = self.board[er][ec]
        if not piece or (target and target[0] == piece[0]):
            return False

        dr = er - sr
        dc = ec - sc
        kind = piece[1]

        if kind == "p":
            direction = -1 if piece[0] == "w" else 1
            start_row = 6 if piece[0] == "w" else 1
            if dc == 0 and dr == direction and not target:
                return True
            if dc == 0 and sr == start_row and dr == 2 * direction and not target:
                middle = sr + direction
                return self.board[middle][sc] == ""
            if abs(dc) == 1 and dr == direction and target and target[0] != piece[0]:
                return True
            return False

        if kind == "n":
            return (abs(dr), abs(dc)) in ((1, 2), (2, 1))

        if kind == "k":
            return max(abs(dr), abs(dc)) == 1

        if kind == "b":
            return abs(dr) == abs(dc) and self.path_clear(start, end)

        if kind == "r":
            return (dr == 0 or dc == 0) and self.path_clear(start, end)

        if kind == "q":
            straight = dr == 0 or dc == 0
            diagonal = abs(dr) == abs(dc)
            return (straight or diagonal) and self.path_clear(start, end)

        return False

    def path_clear(self, start, end):
        sr, sc = start
        er, ec = end
        step_r = (er > sr) - (er < sr)
        step_c = (ec > sc) - (ec < sc)
        row = sr + step_r
        col = sc + step_c
        while (row, col) != (er, ec):
            if self.board[row][col]:
                return False
            row += step_r
            col += step_c
        return True

    def draw(self):
        for row in range(8):
            for col in range(8):
                light = "#f0d9b5"
                dark = "#b58863"
                color = light if (row + col) % 2 == 0 else dark
                if self.selected == (row, col):
                    color = "#fde047"
                piece = self.board[row][col]
                self.buttons[row][col].config(text=PIECES.get(piece, ""), bg=color, activebackground=color)
        if not self.game_over:
            name = "White" if self.turn == "w" else "Black"
            self.status.config(text=f"{name} to move. Basic rules only.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Chess().run()

