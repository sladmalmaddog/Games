import random
import tkinter as tk


COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}


class Game2048:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2048")
        self.root.resizable(False, False)
        self.root.configure(bg="#faf8ef")

        self.score = 0
        self.grid = [[0] * 4 for _ in range(4)]
        self.tiles = []

        top = tk.Frame(self.root, bg="#faf8ef")
        top.pack(fill="x", padx=18, pady=(16, 6))

        tk.Label(
            top,
            text="2048",
            font=("Segoe UI", 28, "bold"),
            bg="#faf8ef",
            fg="#776e65",
        ).pack(side="left")

        self.score_label = tk.Label(
            top,
            text="Score: 0",
            font=("Segoe UI", 13, "bold"),
            bg="#bbada0",
            fg="white",
            padx=12,
            pady=6,
        )
        self.score_label.pack(side="right")

        frame = tk.Frame(self.root, bg="#bbada0", padx=8, pady=8)
        frame.pack(padx=18, pady=8)

        for row in range(4):
            row_tiles = []
            for col in range(4):
                tile = tk.Label(
                    frame,
                    text="",
                    width=5,
                    height=2,
                    font=("Segoe UI", 24, "bold"),
                    bg="#cdc1b4",
                    fg="#776e65",
                )
                tile.grid(row=row, column=col, padx=5, pady=5)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

        tk.Button(
            self.root,
            text="New Game",
            font=("Segoe UI", 11, "bold"),
            bg="#8f7a66",
            fg="white",
            activebackground="#776e65",
            activeforeground="white",
            command=self.reset,
        ).pack(pady=(2, 14))

        self.root.bind("<KeyPress>", self.key_pressed)
        self.reset()

    def reset(self):
        self.score = 0
        self.grid = [[0] * 4 for _ in range(4)]
        self.add_tile()
        self.add_tile()
        self.draw()

    def add_tile(self):
        empty = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty:
            row, col = random.choice(empty)
            self.grid[row][col] = 4 if random.random() < 0.1 else 2

    def compress_line(self, line):
        numbers = [number for number in line if number]
        result = []
        gained = 0
        skip = False
        for i, number in enumerate(numbers):
            if skip:
                skip = False
                continue
            if i + 1 < len(numbers) and numbers[i + 1] == number:
                merged = number * 2
                result.append(merged)
                gained += merged
                skip = True
            else:
                result.append(number)
        result += [0] * (4 - len(result))
        return result, gained

    def key_pressed(self, event):
        directions = {"Left", "Right", "Up", "Down", "a", "d", "w", "s"}
        if event.keysym not in directions:
            return

        old_grid = [row[:] for row in self.grid]
        gained = 0

        if event.keysym in ("Left", "a"):
            for row in range(4):
                self.grid[row], points = self.compress_line(self.grid[row])
                gained += points
        elif event.keysym in ("Right", "d"):
            for row in range(4):
                line, points = self.compress_line(list(reversed(self.grid[row])))
                self.grid[row] = list(reversed(line))
                gained += points
        elif event.keysym in ("Up", "w"):
            for col in range(4):
                line = [self.grid[row][col] for row in range(4)]
                line, points = self.compress_line(line)
                for row in range(4):
                    self.grid[row][col] = line[row]
                gained += points
        elif event.keysym in ("Down", "s"):
            for col in range(4):
                line = [self.grid[row][col] for row in reversed(range(4))]
                line, points = self.compress_line(line)
                for row, value in zip(reversed(range(4)), line):
                    self.grid[row][col] = value
                gained += points

        if self.grid != old_grid:
            self.score += gained
            self.add_tile()
            self.draw()
            if not self.can_move():
                self.score_label.config(text=f"Game over! {self.score}")

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for row in range(4):
            for col in range(4):
                value = self.grid[row][col]
                if row < 3 and self.grid[row + 1][col] == value:
                    return True
                if col < 3 and self.grid[row][col + 1] == value:
                    return True
        return False

    def draw(self):
        self.score_label.config(text=f"Score: {self.score}")
        for row in range(4):
            for col in range(4):
                value = self.grid[row][col]
                bg, fg = COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                self.tiles[row][col].config(text=str(value) if value else "", bg=bg, fg=fg)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Game2048().run()

