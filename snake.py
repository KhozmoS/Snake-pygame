import pygame, random, sys, time, os
from pygame.locals import *

# CONSTANTS
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
SQUARESIDE = 25
UPDIRECT = 8
DOWNDIRECT = 2
RIGHTDIRECT = 6
LEFTDIRECT = 4

pygame.init()
pygame.mixer.init()
hitted = pygame.mixer.Sound(os.path.join('assets', 'hit32.mp3.flac'))
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Snake by KhozmoS")

try:
    snackImage = pygame.image.load(os.path.join('assets', 'egg.png'))
    snackImage = pygame.transform.scale(snackImage, (SQUARESIDE, SQUARESIDE))
except:
    pass


def initializeSurface():
    pos = 0
    while pos < WINDOWHEIGHT and pos < WINDOWWIDTH:
        pygame.draw.line(windowSurface, WHITE, (0, pos), (WINDOWHEIGHT, pos))
        pygame.draw.line(windowSurface, WHITE, (pos, 0), (pos, WINDOWWIDTH))
        pos += SQUARESIDE


class Square:
    def __init__(self, left, top, clr):
        self.square = pygame.Rect(left, top, SQUARESIDE, SQUARESIDE)
        self.color = clr


class SquareSnake(Square):
    direct = RIGHTDIRECT


class Snake:
    def __init__(self):
        self.body = [SquareSnake(9 * SQUARESIDE, 9 * SQUARESIDE, GREEN)]

    def paint(self):
        for sq in self.body:
            pygame.draw.rect(windowSurface, sq.color, sq.square)
        for sq in self.body:
            pygame.draw.rect(windowSurface, (0, 255, 0), (sq.square.left+3, sq.square.top+3,
                                                          SQUARESIDE-6, SQUARESIDE-6))

    def gameover(self):
        if self.body[0].square.left < 0 or self.body[0].square.top < 0:
            return True
        if self.body[0].square.left >= WINDOWWIDTH or self.body[0].square.top >= WINDOWHEIGHT:
            return True
        for i in range(1, len(self.body)):
            if self.body[0].square.colliderect(self.body[i].square):
                return True
        return False


class SquareSnack(Square):
    def get_pos(self, snk=Snake()):
        posX = 0
        avaibles = []
        while posX < WINDOWWIDTH:
            posY = 0
            while posY < WINDOWHEIGHT:
                ok = True
                for sq in snk.body:
                    if pygame.Rect(posX, posY, SQUARESIDE, SQUARESIDE).colliderect(sq.square):
                        ok = False
                if ok:
                    avaibles.append((posX, posY))
                posY += SQUARESIDE
            posX += SQUARESIDE
        left, top = random.choice(avaibles)
        self.square = pygame.Rect(left, top, SQUARESIDE, SQUARESIDE)

    def paint(self):
        try:
            windowSurface.blit(snackImage, self.square)
        except:
            pygame.draw.rect(windowSurface, self.color, self.square)


def start():
    score = 0
    snake = Snake()
    # print(len(snake.body))
    snack = SquareSnack(0, 0, RED)
    snack.get_pos(snake)
    direction = RIGHTDIRECT
    while True:
        pygame.time.delay(50)
        mainClock.tick(11)
        changed_direct = False
        new_head = SquareSnake(snake.body[0].square.left, snake.body[0].square.top, snake.body[0].color)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if (event.key == K_DOWN or event.key == ord('s')) and direction != UPDIRECT and not changed_direct:
                    direction = DOWNDIRECT
                    changed_direct = True
                if (event.key == K_UP or event.key == ord('w')) and direction != DOWNDIRECT and not changed_direct:
                    direction = UPDIRECT
                    changed_direct = True
                if (event.key == K_LEFT or event.key == ord('a')) and direction != RIGHTDIRECT and not changed_direct:
                    direction = LEFTDIRECT
                    changed_direct = True
                if (event.key == K_RIGHT or event.key == ord('d')) and direction != LEFTDIRECT and not changed_direct:
                    direction = RIGHTDIRECT
                    changed_direct = True
        if direction == LEFTDIRECT:
            new_head.square.left -= SQUARESIDE
        if direction == RIGHTDIRECT:
            new_head.square.left += SQUARESIDE
        if direction == UPDIRECT:
            new_head.square.top -= SQUARESIDE
        if direction == DOWNDIRECT:
            new_head.square.top += SQUARESIDE
        snake.body.insert(0, new_head)

        if new_head.square.colliderect(snack.square):
            snack.get_pos(snake)
            score += 1
            pygame.mixer.music.load(os.path.join('assets', 'slime1.wav'))
            pygame.mixer.music.play(1, 0)
        else:
            snake.body.pop()
        if snake.gameover():
            hitted.play()
            mainClock.tick(2)
            return score

        windowSurface.fill(BLACK)
        snake.paint()
        snack.paint()
        initializeSurface()
        pygame.display.update()


def initialScreen():
    while True:
        highscore = open(os.path.join('assets', 'highscore.txt')).readline()
        basicFont = pygame.font.SysFont("monospace", 30, False)
        text2 = basicFont.render("High Score: "+highscore, True, WHITE, BLACK)
        text1 = basicFont.render("Press any key to get started", True, WHITE, BLACK)
        text1Rect = text1.get_rect()
        text2Rect = text2.get_rect()
        text2Rect.centerx = windowSurface.get_rect().centerx
        text2Rect.centery = windowSurface.get_rect().centery
        text1Rect.centerx = windowSurface.get_rect().centerx
        text1Rect.centery = windowSurface.get_rect().centery - text2Rect.height
        windowSurface.fill(BLACK)
        windowSurface.blit(text2, text2Rect)
        windowSurface.blit(text1, text1Rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                return True


def upd_score():
    read_file = open(os.path.join('assets', 'highscore.txt'))
    if int(read_file.read()) < score:
        write_file = open(os.path.join('assets', 'highscore.txt'), 'w')
        write_file.write(str(score))
        write_file.close()
    read_file.close()


def gameover_screen():
    upd_score()
    while True:
        basicFont = pygame.font.SysFont("monospace", 30, False)
        text1 = basicFont.render("Game Over", True, WHITE, BLACK)
        text2 = basicFont.render("Your Score: {}".format(score), True, WHITE, BLACK)
        text1Rect = text1.get_rect()
        text1Rect.centerx = windowSurface.get_rect().centerx
        text1Rect.centery = windowSurface.get_rect().centery
        text2Rect = text2.get_rect()
        text2Rect.centerx = windowSurface.get_rect().centerx
        text2Rect.centery = windowSurface.get_rect().centery + text1Rect.height
        windowSurface.fill(BLACK)
        windowSurface.blit(text1, text1Rect)
        windowSurface.blit(text2, text2Rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                return True


if __name__ == '__main__':
	while True:
		initialScreen()
		score = start()
		gameover_screen()
        

