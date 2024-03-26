# %%
import tkinter as tk
import random
import numpy as np
from itertools import product

from snake_ground import Ground

# %%

class GameUI():
    def __init__(self, master, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.canvas_size = (500, 500)

        self.master = master
        
        self.waiting_frame = tk.Frame(self.master)
        self.run_button = tk.Button(self.waiting_frame, text='New game', command=self.init_new_game)
        self.run_button.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.run_button = tk.Button(self.waiting_frame, text='Quit', command=self.master.destroy)
        self.run_button.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.waiting_frame.grid()
    
    def show_pre_game_window(self):
        self.waiting_frame.grid()
        self.game_frame.grid_remove()
    
    def next_direction(self, event):
        self.action = {'d': 'right', 'q': 'left', 'z': 'up', 's': 'down'}[event.char]
    
    def init_new_game(self):
        self.ground = Ground(self.x_max, self.y_max)
        self.action = 'up'

        self.waiting_frame.grid_remove()

        self.game_frame = tk.Frame(self.master)
        self.game_frame.grid()

        self.can = tk.Canvas(self.game_frame, width=self.canvas_size[1], height=self.canvas_size[0], bg='white')
        self.can.bind('<d>', self.next_direction)
        self.can.bind('<q>', self.next_direction)
        self.can.bind('<z>', self.next_direction)
        self.can.bind('<s>', self.next_direction)
        self.can.grid()

        self.can.focus_set()

        self.loop_game()
    

    def loop_game(self):
        
        self.ground.step(self.action)

        if self.ground.flag != 0:
            self.update_canvas()
            self.master.after(200, self.loop_game)
        
        else:
            self.show_pre_game_window()
        

    def update_canvas(self):
        self.can.delete('all')
        square_size = self.canvas_size[0] / self.x_max, self.canvas_size[1] / self.y_max

        self.can.create_oval(self.ground.apple.x * square_size[0], self.ground.apple.y * square_size[1], (self.ground.apple.x + 1) * square_size[0], (self.ground.apple.y + 1) * square_size[1],
                                 outline='red', fill='red')
        
        head = self.ground.snake.body[0]

        self.can.create_oval(head[0] * square_size[0], head[1] * square_size[1], (head[0] + 1) * square_size[0], (head[1] + 1) * square_size[1],
                                        outline='green', fill='blue')

        for elem in self.ground.snake.body[1:]:
            self.can.create_oval(elem[0] * square_size[0], elem[1] * square_size[1], (elem[0] + 1) * square_size[0], (elem[1] + 1) * square_size[1],
                                 outline='green', fill='grey')


# %%
x_max = 25
y_max = 25

if __name__ == "__main__":
    root = tk.Tk()
    GameUI(root, x_max, y_max)
    root.mainloop()
# %%
