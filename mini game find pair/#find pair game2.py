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
image_dict = {}
#text_font
title_font = pygame.font.Font('freesansbold.ttf',56)
small_font = pygame.font.Font('freesansbold.ttf',26)
#game_setting
current_color =white
new_board = True 
first_guess =False
second_guess = False
Game_over =False
first_guess_img =0
second_guess_img =0
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
    global image_dict
    for item in range(rows *cols //2):
        option_list.append(item)
    for i in range(8):
        image_dict[i] = pygame.image.load(f'mini game find pair/picture/image{i+1}.jpg')
    for item in range(rows * cols):
        image = option_list[random.randint(0,len(option_list)-1)]
        spaces.append(image)
        if image in used:
            used.remove(image)
            option_list.remove(image)
        else:
            used.append(image)

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
    restart_img = pygame.image.load("mini game find pair//picture//restart.png").convert_alpha()    
    restart_img = pygame.transform.scale(restart_img, (200, 70)) 
    restart_rect = restart_img.get_rect(bottomleft=(10,height -10)) 
    screen.blit(restart_img,restart_rect)
    restart_text = title_font.render("Restart",True,white )
    text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text,text_rect)
    #Turn
    Turn_text = small_font.render(f'Turn :{Turn}',True,black)
    screen.blit(Turn_text,(470,510))
    #Wrong
    Wrong_text = small_font.render(f'Wrong :{Wrong}',True,black)
    screen.blit(Wrong_text,(470,550))
    return restart_rect
#draw board
def draw_board():
    global rows
    global cols
    global image_dict

    board_list =[]
    for i in range(cols):
        for j in range (rows):
            image = pygame.draw.rect(screen,white,[i * 160 + 12,j * 100 + 112,95,75],0,4)
                                        #box i =left_right jian ge,j =updown jiange,chang he kuan
            board_list.append(image)
            #number_text = small_font.render(f'{spaces[i * rows +j]}',True,gray)
            #screen.blit(number_text,(i *155+55,j*108+125))       
            if correct[j][i] == 1:
                    pygame.draw.rect(screen, green, [i * 160 + 10, j * 100 + 110, 99, 79], 9, 0)
                    image = image_dict[spaces[i * rows + j]]
                    image = pygame.transform.scale(image, (95, 75)) 
                    screen.blit(image, (i * 160 + 12, j * 100 + 112))
            else:
                pygame.draw.rect(screen, white, [i * 160 + 10, j * 100 + 110, 95, 75], 0, 0)
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
            image = image_dict[spaces[i * rows + j]]
            image = pygame.transform.scale(image, (97, 77))
            location = (i * 160 + 10, j * 100 + 110)
            screen.blit(image, location)
    pygame.display.flip() 
    time.sleep(1)
#game running
game_running = True
while game_running:
    timer.tick(fps)
    #screen.fill(current_color)
    background_img = pygame.image.load("mini game find pair/picture/background.png").convert_alpha()
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
            check_guess(first_guess_img,second_guess_img)
            first_guess =False
            second_guess =False
            time.sleep(0.5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not Game_over and Wrong != 4:
                for i in range(len(board)):
                    button = board[i]
                    row = i % rows
                    col = i // rows
                    if  correct[row][col] == 1:
                        continue
                    if button.collidepoint((event.pos)) and not first_guess :
                        first_guess =True
                        first_guess_img = i
                        print(i)
                    if button.collidepoint((event.pos)) and not second_guess and first_guess and i != first_guess_img:
                        second_guess =True
                        second_guess_img = i
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
        image = image_dict[spaces[first_guess_img]]
        image = pygame.transform.scale(image, (100, 80))
        location = (first_guess_img // rows * 160 + 10, (first_guess_img % rows) * 100 + 110)#(i * 160 + 10, j * 100 + 110)
        screen.blit(image, location)
    if second_guess:
        image = image_dict[spaces[second_guess_img]]
        image = pygame.transform.scale(image, (100, 80))
        location = (second_guess_img // rows * 160 + 10, (second_guess_img % rows) * 100 + 110)
        screen.blit(image, location)
    pygame.display.flip()
pygame.quit()
