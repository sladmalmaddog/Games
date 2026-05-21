import random
import tkinter as tk
from tkinter import messagebox


ROWS = 10
COLS = 10
MINES = 15


class Minesweeper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.root.configure(bg="#f1f5f9")

        self.board = None
        self.revealed = set()
        self.flags = set()
        self.buttons = {}
        self.game_over = False
        self.flag_mode = False

        tk.Label(
            self.root,
            text="Minesweeper",
            font=("Segoe UI", 22, "bold"),
            bg="#f1f5f9",
            fg="#334155",
        ).pack(pady=(12, 2))

        self.status = tk.Label(
            self.root,
            text=f"{MINES} mines. Dig mode. Right click or Flag Mode marks flags.",
            font=("Segoe UI", 11),
            bg="#f1f5f9",
            fg="#475569",
        )
        self.status.pack(pady=(0, 10))
        self.root.bind("f", lambda _event: self.toggle_flag_mode())

        frame = tk.Frame(self.root, bg="#475569", padx=3, pady=3)
        frame.pack()

        for row in range(ROWS):
            for col in range(COLS):
                button = tk.Button(
                    frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Consolas", 12, "bold"),
                    bg="#cbd5e1",
                    activebackground="#e2e8f0",
                    relief="raised",
                    command=lambda r=row, c=col: self.cell_clicked(r, c),
                )
                button.grid(row=row, column=col, padx=1, pady=1)
                button.bind("<Button-3>", lambda event, r=row, c=col: self.flag(r, c))
                button.bind("<Button-2>", lambda event, r=row, c=col: self.flag(r, c))
                self.buttons[(row, col)] = button

        controls = tk.Frame(self.root, bg="#f1f5f9")
        controls.pack(pady=12)

        tk.Button(
            controls,
            text="New Field",
            font=("Segoe UI", 11, "bold"),
            bg="#334155",
            fg="white",
            activebackground="#1e293b",
            activeforeground="white",
            command=self.reset,
        ).pack(side="left", padx=5)

        self.flag_button = tk.Button(
            controls,
            text="Flag Mode: Off",
            font=("Segoe UI", 11, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            command=self.toggle_flag_mode,
        )
        self.flag_button.pack(side="left", padx=5)

        self.reset()

    def reset(self):
        self.board = None
        self.revealed.clear()
        self.flags.clear()
        self.game_over = False
        self.flag_mode = False
        self.flag_button.config(text="Flag Mode: Off", bg="#f59e0b")
        self.update_status("New field ready.")
        for button in self.buttons.values():
            button.config(text="", bg="#cbd5e1", fg="#0f172a", state="normal", relief="raised")

    def update_status(self, message=None):
        mode = "Flag mode" if self.flag_mode else "Dig mode"
        prefix = f"{mode}. Flags: {len(self.flags)} / {MINES}."
        if message:
            self.status.config(text=f"{prefix} {message}")
        else:
            self.status.config(text=prefix)

    def toggle_flag_mode(self):
        if self.game_over:
            return
        self.flag_mode = not self.flag_mode
        if self.flag_mode:
            self.flag_button.config(text="Flag Mode: On", bg="#dc2626")
            self.update_status("Click cells to place or remove flags.")
        else:
            self.flag_button.config(text="Flag Mode: Off", bg="#f59e0b")
            self.update_status("Click cells to dig.")

    def cell_clicked(self, row, col):
        if self.flag_mode:
            self.flag(row, col)
        else:
            self.reveal(row, col)

    def make_board(self, safe_row, safe_col):
        mines = set()
        safe_zone = {
            (r, c)
            for r in range(safe_row - 1, safe_row + 2)
            for c in range(safe_col - 1, safe_col + 2)
            if 0 <= r < ROWS and 0 <= c < COLS
        }
        while len(mines) < MINES:
            spot = (random.randrange(ROWS), random.randrange(COLS))
            if spot not in safe_zone:
                mines.add(spot)

        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for row, col in mines:
            board[row][col] = -1
            for nr, nc in self.neighbors(row, col):
                if board[nr][nc] != -1:
                    board[nr][nc] += 1
        self.board = board

    def neighbors(self, row, col):
        for nr in range(row - 1, row + 2):
            for nc in range(col - 1, col + 2):
                if (nr, nc) != (row, col) and 0 <= nr < ROWS and 0 <= nc < COLS:
                    yield nr, nc

    def flag(self, row, col):
        if self.game_over or (row, col) in self.revealed:
            return
        button = self.buttons[(row, col)]
        if (row, col) in self.flags:
            self.flags.remove((row, col))
            button.config(text="", bg="#cbd5e1")
        else:
            self.flags.add((row, col))
            button.config(text="F", bg="#fde68a", fg="#92400e")
        self.update_status()

    def reveal(self, row, col):
        if self.game_over or (row, col) in self.flags:
            return
        if self.board is None:
            self.make_board(row, col)
            self.update_status("First dig is safe.")
        if self.board[row][col] == -1:
            self.lose()
            return

        self.flood(row, col)
        self.check_win()

    def flood(self, row, col):
        stack = [(row, col)]
        colors = {
            1: "#2563eb",
            2: "#16a34a",
            3: "#dc2626",
            4: "#7c3aed",
            5: "#b91c1c",
            6: "#0891b2",
            7: "#111827",
            8: "#475569",
        }
        while stack:
            current = stack.pop()
            if current in self.revealed or current in self.flags:
                continue
            r, c = current
            self.revealed.add(current)
            value = self.board[r][c]
            button = self.buttons[current]
            button.config(
                text=str(value) if value else "",
                fg=colors.get(value, "#0f172a"),
                bg="#f8fafc",
                relief="sunken",
                state="disabled",
            )
            if value == 0:
                stack.extend(self.neighbors(r, c))

    def lose(self):
        self.game_over = True
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == -1:
                    self.buttons[(row, col)].config(text="*", bg="#fecaca", fg="#7f1d1d")
        self.status.config(text="Boom! You hit a mine.")
        messagebox.showinfo("Minesweeper", "Boom! You hit a mine.")

    def check_win(self):
        if len(self.revealed) == ROWS * COLS - MINES:
            self.game_over = True
            self.status.config(text="You cleared the field!")
            messagebox.showinfo("Minesweeper", "You won!")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Minesweeper().run()
