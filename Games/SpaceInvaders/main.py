import random
import tkinter as tk


WIDTH = 620
HEIGHT = 520


class SpaceInvaders:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#020617", highlightthickness=0)
        self.canvas.pack()

        self.keys = set()
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.reset()
        self.update()

    def reset(self):
        self.player_x = WIDTH // 2
        self.bullets = []
        self.enemy_bullets = []
        self.score = 0
        self.cooldown = 0
        self.alien_direction = 1
        self.game_over = False
        self.win = False
        self.aliens = []
        for row in range(4):
            for col in range(9):
                self.aliens.append({"x": 80 + col * 52, "y": 60 + row * 40, "alive": True})

    def key_down(self, event):
        if event.keysym.lower() == "r":
            self.reset()
        self.keys.add(event.keysym)

    def key_up(self, event):
        self.keys.discard(event.keysym)

    def update(self):
        if not self.game_over:
            self.handle_player()
            self.move_aliens()
            self.move_bullets()
            self.check_hits()
            self.maybe_enemy_shoots()
            if not any(alien["alive"] for alien in self.aliens):
                self.game_over = True
                self.win = True
        self.draw()
        self.root.after(28, self.update)

    def handle_player(self):
        if "Left" in self.keys or "a" in self.keys:
            self.player_x -= 6
        if "Right" in self.keys or "d" in self.keys:
            self.player_x += 6
        self.player_x = max(28, min(WIDTH - 28, self.player_x))

        if self.cooldown > 0:
            self.cooldown -= 1
        if ("space" in self.keys or "Up" in self.keys or "w" in self.keys) and self.cooldown == 0:
            self.bullets.append([self.player_x, HEIGHT - 70])
            self.cooldown = 12

    def move_aliens(self):
        alive = [alien for alien in self.aliens if alien["alive"]]
        if not alive:
            return
        left = min(alien["x"] for alien in alive)
        right = max(alien["x"] for alien in alive)
        if right > WIDTH - 35 and self.alien_direction == 1:
            self.alien_direction = -1
            for alien in alive:
                alien["y"] += 20
        elif left < 35 and self.alien_direction == -1:
            self.alien_direction = 1
            for alien in alive:
                alien["y"] += 20
        for alien in alive:
            alien["x"] += self.alien_direction * 1.2
            if alien["y"] > HEIGHT - 105:
                self.game_over = True

    def move_bullets(self):
        for bullet in self.bullets:
            bullet[1] -= 9
        for bullet in self.enemy_bullets:
            bullet[1] += 5
        self.bullets = [bullet for bullet in self.bullets if bullet[1] > -10]
        self.enemy_bullets = [bullet for bullet in self.enemy_bullets if bullet[1] < HEIGHT + 10]

    def check_hits(self):
        remaining_bullets = []
        for bullet in self.bullets:
            hit = False
            bx, by = bullet
            for alien in self.aliens:
                if alien["alive"] and abs(alien["x"] - bx) < 20 and abs(alien["y"] - by) < 18:
                    alien["alive"] = False
                    self.score += 10
                    hit = True
                    break
            if not hit:
                remaining_bullets.append(bullet)
        self.bullets = remaining_bullets

        for bx, by in self.enemy_bullets:
            if abs(bx - self.player_x) < 25 and HEIGHT - 65 < by < HEIGHT - 32:
                self.game_over = True

    def maybe_enemy_shoots(self):
        alive = [alien for alien in self.aliens if alien["alive"]]
        if alive and random.random() < 0.025:
            shooter = random.choice(alive)
            self.enemy_bullets.append([shooter["x"], shooter["y"] + 14])

    def draw(self):
        self.canvas.delete("all")
        for x in range(15, WIDTH, 70):
            self.canvas.create_oval(x, 30 + (x % 90), x + 2, 32 + (x % 90), fill="#e5e7eb", outline="")

        self.canvas.create_text(12, 12, anchor="nw", text=f"Score: {self.score}", fill="#e5e7eb", font=("Consolas", 15, "bold"))
        self.canvas.create_text(WIDTH - 12, 12, anchor="ne", text="A/D or arrows, Space", fill="#94a3b8", font=("Segoe UI", 10))

        self.canvas.create_polygon(
            self.player_x,
            HEIGHT - 88,
            self.player_x - 26,
            HEIGHT - 38,
            self.player_x + 26,
            HEIGHT - 38,
            fill="#38bdf8",
            outline="#0ea5e9",
        )
        self.canvas.create_rectangle(self.player_x - 14, HEIGHT - 48, self.player_x + 14, HEIGHT - 34, fill="#0284c7", outline="")

        for alien in self.aliens:
            if alien["alive"]:
                x, y = alien["x"], alien["y"]
                self.canvas.create_oval(x - 18, y - 13, x + 18, y + 13, fill="#84cc16", outline="#4d7c0f")
                self.canvas.create_rectangle(x - 10, y + 6, x + 10, y + 18, fill="#65a30d", outline="")
                self.canvas.create_oval(x - 8, y - 5, x - 3, y, fill="#020617", outline="")
                self.canvas.create_oval(x + 3, y - 5, x + 8, y, fill="#020617", outline="")

        for bx, by in self.bullets:
            self.canvas.create_rectangle(bx - 2, by - 10, bx + 2, by + 4, fill="#facc15", outline="")
        for bx, by in self.enemy_bullets:
            self.canvas.create_rectangle(bx - 2, by - 4, bx + 2, by + 10, fill="#fb7185", outline="")

        if self.game_over:
            text = "You Win!" if self.win else "Game Over"
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=text, fill="#f8fafc", font=("Segoe UI", 32, "bold"))
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 42, text="Press R to restart", fill="#cbd5e1", font=("Segoe UI", 13))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SpaceInvaders().run()

