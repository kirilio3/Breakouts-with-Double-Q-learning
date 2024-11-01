import pygame
import random
from player import Player
from ball import Ball
from brickWall import BrickWall

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)
font50 = pygame.font.Font('freesansbold.ttf', 50)

# RGB values of standard colors
BLACK = (0, 0, 0)
background_colour = (234, 212, 252)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atari Breakouts")

clock = pygame.time.Clock() 
FPS = 30

def get_state(paddle, ball):
    # Simple state representation based on positions
    paddle_pos = int(paddle.posx // (WIDTH / 10))  # Divide into regions
    ball_pos = int(ball.posx // (WIDTH / 10))
    return paddle_pos * 10 + ball_pos  # Combine into a single state representation

# Game Manager
def main():
    running = True
    paddle = Player(250, HEIGHT - 20, 100, 10, 20, BLACK, screen, WIDTH, font20)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE, screen, WIDTH, HEIGHT)
    brick_wall = BrickWall(rows = 5, cols = 10, brick_width = WIDTH // 10 - 4, brick_height = 20, padding = 5, color = RED)

    # Initialize Q-tables for double Q-learning
    q_table1 = {}
    q_table2 = {}
    epsilon = 0.1   # Exploration rate
    alpha = 0.1     # Learning rate
    gamma = 0.9     # Discount factor

    episode = 0     # Just for my own use to see how many episodes have passed

    while running:
        screen.fill(background_colour)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_state = get_state(paddle, ball)

        # Initialize Q-values if the state is not already in the table
        if current_state not in q_table1:
            q_table1[current_state] = [0, 0]  # [Q-value for left, Q-value for right]
            q_table2[current_state] = [0, 0]

        # Epsilon-greedy action selection
        if random.random() < epsilon:
            axn = random.choice([0, 1])  # 0 = move left, 1 = move right
        else:
            # Use the average of both Q-tables for action selection
            axn = 0 if (q_table1[current_state][0] + q_table2[current_state][0]) > (q_table1[current_state][1] + q_table2[current_state][1]) else 1

        # Move the paddle based on the chosen action
        paddleXFac = -1 if axn == 0 else 1
        paddle.update(paddleXFac)

        # Check for collisions
        if paddle.geekRect.colliderect(ball.getRect()):
            ball.hit()

        if brick_wall.check_collision(ball.getRect()):
            ball.hit()

        point = ball.update()

        if point == -1:  # Game over condition
            # Reset game state immediately without a game over screen
            # print(f"Game Over! Episode: {episode}")  # Print episode number and Q-table 
            ball.reset()
            brick_wall = BrickWall(rows = 5, cols = 10, brick_width = WIDTH // 10 - 4, brick_height = 20, padding = 5, color = RED)
            episode +=1 
        

        if brick_wall.all_bricks_destroyed():  # Check for win condition
            # If desired, you could implement a win reset here, e.g. print a message
            print("You Won!")
            ball.reset()
            brick_wall = BrickWall(rows = 5, cols = 10, brick_width = WIDTH // 10 - 4, brick_height = 20, padding = 5, color = RED)

        # Get the next state after taking the action
        next_state = get_state(paddle, ball)

        # Initialize the next state in Q-tables
        if next_state not in q_table1:
            q_table1[next_state] = [0, 0]
            q_table2[next_state] = [0, 0]

        # Calculate reward based on game state
        if point == 1:  # Hit brick
            reward = 1
        elif point == -1:  # Game over
            reward = -1
        else:  # Neutral
            reward = 0

        # Double Q-learning update
        if random.random() < 0.5:
            q_table1[current_state][axn] += alpha * (reward + gamma * q_table2[next_state][max(range(2), key=lambda x: q_table1[next_state][x])] - q_table1[current_state][axn])
        else:
            q_table2[current_state][axn] += alpha * (reward + gamma * q_table1[next_state][max(range(2), key=lambda x: q_table2[next_state][x])] - q_table2[current_state][axn])

        paddle.display()
        ball.display()
        brick_wall.draw(screen)
        paddle.displayScore("Score: ", brick_wall.score, 50, HEIGHT - 20, BLACK)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
pygame.quit()

# pretty good results at 130-160 episodes and onwards
