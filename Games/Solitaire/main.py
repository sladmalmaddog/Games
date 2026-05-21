import random
import tkinter as tk
from tkinter import messagebox


CARD_W = 72
CARD_H = 96
GAP = 14
TOP = 145
COL_GAP = 16
X0 = 24
Y_STEP = 24

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["S", "H", "D", "C"]
RED = {"H", "D"}


class Solitaire:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Solitaire")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=760, height=640, bg="#166534", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.root.bind("r", lambda _event: self.reset())
        self.reset()

    def reset(self):
        deck = [{"rank": rank, "suit": suit, "up": False} for suit in SUITS for rank in RANKS]
        random.shuffle(deck)
        self.tableau = [[] for _ in range(7)]
        for col in range(7):
            for row in range(col + 1):
                card = deck.pop()
                card["up"] = row == col
                self.tableau[col].append(card)
        self.stock = deck
        self.waste = []
        self.foundations = {suit: [] for suit in SUITS}
        self.selected = None
        self.message = "Click stock, waste, cards, or foundations. R restarts."
        self.draw()

    def rank_value(self, card):
        return RANKS.index(card["rank"]) + 1

    def card_color(self, card):
        return "red" if card["suit"] in RED else "black"

    def click(self, event):
        x, y = event.x, event.y
        foundation = self.hit_foundation(x, y)
        tableau_col = self.hit_tableau_col(x)

        if self.in_box(x, y, 24, 36, CARD_W, CARD_H):
            self.draw_from_stock()
            return

        if self.selected and foundation:
            if self.move_to_foundation(foundation):
                self.after_move()
                return

        if self.selected and tableau_col is not None and y >= TOP - 20:
            if self.move_to_tableau(tableau_col):
                self.after_move()
                return

        if self.in_box(x, y, 116, 36, CARD_W, CARD_H) and self.waste:
            self.selected = ("waste",)
            self.message = "Waste card selected."
            self.draw()
            return

        if tableau_col is not None:
            index = self.hit_tableau_card(tableau_col, y)
            if index is not None:
                pile = self.tableau[tableau_col]
                card = pile[index]
                if not card["up"]:
                    if index == len(pile) - 1:
                        card["up"] = True
                        self.message = "Card flipped."
                    self.selected = None
                else:
                    self.selected = ("tableau", tableau_col, index)
                    self.message = f"Selected {card['rank']}{card['suit']}."
                self.draw()
                return

        self.selected = None
        self.draw()

    def draw_from_stock(self):
        self.selected = None
        if self.stock:
            card = self.stock.pop()
            card["up"] = True
            self.waste.append(card)
            self.message = "Drew a card."
        else:
            while self.waste:
                card = self.waste.pop()
                card["up"] = False
                self.stock.append(card)
            self.message = "Waste recycled into stock."
        self.draw()

    def selected_cards(self):
        if not self.selected:
            return []
        if self.selected[0] == "waste":
            return [self.waste[-1]] if self.waste else []
        _kind, col, index = self.selected
        return self.tableau[col][index:]

    def remove_selected(self):
        if self.selected[0] == "waste":
            return [self.waste.pop()]
        _kind, col, index = self.selected
        cards = self.tableau[col][index:]
        self.tableau[col] = self.tableau[col][:index]
        if self.tableau[col] and not self.tableau[col][-1]["up"]:
            self.tableau[col][-1]["up"] = True
        return cards

    def move_to_foundation(self, suit):
        cards = self.selected_cards()
        if len(cards) != 1:
            self.message = "Only one card can go to a foundation."
            return False
        card = cards[0]
        pile = self.foundations[suit]
        if card["suit"] != suit:
            self.message = "Wrong suit for that foundation."
            return False
        needed = len(pile) + 1
        if self.rank_value(card) != needed:
            self.message = "Foundations build from Ace to King."
            return False
        self.foundations[suit].extend(self.remove_selected())
        self.message = "Moved to foundation."
        return True

    def move_to_tableau(self, col):
        cards = self.selected_cards()
        if not cards:
            return False
        moving = cards[0]
        pile = self.tableau[col]
        if not pile:
            if moving["rank"] != "K":
                self.message = "Only a King can start an empty column."
                return False
        else:
            top = pile[-1]
            if self.card_color(top) == self.card_color(moving):
                self.message = "Tableau cards must alternate colors."
                return False
            if self.rank_value(top) != self.rank_value(moving) + 1:
                self.message = "Tableau cards build downward."
                return False
        self.tableau[col].extend(self.remove_selected())
        self.message = "Moved card."
        return True

    def after_move(self):
        self.selected = None
        if all(len(pile) == 13 for pile in self.foundations.values()):
            self.draw()
            messagebox.showinfo("Solitaire", "You won!")
        self.draw()

    def hit_foundation(self, x, y):
        for i, suit in enumerate(SUITS):
            fx = 390 + i * 86
            if self.in_box(x, y, fx, 36, CARD_W, CARD_H):
                return suit
        return None

    def hit_tableau_col(self, x):
        for col in range(7):
            cx = X0 + col * (CARD_W + COL_GAP)
            if cx <= x <= cx + CARD_W:
                return col
        return None

    def hit_tableau_card(self, col, y):
        pile = self.tableau[col]
        for index in reversed(range(len(pile))):
            cy = TOP + index * Y_STEP
            bottom = cy + CARD_H if index == len(pile) - 1 else cy + Y_STEP
            if cy <= y <= bottom:
                return index
        return None

    def in_box(self, x, y, bx, by, bw, bh):
        return bx <= x <= bx + bw and by <= y <= by + bh

    def draw_card(self, x, y, card, selected=False):
        if not card["up"]:
            self.canvas.create_rectangle(x, y, x + CARD_W, y + CARD_H, fill="#334155", outline="#dbeafe", width=2)
            self.canvas.create_text(x + CARD_W // 2, y + CARD_H // 2, text="PY", fill="#dbeafe", font=("Consolas", 18, "bold"))
            return
        fill = "#f8fafc"
        outline = "#fde047" if selected else "#e5e7eb"
        self.canvas.create_rectangle(x, y, x + CARD_W, y + CARD_H, fill=fill, outline=outline, width=3 if selected else 2)
        color = "#dc2626" if card["suit"] in RED else "#111827"
        self.canvas.create_text(x + 10, y + 10, anchor="nw", text=f"{card['rank']}{card['suit']}", fill=color, font=("Consolas", 14, "bold"))
        self.canvas.create_text(x + CARD_W // 2, y + CARD_H // 2, text=card["suit"], fill=color, font=("Consolas", 24, "bold"))

    def draw_empty(self, x, y, label):
        self.canvas.create_rectangle(x, y, x + CARD_W, y + CARD_H, fill="#15803d", outline="#86efac", dash=(3, 3), width=2)
        self.canvas.create_text(x + CARD_W // 2, y + CARD_H // 2, text=label, fill="#bbf7d0", font=("Segoe UI", 12, "bold"))

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(18, 12, anchor="nw", text="Solitaire", fill="#f0fdf4", font=("Segoe UI", 24, "bold"))
        self.canvas.create_text(18, 610, anchor="sw", text=self.message, fill="#dcfce7", font=("Segoe UI", 11))

        if self.stock:
            self.draw_card(24, 36, {"rank": "", "suit": "", "up": False})
        else:
            self.draw_empty(24, 36, "Stock")
        if self.waste:
            selected = self.selected == ("waste",)
            self.draw_card(116, 36, self.waste[-1], selected)
        else:
            self.draw_empty(116, 36, "Waste")

        for i, suit in enumerate(SUITS):
            x = 390 + i * 86
            pile = self.foundations[suit]
            if pile:
                self.draw_card(x, 36, pile[-1])
            else:
                self.draw_empty(x, 36, suit)

        for col, pile in enumerate(self.tableau):
            x = X0 + col * (CARD_W + COL_GAP)
            if not pile:
                self.draw_empty(x, TOP, "K")
            for index, card in enumerate(pile):
                y = TOP + index * Y_STEP
                selected = self.selected == ("tableau", col, index)
                self.draw_card(x, y, card, selected)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Solitaire().run()

