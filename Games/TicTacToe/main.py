import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f3ff")

        self.turn = "X"
        self.board = [""] * 9
        self.buttons = []

        title = tk.Label(
            self.root,
            text="Tic Tac Toe",
            font=("Segoe UI", 22, "bold"),
            bg="#f5f3ff",
            fg="#4c1d95",
        )
        title.pack(pady=(14, 4))

        self.status = tk.Label(
            self.root,
            text="Player X starts",
            font=("Segoe UI", 12),
            bg="#f5f3ff",
            fg="#5b21b6",
        )
        self.status.pack(pady=(0, 10))

        frame = tk.Frame(self.root, bg="#7c3aed", padx=3, pady=3)
        frame.pack()

        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                button = tk.Button(
                    frame,
                    text="",
                    width=5,
                    height=2,
                    font=("Consolas", 30, "bold"),
                    bg="#ffffff",
                    fg="#1f2937",
                    activebackground="#ede9fe",
                    command=lambda i=index: self.play(i),
                )
                button.grid(row=row, column=col, padx=3, pady=3)
                self.buttons.append(button)

        tk.Button(
            self.root,
            text="New Game",
            font=("Segoe UI", 11, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            command=self.reset,
        ).pack(pady=14)

    def play(self, index):
        if self.board[index]:
            return

        self.board[index] = self.turn
        self.buttons[index].config(text=self.turn, fg="#dc2626" if self.turn == "X" else "#2563eb")

        winner = self.find_winner()
        if winner:
            for i in winner:
                self.buttons[i].config(bg="#bbf7d0")
            messagebox.showinfo("Game over", f"Player {self.turn} wins!")
            self.status.config(text=f"Player {self.turn} wins!")
            self.disable_board()
            return

        if all(self.board):
            self.status.config(text="It is a draw.")
            messagebox.showinfo("Game over", "It is a draw.")
            return

        self.turn = "O" if self.turn == "X" else "X"
        self.status.config(text=f"Player {self.turn}'s turn")

    def find_winner(self):
        lines = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        )
        for line in lines:
            a, b, c = line
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return line
        return None

    def disable_board(self):
        for button in self.buttons:
            button.config(state="disabled")

    def reset(self):
        self.turn = "X"
        self.board = [""] * 9
        self.status.config(text="Player X starts")
        for button in self.buttons:
            button.config(text="", bg="#ffffff", state="normal")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TicTacToe().run()

