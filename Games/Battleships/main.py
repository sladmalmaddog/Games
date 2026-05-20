import random
import tkinter as tk
from tkinter import messagebox


SIZE = 10
SHIPS = [5, 4, 3, 3, 2]


class Battleships:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battleships")
        self.root.resizable(False, False)
        self.root.configure(bg="#eff6ff")

        title = tk.Label(
            self.root,
            text="Battleships",
            font=("Segoe UI", 22, "bold"),
            bg="#eff6ff",
            fg="#1e3a8a",
        )
        title.pack(pady=(12, 2))

        self.status = tk.Label(
            self.root,
            text="Click the enemy ocean to fire.",
            font=("Segoe UI", 11),
            bg="#eff6ff",
            fg="#1e40af",
        )
        self.status.pack(pady=(0, 10))

        boards = tk.Frame(self.root, bg="#eff6ff")
        boards.pack(padx=12)

        self.player_buttons = {}
        self.enemy_buttons = {}
        self.make_grid(boards, "Your Ships", 0, self.player_buttons, False)
        self.make_grid(boards, "Enemy Ocean", 1, self.enemy_buttons, True)

        tk.Button(
            self.root,
            text="New Battle",
            font=("Segoe UI", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            command=self.reset,
        ).pack(pady=12)

        self.reset()

    def make_grid(self, parent, label, column, store, enemy):
        wrapper = tk.Frame(parent, bg="#eff6ff")
        wrapper.grid(row=0, column=column, padx=10)
        tk.Label(wrapper, text=label, font=("Segoe UI", 12, "bold"), bg="#eff6ff", fg="#1e3a8a").pack()
        frame = tk.Frame(wrapper, bg="#1e40af", padx=2, pady=2)
        frame.pack()
        for row in range(SIZE):
            for col in range(SIZE):
                button = tk.Button(
                    frame,
                    text="",
                    width=2,
                    height=1,
                    font=("Consolas", 10, "bold"),
                    bg="#bfdbfe",
                    activebackground="#dbeafe",
                    command=lambda r=row, c=col: self.fire(r, c) if enemy else None,
                )
                button.grid(row=row, column=col, padx=1, pady=1)
                store[(row, col)] = button

    def reset(self):
        self.player_ships = self.place_ships()
        self.enemy_ships = self.place_ships()
        self.player_hits = set()
        self.enemy_hits = set()
        self.player_misses = set()
        self.enemy_misses = set()
        self.game_over = False
        self.status.config(text="Click the enemy ocean to fire.")
        self.draw()

    def place_ships(self):
        ships = set()
        for size in SHIPS:
            placed = False
            while not placed:
                horizontal = random.choice([True, False])
                if horizontal:
                    row = random.randrange(SIZE)
                    col = random.randrange(SIZE - size + 1)
                    cells = {(row, col + i) for i in range(size)}
                else:
                    row = random.randrange(SIZE - size + 1)
                    col = random.randrange(SIZE)
                    cells = {(row + i, col) for i in range(size)}
                if not cells & ships:
                    ships.update(cells)
                    placed = True
        return ships

    def fire(self, row, col):
        if self.game_over or (row, col) in self.enemy_hits or (row, col) in self.enemy_misses:
            return

        if (row, col) in self.enemy_ships:
            self.enemy_hits.add((row, col))
            self.status.config(text="Hit! Fire again.")
        else:
            self.enemy_misses.add((row, col))
            self.status.config(text="Miss. Enemy fires back.")
            self.enemy_turn()

        self.draw()
        self.check_win()

    def enemy_turn(self):
        choices = [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if (r, c) not in self.player_hits and (r, c) not in self.player_misses
        ]
        if not choices:
            return
        row, col = random.choice(choices)
        if (row, col) in self.player_ships:
            self.player_hits.add((row, col))
            self.status.config(text="Enemy hit your ship!")
        else:
            self.player_misses.add((row, col))

    def check_win(self):
        if self.enemy_ships <= self.enemy_hits:
            self.game_over = True
            self.status.config(text="You sank the enemy fleet!")
            messagebox.showinfo("Battleships", "You won!")
        elif self.player_ships <= self.player_hits:
            self.game_over = True
            self.status.config(text="Your fleet was sunk.")
            messagebox.showinfo("Battleships", "You lost.")

    def draw(self):
        for row in range(SIZE):
            for col in range(SIZE):
                spot = (row, col)
                player_button = self.player_buttons[spot]
                if spot in self.player_hits:
                    player_button.config(text="X", bg="#ef4444", fg="white")
                elif spot in self.player_misses:
                    player_button.config(text="o", bg="#dbeafe", fg="#1d4ed8")
                elif spot in self.player_ships:
                    player_button.config(text="", bg="#64748b")
                else:
                    player_button.config(text="", bg="#bfdbfe")

                enemy_button = self.enemy_buttons[spot]
                if spot in self.enemy_hits:
                    enemy_button.config(text="X", bg="#ef4444", fg="white")
                elif spot in self.enemy_misses:
                    enemy_button.config(text="o", bg="#dbeafe", fg="#1d4ed8")
                else:
                    enemy_button.config(text="", bg="#bfdbfe")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Battleships().run()

