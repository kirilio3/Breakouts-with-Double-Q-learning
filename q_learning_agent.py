import numpy as np
import random

class DoubleQLearningAgent:
    def __init__(self, action_size, state_size, learning_rate=0.1, discount_factor=0.95, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01):
        self.action_size = action_size          # Number of possible actions
        self.state_size = state_size            # Size of state space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon                  # Exploration rate
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

        # Initialize two Q-tables
        self.q_table1 = np.zeros((state_size, action_size))
        self.q_table2 = np.zeros((state_size, action_size))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # Explore
            return random.randint(0, self.action_size - 1)  
        else:
            # Exploit
            return np.argmax(self.q_table1[state] + self.q_table2[state])

    def update(self, state, action, reward, next_state):
        if random.random() < 0.5:
            # Update Q-table 1
            best_next_action = np.argmax(self.q_table1[next_state])
            target = reward + self.discount_factor * self.q_table2[next_state][best_next_action]
            self.q_table1[state][action] += self.learning_rate * (target - self.q_table1[state][action])
        else:
            # Update Q-table 2
            best_next_action = np.argmax(self.q_table2[next_state])
            target = reward + self.discount_factor * self.q_table1[next_state][best_next_action]
            self.q_table2[state][action] += self.learning_rate * (target - self.q_table2[state][action])

        # Epsilon decay
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
