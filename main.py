import pygame
import random

# Initializing Pygame
pygame.init()
# Initializing surface
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

infoObject = pygame.display.Info()


class Piece:
    def __init__(self, type, rotation):
        self.type = type
        self.grid = [[0 for x in range(4)] for y in range(4)]
        self.color = (0, 0, 0)
        self.set_piece()
        self.rotate_piece(rotation)

    def set_piece(self):
        if self.type == 1:
            self.grid = [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
            self.color = (0, 255, 255)
        elif self.type == 2:
            self.grid = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
            self.color = (0, 100, 0)
        elif self.type == 3:
            self.grid = [[0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0]]
            self.color = (238, 201, 0)
        elif self.type == 4:
            self.grid = [[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
            self.color = (220, 20, 60)
        elif self.type == 5:
            self.grid = [[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]]
            self.color = (127, 255, 0)
        elif self.type == 6:
            self.grid = [[0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]]
            self.color = (238, 106, 167)
        elif self.type == 7:
            self.grid = [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
            self.color = (238, 230, 133)

    def rotate_piece(self, rotation):
        for i in range(rotation):
            self.rotate()

    def rotate(self):
        temp_grid = [[0 for x in range(4)] for y in range(4)]
        for i in range(4):
            for j in range(4):
                temp_grid[j][3 - i] = self.grid[i][j]
        self.grid = temp_grid


class Tetris:
    def __init__(self, level):
        self.HEIGHT = 20
        self.WIDTH = 10
        self.box_size = 40
        self.box_margin = 2
        self.level_index = 60
        self.empty_box_color = (20, 20, 20)
        self.filled_box_color = (80, 80, 80)
        self.grid = [[0 for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
        self.initialize_grid(level)

    def new_piece(self, piece):
        temp, skip = (0,) * 2
        for i in range(len(piece.grid)):
            for j in range(len(piece.grid[i])):
                temp += piece.grid[i][j]
            if temp == 0:
                skip += 1
            else:
                for j in range(len(piece.grid[i])):
                    self.grid[i-skip][j+3] = (False, self.empty_box_color) if piece.grid[i][j] == 0 else (True, piece.color)
        self.slim_piece(piece)

    def slim_piece(self, piece):
        up, down, right, left, temp_up, temp_down, temp_right, temp_left = (0,) * 8
        for i in range(len(piece.grid)):
            for j in range(len(piece.grid[i])):
                temp_up += 1 if piece.grid[i][j] != 0 else 0
                temp_down += 1 if piece.grid[3 - i][j] != 0 else 0
                temp_left += 1 if piece.grid[j][i] != 0 else 0
                temp_right += 1 if piece.grid[j][3 - i] != 0 else 0
            up += 1 if temp_up == 0 else 0
            down += 1 if temp_down == 0 else 0
            left += 1 if temp_left == 0 else 0
            right += 1 if temp_right == 0 else 0

        temp_grid = [[0 for x in range(4 - (left + right))] for y in range(4 - (up + down))]
        x = 0
        for i in range(len(piece.grid)):
            if up <= i <= 3 - down:
                y = 0
                for j in range(len(piece.grid[i])):
                    if left <= j <= 3 - right:
                        temp_grid[x][y] = piece.grid[i][j]
                        y += 1
                x += 1
        # print("slim up", up, "down", down, "left", left, "right", right)
        # print(temp_grid)
        return temp_grid

    def initialize_grid(self, level):
        x = 0
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if i >= self.HEIGHT - level:
                    x = random.randint(0, 100)
                if x > 100 - self.level_index:
                    self.grid[i][j] = (True, self.filled_box_color)
                else:
                    self.grid[i][j] = (False, self.empty_box_color)

    def refresh_board(self):
        pygame.draw.rect(win, (150, 0, 0),
                         pygame.Rect(
                             (infoObject.current_w / 2) - (((self.box_size + self.box_margin) * self.WIDTH / 2) + 6),
                             (infoObject.current_h / 2) - (((self.box_size + self.box_margin) * self.HEIGHT / 2) + 6),
                             ((self.box_size + self.box_margin) * self.WIDTH) + 10,
                             ((self.box_size + self.box_margin) * self.HEIGHT) + 10))
        pygame.draw.rect(win, (0, 0, 0),
                         pygame.Rect(
                             (infoObject.current_w / 2) - (((self.box_size + self.box_margin) * self.WIDTH / 2) + 4),
                             (infoObject.current_h / 2) - (((self.box_size + self.box_margin) * self.HEIGHT / 2) + 4),
                             ((self.box_size + self.box_margin) * self.WIDTH) + 6,
                             ((self.box_size + self.box_margin) * self.HEIGHT) + 6))

        for j in range(self.HEIGHT):
            for i in range(self.WIDTH):
                pygame.draw.rect(win, self.grid[j][i][1],
                                 pygame.Rect((infoObject.current_w / 2) - ((self.box_size + self.box_margin)
                                                                           * self.WIDTH / 2) + (
                                                         i * (self.box_size + self.box_margin)),
                                             (infoObject.current_h / 2) - ((self.box_size + self.box_margin)
                                                                           * self.HEIGHT / 2) + (
                                                         j * (self.box_size + self.box_margin)),
                                             self.box_size, self.box_size))
        pygame.display.flip()


myTetris = Tetris(6)
alive = True
while alive:

    myTetris.refresh_board()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('Left')
            elif event.key == pygame.K_RIGHT:
                print('Right')
            elif event.key == pygame.K_UP:
                print('Up')
            elif event.key == pygame.K_DOWN:
                print('Down')
            elif event.key == pygame.K_z:
                myTetris.new_piece(Piece(random.randint(1, 7), random.randint(0, 3)))
            elif event.key == pygame.K_q:
                alive = False

pygame.quit()
