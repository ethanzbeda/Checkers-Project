#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Color:
    
    grid_white = 'aliceblue'
    grid_black = 'grey30'
    piece_red = 'orangered4'
    piece_blue = 'steelblue4'
    high = 'forestgreen'
    king = 'goldenrod1'
    screen = 'floralwhite'
    


# In[2]:


import pygame
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)


# In[11]:


class Game:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((500,800))
        pygame.display.set_caption('Checkers')
        self.board = Board()
        self.p1 = []
        self.p2 = []
        self.p1_grave = []
        self.p2_grave = []
        self.p_names = {Color.piece_red : 'Orange Red', Color.piece_blue : 'Steel Blue'} 
        self.init_pieces()
        self.turn = 0
        self.turn_text = ""
        self.sub_text = ""
        self.turn_color = Color.piece_red
        self.show_splash()
    
    def draw(self):
        self.screen.fill(Color.screen)
        self.board.draw(self.screen)
        text = my_font.render(self.turn_text, True, self.turn_color)
        self.screen.blit(text, (20,450))
        s_text = my_font.render(self.sub_text, True, 'gray19')
        self.screen.blit(s_text, (20,500))
        pygame.display.flip()
        
        
    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 'r'
                    if event.key == pygame.K_n:
                        return 'n'
                    if event.key == pygame.K_q:
                        exit()
            self.draw()
            
    def init_pieces(self):
        self.board = Board()
        self.p1.clear()
        self.p2.clear()
        self.p1_grave.clear()
        self.p2_grave.clear()
        direction = 1
        color = Color.piece_red
        for row in range(3):
            if row % 2 == 0:
                for col in range(1,8,2):
                    self.p1.append(Piece(self.board.get_square(row,col) ,direction, color))
            else:
                for col in range(0,8,2):
                    self.p1.append(Piece(self.board.get_square(row,col) ,direction, color))
        direction = -1
        color = Color.piece_blue
        for row in range(5,8):
            if row % 2 == 0:
                for col in range(1,8,2):
                    self.p2.append(Piece(self.board.get_square(row,col) ,direction, color))
            else:
                for col in range(0,8,2):
                    self.p2.append(Piece(self.board.get_square(row,col) ,direction, color))
    
    def play_game(self):
        while len(self.p1) > 0 and len(self.p2) > 0:
            player = self.get_player()
            self.turn_text = self.p_names[player[0].color] + "'s Turn"
            self.turn_color = player[0].color
            self.play_turn(player)
            self.turn += 1
        return self.show_win()
        
    def get_player(self):
        if self.turn % 2 == 0:
            return self.p1
        return self.p2
    
    def play_turn(self, player):
        piece = None
        jumping = False
        highlight = []
        self.sub_text = 'Select a Piece'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    x = pos[0]
                    y = pos[1] 
                    square = self.board.get_squarexy(x,y)
                    # perform a move or jump
                    if square in highlight:
                        # this is True if the move is a jump
                        if max(piece.square.col, square.col) -min(piece.square.col, square.col) == 2: 
                            row = (piece.square.row + square.row) // 2
                            col = (piece.square.col + square.col) // 2
                            jump_square = self.board.get_square(row, col)
                            self.take_piece(jump_square.piece)
                            piece.move(square)
                            self.board.un_highlight(highlight)
                            highlight.clear()
                            jumps = self.get_moves(piece, jump_only = True)
                            if len(jumps) == 0:
                                return True
                            #multiple jumps available
                            else:
                                highlight = jumps
                                self.board.highlight(highlight)
                                jumping = True
                        #otherwise its a regular move
                        else:
                            piece.move(square)
                            self.board.un_highlight(highlight)
                            highlight.clear()
                            return True
                    elif square != None and square.piece in player and jumping == False:
                        self.board.un_highlight(highlight)
                        piece = square.piece
                        highlight.clear()
                        highlight = self.get_moves(piece)
                        self.board.highlight(highlight)
                    elif square != None:
                        print("misclick", square)
            if piece is None:
                self.sub_text = 'Select a Piece'
            elif jumping == True:
                self.sub_text = 'Must keep Jumping'
            else:
                self.sub_text = 'Click a Highlighted Square'
            self.draw()   
            
    def take_piece(self, piece):
        if piece in self.p1:
            piece.square.piece = None
            self.p1.remove(piece)
            piece.move(self.board.get_grave(piece.color))
            self.p1_grave.append(piece)
        elif piece in self.p2:
            piece.square.piece = None
            self.p2.remove(piece)
            piece.move(self.board.get_grave(piece.color))
            self.p2_grave.append(piece)
            
    def show_win(self):
        if len(self.p1) == 0:
            self.turn_text = self.p_names[self.p2[0].color] + " Is The Winner "
        else:
            self.turn_text = self.p_names[self.p1[0].color] + " Is The Winner "
        self.sub_text = 'Press R to Replay or N to Start New Game'
        return self.wait()
        
    
    def get_moves(self, piece, jump_only = False):
        targets = [[piece.square.row + piece.direction, piece.square.col + 1]]
        targets.append([piece.square.row + piece.direction, piece.square.col - 1])
        if piece.is_king:
            targets.append([piece.square.row - piece.direction, piece.square.col + 1])
            targets.append([piece.square.row - piece.direction, piece.square.col - 1])
        moves = []
        for row,col in targets:
            square_t = self.board.get_square(row, col)
            if square_t is not None:
                if square_t.piece is None and jump_only == False:
                    moves.append(square_t)
                elif square_t.piece != None and square_t.piece.direction != piece.direction:
                    r_change = row - piece.square.row
                    c_change = col - piece.square.col
                    square2 = self.board.get_square(row + r_change, col + c_change)
                    if square2 is not None and square2.piece is None:
                        moves.append(square2)
        return moves
    
    def show_splash(self):
        self.screen.fill(Color.screen)
        name = self.get_name('Enter Player 1 Name:')
        self.p_names[Color.piece_red] = name
        name = self.get_name('Enter Player 2 Name')
        self.p_names[Color.piece_blue] = name
    
    def get_name(self, question):
        screen = self.screen
        current_string = []
        while 1:
            self.screen.fill(Color.screen)
            text = my_font.render(question , True, Color.piece_red)
            self.screen.blit(text, (20,200))
            s_text = my_font.render("".join(current_string), True, Color.piece_blue)
            self.screen.blit(s_text, (20,250))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        current_string = current_string[0:-1]
                    elif event.key == pygame.K_RETURN:
                        return "".join(current_string)
                    elif event.key == pygame.K_MINUS:
                        current_string.append("_")
                    elif event.key <= 127:
                        current_string.append(chr(event.key))
        return "".join(current_string)


# In[12]:


class Piece:
    
    radius = 20
    
    def __init__(self, square, direction, color = Color.piece_red):
        self.square = square
        self.color = color
        self.is_king = False
        self.direction = direction
        square.piece = self
        
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.square.x,self.square.y), Piece.radius)
        if self.is_king:
            pygame.draw.circle(screen, Color.king, (self.square.x,self.square.y), int(Piece.radius / 2))
       
        
    def move(self, square):
        self.square.piece = None
        self.square = square
        self.square.piece = self
        if square.is_king:
            self.is_king = True
        
        


# In[13]:


class Square:
    
    def __init__(self, col, row, color):
        self.col = col
        self.row = row
        self.color = color
        self.x = col * Board.tile_size + int(Board.tile_size/2)
        self.y = row * Board.tile_size + int(Board.tile_size/2)
        self.piece = None
        if row == 0 or row == Board.boardx - 1:
            self.is_king = True
        else:
            self.is_king = False
        self.high = False
        
    def draw(self, screen):
        rad = int(Board.tile_size/2)
        if self.high == True:
            color = Color.high
        else:
            color = self.color
        pygame.draw.rect(screen, color, pygame.Rect(self.x - rad, self.y - rad, 2 * rad, 2 * rad))
        if self.piece is not None:
            self.piece.draw(screen)
            
    def __str__(self):
        if self.piece != None:
            piece = self.piece.color
        else:
            piece = ""
        return f"({self.col},{self.row}) {self.high} {self.color} {piece}"
        


# In[14]:


class Board:
    
    boardx = 8
    tile_size = 50
    
    def __init__(self):
        self.grid = []
        self.grave = []
        self.init_board()
        
    def init_board(self):
        self.grid = []
        for row in range(Board.boardx):
            line = []
            for col in range(Board.boardx):
                line.append(Square(col,row,Color.grid_white if (col + row) %2 == 0 else Color.grid_black))
            self.grid.append(line)
        stack1 = []
        stack2 = []
        for i in range(12):
            stack1.append(Square(8,i,Color.screen))
            stack2.append(Square(9,i,Color.screen))
        stack1[0].is_king = False
        stack1[Board.boardx - 1].is_king = False
        stack2[0].is_king = False
        stack2[Board.boardx - 1].is_king = False
        self.grave.append(stack1)
        self.grave.append(stack2)
            
            
            
    def get_square(self, row, col):
        if row >= 0 and col >= 0 and row < Board.boardx and col < Board.boardx:
            return self.grid[row][col]
        return None
        
    def get_squarexy(self, x, y):
        rad = int(Board.tile_size/2)
        return self.get_square(y // Board.tile_size, x // Board.tile_size)
        
            
    def draw(self, screen):
        for row in self.grid:
            for square in row:
                square.draw(screen)
        for col in self.grave:
            for square in col:
                square.draw(screen)
    
    def highlight(self, squares):
        for square in squares:
            square.high = True
            
    def un_highlight(self, squares):
        for square in squares:
            square.high = False
            
    def get_grave(self, color):
        if color == Color.piece_red:
            for i in range(12):
                if self.grave[0][i].piece is None:
                    return self.grave[0][i]
        else: 
            for i in range(12):
                if self.grave[1][i].piece is None:
                    return self.grave[1][i]


# In[ ]:


game = Game()
while True:
    ret = game.play_game()
    if ret == 'r':
        game.turn = 0
        game.init_pieces()
    if ret == 'n':
        game.turn = 0
        game.init_pieces()
        game.show_splash()
    


# In[ ]:




