import random
import tkinter as tk


class MemoryGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory")
        self.root.resizable(False, False)
        self.root.configure(bg="#ecfeff")

        self.symbols = list("AABBCCDDEEFFGGHH")
        self.buttons = []
        self.first = None
        self.second = None
        self.locked = False
        self.moves = 0
        self.matches = 0

        tk.Label(
            self.root,
            text="Memory",
            font=("Segoe UI", 22, "bold"),
            bg="#ecfeff",
            fg="#155e75",
        ).pack(pady=(12, 0))

        self.status = tk.Label(
            self.root,
            text="Find all pairs",
            font=("Segoe UI", 12),
            bg="#ecfeff",
            fg="#164e63",
        )
        self.status.pack(pady=(2, 10))

        self.frame = tk.Frame(self.root, bg="#0891b2", padx=4, pady=4)
        self.frame.pack()

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                button = tk.Button(
                    self.frame,
                    text="?",
                    width=5,
                    height=2,
                    font=("Consolas", 22, "bold"),
                    bg="#cffafe",
                    fg="#155e75",
                    activebackground="#a5f3fc",
                    command=lambda i=index: self.flip(i),
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                self.buttons.append(button)

        tk.Button(
            self.root,
            text="Restart",
            font=("Segoe UI", 11, "bold"),
            bg="#0891b2",
            fg="white",
            activebackground="#0e7490",
            activeforeground="white",
            command=self.reset,
        ).pack(pady=12)

        self.reset()

    def reset(self):
        random.shuffle(self.symbols)
        self.first = None
        self.second = None
        self.locked = False
        self.moves = 0
        self.matches = 0
        self.status.config(text="Find all pairs")
        for button in self.buttons:
            button.config(text="?", state="normal", bg="#cffafe", fg="#155e75")

    def flip(self, index):
        if self.locked or self.buttons[index]["text"] != "?":
            return

        self.buttons[index].config(text=self.symbols[index], bg="#ffffff", fg="#0f172a")
        if self.first is None:
            self.first = index
            return

        self.second = index
        self.moves += 1
        self.status.config(text=f"Moves: {self.moves}")
        self.locked = True
        self.root.after(500, self.check_pair)

    def check_pair(self):
        if self.symbols[self.first] == self.symbols[self.second]:
            for index in (self.first, self.second):
                self.buttons[index].config(bg="#bbf7d0", state="disabled")
            self.matches += 1
            if self.matches == 8:
                self.status.config(text=f"You won in {self.moves} moves!")
        else:
            for index in (self.first, self.second):
                self.buttons[index].config(text="?", bg="#cffafe", fg="#155e75")

        self.first = None
        self.second = None
        self.locked = False

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MemoryGame().run()

