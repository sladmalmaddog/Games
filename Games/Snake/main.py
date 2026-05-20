import random
import tkinter as tk


CELL = 24
GRID = 24
WIDTH = CELL * GRID
HEIGHT = CELL * GRID


class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.resizable(False, False)

        self.score_text = tk.StringVar()
        self.score_label = tk.Label(
            self.root,
            textvariable=self.score_text,
            font=("Consolas", 16, "bold"),
            bg="#16213e",
            fg="#f7f7f7",
            pady=8,
        )
        self.score_label.pack(fill="x")

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg="#101828",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.root.bind("<KeyPress>", self.change_direction)
        self.root.bind("r", lambda _event: self.reset())
        self.reset()
        self.tick()

    def reset(self):
        center = GRID // 2
        self.snake = [(center, center), (center - 1, center), (center - 2, center)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.food = self.make_food()
        self.score = 0
        self.game_over = False
        self.speed = 110
        self.update_score()
        self.draw()

    def update_score(self):
        self.score_text.set(f"Snake  |  Score: {self.score}  |  R to restart")

    def make_food(self):
        while True:
            food = (random.randrange(GRID), random.randrange(GRID))
            if food not in self.snake:
                return food

    def change_direction(self, event):
        keys = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
        }
        new_direction = keys.get(event.keysym)
        if not new_direction:
            return
        if new_direction[0] != -self.direction[0] or new_direction[1] != -self.direction[1]:
            self.next_direction = new_direction

    def tick(self):
        if not self.game_over:
            self.move()
            self.draw()
        self.root.after(self.speed, self.tick)

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        hit_wall = not (0 <= new_head[0] < GRID and 0 <= new_head[1] < GRID)
        hit_body = new_head in self.snake
        if hit_wall or hit_body:
            self.game_over = True
            self.score_text.set(f"Game over! Final score: {self.score}  |  Press R")
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.speed = max(55, self.speed - 3)
            self.food = self.make_food()
            self.update_score()
        else:
            self.snake.pop()

    def draw_cell(self, x, y, color, padding=2):
        self.canvas.create_rectangle(
            x * CELL + padding,
            y * CELL + padding,
            (x + 1) * CELL - padding,
            (y + 1) * CELL - padding,
            fill=color,
            outline="",
        )

    def draw(self):
        self.canvas.delete("all")
        for i in range(GRID + 1):
            color = "#1f2937"
            self.canvas.create_line(i * CELL, 0, i * CELL, HEIGHT, fill=color)
            self.canvas.create_line(0, i * CELL, WIDTH, i * CELL, fill=color)

        food_x, food_y = self.food
        self.draw_cell(food_x, food_y, "#ef4444", 4)

        for index, (x, y) in enumerate(self.snake):
            color = "#22c55e" if index == 0 else "#84cc16"
            self.draw_cell(x, y, color)

        if self.game_over:
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2,
                text="GAME OVER",
                font=("Consolas", 36, "bold"),
                fill="#f8fafc",
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SnakeGame().run()

