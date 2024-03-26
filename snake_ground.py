import numpy as np
from itertools import product
import random

class Snake():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = [(self.x, self.y)]
        self.face = 'up'
        self.last_move = 'up'
        self.possible_actions = ["up", "down", "left", "right"]
        self.possible_actions_vector = [0, 1, 2, 3]
        self.possible_actions_map = {0: "up", 1: "down", 2: "left", 3: "right"}
    
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
        self.body.pop()
    
    def update_face(self, action):
        if isinstance(action, int):
            action = self.possible_actions_map[action]
        if action == 'right' and self.last_move != 'left':
            self.face = 'right'
        if action == 'left' and self.last_move != 'right':
            self.face = 'left'
        if action == 'down' and self.last_move != 'up':
            self.face = 'down'
        if action == 'up' and self.last_move != 'down':
            self.face = 'up'

    def __len__(self):
        return len(self.body)
    
    def grow(self):
        self.body.append(self.body[-1])


class Apple():
    def __init__(self, x_max, y_max, snake_body):
        possibilities = set(product(range(x_max), range(y_max))).difference(set(snake_body))

        self.x, self.y = random.choice(list(possibilities))        

class Ground():
    def __init__(self, x_max=4, y_max=4, max_steps=200):
        self.x_max = x_max
        self.y_max = y_max
        self.snake = Snake(int((self.x_max - 1) / 2), int((self.y_max - 1) / 2))
        self.apple = Apple(self.x_max, self.y_max, self.snake.body)
        self.flag = 1
        self.max_steps = max_steps
    
    def step(self, action):
        self.snake.update_face(action)
        self.snake.move()

        reward = 0
        terminated = False

        # snake is outbound
        if self.snake.x < 0 or self.snake.x >= self.x_max or self.snake.y < 0 or self.snake.y >= self.y_max:
            self.flag = 0
            reward = 0
            terminated = True
        
        # snake bites its tail
        elif len(self.snake) > 1 and (self.snake.x, self.snake.y) in self.snake.body[1:]:
            self.flag = 0
            reward = 0
            terminated = True
        
        # snake eats the apple
        elif (self.snake.x, self.snake.y) == (self.apple.x, self.apple.y):
            self.snake.grow()
            self.apple = Apple(self.x_max, self.y_max, self.snake.body)
            reward = len(self.snake)
        
        # snake continues its road
        else:
            reward = 0

        return self.get_state(), reward, terminated
    
    def get_state(self):
        ground_state = np.zeros((self.x_max, self.y_max))
        for elem in self.snake.body:
            if elem[0] < self.x_max and elem[1] < self.y_max:
                ground_state[elem] = 1
        ground_state[self.apple.x, self.apple.y] = 2
        ground_state = list(ground_state.flatten())
        map = {"up": 0, "down": 1, "left": 2, "right": 3}
        snake_state = [map[self.snake.face], len(self.snake)]

        return snake_state + ground_state
    
    def reset(self):
        self.__init__()
        return (
            self.get_state(),
            {}
        )

