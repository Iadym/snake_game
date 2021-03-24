import sys
import pygame
import random

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 640

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)

class Window():
    def __init__(self, window):
        self.window = window

    def draw_stage(self):
        self.window.fill(BLACK_COLOR)

    def draw_snake(self, game, snake_body):
        for pixel in snake_body:
            game.draw.rect(self, GREEN_COLOR, game.Rect(pixel[0], pixel[1], 10, 10))

    def draw_food(self, game, food):
        game.draw.rect(self, BLUE_COLOR, game.Rect(food[0], food[1], 8, 8))

    def draw_score(self, game, score):
        SCORE_FONT = game.font.SysFont('Times New Roman', 20)
        score_surface = SCORE_FONT.render(f'Score: ${score}', True, WHITE_COLOR)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (WINDOW_WIDTH // 2, 20)
        self.window.blit(score_surface, score_rect)

    def draw_game_over(self, game, exit_game):
        FINAL_FONT = game.font.SysFont('Comic Sans', 50)
        final_surface = FINAL_FONT.render('GAME OVER', True, RED_COLOR)
        final_rect = final_surface.get_rect()
        final_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.window.fill(BLACK_COLOR)
        self.window.blit(final_surface, final_rect)
        exit_game()

class Snake:
    def __init__(self):
        self.snake_head = [100, 50]
        self.snake_direction = 'RIGHT'
        self.snake_body = [
            self.snake_head,
            [self.snake_head[0] - 10, self.snake_head[1]],
            [self.snake_head[0] - 20, self.snake_head[1]]
        ]

    def snake_change_direction(self, new_direction: str):
        if new_direction == self.snake_direction:
            return
        if self.snake_direction == 'DOWN' and new_direction == 'UP':
            return
        if self.snake_direction == 'UP' and new_direction == 'DOWN':
            return
        if self.snake_direction == 'RIGHT' and new_direction == 'LEFT':
            return
        if self.snake_direction == 'LEFT' and new_direction == 'RIGHT':
            return
        self.snake_direction = new_direction

    def snake_move(self):
        if self.snake_direction == 'UP':
            new_snake_head = [self.snake_head[0], self.snake_head[1] + 10]
        if self.snake_direction == 'DOWN':
            new_snake_head = [self.snake_head[0], self.snake_head[1] - 10]
        if self.snake_direction == 'RIGHT':
            new_snake_head = [self.snake_head[0] + 10, self.snake_head[1]]
        if self.snake_direction == 'LEFT':
            new_snake_head = [self.snake_head[0] - 10, self.snake_head[1]]
        self.snake_body.insert(0, new_snake_head)
        self.snake_body.pop()

    def snake_grow(self):
        self.snake_body.insert(0, self.snake_head)
        self.snake_move()

class Food:
    def __init__(self):
        self.position = [100, 100]

    def food_respawn(self):
        self.position = [random.randrange(1, WINDOW_WIDTH // 10) * 10,
                         random.randrange(1, WINDOW_HEIGHT // 10) * 10]

class Score:
    def __init__(self):
        self.score = 0

    def increase(self):
        self.score += 10

class Game:
    def __init__(self):
        # initializing all the Game objects
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        # initializing game vars
        self.game = pygame
        self.game.init()
        self.game.display.set_caption('Snake')
        # making the game window appeared on the screen
        self.window = Window(self.game.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT)))

    def run(self):
        self.make_snake_turn()
        self.window.draw_stage()
        self.window.draw_snake()
        self.window.draw_food()
        self.window.draw_score()
        self.window.draw_game_over()
        self.game.display.update()
        self.food_control()

    def exit_game(self):
        self.game.quit()
        sys.exit()

    # checking if snake ate and if so, the food will reappear and score will be increased!
    def food_control(self):
        self.snake.snake_move()
        if self.snake.snake_head[0] == self.food.position[0] and self.snake.snake_head[1] == self.food.position[1]:
            self.snake.snake_grow()
            self.food.food_respawn()
            self.score.increase()

    def make_snake_turn(self):
        while True:
            for event in self.game.event.get():
                if event.type == self.game.QUIT or event.type == self.game.K_ESCAPE:
                    self.exit_game()
                elif event.type == self.game.K_DOWN or event.type == self.game.K_s:
                    self.snake.snake_change_direction('DOWN')
                elif event.type == self.game.K_UP or event.type == self.game.K_n:
                    self.snake.snake_change_direction('UP')
                elif event.type == self.game.K_RIGHT or event.type == self.game.K_e:
                    self.snake.snake_change_direction('RIGHT')
                elif event.type == self.game.K_LEFT or event.type == self.game.K_w:
                    self.snake.snake_change_direction('LEFT')

    def game_over(self):
        #snake head running into the borders of the window
        if self.snake.snake_head[0] < 0 or self.snake.snake_head[0] > WINDOW_WIDTH:
            self.window.draw_game_over(self.game, self.exit_game)
        if self.snake.snake_head[1] < 0 or self.snake.snake_head[1] > WINDOW_HEIGHT:
            self.window.draw_game_over(self.game, self.exit_game)

        #snake is running into itself
        for block in self.snake.snake_body[1:]:
            if block[0] == self.snake.snake_head[0] and block[1] == self.snake.snake_head[1]:
                self.window.draw_game_over(self.game, self.exit_game)