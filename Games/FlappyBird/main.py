import random
import tkinter as tk


WIDTH = 420
HEIGHT = 560
GROUND = 510


class FlappyBird:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flappy Bird")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#7dd3fc", highlightthickness=0)
        self.canvas.pack()
        self.root.bind("<space>", self.flap)
        self.root.bind("r", lambda _event: self.reset())
        self.reset()
        self.update()

    def reset(self):
        self.bird_y = HEIGHT // 2
        self.velocity = 0
        self.pipes = []
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False
        self.started = False

    def flap(self, _event=None):
        if self.game_over:
            self.reset()
            return
        self.started = True
        self.velocity = -8

    def add_pipe(self):
        gap = 145
        top_height = random.randint(70, 320)
        self.pipes.append({"x": WIDTH + 20, "top": top_height, "bottom": top_height + gap, "scored": False})

    def update(self):
        if self.started and not self.game_over:
            self.velocity += 0.45
            self.bird_y += self.velocity
            self.pipe_timer += 1
            if self.pipe_timer > 78:
                self.add_pipe()
                self.pipe_timer = 0

            for pipe in self.pipes:
                pipe["x"] -= 3
                if not pipe["scored"] and pipe["x"] + 52 < 90:
                    pipe["scored"] = True
                    self.score += 1
            self.pipes = [pipe for pipe in self.pipes if pipe["x"] > -70]
            self.check_collision()

        self.draw()
        self.root.after(25, self.update)

    def check_collision(self):
        bird_box = (62, self.bird_y - 16, 98, self.bird_y + 16)
        if self.bird_y - 16 < 0 or self.bird_y + 16 > GROUND:
            self.game_over = True
            return
        for pipe in self.pipes:
            x1 = pipe["x"]
            x2 = pipe["x"] + 56
            top_box = (x1, 0, x2, pipe["top"])
            bottom_box = (x1, pipe["bottom"], x2, GROUND)
            if self.overlap(bird_box, top_box) or self.overlap(bird_box, bottom_box):
                self.game_over = True
                return

    def overlap(self, a, b):
        return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, GROUND, WIDTH, HEIGHT, fill="#84cc16", outline="")
        self.canvas.create_rectangle(0, GROUND + 14, WIDTH, HEIGHT, fill="#65a30d", outline="")

        for cloud_x in (60, 220, 350):
            self.canvas.create_oval(cloud_x, 60, cloud_x + 70, 100, fill="#e0f2fe", outline="")
            self.canvas.create_oval(cloud_x + 28, 45, cloud_x + 92, 94, fill="#f0f9ff", outline="")

        for pipe in self.pipes:
            x = pipe["x"]
            self.canvas.create_rectangle(x, 0, x + 56, pipe["top"], fill="#22c55e", outline="#15803d", width=3)
            self.canvas.create_rectangle(x - 4, pipe["top"] - 18, x + 60, pipe["top"], fill="#16a34a", outline="#15803d")
            self.canvas.create_rectangle(x, pipe["bottom"], x + 56, GROUND, fill="#22c55e", outline="#15803d", width=3)
            self.canvas.create_rectangle(x - 4, pipe["bottom"], x + 60, pipe["bottom"] + 18, fill="#16a34a", outline="#15803d")

        self.canvas.create_oval(62, self.bird_y - 16, 98, self.bird_y + 16, fill="#facc15", outline="#ca8a04", width=2)
        self.canvas.create_oval(88, self.bird_y - 8, 96, self.bird_y, fill="#111827", outline="")
        self.canvas.create_polygon(98, self.bird_y, 112, self.bird_y + 6, 98, self.bird_y + 12, fill="#fb923c", outline="")

        self.canvas.create_text(18, 16, anchor="nw", text=f"Score: {self.score}", font=("Consolas", 18, "bold"), fill="#0f172a")
        if not self.started:
            self.canvas.create_text(WIDTH // 2, 240, text="Press Space", font=("Segoe UI", 24, "bold"), fill="#0f172a")
        if self.game_over:
            self.canvas.create_text(WIDTH // 2, 245, text="Game Over", font=("Segoe UI", 28, "bold"), fill="#7f1d1d")
            self.canvas.create_text(WIDTH // 2, 282, text="Space or R to restart", font=("Segoe UI", 13, "bold"), fill="#7f1d1d")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    FlappyBird().run()

