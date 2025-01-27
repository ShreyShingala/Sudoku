import pygame as pg
from solver import solve, valid_checker, find_empty
import random
import requests

def randomize_board(setting):
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    if setting == 0:
        return board
    elif setting == 1: # easy mode
        # Get a medium board first
        medium_board = randomize_board(2)
        
        revealed = 0
        
        for i in range(9):
            for j in range(9):
                if medium_board[i][j] != 0:
                    board[i][j] = medium_board[i][j]
                    revealed += 1
        
        solve(medium_board)
        
        while revealed < 40:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if board[row][col] == 0:
                board[row][col] = medium_board[row][col]
                revealed += 1
                
        return board
         
    elif setting == 2: #medium
        while True:
            response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
            
            if response.status_code == 200:
                data = response.json()
                difficulty = data['newboard']['grids'][0]['difficulty']
                if difficulty == 'Medium':
                    board = data['newboard']['grids'][0]['value']
                    return board
            else:
                raise Exception("Failed to fetch Sudoku board")
                break
        
    elif setting == 3: #hard;
        while True:
            response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
            
            if response.status_code == 200:
                data = response.json()
                difficulty = data['newboard']['grids'][0]['difficulty']
                if difficulty == 'Hard':
                    board = data['newboard']['grids'][0]['value']
                    return board
            else:
                raise Exception("Failed to fetch Sudoku board")
                break
   
class Grid:
    def __init__(self, board):
        self.size = 60
        self.board = board
        self.solved_board = [row[:] for row in board]  # Copy the board
        solve(self.solved_board)  # Solve the copied board
        self.rows = len(board)
        self.cols = len(board[0])
        self.blocks = [[Block(i, j, self.board[i][j]) for j in range(self.cols)] for i in range(self.rows)]
        self.selected_block = None
        self.gameover = False
        self.solvedtime = None
        self.totalmistakes = 0
        self.start_time = pg.time.get_ticks()  # Store the start time
        self.exist = False
        
        for row in self.blocks:
            for block in row:
                if block.value != 0:
                    block.lockedin = True
                    
        grid_width = self.cols * self.size
        grid_height = self.rows * self.size
        offset_x = (Screen_Width - grid_width) // 2
        offset_y = (Screen_Height - grid_height) // 2
        for i in range(self.rows):
            for j in range(self.cols):
                block = self.blocks[i][j]
                x = j * self.size + offset_x
                y = i * self.size + offset_y
                block.cordx = x
                block.cordy = y
    
    def draw(self):
        grid_width = self.cols * self.size
        grid_height = self.rows * self.size
        offset_x = (Screen_Width - grid_width) // 2
        offset_y = (Screen_Height - grid_height) // 2

        for i in range(self.rows):
            for j in range(self.cols):
                block = self.blocks[i][j]
                x = j * self.size + offset_x
                y = i * self.size + offset_y
                pg.draw.rect(screen, (255, 255, 255), (x, y, self.size, self.size))  # Draw white square
                
                if block.selected:
                    pg.draw.rect(screen, (0, 255, 0), (x, y, self.size, self.size))  # Draw green square if selected
                if block.temp != 0:
                    text = font.render(str(block.temp), True, (128, 128, 128))
                    text_rect = text.get_rect(bottomright=(x + self.size - 35, y + self.size -3))
                    screen.blit(text, text_rect)
                    
                pg.draw.rect(screen, (0, 0, 0), (x, y, self.size, self.size), 1)  # Draw black border
                
                if block.value != 0:
                    text = font.render(str(block.value), True, (0, 0, 0))
                    screen.blit(text, (x + self.size//2 - 10, y + self.size//2 - 15))
                
                if j % 3 == 0 and j != 0:
                    pg.draw.line(screen, (0, 0, 0), (j * self.size + offset_x, offset_y), (j * self.size + offset_x, grid_height + offset_y), 5)
                    
            if i % 3 == 0 and i != 0: 
                pg.draw.line(screen, (0, 0, 0), (offset_x, i * self.size + offset_y), (grid_width + offset_x, i * self.size + offset_y), 5)
           
        if self.exist == False:
            if self.gameover == False:         
                text = font.render("Time Taken:", True, (0, 0, 0))
            else:
                text = font.render("Solved In:", True, (0, 0, 0))
            timex = Screen_Width - offset_x + self.size
            timey = offset_y
            screen.blit(text, (timex, timey))
            
            if self.gameover == False:         
                elapsed_time = (pg.time.get_ticks() - self.start_time) // 1000  # Calculate elapsed time
                text = large_font.render(str(elapsed_time) + "s", True, (0, 0, 0))
            else:
                text = large_font.render(str(self.solvedtime) + "s", True, (0, 0, 0))
            timex = Screen_Width - offset_x + self.size
            timey = offset_y + 40
            screen.blit(text, (timex, timey))
            
            mistakes_text = font.render("Total Mistakes:", True, (0, 0, 0))
            mistakes_x = Screen_Width - offset_x + self.size
            mistakes_y = offset_y + 150
            screen.blit(mistakes_text, (mistakes_x, mistakes_y))
            
            mistakes_count = large_font.render(str(self.totalmistakes), True, (0, 0, 0))
            mistakes_count_x = Screen_Width - offset_x + self.size
            mistakes_count_y = offset_y + 190
            screen.blit(mistakes_count, (mistakes_count_x, mistakes_count_y))
        
    def determine_selection(self, x, y):
        grid_width = self.cols * self.size
        grid_height = self.rows * self.size
        offset_x = (Screen_Width - grid_width) // 2
        offset_y = (Screen_Height - grid_height) // 2

        if (x >= offset_x and x <= grid_width + offset_x) and (y >= offset_y and y <= grid_height + offset_y):
            row = (y - offset_y) // self.size
            col = (x - offset_x) // self.size
            if (row >= self.rows or col >= self.cols):
                return
            temp = self.blocks[int(row)][int(col)]
            if temp.lockedin:
                return
            if self.selected_block:
                self.selected_block.selected = False
                self.selected_block = temp
                self.selected_block.selected = True
            else:
                self.selected_block = temp
                self.selected_block.selected = True
                
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    return False
        
        self.solvedtime = (pg.time.get_ticks() - self.start_time) // 1000  # Calculate solved time
        return True
    
    def test_right(self):
        if self.selected_block and self.gameover == False:
            y = self.selected_block.y
            x = self.selected_block.x
            if self.selected_block.temp != 0:
                if self.selected_block.temp == self.solved_board[x][y]:
                    self.board[x][y] = self.selected_block.temp
                    self.selected_block.value = self.selected_block.temp
                    self.selected_block.temp = 0
                    self.selected_block.lockedin = True
                    self.selected_block.selected = False
                    self.selected_block = None
                else:
                    self.totalmistakes += 1

        if self.is_finished():
            self.gameover = True
            self.solvedtime = (pg.time.get_ticks() - self.start_time) // 1000  # Calculate solved time
    
    def solver(self):
        screen.fill(bg)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.blocks[i][j].value == 0:
                    self.blocks[i][j].temp = 0
                    self.blocks[i][j].selected = False
                    self.blocks[i][j].lockedin = False
        
        startpoint = find_empty(self.board)
        
        if not startpoint:
            return True
        else:
            row, col = startpoint
            
        for i in range(1, 10):
            if valid_checker(self.board, i, (row, col)):
                self.board[row][col] = i
                self.blocks[row][col].value = i
                self.blocks[row][col].selected = True
                self.blocks[row][col].lockedin = True
                self.draw()
                pg.display.update()
                if self.exist == False:
                    pg.time.delay(75)
                else:
                    pg.time.delay(25)
                
                if self.solver():
                    return True
                
                self.board[row][col] = 0
                self.blocks[row][col].value = 0
                self.blocks[row][col].selected = False
                self.blocks[row][col].lockedin = False  # Ensure lockedin is reset
                self.draw()
                pg.display.update()
                if self.exist == False:
                    pg.time.delay(75)
                else:
                    pg.time.delay(25)
    
        self.gameover = True
        self.solvedtime = (pg.time.get_ticks() - self.start_time) // 1000  # Calculate solved time
        return False

        

class Block:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.cordx = None
        self.cordy = None
        self.value = value
        self.selected = False
        self.lockedin = False
        self.temp = 0
        
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.hovered = False
        
    def draw(self, screen):
        color = (135, 206, 250) if self.hovered else (173, 216, 230)  # Change color on hover
        pg.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=10)  # Light blue with rounded corners
        text = small_font.render(self.text, True, (0, 0, 0))  # Smaller text
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)
        
    def check_click(self, mousex, mousey):
        if (mousex >= self.x and mousex <= self.x + self.width) and (mousey >= self.y and mousey <= self.y + self.height):
            return True
        return False
    
    def check_hover(self, mousex, mousey):
        self.hovered = (mousex >= self.x and mousex <= self.x + self.width) and (mousey >= self.y and mousey <= self.y + self.height)

class Confetti:
    def __init__(self):
        self.particles = []
        
        while len(self.particles) < 50:
            pos_x = random.randint(0, Screen_Width)
            pos_y = random.randint(0, Screen_Height // 2)
            velocity = [random.uniform(-1, 1), random.uniform(1, 3)]
            self.particles.append([pos_x, pos_y, velocity])
    
    def emit(self):
        for particle in self.particles:
            particle[0] += particle[2][0]
            particle[1] += particle[2][1]
            pg.draw.circle(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (int(particle[0]), int(particle[1])), 5)
        
        self.particles = [p for p in self.particles if p[1] < Screen_Height]

Screen_Width = 1200
Screen_Height = 700
bg = (200, 200, 200)

pg.init()
screen = pg.display.set_mode((Screen_Width, Screen_Height))
screen.fill(bg)
font = pg.font.Font(pg.font.match_font('Arial'), 32)
small_font = pg.font.Font(pg.font.match_font('Arial'), 24)  # Smaller font for buttons
large_font = pg.font.Font(pg.font.match_font('Arial'), 48)
pg.display.set_caption("Sudoku")

time = pg.time.Clock()
confetti = Confetti()

buttonlistchoose = [
    Button(500, 250, 200, 100, "Easy"),
    Button(500, 375, 200, 100, "Medium"),
    Button(500, 500, 200, 100, "Hard")
]

buttonlistintro = [
    Button(500, 250, 200, 100, "Play"),
    Button(500, 450, 200, 100, "Solve"),
]

buttonlistgame = [
    Button(50, 50, 100, 50, "Go back"),
    Button(Screen_Width // 2 - 100, Screen_Height - 70, 200, 50, "Solve for me")
]

buttonlistsolve = [
    Button(50, 50, 100, 50, "Play"),
    Button(200, 50, 100, 50, "Solve"),
    Button(350, 50, 100, 50, "How to Play")
]
choosediff = False
intro = True
gameloop = False
solvemode = False

def game():
    global intro, choosediff, gameloop, solvemode, grid
    
    mousex, mousey = pg.mouse.get_pos()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            break
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            x, y = pos[0], pos[1]
            grid.determine_selection(x, y)
            for button in buttonlistgame:
                if button.check_click(x, y):
                    if button.text == "Go back":                        
                        intro = True
                        choosediff = False
                        gameloop = False
                        solvemode = False
                        pass
                    elif button.text == "Solve for me":
                        if grid.selected_block:
                            grid.selected_block.selected = False
                            grid.selected_block = None
                        grid.solver()
                        
        if event.type == pg.KEYDOWN and grid.selected_block != None:
            if event.key == pg.K_DOWN:   
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x, block_y + grid.size)
            if event.key == pg.K_UP:
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x, block_y - grid.size)
            if event.key == pg.K_RIGHT:
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x + grid.size, block_y)
            if event.key == pg.K_LEFT:        
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x - grid.size, block_y)
            elif event.key == pg.K_1:
                grid.selected_block.temp = 1
            elif event.key == pg.K_2:
                grid.selected_block.temp = 2
            elif event.key == pg.K_3:
                grid.selected_block.temp = 3
            elif event.key == pg.K_4:
                grid.selected_block.temp = 4
            elif event.key == pg.K_5:
                grid.selected_block.temp = 5
            elif event.key == pg.K_6:
                grid.selected_block.temp = 6
            elif event.key == pg.K_7:
                grid.selected_block.temp = 7
            elif event.key == pg.K_8:
                grid.selected_block.temp = 8
            elif event.key == pg.K_9:
                grid.selected_block.temp = 9
            elif event.key == pg.K_BACKSPACE:
                grid.selected_block.temp = 0
            elif event.key == pg.K_RETURN:
                grid.test_right()

    for button in buttonlistgame:
        button.check_hover(mousex, mousey)
        button.draw(screen)
    
    grid.draw()
    if grid.gameover:
        text = large_font.render("Congratulations you finished!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(Screen_Width // 2, 50))  # Adjust position to be above the board
        screen.blit(text, text_rect)
        confetti.emit()
        
    time.tick(60)

def introduction():
    global intro, choosediff, gameloop, solvemode, grid, confetti
    
    mousex, mousey = pg.mouse.get_pos()
    
    text = large_font.render("Welcome to Sudoku", True, (0, 0, 0))
    text_rect = text.get_rect(center=(Screen_Width // 2, 100))
    screen.blit(text, text_rect)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            break
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            x, y = pos[0], pos[1]
            for button in buttonlistintro:
                if button.check_click(x, y):
                    if button.text == "Play":
                        intro = False
                        choosediff = True
                        gameloop = False
                        solvemode = False
                        pass
                    elif button.text == "Solve":
                        intro = False
                        choosediff = False
                        gameloop = False
                        solvemode = True
                        board = randomize_board(0)
                        grid = Grid(board)
                        grid.exist = True
                        confetti = Confetti()
                        
    for button in buttonlistintro:
        button.check_hover(mousex, mousey)
        button.draw(screen)
    
    time.tick(60)
    
def choose():
    global intro, choosediff, gameloop, solvemode, grid, confetti
    
    mousex, mousey = pg.mouse.get_pos()
    
    text = large_font.render("Choose Difficulty", True, (0, 0, 0))
    text_rect = text.get_rect(center=(Screen_Width // 2, 100))
    screen.blit(text, text_rect)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            break
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            x, y = pos[0], pos[1]
            for button in buttonlistchoose:
                if button.check_click(x, y):
                    if button.text == "Easy":
                        board = randomize_board(1)
                        grid = Grid(board)
                        confetti = Confetti()
                        intro = False
                        choosediff = False
                        gameloop = True
                        solvemode = False
                        pass
                    elif button.text == "Medium":
                        board = randomize_board(2)
                        grid = Grid(board)
                        confetti = Confetti()
                        intro = False
                        choosediff = False
                        gameloop = True
                        solvemode = False
                        pass
                    elif button.text == "Hard":
                        board = randomize_board(3)
                        grid = Grid(board)
                        confetti = Confetti()
                        intro = False
                        choosediff = False
                        gameloop = True
                        solvemode = False
                        pass
    for button in buttonlistchoose:
        button.check_hover(mousex, mousey)
        button.draw(screen)
    
    time.tick(60)

def solveagiven():
    global intro, choosediff, gameloop, solvemode, grid
    
    mousex, mousey = pg.mouse.get_pos()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            break
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            x, y = pos[0], pos[1]
            grid.determine_selection(x, y)
            for button in buttonlistgame:
                if button.check_click(x, y):
                    if button.text == "Go back":    
                        intro = True
                        choosediff = False
                        gameloop = False
                        solvemode = False
                    elif button.text == "Solve for me":
                        if grid.selected_block:
                            grid.selected_block.selected = False
                            grid.selected_block = None
                        grid.solver()
                        
        if event.type == pg.KEYDOWN and grid.selected_block != None:
            if event.key == pg.K_DOWN:   
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x, block_y + grid.size)
            if event.key == pg.K_UP:
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x, block_y - grid.size)
            if event.key == pg.K_RIGHT:
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x + grid.size, block_y)
            if event.key == pg.K_LEFT:        
                block_x = grid.selected_block.cordx
                block_y = grid.selected_block.cordy
                grid.determine_selection(block_x - grid.size, block_y)
            elif event.key == pg.K_1:
                if valid_checker(grid.board, 1, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 1
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 1
            elif event.key == pg.K_2:
                if valid_checker(grid.board, 2, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 2
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 2
            elif event.key == pg.K_3:
                if valid_checker(grid.board, 3, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 3
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 3
            elif event.key == pg.K_4:
                if valid_checker(grid.board, 4, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 4
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 4
            elif event.key == pg.K_5:
                if valid_checker(grid.board, 5, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 5
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 5
            elif event.key == pg.K_6:
                if valid_checker(grid.board, 6, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 6
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 6
            elif event.key == pg.K_7:
                if valid_checker(grid.board, 7, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 7
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 7
            elif event.key == pg.K_8:
                if valid_checker(grid.board, 8, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 8
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 8
            elif event.key == pg.K_9:
                if valid_checker(grid.board, 9, (grid.selected_block.x, grid.selected_block.y)):
                    grid.selected_block.value = 9
                    grid.board[grid.selected_block.x][grid.selected_block.y] = 9
            elif event.key == pg.K_BACKSPACE:
                grid.selected_block.value = 0
                grid.board[grid.selected_block.x][grid.selected_block.y] = 0

    for button in buttonlistgame:
        button.check_hover(mousex, mousey)
        button.draw(screen)
    
    grid.draw()
    if grid.gameover:
        text = large_font.render("Program Solved It!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(Screen_Width // 2, 50))  # Adjust position to be above the board
        screen.blit(text, text_rect)
        confetti.emit()

def main_loop():
    while True: 
        screen.fill(bg)
        if intro:
            introduction()
        elif choosediff:
            choose()
        elif gameloop:
            game()
        elif solvemode:
            solveagiven()
            
        pg.display.update()
        time.tick(60)

if __name__ == "__main__":
    main_loop()
