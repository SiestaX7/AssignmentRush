import pygame
import time 
import random
pygame.init()

#Windows
width = 600
height =600
cols = 4
rows = 4
fps = 60
timer = pygame.time.Clock()
#color
white =(255, 255, 255)
black =(0, 0, 0)
red = (255,0 ,0)
green =(0,255, 0)
gray = (128,128,128)
Turquoise =(64,224,208)
#global variable
used = []
option_list = []
spaces = []
correct=[[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
#text_font
title_font = pygame.font.Font('freesansbold.ttf',56)
small_font = pygame.font.Font('freesansbold.ttf',26)
#game_setting
current_color =white
new_board = True 
first_guess =False
second_guess = False
Game_over =False
first_guess_num =0
second_guess_num =0
Turn = 0
matches =0
Wrong = 0


#create screen
screen =pygame.display.set_mode([width, height])
pygame.display.set_caption("Find Pair Game!")
#generated spaced
def generate_board():
    global option_list
    global spaces
    global used
    for item in range(rows *cols //2):
        option_list.append(item)
    for item in range(rows * cols):
        number = option_list[random.randint(0,len(option_list)-1)]
        spaces.append(number)
        if number in used:
            used.remove(number)
            option_list.remove(number)
        else:
            used.append(number)

#background and text
def game_background():
    #top
    #top_menu = pygame.draw.rect(screen,black,[0,0,width,100],0)
    #bottom
    #bottom_menu = pygame.draw.rect(screen,black,[0,height -100,width,100],0)
    #middle
    #board_space = pygame.draw.rect(screen, gray,[0,100,width,height -200],0)
    #text
    title_text = title_font.render('Find Pair Game!',True,white)
    #the txet place(left_right,up_down) 
    screen.blit(title_text,(100,20))
    #Restart
    restart = title_font.render("Restart",True,white )
    restart_button = pygame.draw.rect(screen,Turquoise,[12,height -85,205,75],0,15)   
    screen.blit(restart,(15,530))
    #Turn
    Turn_text = small_font.render(f'Turn :{Turn}',True,black)
    screen.blit(Turn_text,(470,510))
    #Wrong
    Wrong_text = small_font.render(f'Wrong :{Wrong}',True,black)
    screen.blit(Wrong_text,(470,550))
    return restart_button
#draw board
def draw_board():
    global rows
    global cols
    board_list =[]
    for i in range(cols):
        for j in range (rows):
            number = pygame.draw.rect(screen,white,[i * 160 + 12,j * 100 + 112,95,75],0,4)
                                        #box i =left_right jian ge,j =updown jiange,chang he kuan
            board_list.append(number)
            #number_text = small_font.render(f'{spaces[i * rows +j]}',True,gray)
            #screen.blit(number_text,(i *155+55,j*108+125))
        
        for row in range(rows):
            for col in range(cols):
                if  correct[row][col] ==1:
                    pygame.draw.rect(screen,green,[col * 160 + 10,row * 100 + 110,99,79],3,4)
                    number_text = small_font.render(f'{spaces[col * rows + row]}',True,black)
                    screen.blit(number_text,(col *155+55,row *108+125))
    return board_list
#check_guess
def check_guess(first,second):
    global spaces
    global correct
    global Turn
    global matches
    global Wrong
    col_1 = first // rows
    row_1 = first - (col_1 * rows)
    col_2 = second // rows
    row_2 = second - (col_2*rows)
    if spaces[first] == spaces[second] and correct[row_1][col_1] == 0 and correct[row_2][col_2] == 0:
            correct[row_1][col_1]=1
            correct[row_2][col_2]=1
            Turn += 1
            matches += 1
            print(correct)
        
    elif spaces[first] != spaces[second] and correct[row_1][col_1] == 0 and correct[row_2][col_2] == 0 :
        Turn += 1
        Wrong += 1
#Reset game
def Reset_game():
    global option_list,used,spaces,new_board,Turn,Wrong,correct,first_guess,second_guess,Game_over,matches
    option_list =[]
    used =[]
    spaces =[]
    new_board = True
    Turn = 0
    Wrong = 0
    matches = 0
    correct =[[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
    first_guess =False
    second_guess =False
    Game_over =False
def show_all_numbers():
    global rows, cols
    game_background()
    draw_board()
    for i in range(cols):
        for j in range(rows):
            number_text = small_font.render(f'{spaces[i * rows + j]}', True, black)
            location = (i * 155 + 55, j * 108 + 120)
            screen.blit(number_text, location)
    pygame.display.flip() 
    time.sleep(1)
#game running

game_running = True
while game_running:
    timer.tick(fps)
    #screen.fill(current_color)
    background_img = pygame.image.load("picture/background.png").convert_alpha()
    pygame.display.flip()
    screen.blit(background_img,(0,0))
    if new_board == True:
        generate_board()
        show_all_numbers()
        print(spaces)
        new_board = False
    restart = game_background()
    board = draw_board()
    if first_guess and second_guess:
            check_guess(first_guess_num,second_guess_num)
            first_guess =False
            second_guess =False
            time.sleep(0.5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not Game_over :
                for i in range(len(board)):
                    button = board[i]
                    row = i % rows
                    col = i // rows
                    if  correct[row][col] == 1:
                        continue
                    if button.collidepoint((event.pos)) and not first_guess :
                        first_guess =True
                        first_guess_num = i
                        print(i)
                    if button.collidepoint((event.pos)) and not second_guess and first_guess and i != first_guess_num:
                        second_guess =True
                        second_guess_num = i
                        print(i)                                      
            if restart.collidepoint((event.pos)):
                Reset_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                Reset_game()
    
    if matches == rows*cols // 2:
        Game_over =True
        win = pygame.draw.rect(screen,black,[10,height -350,width -20,80],0,5)
        win_text = title_font.render("You Win",True,white)
        screen.blit(win_text,(200,height -325))
    if Wrong == 4:
        Game_over =True
        lose = pygame.draw.rect(screen,black,[10,height -350,width -20,80],0,5)
        lose_text = title_font.render("You lose",True,white)
        screen.blit(lose_text,(200,height -325))
    if first_guess :
        number_text = small_font.render(f'{spaces[first_guess_num]}',True,black)
        location = (first_guess_num // rows *155 +55,(first_guess_num -(first_guess_num //rows * rows))*108 +120)
        screen.blit(number_text,(location))
    if second_guess:
        number_text = small_font.render(f'{spaces[second_guess_num]}',True,black)
        location = (second_guess_num // rows *155 +55,(second_guess_num -(second_guess_num //rows * rows))*108 +120)
        screen.blit(number_text,(location))
    pygame.display.flip()
pygame.quit()
