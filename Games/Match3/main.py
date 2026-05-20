import random
import tkinter as tk


SIZE = 8
TYPES = ["A", "B", "C", "D", "E", "F"]
COLORS = {
    "A": "#ef4444",
    "B": "#3b82f6",
    "C": "#22c55e",
    "D": "#eab308",
    "E": "#a855f7",
    "F": "#f97316",
}


class Match3:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Match 3")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8fafc")

        self.score = 0
        self.selected = None
        self.board = []
        self.buttons = []

        top = tk.Frame(self.root, bg="#f8fafc")
        top.pack(fill="x", padx=16, pady=(14, 8))
        tk.Label(top, text="Match 3", font=("Segoe UI", 22, "bold"), bg="#f8fafc", fg="#0f172a").pack(side="left")
        self.score_label = tk.Label(top, text="Score: 0", font=("Segoe UI", 13, "bold"), bg="#f8fafc", fg="#334155")
        self.score_label.pack(side="right")

        frame = tk.Frame(self.root, bg="#334155", padx=4, pady=4)
        frame.pack(padx=16, pady=4)

        for row in range(SIZE):
            row_buttons = []
            for col in range(SIZE):
                button = tk.Button(
                    frame,
                    width=4,
                    height=2,
                    font=("Consolas", 13, "bold"),
                    fg="white",
                    relief="raised",
                    command=lambda r=row, c=col: self.click(r, c),
                )
                button.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        tk.Button(
            self.root,
            text="New Board",
            font=("Segoe UI", 11, "bold"),
            bg="#0f172a",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            command=self.reset,
        ).pack(pady=12)

        self.reset()

    def reset(self):
        self.score = 0
        self.selected = None
        self.board = [[random.choice(TYPES) for _ in range(SIZE)] for _ in range(SIZE)]
        while self.find_matches():
            self.board = [[random.choice(TYPES) for _ in range(SIZE)] for _ in range(SIZE)]
        self.draw()

    def click(self, row, col):
        if self.selected is None:
            self.selected = (row, col)
            self.draw()
            return

        old_row, old_col = self.selected
        if (row, col) == self.selected:
            self.selected = None
            self.draw()
            return

        adjacent = abs(row - old_row) + abs(col - old_col) == 1
        if not adjacent:
            self.selected = (row, col)
            self.draw()
            return

        self.swap((row, col), self.selected)
        matches = self.find_matches()
        if matches:
            self.selected = None
            self.remove_matches(matches)
        else:
            self.swap((row, col), self.selected)
            self.selected = None
            self.draw()

    def swap(self, first, second):
        r1, c1 = first
        r2, c2 = second
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]

    def find_matches(self):
        matches = set()
        for row in range(SIZE):
            count = 1
            for col in range(1, SIZE):
                if self.board[row][col] == self.board[row][col - 1]:
                    count += 1
                else:
                    if count >= 3:
                        matches.update((row, c) for c in range(col - count, col))
                    count = 1
            if count >= 3:
                matches.update((row, c) for c in range(SIZE - count, SIZE))

        for col in range(SIZE):
            count = 1
            for row in range(1, SIZE):
                if self.board[row][col] == self.board[row - 1][col]:
                    count += 1
                else:
                    if count >= 3:
                        matches.update((r, col) for r in range(row - count, row))
                    count = 1
            if count >= 3:
                matches.update((r, col) for r in range(SIZE - count, SIZE))
        return matches

    def remove_matches(self, matches):
        self.score += len(matches) * 10
        for row, col in matches:
            self.board[row][col] = None
        self.draw()
        self.root.after(180, self.drop_tiles)

    def drop_tiles(self):
        for col in range(SIZE):
            values = [self.board[row][col] for row in range(SIZE) if self.board[row][col] is not None]
            missing = SIZE - len(values)
            new_values = [random.choice(TYPES) for _ in range(missing)] + values
            for row in range(SIZE):
                self.board[row][col] = new_values[row]

        matches = self.find_matches()
        if matches:
            self.root.after(160, lambda: self.remove_matches(matches))
        else:
            self.draw()

    def draw(self):
        self.score_label.config(text=f"Score: {self.score}")
        for row in range(SIZE):
            for col in range(SIZE):
                gem = self.board[row][col]
                button = self.buttons[row][col]
                if gem is None:
                    button.config(text="", bg="#e2e8f0", relief="sunken")
                else:
                    border = "sunken" if self.selected == (row, col) else "raised"
                    button.config(text=gem, bg=COLORS[gem], activebackground=COLORS[gem], relief=border)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Match3().run()

