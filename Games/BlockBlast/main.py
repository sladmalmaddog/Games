import random
import tkinter as tk
from tkinter import messagebox


GRID = 8
CELL = 40
OX = 40
OY = 72
PIECE_Y = 430

SHAPES = [
    [(0, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]
COLORS = ["#ef4444", "#3b82f6", "#22c55e", "#eab308", "#a855f7", "#f97316", "#06b6d4"]


class BlockBlast:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Block Blast")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=420, height=570, bg="#f8fafc", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.root.bind("r", lambda _event: self.reset())
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(GRID)] for _ in range(GRID)]
        self.score = 0
        self.selected = None
        self.game_over = False
        self.message = "Pick a piece, then click the grid. R restarts."
        self.new_pieces()
        self.draw()

    def new_pieces(self):
        self.pieces = []
        for _ in range(3):
            shape = random.choice(SHAPES)
            self.pieces.append({"shape": shape, "color": random.choice(COLORS)})

    def click(self, event):
        if self.game_over:
            return
        piece_index = self.hit_piece(event.x, event.y)
        if piece_index is not None and self.pieces[piece_index] is not None:
            self.selected = piece_index
            self.message = "Piece selected."
            self.draw()
            return

        cell = self.hit_grid(event.x, event.y)
        if cell and self.selected is not None:
            row, col = cell
            piece = self.pieces[self.selected]
            if self.can_place(piece["shape"], row, col):
                self.place(piece, row, col)
                self.pieces[self.selected] = None
                self.selected = None
                if all(piece is None for piece in self.pieces):
                    self.new_pieces()
                if not self.any_moves_left():
                    self.game_over = True
                    self.message = "No moves left."
                    self.draw()
                    messagebox.showinfo("Block Blast", f"Game over! Score: {self.score}")
                    return
            else:
                self.message = "That piece does not fit there."
            self.draw()

    def hit_grid(self, x, y):
        if OX <= x < OX + GRID * CELL and OY <= y < OY + GRID * CELL:
            return (y - OY) // CELL, (x - OX) // CELL
        return None

    def hit_piece(self, x, y):
        for index in range(3):
            px = 56 + index * 122
            if px - 10 <= x <= px + 95 and PIECE_Y - 10 <= y <= PIECE_Y + 95:
                return index
        return None

    def can_place(self, shape, row, col):
        for dr, dc in shape:
            r = row + dr
            c = col + dc
            if r < 0 or r >= GRID or c < 0 or c >= GRID or self.board[r][c] is not None:
                return False
        return True

    def place(self, piece, row, col):
        for dr, dc in piece["shape"]:
            self.board[row + dr][col + dc] = piece["color"]
        self.score += len(piece["shape"]) * 5
        cleared = self.clear_lines()
        if cleared:
            self.score += cleared * 60
            self.message = f"Cleared {cleared} line(s)!"
        else:
            self.message = "Piece placed."

    def clear_lines(self):
        rows = [r for r in range(GRID) if all(self.board[r][c] for c in range(GRID))]
        cols = [c for c in range(GRID) if all(self.board[r][c] for r in range(GRID))]
        for row in rows:
            for col in range(GRID):
                self.board[row][col] = None
        for col in cols:
            for row in range(GRID):
                self.board[row][col] = None
        return len(rows) + len(cols)

    def any_moves_left(self):
        for piece in self.pieces:
            if piece is None:
                continue
            for row in range(GRID):
                for col in range(GRID):
                    if self.can_place(piece["shape"], row, col):
                        return True
        return False

    def draw_square(self, x, y, size, color):
        self.canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline="#f8fafc", width=2)

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(22, 18, anchor="nw", text="Block Blast", fill="#0f172a", font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(398, 24, anchor="ne", text=f"Score: {self.score}", fill="#334155", font=("Segoe UI", 13, "bold"))
        self.canvas.create_text(22, 540, anchor="sw", text=self.message, fill="#475569", font=("Segoe UI", 10))

        for row in range(GRID):
            for col in range(GRID):
                x = OX + col * CELL
                y = OY + row * CELL
                color = self.board[row][col] or "#e2e8f0"
                self.draw_square(x, y, CELL, color)

        for index, piece in enumerate(self.pieces):
            px = 56 + index * 122
            self.canvas.create_rectangle(px - 12, PIECE_Y - 12, px + 96, PIECE_Y + 88, outline="#fde047" if self.selected == index else "#cbd5e1", width=3)
            if piece is None:
                self.canvas.create_text(px + 40, PIECE_Y + 34, text="Used", fill="#94a3b8", font=("Segoe UI", 11, "bold"))
                continue
            for dr, dc in piece["shape"]:
                self.draw_square(px + dc * 24, PIECE_Y + dr * 24, 24, piece["color"])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    BlockBlast().run()

