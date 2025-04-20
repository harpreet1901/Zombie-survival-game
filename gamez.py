import tkinter as tk
import random

ROWS, COLS = 10, 10
ZOMBIE_SPAWN_INTERVAL = 3
RESOURCE_GOAL = 5

EMPTY = ' '
PLAYER = 'P'
ZOMBIE = 'Z'
RESOURCE = 'R'
ESCAPE = 'E'

class ZombieGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zombie Survival Game")
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.cell_size = 50
        self.city = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.player = [1, 1]
        self.zombies = []
        self.resources_collected = 0
        self.turns = 0

        self.generate_city()
        self.root.bind("<Key>", self.handle_key)
        self.draw_city()

    def generate_city(self):
        for i in range(ROWS):
            for j in range(COLS):
                self.city[i][j] = EMPTY
        self.city[self.player[0]][self.player[1]] = PLAYER
        for _ in range(3):
            while True:
                x, y = random.randint(0, ROWS-1), random.randint(0, COLS-1)
                if self.city[x][y] == EMPTY:
                    self.city[x][y] = RESOURCE
                    break
        self.spawn_escape()

    def spawn_escape(self):
        while True:
            x, y = random.randint(0, ROWS-1), random.randint(0, COLS-1)
            if self.city[x][y] == EMPTY:
                self.city[x][y] = ESCAPE
                break

    def draw_city(self):
        self.canvas.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = "white"
                text = self.city[i][j]
                if text == PLAYER:
                    color = "blue"
                elif text == ZOMBIE:
                    color = "red"
                elif text == RESOURCE:
                    color = "green"
                elif text == ESCAPE:
                    color = "yellow"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
                if text != EMPTY:
                    self.canvas.create_text(x0 + 25, y0 + 25, text=text, font=("Arial", 16, "bold"))
        self.canvas.create_text(250, 10, text=f"Resources: {self.resources_collected}/{RESOURCE_GOAL}", font=("Arial", 14))

    def handle_key(self, event):
        key = event.keysym.lower()
        if key in ('w', 'a', 's', 'd'):
            self.move_player(key)
            self.turns += 1
            if self.turns % ZOMBIE_SPAWN_INTERVAL == 0:
                self.add_zombie()
            self.move_zombies()
            self.draw_city()

    def move_player(self, direction):
        dx, dy = 0, 0
        if direction == 'w': dx = -1
        elif direction == 's': dx = 1
        elif direction == 'a': dy = -1
        elif direction == 'd': dy = 1

        new_x = self.player[0] + dx
        new_y = self.player[1] + dy

        if not (0 <= new_x < ROWS and 0 <= new_y < COLS):
            return

        target = self.city[new_x][new_y]
        if target == ZOMBIE:
            self.end_game("A zombie got you! Game Over!")
        elif target == RESOURCE:
            self.resources_collected += 1
            if self.resources_collected >= RESOURCE_GOAL:
                self.end_game("You collected enough resources! You win!")
        elif target == ESCAPE:
            self.end_game("You escaped! You win!")

        self.city[self.player[0]][self.player[1]] = EMPTY
        self.player[0], self.player[1] = new_x, new_y
        self.city[self.player[0]][self.player[1]] = PLAYER

    def add_zombie(self):
        while True:
            x, y = random.randint(0, ROWS-1), random.randint(0, COLS-1)
            if self.city[x][y] == EMPTY:
                self.zombies.append([x, y])
                self.city[x][y] = ZOMBIE
                break

    def move_zombies(self):
        new_zombies = []
        for z in self.zombies:
            self.city[z[0]][z[1]] = EMPTY
            zx, zy = z
            if zx < self.player[0]: zx += 1
            elif zx > self.player[0]: zx -= 1
            if zy < self.player[1]: zy += 1
            elif zy > self.player[1]: zy -= 1

            if [zx, zy] == self.player:
                self.end_game("A zombie got you! Game Over!")
                return

            if self.city[zx][zy] != PLAYER:
                self.city[zx][zy] = ZOMBIE
                new_zombies.append([zx, zy])
        self.zombies = new_zombies

    def end_game(self, message):
        self.canvas.create_text(250, 250, text=message, font=("Arial", 20), fill="black")
        self.root.unbind("<Key>")

# Run the game
root = tk.Tk()
game = ZombieGameGUI(root)
root.mainloop()