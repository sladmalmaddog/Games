import random
import tkinter as tk


MAZE = [
    "###################",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#.................#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.### # ###.####",
    "   #.#       #.#   ",
    "####.# ## ## #.####",
    "     . #   # .     ",
    "####.# ##### #.####",
    "   #.#       #.#   ",
    "####.#.#####.#.####",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#..#.....P.....#..#",
    "##.#.#.#####.#.#.##",
    "#....#...#...#....#",
    "###################",
]

CELL = 24
ROWS = len(MAZE)
COLS = len(MAZE[0])
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 42


class Pacman:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pacman")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#020617", highlightthickness=0)
        self.canvas.pack()
        self.root.bind("<KeyPress>", self.key_pressed)
        self.reset()
        self.update()

    def reset(self):
        self.walls = set()
        self.pellets = set()
        self.score = 0
        self.game_over = False
        self.win = False
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.ghosts = [
            {"pos": (9, 9), "dir": (1, 0), "color": "#ef4444"},
            {"pos": (8, 9), "dir": (-1, 0), "color": "#ec4899"},
            {"pos": (10, 9), "dir": (0, -1), "color": "#22d3ee"},
        ]
        for row, line in enumerate(MAZE):
            for col, char in enumerate(line):
                if char == "#":
                    self.walls.add((row, col))
                elif char == ".":
                    self.pellets.add((row, col))
                elif char == "P":
                    self.player = (row, col)

    def key_pressed(self, event):
        if event.keysym.lower() == "r":
            self.reset()
            return
        keys = {
            "Up": (-1, 0),
            "Down": (1, 0),
            "Left": (0, -1),
            "Right": (0, 1),
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1),
        }
        if event.keysym in keys:
            self.next_direction = keys[event.keysym]

    def update(self):
        if not self.game_over:
            self.move_player()
            self.move_ghosts()
            self.check_status()
        self.draw()
        self.root.after(135, self.update)

    def can_move(self, row, col):
        row %= ROWS
        col %= COLS
        return (row, col) not in self.walls

    def move_player(self):
        row, col = self.player
        nr = (row + self.next_direction[0]) % ROWS
        nc = (col + self.next_direction[1]) % COLS
        if self.can_move(nr, nc):
            self.direction = self.next_direction
        nr = (row + self.direction[0]) % ROWS
        nc = (col + self.direction[1]) % COLS
        if self.can_move(nr, nc):
            self.player = (nr, nc)
        if self.player in self.pellets:
            self.pellets.remove(self.player)
            self.score += 10

    def move_ghosts(self):
        choices = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for ghost in self.ghosts:
            row, col = ghost["pos"]
            possible = []
            for direction in choices:
                nr = (row + direction[0]) % ROWS
                nc = (col + direction[1]) % COLS
                if self.can_move(nr, nc):
                    possible.append(direction)
            if ghost["dir"] not in possible or random.random() < 0.25:
                ghost["dir"] = random.choice(possible)
            nr = (row + ghost["dir"][0]) % ROWS
            nc = (col + ghost["dir"][1]) % COLS
            ghost["pos"] = (nr, nc)

    def check_status(self):
        if any(ghost["pos"] == self.player for ghost in self.ghosts):
            self.game_over = True
        elif not self.pellets:
            self.game_over = True
            self.win = True

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#020617", outline="")
        for row, col in self.walls:
            x = col * CELL
            y = row * CELL + 42
            self.canvas.create_rectangle(x, y, x + CELL, y + CELL, fill="#1d4ed8", outline="#2563eb")
        for row, col in self.pellets:
            x = col * CELL + CELL // 2
            y = row * CELL + 42 + CELL // 2
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="#fef3c7", outline="")

        row, col = self.player
        x = col * CELL + CELL // 2
        y = row * CELL + 42 + CELL // 2
        self.canvas.create_arc(x - 11, y - 11, x + 11, y + 11, start=30, extent=300, fill="#facc15", outline="#eab308")

        for ghost in self.ghosts:
            row, col = ghost["pos"]
            x = col * CELL + CELL // 2
            y = row * CELL + 42 + CELL // 2
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=ghost["color"], outline="")
            self.canvas.create_rectangle(x - 10, y, x + 10, y + 11, fill=ghost["color"], outline="")
            self.canvas.create_oval(x - 5, y - 3, x - 1, y + 1, fill="#020617", outline="")
            self.canvas.create_oval(x + 3, y - 3, x + 7, y + 1, fill="#020617", outline="")

        self.canvas.create_text(12, 12, anchor="nw", text=f"Score: {self.score}", fill="#f8fafc", font=("Consolas", 15, "bold"))
        self.canvas.create_text(WIDTH - 12, 12, anchor="ne", text="Arrows/WASD. R restarts.", fill="#94a3b8", font=("Segoe UI", 10))

        if self.game_over:
            text = "You Win!" if self.win else "Caught!"
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=text, fill="#f8fafc", font=("Segoe UI", 32, "bold"))
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 38, text="Press R to restart", fill="#cbd5e1", font=("Segoe UI", 13))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Pacman().run()

