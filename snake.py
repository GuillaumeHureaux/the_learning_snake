# %%
import tkinter as tk
import random
import numpy as np
from itertools import product

# %%

class Snake():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = [(self.x, self.y)]
        self.face = 'up'
        self.last_move = 'up'
    
    def move(self):
        if self.face == 'up':
            self.y -= 1
        if self.face == 'down':
            self.y += 1
        if self.face == 'left':
            self.x -= 1
        if self.face == 'right':
            self.x += 1
        self.last_move = self.face
        self.body.insert(0, (self.x, self.y))
        self.body = self.body[:-1]
    
    def face_right(self, event):
        if self.last_move != 'left':
            self.face = 'right'
    
    def face_left(self, event):
        if self.last_move != 'right':
            self.face = 'left'

    def face_up(self, event):
        if self.last_move != 'down':
            self.face = 'up'

    def face_down(self, event):
        if self.last_move != 'up':
            self.face = 'down'

    def __len__(self):
        return len(self.body)
    
    def grow(self):
        self.body.append(self.body[-1])

class Apple():
    def __init__(self, x_max, y_max, snake_body):
        possibilities = set(product(range(x_max), range(y_max))).difference(set(snake_body))

        self.x, self.y = random.choice(list(possibilities))        


class Game():
    def __init__(self, master):
        self.x_max = 25
        self.y_max = 25
        self.canvas_size = (500, 500)
        self.flag = 0

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
    
    def init_new_game(self):
        self.flag = 1
        self.snake = Snake(int((self.x_max - 1) / 2), int((self.y_max - 1) / 2))
        self.apple = Apple(self.x_max, self.y_max, self.snake.body)

        self.waiting_frame.grid_remove()

        self.game_frame = tk.Frame(self.master)
        self.game_frame.grid()

        self.can = tk.Canvas(self.game_frame, width=self.canvas_size[1], height=self.canvas_size[0], bg='white')
        self.can.bind('<d>', self.snake.face_right)
        self.can.bind('<q>', self.snake.face_left)
        self.can.bind('<z>', self.snake.face_up)
        self.can.bind('<s>', self.snake.face_down)
        self.can.grid()

        self.can.focus_set()

        self.loop_game()
    

    def loop_game(self):
        self.snake.move()

        if self.snake.x < 0 or self.snake.x >= self.x_max or self.snake.y < 0 or self.snake.y >= self.y_max:
            self.flag = 0
            self.show_pre_game_window()
        
        if len(self.snake) > 1 and (self.snake.x, self.snake.y) in self.snake.body[1:]:
            self.flag = 0
            self.show_pre_game_window()
        
        if (self.snake.x, self.snake.y) == (self.apple.x, self.apple.y):
            self.snake.grow()
            self.apple = Apple(self.x_max, self.y_max, self.snake.body)
        
        if self.flag != 0:
            self.update_canvas()
            self.master.after(200, self.loop_game)
        

    def update_canvas(self):
        self.can.delete('all')
        square_size = self.canvas_size[0] / self.x_max, self.canvas_size[1] / self.y_max

        self.can.create_oval(self.apple.x * square_size[0], self.apple.y * square_size[1], (self.apple.x + 1) * square_size[0], (self.apple.y + 1) * square_size[1],
                                 outline='red', fill='red')
        
        head = self.snake.body[0]

        self.can.create_oval(head[0] * square_size[0], head[1] * square_size[1], (head[0] + 1) * square_size[0], (head[1] + 1) * square_size[1],
                                        outline='green', fill='blue')

        for elem in self.snake.body[1:]:
            self.can.create_oval(elem[0] * square_size[0], elem[1] * square_size[1], (elem[0] + 1) * square_size[0], (elem[1] + 1) * square_size[1],
                                 outline='green', fill='grey')


# %%
if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
# %%
