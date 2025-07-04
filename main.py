import pygame
from sys import exit
import random
import time

pygame.init()


# --- Cell class ---
class Cell:
    def __init__(self):
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False


# --- Player class ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.row = ROWS - 1
        self.col = 0

        self.image = pygame.image.load("transplayer.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

        self.rect = self.image.get_rect()
        self.won = False
        self.rect.topleft = (self.col * CELL_SIZE, self.row * CELL_SIZE)

        self.trail = [{"row": ROWS - 1, "col": 0, "time": time.time()}]
        self.steps = 0

    def update(self):
        speed = 0.2
        target_x = self.col * CELL_SIZE
        target_y = self.row * CELL_SIZE

        self.rect.x += (target_x - self.rect.x) * speed
        self.rect.y += (target_y - self.rect.y) * speed

    def move(self, move_x, move_y):
        if not (self.row == 0 and self.col == COLS - 1):
            self.row += move_y
            self.col += move_x
            self.trail.append({"row": self.row, "col": self.col, "time": time.time()})
            self.steps += 1
        else:
            self.won = True


# --- Screen and grid setup ---
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

ROWS, COLS = 30, 30

MAX_WIDTH = int(SCREEN_WIDTH * 0.8)
MAX_HEIGHT = int(SCREEN_HEIGHT * 0.8)

CELL_SIZE_W = MAX_WIDTH // COLS
CELL_SIZE_H = MAX_HEIGHT // ROWS

CELL_SIZE = min(CELL_SIZE_W, CELL_SIZE_H)

WIDTH, HEIGHT, FPS = CELL_SIZE * COLS, CELL_SIZE * ROWS, 60

# --- Color themes ---
themes = [
    {"bg": (30, 30, 30), "wall": (240, 240, 240)},
    {"bg": (10, 0, 30), "wall": (255, 0, 200)},
    {"bg": (0, 30, 0), "wall": (0, 255, 0)},
    {"bg": (70, 20, 0), "wall": (255, 140, 0)},
    {"bg": (0, 0, 0), "wall": (0, 255, 255)},
]

theme_index = 0
BACKGROUND_COLOR = themes[theme_index]["bg"]
WALL_COLOR = themes[theme_index]["wall"]

# --- Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

clock = pygame.time.Clock()

maze = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]


# --- Maze Generation ---
def get_random_neighbour(cell):
    neighbours = {}
    row, col = cell

    if row > 0 and not maze[row - 1][col].visited:
        neighbours["top"] = (row - 1, col)
    if col < COLS - 1 and not maze[row][col + 1].visited:
        neighbours["right"] = (row, col + 1)
    if row < ROWS - 1 and not maze[row + 1][col].visited:
        neighbours["bottom"] = (row + 1, col)
    if col > 0 and not maze[row][col - 1].visited:
        neighbours["left"] = (row, col - 1)
    return random.choice(list(neighbours.items())) if neighbours else None


def backtracker(stack):
    while stack:
        current_pos = stack[-1]
        result = get_random_neighbour(current_pos)
        if result:
            neighbour_dir, neighbour_pos = result
            current_cell = maze[current_pos[0]][current_pos[1]]
            neighbour_cell = maze[neighbour_pos[0]][neighbour_pos[1]]

            match neighbour_dir:
                case "top":
                    current_cell.walls["top"] = False
                    neighbour_cell.walls["bottom"] = False
                case "right":
                    current_cell.walls["right"] = False
                    neighbour_cell.walls["left"] = False
                case "bottom":
                    current_cell.walls["bottom"] = False
                    neighbour_cell.walls["top"] = False
                case "left":
                    current_cell.walls["left"] = False
                    neighbour_cell.walls["right"] = False

            neighbour_cell.visited = True
            stack.append(neighbour_pos)
        else:
            stack.pop()


def generate_maze():
    for row in maze:
        for cell in row:
            cell.visited = False
            cell.walls = {"top": True, "right": True, "bottom": True, "left": True}
    maze[0][0].visited = True
    backtracker([(0, 0)])


generate_maze()

goal_image = pygame.image.load("goal.png")
goal_image = pygame.transform.scale(goal_image, (CELL_SIZE, CELL_SIZE))

player = Player()
player_group = pygame.sprite.GroupSingle(player)

show_instructions = True
show_steps = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                show_instructions = False
            if event.key in [
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
            ]:
                theme_index = int(event.unicode) - 1
                BACKGROUND_COLOR = themes[theme_index]["bg"]
                WALL_COLOR = themes[theme_index]["wall"]
            if event.key == pygame.K_r:
                player.steps = 0
                player.row, player.col = ROWS - 1, 0
                player.trail = [{"row": ROWS - 1, "col": 0, "time": time.time()}]
                player.won = False
                generate_maze()
            if not show_instructions:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    row, col = player.row, player.col
                    if not maze[row][col].walls["right"]:
                        player.move(1, 0)
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    row, col = player.row, player.col
                    if not maze[row][col].walls["left"]:
                        player.move(-1, 0)
                if event.key in [pygame.K_UP, pygame.K_w]:
                    row, col = player.row, player.col
                    if not maze[row][col].walls["top"]:
                        player.move(0, -1)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    row, col = player.row, player.col
                    if not maze[row][col].walls["bottom"]:
                        player.move(0, 1)
            if event.key == pygame.K_t:
                show_steps = not show_steps

    screen.fill(BACKGROUND_COLOR)

    trail_life = 5.0
    for cell in player.trail[:-1]:
        age = time.time() - cell["time"]
        if age < trail_life:
            alpha = max(0, 200 - int((age / trail_life) * 200))
            trail_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            trail_surface.fill((255, 215, 0, alpha))
            screen.blit(
                trail_surface, (cell["col"] * CELL_SIZE, cell["row"] * CELL_SIZE)
            )

    if player.trail:
        current = player.trail[-1]
        square_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        square_surface.fill((255, 255, 255, 255))
        screen.blit(
            square_surface, (current["col"] * CELL_SIZE, current["row"] * CELL_SIZE)
        )

    for row in range(ROWS):
        for col in range(COLS):
            if row == 0 and col == COLS - 1:
                screen.blit(goal_image, (col * CELL_SIZE, row * CELL_SIZE))

            cell = maze[row][col]
            x, y = col * CELL_SIZE, row * CELL_SIZE

            if cell.walls["top"]:
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x + CELL_SIZE, y), 2)
            if cell.walls["right"]:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE, y + CELL_SIZE),
                    2,
                )
            if cell.walls["bottom"]:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    (x + CELL_SIZE, y + CELL_SIZE),
                    (x, y + CELL_SIZE),
                    2,
                )
            if cell.walls["left"]:
                pygame.draw.line(screen, WALL_COLOR, (x, y + CELL_SIZE), (x, y), 2)

    if player.won:
        modal = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 4)
        pygame.draw.rect(screen, (255, 255, 255), modal, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), modal, 3, border_radius=15)
        font = pygame.font.SysFont(None, 48)
        text = font.render("You Won!", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=modal.center))

    if show_instructions:
        modal = pygame.Rect(WIDTH // 6, HEIGHT // 4, WIDTH * 2 // 3, HEIGHT // 2)
        pygame.draw.rect(screen, (255, 255, 255), modal, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), modal, 3, border_radius=15)

        font = pygame.font.SysFont(None, 24)
        lines = [
            "Arrow keys or WASD to move",
            "Reach the goal (top right) to win",
            "Press R to restart",
            "Press 1-5 to change color scheme",
            "Press T to toggle step counter",
            "Press ESC to quit",
            "Press SPACE to close these instructions",
        ]

        for i, line in enumerate(lines):
            txt = font.render(line, True, (0, 0, 0))
            screen.blit(txt, (modal.x + 30, modal.y + 30 + i * 35))

    player_group.update()
    player_group.draw(screen)

    if show_steps:
        font = pygame.font.SysFont(None, 32)
        steps_text = font.render(f"Steps: {player.steps}", True, (255, 255, 255))

        text_rect = steps_text.get_rect(topleft=(20, 20))
        bg_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
        screen.blit(steps_text, text_rect)

    pygame.display.update()
    clock.tick(FPS)
