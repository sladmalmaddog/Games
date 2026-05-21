import random
import tkinter as tk
from tkinter import messagebox


ROWS = 6
COLS = 8
SYMBOLS = list("ABCDEFGHIJKLMNOPQRSTUVWX")


class Mahjong:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mahjong")
        self.root.resizable(False, False)
        self.root.configure(bg="#fefce8")

        tk.Label(self.root, text="Mahjong", font=("Segoe UI", 22, "bold"), bg="#fefce8", fg="#713f12").pack(pady=(12, 2))
        self.status = tk.Label(self.root, text="", font=("Segoe UI", 11), bg="#fefce8", fg="#854d0e")
        self.status.pack(pady=(0, 10))

        self.frame = tk.Frame(self.root, bg="#a16207", padx=4, pady=4)
        self.frame.pack()
        self.buttons = []
        for row in range(ROWS):
            row_buttons = []
            for col in range(COLS):
                button = tk.Button(
                    self.frame,
                    width=4,
                    height=2,
                    font=("Consolas", 14, "bold"),
                    bg="#fef3c7",
                    activebackground="#fde68a",
                    command=lambda r=row, c=col: self.pick(r, c),
                )
                button.grid(row=row, column=col, padx=3, pady=3)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        controls = tk.Frame(self.root, bg="#fefce8")
        controls.pack(pady=12)
        tk.Button(controls, text="New Layout", font=("Segoe UI", 10, "bold"), bg="#ca8a04", fg="white", command=self.reset).pack(side="left", padx=5)
        tk.Button(controls, text="Shuffle", font=("Segoe UI", 10, "bold"), bg="#854d0e", fg="white", command=self.shuffle_open_tiles).pack(side="left", padx=5)

        self.reset()

    def reset(self):
        tiles = SYMBOLS[:] * 2
        random.shuffle(tiles)
        self.board = []
        index = 0
        for row in range(ROWS):
            self.board.append([])
            for _col in range(COLS):
                self.board[row].append(tiles[index])
                index += 1
        self.selected = None
        self.removed = set()
        self.status.config(text="Match pairs. Only tiles with a free left or right side can be used.")
        self.draw()

    def shuffle_open_tiles(self):
        remaining = [self.board[r][c] for r in range(ROWS) for c in range(COLS) if (r, c) not in self.removed]
        random.shuffle(remaining)
        index = 0
        for row in range(ROWS):
            for col in range(COLS):
                if (row, col) not in self.removed:
                    self.board[row][col] = remaining[index]
                    index += 1
        self.selected = None
        self.status.config(text="Remaining tiles shuffled.")
        self.draw()

    def is_free(self, row, col):
        if (row, col) in self.removed:
            return False
        left_free = col == 0 or (row, col - 1) in self.removed
        right_free = col == COLS - 1 or (row, col + 1) in self.removed
        return left_free or right_free

    def pick(self, row, col):
        if (row, col) in self.removed:
            return
        if not self.is_free(row, col):
            self.status.config(text="That tile is blocked on both sides.")
            return
        if self.selected is None:
            self.selected = (row, col)
            self.status.config(text=f"Selected {self.board[row][col]}.")
            self.draw()
            return
        if self.selected == (row, col):
            self.selected = None
            self.draw()
            return

        sr, sc = self.selected
        if self.board[sr][sc] == self.board[row][col]:
            self.removed.add((sr, sc))
            self.removed.add((row, col))
            self.selected = None
            if len(self.removed) == ROWS * COLS:
                self.status.config(text="All pairs cleared!")
                self.draw()
                messagebox.showinfo("Mahjong", "You cleared the board!")
                return
            self.status.config(text="Pair removed.")
        else:
            self.selected = (row, col)
            self.status.config(text="Not a match. New tile selected.")
        self.draw()

    def draw(self):
        for row in range(ROWS):
            for col in range(COLS):
                button = self.buttons[row][col]
                if (row, col) in self.removed:
                    button.config(text="", bg="#fefce8", state="disabled", relief="flat")
                else:
                    free = self.is_free(row, col)
                    bg = "#fde047" if self.selected == (row, col) else "#fef3c7" if free else "#d6d3d1"
                    button.config(text=self.board[row][col], bg=bg, activebackground=bg, state="normal", relief="raised")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Mahjong().run()

