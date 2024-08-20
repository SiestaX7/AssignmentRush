import pygame
from pygame.locals import *
import random

pygame.init()

# create game widow 
width = 400
height = 400
scoareboard_height =25
window_size = (width, height + scoareboard_height)
screen= pygame.display.set_mode(window_size)
pygame.display.set_caption("Match Three Game")

#variables
score = 0
moves = 0

#list of colours
shape_colour = ['red','yellow','blue','green']

#shape size
shape_width = 40
shape_height = 40
shape_size =(shape_width,shape_height)

class Shape:
    def __init__(self, row_num, col_num):

#set shape location
        self.row_num = row_num
        self.col_num = col_num

#assign image
        self.color = random.choice(shape_colour)
        image_name = f'pic_{self.color}.png'
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image, shape_size)
        self.rect = self.image.get_rect()
        self.rect.left = col_num * shape_width
        self.rect.top = row_num * shape_height

#draw image to screen
    def draw(self):
        screen.blit(self.image,self.rect)

#snap the shape(fruit) to its position
def snap(self):
    self.snap_row()
    self.snap_col()

def snap_row(self):
    self.rect.top = self.row_num * shape_height

def snap_col(self):
    self.rect.left = self.col_num * shape_width
    

#create board 
board = []
for row_num in range(height//shape_height):

#add new row to board
    board.append([])

    for col_num in range(width//shape_width):

#create shape and add it to board
        shape = Shape(row_num, col_num)
        board[row_num].append(shape)



def draw():
#background
    pygame.draw.rect(screen,(173,216,230),(0,0,width,height + scoareboard_height))

#draw shape
    for row in board:
        for shape in row:
            shape.draw()

#score and moves dispaly
font = pygame.font.SysFont('monoface',18)
score_text = font.render(f'Score: {score}',1,(0,0,0))
score_text_rect = score_text.get_rect(center=(width/4, height + scoareboard_height /2 ))
screen.blit(score_text,score_text_rect)

moves_text = font.render(f'Moves: {moves}',1, (0,0,0))
moves_text_rect = moves_text.get_rect(center=(width * 3/4, height + scoareboard_height /2 ))
screen.blit(moves_text, moves_text_rect)

#swap positions
def swap (shape1, shape2):
    temp_row = shape1.row_num
    temp_col = shape1.col_num
    
    shape1.row_num = shape2.row_num
    shape1.col_num = shape2.col_num

    shape2.row_num = temp_row
    shape2.col_num = temp_col

# updates on board list
    board[shape1.row_num][shape1.col_num] = shape1
    board[shape2.row_num][shape2.col_num] = shape2

# snap shapes in board position
    shape1.snap()
    shape2.snap()

#find shape next to it is match or not
def find_matches(shape, matches):
 
#add shape into set
    matches.add(shape)

#check shape is the same colour
    if shape.row_num>0:
        next = board[shape.row_num - 1][shape.col_num]
        if shape.color == next.color and next not in matches:
            matches.update(find_matches(next, matches))

#check shape below is same colour or not
    if shape.row_num < height / shape_height - 1:
        next = board[shape.row_num + 1][shape.col_num]
        if shape.color == next.color and next not in matches:
            matches.update(find_matches(next, matches))

#check left one is same or not
    if shape.col_num >0:
        next = board[shape.row_num][shape.col_num - 1]
        if shape.color == next.color and next not in matches:
            matches.update(find_matches(next, matches))

#check right one is same or not
    if shape.col_num < width / shape_width -1:
        next = board[shape.row_num][shape.col_num + 1]
        if shape.color == next.color and next not in matches:
            matches.update(find_matches(next, matches))

    return matches

#return a set of 3 matches or an empty set
def match_three(shape):

    matches = find_matches(shape,set())
    if len(matches) == 3:
        return matches
    else:
        return set()

#shape that clicked on
clicked_shape = None

#the adjacent shape that will be swapped with the clicked shape
swapped_shape = None

#position when user clicked on
click_x = None 
click_y = None

#game function
clock = pygame.time.Clock()
running = True
while running:

#Set of matched shapes
    matches = set()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

#Detect click
        if clicked_shape is None and event.type == "ClickNotDetected":

#get the shape that clicked
            for row in board:
                for shape in row:
                    if shape.rect.collidepoint(event.pos):

                        clicked_shape = shape

#safe position were clicked
                        click_x = event.pos[0]
                        click_y = event.pos[1]

#detect mouse motion
            if clicked_shape is not None and event.type == "MouseMotion":

#calculate distance between point that clicked on
                distance_x= abs(click_x - event.pos[0])
                distance_y =abs(click_y = event.pos[1])

#reset position of swapped shape if direction of mouse change
                if swapped_shape is not None:
                    swapped_shape.snap()

#determine the direction of the next shape to swap with
                if distance_x > distance_y and click_x > event.pos[0]:
                    direction ='left'
                elif distance_x > distance_y and click_x < event.pos[0]:
                    direction ='right'
                elif distance_y > distance_x and click_y > event.pos[1]:
                    direction = 'up'
                else:
                    direction = 'down'

#if moving (left/right),snap new shapped to its row positon,col position
                if direction in ['left', 'right']:
                    clicked_shape.snap_row()
                else:
                    clicked_shape.snap_col()

#if move right make sure its not on the first col
                if direction == 'left' and clicked_shape.col_num > 0:

#get it to the left
                    swapped_shape = board[clicked_shape.row_num][clicked_shape.col_num - 1]

#move those two shape
                    clicked_shape.rect.left = clicked_shape.col_num * shape_width - distance_x
                    swapped_shape.rect.left = swapped_shape.col.num * shape_width + distance_x

#snap them into their new position
                    if clicked_shape.rect.left <= swapped_shape.col_num * shape_width + shape_width / 4:
                        swap(clicked_shape, swapped_shape)
                        matches.update(match_three(clicked_shape))
                        matches.update(match_three(swapped_shape))
                        moves += 1
                        clicked_shape = None

#if moving the clicked shape to right make sure its not on the last col
                if direction == 'right' and clicked_shape.col_num < width/ shape_width -1:
                    
#get it to  right
                    swapped_shape = board[clicked_shape.row_num][clicked_shape.col_num + 1]

#move those two shape 2.0
                    clicked_shape.rect.left = clicked_shape.col_num * shape_width + distance_x
                    swapped_shape.rect.left= swapped_shape.col_num * shape_width - distance_x

#swap to new pos 2.0
                    if clicked_shape.rect.left >= swapped_shape.col_num * shape_width / 4:
                        swap(clicked_shape,swapped_shape)
                        matches.update(match_three(clicked_shape))
                        matches.update(match_three(swapped_shape))
                        moves += 1
                        clicked_shape = None
                        swapped_shape = None

#if move up make sure is not on first row
                if direction == 'up' and clicked_shape.row_num > 0:

#move it above
                    swapped_shape = board[clicked_shape.row_num - 1][clicked_shape.col_num]

#move two shape 3.0
                    clicked_shape.rect.top = clicked_shape.row_num * shape_height - distance_y
                    swapped_shape.rect.top = swapped_shape.row_num * shape_height + distance_y

#snap to new position 3.0
                    if clicked_shape.rect.top<= swapped_shape.row_num * shape_height + shape_height / 4:
                        swap(clicked_shape, swapped_shape)
                        matches.update(match_three(clicked_shape))
                        matches.update(match_three(swapped_shape))
                        moves += 1
                        clicked_shape = None
                        swapped_shape = None

#if moving down make sure no at last row
                if direction == 'down' and clicked_shape.row_num < height / shape_height - 1:

#get the candy below
                    swapped_shape = board[clicked_shape.row_num + 1][clicked_shape.col_num]

#move two shape 4.0
                    clicked_shape.rect.top = clicked_shape.row_num * shape_height + distance_y
                    swapped_shape.rect.top = swapped_shape.row_num * shape_height - distance_y

#snap them to new position 4.0
                    if clicked_shape.rect.top >= swapped_shape.row_num * shape_height - shape_height / 4:
                        swap(clicked_shape, swapped_shape)
                        matches.update(match_three(clicked_shape))
                        matches.update(match_three(swapped_shape))
                        moves +=1
                        clicked_shape = None
                        swapped_shape = None

#detect mouse release
        if clicked_shape is not None and event.type == MOUSEBUTTONUP:

#Snap shape back to original position
            clicked_shape.snap()
            clicked_shape = None
            if swapped_shape is not None:
                swapped_shape.snap()
                swapped_shape = None
    draw()
    pygame.display.update()

#check is there three matched or not
    if len(matches) == 3:
        score += len(matches)

#animate the matching shrinking
        while len(matches) > 0:
            clock.tick(100)

#decrease width and height
        for shape in matches:
            new_width = shape.image.get_width() - 1
            new_height = shape.image.get_height() - 1
            new_size =(new_width, new_height)
            shape.image = pygame.transform.smoothscale(shape.image, new_size)
            shape.rect.left = shape.col_num * shape_width + (shape_width - new_width) / 2
            shape.rect.top = shape.row_num * shape_height + (shape_height - new_height) / 2

#check if have shrink to zero size
        for row_num in range(len(board)):
            for col_num in range(len(board[row_num])):
                shape = board[row_num][col_num]
                if shape.image.get_width() <= 0 or shape.image.get_height() <=0:
                    matches.remove(shape)

#generate new shape
                    board[row_num][col_num]= shape(row_num, col_num)

        draw()
        pygame.display.update()

pygame.quit()




