import random
import tkinter as tk
from tkinter import messagebox


CELL = 28
COLS = 10
ROWS = 20
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS

SHAPES = {
    "I": ([(0, 1), (1, 1), (2, 1), (3, 1)], "#22d3ee"),
    "O": ([(1, 0), (2, 0), (1, 1), (2, 1)], "#facc15"),
    "T": ([(1, 0), (0, 1), (1, 1), (2, 1)], "#a855f7"),
    "S": ([(1, 0), (2, 0), (0, 1), (1, 1)], "#22c55e"),
    "Z": ([(0, 0), (1, 0), (1, 1), (2, 1)], "#ef4444"),
    "J": ([(0, 0), (0, 1), (1, 1), (2, 1)], "#3b82f6"),
    "L": ([(2, 0), (0, 1), (1, 1), (2, 1)], "#f97316"),
}


class Tetris:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        self.info = tk.StringVar()
        tk.Label(
            self.root,
            textvariable=self.info,
            font=("Consolas", 15, "bold"),
            bg="#111827",
            fg="#f9fafb",
            pady=8,
        ).pack(fill="x")

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg="#030712",
            highlightthickness=0,
        )
        self.canvas.pack(padx=12, pady=(0, 12))

        self.root.bind("<KeyPress>", self.key_pressed)
        self.reset()
        self.loop()

    def reset(self):
        self.board = [["" for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.lines = 0
        self.game_over = False
        self.drop_delay = 450
        self.new_piece()
        self.update_info()
        self.draw()

    def update_info(self):
        self.info.set(f"Tetris  |  Score: {self.score}  Lines: {self.lines}  |  Arrows, Space, R")

    def new_piece(self):
        name = random.choice(list(SHAPES))
        blocks, color = SHAPES[name]
        self.piece = {
            "name": name,
            "blocks": [tuple(block) for block in blocks],
            "color": color,
            "x": 3,
            "y": 0,
        }
        if not self.valid(self.piece["blocks"], self.piece["x"], self.piece["y"]):
            self.game_over = True

    def valid(self, blocks, offset_x, offset_y):
        for x, y in blocks:
            board_x = offset_x + x
            board_y = offset_y + y
            if board_x < 0 or board_x >= COLS or board_y >= ROWS:
                return False
            if board_y >= 0 and self.board[board_y][board_x]:
                return False
        return True

    def move(self, dx, dy):
        if self.game_over:
            return False
        new_x = self.piece["x"] + dx
        new_y = self.piece["y"] + dy
        if self.valid(self.piece["blocks"], new_x, new_y):
            self.piece["x"] = new_x
            self.piece["y"] = new_y
            self.draw()
            return True
        return False

    def rotate(self):
        if self.game_over or self.piece["name"] == "O":
            return
        rotated = [(y, 3 - x) for x, y in self.piece["blocks"]]
        for kick in (0, -1, 1, -2, 2):
            if self.valid(rotated, self.piece["x"] + kick, self.piece["y"]):
                self.piece["blocks"] = rotated
                self.piece["x"] += kick
                self.draw()
                return

    def key_pressed(self, event):
        if event.keysym.lower() == "r":
            self.reset()
            return
        if event.keysym in ("Left", "a"):
            self.move(-1, 0)
        elif event.keysym in ("Right", "d"):
            self.move(1, 0)
        elif event.keysym in ("Down", "s"):
            if self.move(0, 1):
                self.score += 1
                self.update_info()
        elif event.keysym in ("Up", "w"):
            self.rotate()
        elif event.keysym == "space":
            while self.move(0, 1):
                self.score += 2
            self.lock_piece()

    def loop(self):
        if not self.game_over:
            if not self.move(0, 1):
                self.lock_piece()
        self.root.after(self.drop_delay, self.loop)

    def lock_piece(self):
        for x, y in self.piece["blocks"]:
            board_x = self.piece["x"] + x
            board_y = self.piece["y"] + y
            if 0 <= board_y < ROWS and 0 <= board_x < COLS:
                self.board[board_y][board_x] = self.piece["color"]
        self.clear_lines()
        self.new_piece()
        self.draw()
        if self.game_over:
            self.info.set(f"Game over! Score: {self.score}  |  Press R")
            messagebox.showinfo("Tetris", "Game over!")

    def clear_lines(self):
        new_board = [row for row in self.board if not all(row)]
        cleared = ROWS - len(new_board)
        if cleared:
            self.lines += cleared
            self.score += [0, 100, 300, 500, 800][cleared]
            self.drop_delay = max(120, self.drop_delay - cleared * 18)
            for _ in range(cleared):
                new_board.insert(0, ["" for _ in range(COLS)])
            self.board = new_board
            self.update_info()

    def draw_block(self, x, y, color):
        self.canvas.create_rectangle(
            x * CELL + 1,
            y * CELL + 1,
            (x + 1) * CELL - 1,
            (y + 1) * CELL - 1,
            fill=color,
            outline="#111827",
        )

    def draw(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                color = self.board[row][col]
                if color:
                    self.draw_block(col, row, color)
                else:
                    self.canvas.create_rectangle(
                        col * CELL,
                        row * CELL,
                        (col + 1) * CELL,
                        (row + 1) * CELL,
                        outline="#111827",
                    )

        if not self.game_over:
            for x, y in self.piece["blocks"]:
                self.draw_block(self.piece["x"] + x, self.piece["y"] + y, self.piece["color"])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Tetris().run()

