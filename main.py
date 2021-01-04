import pygame
import time
import random
from pygame.locals import *

SIZE = 40 #Snake BLock Size

# Class Apple to draw an apple on the screen.
class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        # self.parent_screen.fill((110, 110, 5))
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 11) * SIZE

#Class Snake to define and draw sanke on the screen.
class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.dir = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.dir == 'down':
            self.y[0] += SIZE
        if self.dir == 'up':
            self.y[0] -= SIZE
        if self.dir == 'left':
            self.x[0] -= SIZE
        if self.dir == 'right':
            self.x[0] += SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.dir = 'left'

    def move_right(self):
        self.dir = 'right'

    def move_up(self):
        self.dir = 'up'

    def move_down(self):
        self.dir = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

#Class Game to start the game screen and draw snake and apple over it.
class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 500))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load("resources/bgm.wav")
        pygame.mixer.music.play(loops = -1)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.wav")
        elif sound_name == "ding":
            sound = pygame.mixer.Sound("resources/ding.wav")

        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    #Snake collision with Apple (Eating the apple).
    def is_collide(self,x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #Snake eating apple.
        if self.is_collide(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            # sound = pygame.mixer.Sound("resources/ding.wav")
            # pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        # Snake collision with itself.
        for i in range(3, self.snake.length):
            if self.is_collide(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                # sound = pygame.mixer.Sound("resources/crash.wav")
                # pygame.mixer.Sound.play(sound)
                raise Exception("Game Over")

    def show_game_over(self):
        self.render_background()
        self.surface.fill((110, 110, 5))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over..! Your Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255,255,255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()


    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if event.key == pygame.K_RIGHT:
                        self.snake.move_right()

                    if event.key == pygame.K_LEFT:
                        self.snake.move_left()

                    if event.key == pygame.K_UP:
                        self.snake.move_up()

                    if event.key == pygame.K_DOWN:
                        self.snake.move_down()

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.25)


if __name__ == "__main__":
    game = Game()
    game.run()