#find pair game
import pygame  
import  random 
import os
import time



pygame.init()

width = 600
height =600
white =(255, 255, 255)
black =(0, 0, 0)
red = (255,0 ,0)
green =(0,255, 0)
gray = (128,128,128)
Turquoise =(64,224,208)

fps = 120
timer = pygame.time.Clock()

rows =4
cols=4
correct=[[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
used =[]
option_list=[]
spaces =[]
image_pair =[]
new_board = True 
first_guess =False
second_guess = False
Game_over =False
first_guess_img =0
second_guess_img =0
Turn = 0
matches =0
Wrong = 0
chosen = False




#create screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Find Pair Game!")
title_font = pygame.font.Font('freesansbold.ttf',56)
small_font = pygame.font.Font('freesansbold.ttf',26)
def draw_background():
    #top
    top_menu = pygame.draw.rect(screen,black,[0,0,width,100],0)
    #bottom
    bottom_menu = pygame.draw.rect(screen,black,[0,height -100,width,100],0)
    #middle
    board_space = pygame.draw.rect(screen, gray,[0,100,width,height -200],0)
    #text
    title_text = title_font.render('Find Pair Game!',True,gray)
    #the txet place(left_right,up_down) 
    screen.blit(title_text,(100,20))
    #Restart
    restart = title_font.render("Restart",True,white )
    restart_button = pygame.draw.rect(screen,Turquoise,[12,height -85,205,75],0,15)   
    screen.blit(restart,(15,530))
    #Turn
    Turn_text = small_font.render(f'Turn :{Turn}',True,white)
    screen.blit(Turn_text,(470,510))
    #Wrong
    Wrong_text = small_font.render(f'Wrong :{Wrong}',True,white)
    screen.blit(Wrong_text,(470,550))
    return restart_button
#ge zi
def draw_board():
    global rows
    global cols
    board_list =[]
    for i in range(cols):
        for j in range (rows):
            x = i * 160 + 12
            y = j * 100 + 112
            piece = pygame.draw.rect(screen,white,[x,y,95,75],0,4)
                                        #box i =left_right jian ge,j =updown jiange,chang he kuan
            board_list.append(piece)
            #piece_text = small_font.render(f'{spaces[i * rows +j]}',True,gray)
            #screen.blit(piece_text,(i *155+55,j*108+125))
        
            if correct[j][i] == 1:
                screen.blit(spaces[i * rows + j], (x,y))
    return board_list
def load_images(folder_path):
    image_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img = pygame.image.load(os.path.join(folder_path, filename))
            img = pygame.transform.scale(img, (95, 75))
            image_list.append(img)
    return image_list
def generate_board():
    global option_list
    global spaces
    global used
    global  image_pair
    image_list = load_images(r"C:\Users\User\Documents\mini game\picture")
    image_pairs = random.sample(image_list, rows * cols // 2)
    option_list = image_pairs + image_pairs
    random.shuffle(option_list)
    for item in range(rows * cols):
        spaces.append(option_list[item])
def check_guesses(first,second):
    global spaces
    global correct
    global Turn
    global matches
    global Wrong
    col_1, row_1 = first // rows, first % rows
    col_2, row_2 = second // rows, second % rows
    if spaces[first] == spaces[second] and correct[row_1][col_1] == 0 and correct[row_2][col_2] == 0:
        correct[row_1][col_1] = 1
        correct[row_2][col_2] = 1
        Turn += 1
        matches += 1
        print(correct)
        
    elif spaces[first] != spaces[second] and correct[row_1][col_1] == 0 and correct[row_2][col_2] == 0:
        Turn += 1
        Wrong += 1
def Reset_game():
    global option_list,used,spaces,new_board,Turn,Wrong,correct,first_guess,second_guess,Game_over
    option_list =[]
    used =[]
    spaces =[]
    new_board = True
    Turn = 0
    Wrong = 0
    correct =[[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
    first_guess =False
    second_guess =False
    Game_over =False
def draw_images():
    # 绘制第一张猜测的图片
    if first_guess:
        x = first_guess_img // rows * 160 + 12
        y = (first_guess_img % rows) * 100 + 112
        screen.blit(spaces[first_guess_img], (x, y))

    # 绘制第二张猜测的图片
    if second_guess:
        x = second_guess_img // rows * 160 + 12
        y = (second_guess_img % rows) * 100 + 112
        screen.blit(spaces[second_guess_img], (x, y))
current_color = white

game_running = True
while game_running:
    timer.tick(fps)
    screen.fill(current_color)
    if new_board == True:
        generate_board()
        new_board = False
    restart =draw_background()
    board = draw_board()
    draw_images()
    

    if first_guess and second_guess:
            check_guesses(first_guess_img,second_guess_img)
            first_guess =False
            second_guess =False
            time.sleep(0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not Game_over and not chosen:
                for i in range(len(board)):
                    button = board[i]                                      
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
    if matches == rows * cols //2:
        Game_over =True
        win = pygame.draw.rect(screen,gray,[10,height -300,width -20,80],0,5)
        win_text = title_font.render("You Win",True,white)
        screen.blit(win_text,(200,height -290))
                
    #if first_guess: 
       # location = (first_guess_img // rows *115 +115,(first_guess_img -(first_guess_img //rows * rows))*120 +100)
        #screen.blit(spaces[first_guess_img],(location))

 

  #  if second_guess:
        location = (second_guess_img // rows *115 +115,(second_guess_img -(second_guess_img //rows * rows))*120 +100)
        screen.blit(spaces[second_guess_img],(location))
        
        
        

    pygame.display.flip()
pygame.quit()