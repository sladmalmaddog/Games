import tkinter as tk
from tkinter import messagebox


PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


class Sudoku:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8fafc")
        self.cells = []

        tk.Label(
            self.root,
            text="Sudoku",
            font=("Segoe UI", 24, "bold"),
            bg="#f8fafc",
            fg="#0f172a",
        ).pack(pady=(14, 4))

        self.status = tk.Label(
            self.root,
            text="Fill the empty squares with 1-9",
            font=("Segoe UI", 11),
            bg="#f8fafc",
            fg="#475569",
        )
        self.status.pack(pady=(0, 10))

        board = tk.Frame(self.root, bg="#0f172a", padx=3, pady=3)
        board.pack()

        for row in range(9):
            cell_row = []
            for col in range(9):
                value = PUZZLE[row][col]
                bg = "#e2e8f0" if value else "#ffffff"
                cell = tk.Entry(
                    board,
                    width=2,
                    justify="center",
                    font=("Consolas", 20, "bold"),
                    bg=bg,
                    fg="#0f172a",
                    disabledbackground="#cbd5e1",
                    disabledforeground="#0f172a",
                    relief="flat",
                )
                cell.grid(
                    row=row,
                    column=col,
                    padx=(1, 4 if col in (2, 5) else 1),
                    pady=(1, 4 if row in (2, 5) else 1),
                    ipady=4,
                )
                if value:
                    cell.insert(0, str(value))
                    cell.config(state="disabled")
                else:
                    cell.bind("<KeyRelease>", self.keep_one_digit)
                cell_row.append(cell)
            self.cells.append(cell_row)

        controls = tk.Frame(self.root, bg="#f8fafc")
        controls.pack(pady=14)

        for text, command, color in (
            ("Check", self.check, "#2563eb"),
            ("Clear", self.clear, "#64748b"),
            ("Solve", self.solve, "#16a34a"),
        ):
            tk.Button(
                controls,
                text=text,
                font=("Segoe UI", 10, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                command=command,
                width=8,
            ).pack(side="left", padx=5)

    def keep_one_digit(self, event):
        text = event.widget.get()
        valid = "".join(ch for ch in text if ch in "123456789")
        event.widget.delete(0, "end")
        event.widget.insert(0, valid[:1])

    def check(self):
        wrong = False
        incomplete = False
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                if PUZZLE[row][col]:
                    continue
                value = cell.get()
                if not value:
                    incomplete = True
                    cell.config(bg="#ffffff")
                elif int(value) == SOLUTION[row][col]:
                    cell.config(bg="#dcfce7")
                else:
                    wrong = True
                    cell.config(bg="#fecaca")

        if wrong:
            self.status.config(text="Some numbers are wrong.")
        elif incomplete:
            self.status.config(text="Looks good so far, but not finished.")
        else:
            self.status.config(text="Solved! Nice job.")
            messagebox.showinfo("Sudoku", "Puzzle solved!")

    def clear(self):
        for row in range(9):
            for col in range(9):
                if not PUZZLE[row][col]:
                    self.cells[row][col].delete(0, "end")
                    self.cells[row][col].config(bg="#ffffff")
        self.status.config(text="Fill the empty squares with 1-9")

    def solve(self):
        for row in range(9):
            for col in range(9):
                if not PUZZLE[row][col]:
                    self.cells[row][col].delete(0, "end")
                    self.cells[row][col].insert(0, str(SOLUTION[row][col]))
                    self.cells[row][col].config(bg="#dcfce7")
        self.status.config(text="Solved puzzle shown.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Sudoku().run()

