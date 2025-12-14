import pygame
import sys

# Constants
WIDTH = 540
HEIGHT = 600
GRID_SIZE = WIDTH // 9
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (200, 220, 255)

screen = None
clock = None
font = None
small_font = None

def draw_grid(board, original_board, current_cell=None):
    screen.fill(WHITE)
    
    for i in range(9):
        for j in range(9):
            x = j * GRID_SIZE
            y = i * GRID_SIZE
            
            if current_cell and current_cell == (i, j):
                pygame.draw.rect(screen, LIGHT_BLUE, (x, y, GRID_SIZE, GRID_SIZE))
            
            if board[i][j] != 0:
                color = BLACK if original_board[i][j] != 0 else BLUE
                text = font.render(str(board[i][j]), True, color)
                text_rect = text.get_rect(center=(x + GRID_SIZE // 2, y + GRID_SIZE // 2))
                screen.blit(text, text_rect)
    
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, WIDTH), thickness)
    
    status_text = small_font.render("Solving...", True, BLACK)
    screen.blit(status_text, (10, HEIGHT - 50))
    
    pygame.display.flip()

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    
    for x in range(9):
        if board[x][col] == num:
            return False
    
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    
    return True

def solve_sudoku(board, original_board, delay=50):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        draw_grid(board, original_board, (i, j))
                        pygame.time.delay(delay)
                        
                        if solve_sudoku(board, original_board, delay):
                            return True
                        
                        board[i][j] = 0
                        draw_grid(board, original_board, (i, j))
                        pygame.time.delay(delay)
                
                return False
    return True

def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j], end=" ")
        print()

def draw_input_grid(board, selected_cell=None):
    """Draw grid for user input"""
    screen.fill(WHITE)
    
    for i in range(9):
        for j in range(9):
            x = j * GRID_SIZE
            y = i * GRID_SIZE
            
            if selected_cell and selected_cell == (i, j):
                pygame.draw.rect(screen, LIGHT_BLUE, (x, y, GRID_SIZE, GRID_SIZE))
            
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(x + GRID_SIZE // 2, y + GRID_SIZE // 2))
                screen.blit(text, text_rect)
    
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, WIDTH), thickness)
    
    instruction_text = small_font.render("Click cells and type 1-9." + " " * 10 + "Press ENTER to solve. ", True, BLACK)
    screen.blit(instruction_text, (10, HEIGHT - 50))
    
    pygame.display.flip()

def get_user_input():
    """Interactive pygame input for sudoku puzzle"""
    board = [[0 for _ in range(9)] for _ in range(9)]
    selected_cell = None
    running = True
    
    while running:
        draw_input_grid(board, selected_cell)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < WIDTH:  
                    col = x // GRID_SIZE
                    row = y // GRID_SIZE
                    selected_cell = (row, col)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return board
                
                elif selected_cell and event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, 
                                                      pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, 
                                                      pygame.K_8, pygame.K_9]:
                    row, col = selected_cell
                    num = int(event.unicode)
                    board[row][col] = num
                
                elif selected_cell and event.key == pygame.K_BACKSPACE:
                    row, col = selected_cell
                    board[row][col] = 0
                
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    return board

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver - Enter Puzzle")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

print("Enter your sudoku puzzle in the pygame window...")
print("Click cells and type numbers 1-9 (or 0 to clear)")
print("Press ENTER when done to start solving")
board = get_user_input()

print("\nOriginal Sudoku:")
print_board(board)

original_board = [row[:] for row in board]

pygame.display.set_caption("Sudoku Solver - Solving...")

draw_grid(board, original_board)
pygame.time.delay(2000)

delay = 5
running = True
solved = False

print("\nStarting solver...")
if solve_sudoku(board, original_board, delay):
    print("Solved!")
    solved = True
    screen.fill(WHITE)
    draw_grid(board, original_board)
    success_text = font.render("Solved!", True, GREEN)
    screen.blit(success_text, (WIDTH // 2 - 60, HEIGHT - 45))
    pygame.display.flip()
else:
    print("No solution exists")
    screen.fill(WHITE)
    draw_grid(board, original_board)
    error_text = font.render("No Solution!", True, RED)
    screen.blit(error_text, (WIDTH // 2 - 100, HEIGHT - 45))
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(FPS)

pygame.quit()