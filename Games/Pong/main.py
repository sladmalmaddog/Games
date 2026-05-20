import tkinter as tk


WIDTH = 640
HEIGHT = 420


class Pong:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pong")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#111827", highlightthickness=0)
        self.canvas.pack()

        self.keys = set()
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.reset()
        self.update()

    def reset(self):
        self.left_y = HEIGHT // 2
        self.right_y = HEIGHT // 2
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_dx = 5
        self.ball_dy = 3
        self.left_score = 0
        self.right_score = 0

    def key_down(self, event):
        if event.keysym.lower() == "r":
            self.reset()
        self.keys.add(event.keysym)

    def key_up(self, event):
        self.keys.discard(event.keysym)

    def update(self):
        if "w" in self.keys:
            self.left_y -= 7
        if "s" in self.keys:
            self.left_y += 7
        if "Up" in self.keys:
            self.right_y -= 7
        if "Down" in self.keys:
            self.right_y += 7

        self.left_y = max(50, min(HEIGHT - 50, self.left_y))
        self.right_y = max(50, min(HEIGHT - 50, self.right_y))

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_y < 12 or self.ball_y > HEIGHT - 12:
            self.ball_dy *= -1

        if self.ball_dx < 0 and 32 < self.ball_x < 48 and abs(self.ball_y - self.left_y) < 55:
            self.ball_dx *= -1
            self.ball_dy += (self.ball_y - self.left_y) / 18
        if self.ball_dx > 0 and WIDTH - 48 < self.ball_x < WIDTH - 32 and abs(self.ball_y - self.right_y) < 55:
            self.ball_dx *= -1
            self.ball_dy += (self.ball_y - self.right_y) / 18

        if self.ball_x < -20:
            self.right_score += 1
            self.serve(-1)
        if self.ball_x > WIDTH + 20:
            self.left_score += 1
            self.serve(1)

        self.draw()
        self.root.after(18, self.update)

    def serve(self, direction):
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_dx = 5 * direction
        self.ball_dy = 3

    def draw(self):
        self.canvas.delete("all")
        for y in range(0, HEIGHT, 28):
            self.canvas.create_rectangle(WIDTH // 2 - 2, y + 6, WIDTH // 2 + 2, y + 18, fill="#374151", outline="")

        self.canvas.create_text(WIDTH // 2, 28, text=f"{self.left_score}   {self.right_score}", fill="#f9fafb", font=("Consolas", 24, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT - 18, text="W/S and Up/Down. R restarts.", fill="#9ca3af", font=("Segoe UI", 10))

        self.canvas.create_rectangle(28, self.left_y - 50, 44, self.left_y + 50, fill="#60a5fa", outline="")
        self.canvas.create_rectangle(WIDTH - 44, self.right_y - 50, WIDTH - 28, self.right_y + 50, fill="#f97316", outline="")
        self.canvas.create_oval(self.ball_x - 11, self.ball_y - 11, self.ball_x + 11, self.ball_y + 11, fill="#f8fafc", outline="")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Pong().run()

