import random
import tkinter as tk


WIDTH = 640
HEIGHT = 520


class BrickBlast:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Brick Blast")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#111827", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.mouse_move)
        self.root.bind("<KeyPress>", self.key_down)
        self.reset()
        self.update()

    def reset(self):
        self.paddle_x = WIDTH // 2
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT - 90
        self.ball_dx = random.choice([-4, 4])
        self.ball_dy = -5
        self.score = 0
        self.lives = 3
        self.started = False
        self.game_over = False
        self.win = False
        self.make_bricks()

    def make_bricks(self):
        colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#3b82f6"]
        self.bricks = []
        for row in range(5):
            for col in range(9):
                x1 = 36 + col * 64
                y1 = 58 + row * 28
                self.bricks.append({"box": (x1, y1, x1 + 54, y1 + 18), "color": colors[row], "alive": True})

    def mouse_move(self, event):
        self.paddle_x = max(50, min(WIDTH - 50, event.x))

    def key_down(self, event):
        key = event.keysym.lower()
        if key == "r":
            self.reset()
        elif key == "space":
            self.started = True
        elif key in ("left", "a"):
            self.paddle_x -= 28
        elif key in ("right", "d"):
            self.paddle_x += 28
        self.paddle_x = max(50, min(WIDTH - 50, self.paddle_x))

    def update(self):
        if self.started and not self.game_over:
            self.move_ball()
        self.draw()
        self.root.after(16, self.update)

    def move_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x < 10 or self.ball_x > WIDTH - 10:
            self.ball_dx *= -1
        if self.ball_y < 10:
            self.ball_dy *= -1

        if HEIGHT - 58 <= self.ball_y <= HEIGHT - 42 and abs(self.ball_x - self.paddle_x) < 58 and self.ball_dy > 0:
            self.ball_dy *= -1
            self.ball_dx += (self.ball_x - self.paddle_x) / 22

        for brick in self.bricks:
            if not brick["alive"]:
                continue
            x1, y1, x2, y2 = brick["box"]
            if x1 <= self.ball_x <= x2 and y1 <= self.ball_y <= y2:
                brick["alive"] = False
                self.ball_dy *= -1
                self.score += 10
                break

        if self.ball_y > HEIGHT + 20:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.started = False
                self.ball_x = self.paddle_x
                self.ball_y = HEIGHT - 90
                self.ball_dx = random.choice([-4, 4])
                self.ball_dy = -5

        if not any(brick["alive"] for brick in self.bricks):
            self.game_over = True
            self.win = True

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(16, 14, anchor="nw", text=f"Score: {self.score}", fill="#f8fafc", font=("Consolas", 15, "bold"))
        self.canvas.create_text(WIDTH - 16, 14, anchor="ne", text=f"Lives: {self.lives}", fill="#f8fafc", font=("Consolas", 15, "bold"))
        self.canvas.create_text(WIDTH // 2, 18, text="Brick Blast", fill="#e5e7eb", font=("Segoe UI", 18, "bold"))

        for brick in self.bricks:
            if brick["alive"]:
                x1, y1, x2, y2 = brick["box"]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=brick["color"], outline="#111827", width=2)

        self.canvas.create_rectangle(self.paddle_x - 58, HEIGHT - 48, self.paddle_x + 58, HEIGHT - 34, fill="#38bdf8", outline="")
        self.canvas.create_oval(self.ball_x - 9, self.ball_y - 9, self.ball_x + 9, self.ball_y + 9, fill="#facc15", outline="")

        if not self.started and not self.game_over:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Press Space", fill="#f8fafc", font=("Segoe UI", 26, "bold"))
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 36, text="Mouse or arrows move the paddle", fill="#cbd5e1", font=("Segoe UI", 11))
        if self.game_over:
            text = "You Win!" if self.win else "Game Over"
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=text, fill="#f8fafc", font=("Segoe UI", 30, "bold"))
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 40, text="Press R to restart", fill="#cbd5e1", font=("Segoe UI", 12))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    BrickBlast().run()

