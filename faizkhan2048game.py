import random

class Game2048:
    def __init__(self):
        self.grid = [[0]*4 for _ in range(4)]
        self.score = 0
        self.generate_tile()
        self.generate_tile()

    def generate_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.grid[r][c] = random.choice([2, 4])

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return row

    def move(self, direction):
        if direction == 'up':
            self.grid = [list(row) for row in zip(*self.grid)]
            self.grid = [self.compress(self.merge(self.compress(row))) for row in self.grid]
            self.grid = [list(row) for row in zip(*self.grid)]
        elif direction == 'down':
            self.grid = [list(row) for row in zip(*self.grid)]
            self.grid = [self.compress(self.merge(self.compress(row[::-1])))[::-1] for row in self.grid]
            self.grid = [list(row) for row in zip(*self.grid)]
        elif direction == 'left':
            self.grid = [self.compress(self.merge(self.compress(row))) for row in self.grid]
        elif direction == 'right':
            self.grid = [self.compress(self.merge(self.compress(row[::-1])))[::-1] for row in self.grid]

        self.generate_tile()

    def print_grid(self):
        for row in self.grid:
            print(row)
        print(f"Score: {self.score}")
import tkinter as tk

class Game2048GUI:
    def __init__(self, root):
        self.game = Game2048()
        self.root = root
        self.root.title("2048 Game")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.draw_grid()
        self.root.bind("<Up>", lambda event: self.on_key("up"))
        self.root.bind("<Down>", lambda event: self.on_key("down"))
        self.root.bind("<Left>", lambda event: self.on_key("left"))
        self.root.bind("<Right>", lambda event: self.on_key("right"))

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(4):
            for c in range(4):
                value = self.game.grid[r][c]
                color = "#f2f2f2" if value == 0 else "#ffcc00"  # Adjust colors as needed
                self.canvas.create_rectangle(c*100, r*100, c*100 + 100, r*100 + 100, fill=color)
                if value:
                    self.canvas.create_text(c*100 + 50, r*100 + 50, text=str(value), font=("Arial", 24))

    def on_key(self, direction):
        self.game.move(direction)
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    game_gui = Game2048GUI(root)
    root.mainloop()
