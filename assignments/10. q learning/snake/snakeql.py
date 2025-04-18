import numpy as np
import random
from snake import LearnSnake
import pickle

class SnakeQAgent():
    def __init__(self):
        self.discount_rate = 0.95
        self.learning_rate = 0.01
        self.eps = 1.0
        self.eps_discount = 0.9992
        self.min_eps = 0.001
        self.num_episodes = 10000
        self.table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        self.env = LearnSnake()
        self.score = 0
        self.survived = 0
        
    def get_action(self, state):
        if random.random() < self.eps:
            return random.choice([0, 1, 2, 3])
        return np.argmax(self.table[state])
    
    def train(self):
        max_score = 0
        with open("logs/training.log", "w") as f:
            f.write("Training . . . \n")
        for i in range(1, self.num_episodes + 1):
            self.env  = LearnSnake()
            steps_without_food = 0
            length = self.env.snake_length
            
            msg = f"Episodes: {i}, score: {np.mean(self.score)}, survived: {np.mean(self.survived)}, eps: {self.eps}"
            
            if i == 10000:
                with open(f'model/{i}.pickle', 'wb') as file:
                    pickle.dump(self.table, file)
            if max_score < self.score:
                max_score = self.score
                msg = msg + " --- (new best score)"
                with open(f'model/{i}.pickle', 'wb') as file:
                    pickle.dump(self.table, file)

            with open("logs/training.log", "a") as f:
                f.write(msg + "\n")
                
            current_state = self.env.get_state()
            self.eps = max(self.eps * self.eps_discount, self.min_eps)
            done = False
            while not done:
                action = self.get_action(current_state)
                new_state, reward, done = self.env.step(action)
                
                self.table[current_state][action] = (1 - self.learning_rate)\
                    * self.table[current_state][action] + self.learning_rate\
                    * (reward + self.discount_rate * max(self.table[new_state])) 
                current_state = new_state
                
                steps_without_food += 1
                if length != self.env.snake_length:
                    length = self.env.snake_length
                    steps_without_food = 0
                if steps_without_food == 1000:
                    break
            
            self.score = self.env.snake_length - 1
            self.survived = self.env.survived