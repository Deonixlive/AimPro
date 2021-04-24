import pygame
import random
import math

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)       
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (100, 150, 0)
PURPLE = (128, 0, 128)
REDDIE = (200, 50, 50)
RED = (240,20,20)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
YELLOW = (200, 200, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)

# basic constants to set up your game

FPS = 60
BGCOLOR = BLACK

title = "MICROSOFT TEAMS PRO PLAYER GMBH SHEESH"
#settings
lifetime = 2500
delta_t = 20
#initial circle size (in px)
init_size = 100
spawn_delay = 500
#Border where there won't be aimpoints (in px)
border = 200
#list containing all aimpoints
pointlist = []
t = 0
game_duration = 20000  #20 seconds

difficulty = None
#change of size in 1ms
delta_size = (init_size/lifetime)



pygame.init()
pygame.FULLSCREEN = True

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(title)

clock = pygame.time.Clock()


running = True

b_x = WIDTH / 3
b_y = HEIGHT * 0.8
grid_x = WIDTH / 3
easy_b = [0, 0]
intermediate_b = [grid_x, 0]
hard_b = [grid_x*2, 0]
leave_b = [2.5*b_x,0.85*HEIGHT,0.3*b_x,0.099*HEIGHT]


class aimpoint():
    def __init__(self):
        global init_size, WIDTH, HEIGHT, border

        self.cords = (random.randrange(border,WIDTH-border,1), random.randrange(border,HEIGHT-border,1))
        self.rem_life = 2000
        self.size = init_size
        self.avg = 0

    def change(self):
        global delta_size, delta_t
        self.size -= delta_size * delta_t
        self.rem_life -= delta_t

class scores:
    def __init__(self):

        self.score = 0
        self.score_adj = 0
#registers every instance of a click while the game is running
        self.acc_history = []


#acc is a list: [hittype ="center,outer or miss", accuracy/score, where the inner circle is 100]
    def update(self, acc_data):
        global difficulty
        self.acc_history.append(acc_data)
        self.score += acc_data[1]

        if difficulty == "hard":
            self.score_adj = score.score * 1.5

        elif difficulty == "intermediate":
            self.score_adj = score.score * 1.15
        else:
            self.score_adj = score.score

    def reset(self):
        self.acc_history = []
        self.score = 0

def endscreen():
    global score, WIDTH, HEIGHT, pointlist, difficulty
    pointlist = []
    i = 1
    center_hits = 0
    hits = 0
    misses = 0
   # t_dict = {"center": 0, "outer": 0, "miss": 0}
    for round in score.acc_history:
       if round[0] == "center":
           center_hits += 1
       elif round[0] == "outer":
           hits += 1
       else:
           misses += 1
       i += 1


    acc = (score.score/i).__round__(2)


    score.score_adj = r(score.score_adj)

    pos_factor = 0.425
    text_to_screen(screen, f"Score: {score.score_adj}", pos_factor*WIDTH,0.1*HEIGHT)
    text_to_screen(screen, f"Accuracy: {acc}%", pos_factor * WIDTH, 0.2 * HEIGHT)
    text_to_screen(screen, f"Center hits: {center_hits}", pos_factor * WIDTH, 0.3 * HEIGHT)
    text_to_screen(screen, f"Outer Hits: {hits}", pos_factor * WIDTH, 0.4 * HEIGHT)
    text_to_screen(screen, f"Misses: {misses}", pos_factor * WIDTH, 0.5 * HEIGHT)
    text_to_screen(screen, f"Clicks: {i}", pos_factor * WIDTH, 0.6 * HEIGHT)

    button("Menu", 0.4*WIDTH,0.75*HEIGHT,0.2*WIDTH,0.1*HEIGHT,WHITE,SILVER,BLACK)




def main():
    global WIDTH, HEIGHT, OLIVE, GREEN, REDDIE, title, b_x, b_y, easy_b, leave_b

    button("EASY",easy_b[0], easy_b[1], b_x, b_y, GREEN, OLIVE, BLACK)
    button("INTERMEDIATE", intermediate_b[0],intermediate_b[1], b_x, 0.8*HEIGHT, YELLOW, ORANGE,BLACK)
    button("HARD", hard_b[0], hard_b[1], b_x, 0.8*HEIGHT, RED, REDDIE, BLACK)
    button("LEAVE", leave_b[0], leave_b[1], leave_b[2], leave_b[3], WHITE, SILVER,BLACK)

    text_to_screen(screen, text=title,x=WIDTH*0.35,y=HEIGHT*0.9)

def set_to_menu():
    global gamestate, score

    gamestate = "main"
    score.reset()
def set_to_easy():
    global lifetime, init_size, spawn_delay, border, gamestate, game_duration, difficulty

    lifetime = 4000
    init_size = 120
    spawn_delay = 1500
    border = 400
    pygame.time.set_timer(pygame.USEREVENT+1, game_duration)
    gamestate = "ingame"

    difficulty = "easy"
def set_to_intermediate():
    global lifetime, init_size, spawn_delay, border, gamestate, game_duration, difficulty
    lifetime = 2500
    init_size = 100
    spawn_delay = 700
    border = 300
    pygame.time.set_timer(pygame.USEREVENT+1, game_duration)
    gamestate = "ingame"
    difficulty = "intermediate"

def set_to_hard():
    global lifetime, init_size, spawn_delay, border, gamestate, game_duration, difficulty
    lifetime = 1800
    init_size = 80
    spawn_delay = 500
    border = 200
    pygame.time.set_timer(pygame.USEREVENT + 1, game_duration)
    gamestate = "ingame"
    difficulty = "hard"

def clickhandle(x,y,w,h,action=None):
    mouse = pygame.mouse.get_pos()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, WHITE, (x, y, w, h))
        action()

def text_to_screen(screen, text, x, y, size = 20,
            color = WHITE, font_type = 'comicsansms'):
    text = str(text)
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def text_objects(text, font,fc):
    textSurface = font.render(text, True, fc)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, fc=WHITE,action=None):
    x = r(x)
    y = r(y)
    w = r(w)
    h = r(h)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, ic, (x, y, w, h))
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText,fc)
    textRect.center = (r((x + (w / 2))), (r(y + (h / 2))))
    screen.blit(textSurf, textRect)

def r(to_round):
    return round(to_round)

def game():

    global t, spawn_delay, pointlist

    t += delta_t
    if t % spawn_delay == 0:
        pointlist.append(aimpoint())

    i = 0

    for point in pointlist:

        point.outer_size = point.size+5
        point.inner_size = point.size/4+10
        pygame.draw.circle(screen,RED,point.cords,point.outer_size)
        pygame.draw.circle(screen, ORANGE, point.cords, point.inner_size)
        if point.size < 10:
            pointlist.pop(i)

        point.change()
        i += 1
    points = r(score.score)
    text_to_screen(screen, f"Score: {points}", 0.35*WIDTH,0.05*HEIGHT)
    text_to_screen(screen, f"Press ESC to end early", 0.5*WIDTH,0.05*HEIGHT)
def hit(close_point, index):
    global score, pointlist
    if close_point == "miss":
        score.update(["miss", 0])
    elif close_point.delta_d <= close_point.inner_size:
        score.update(["center", 100])
        pointlist.pop(index)
    else:
        #distance from outer circle
        dis_ic = close_point.outer_size - close_point.delta_d
        scale = close_point.outer_size - close_point.inner_size
        score.update(["outer", (dis_ic/scale)*100])
        pointlist.pop(index)

def check_hit():
    global pointlist
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    min_delta = 100000
    min_point = None
    min_point_index = 0
    nd_point = None
    nd_point_index = 0

    i = 0
    for point in pointlist:
        point.delta_d = math.sqrt(abs(point.cords[0]-x)**2 + abs(point.cords[1]-y)**2)

        if point.delta_d < min_delta:
            nd_point = min_point
            nd_point_index = min_point_index
            min_point = point
            min_point_index = i
            min_delta = point.delta_d
        else:
            nd_point = min_point
        i += 1
#if the mouse is in the circle, call the hit function
    if (min_point != None) and (min_point.delta_d < min_point.outer_size):
        hit(min_point, min_point_index)
#the mouse might not hit the nearest circle, but the 2nd nearest who is big enough
    elif (nd_point != None) and (nd_point.delta_d < nd_point.outer_size):
        hit(min_point)
#else: register a miss
    else:
        #print("3")
        hit("miss", None)
#print(num_item, pointlist[num_min].delta_d)



pointlist.append(aimpoint())
#initiate the scores
score = scores()

#selection
gamestate = "main"
gamemode = {"main": main, "ingame": game, "endscreen": endscreen}
while running:
    clock.tick(FPS)


#events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            if gamestate == "ingame":
                check_hit()
            if gamestate == "main":
                clickhandle(easy_b[0], easy_b[1], b_x, b_y, set_to_easy)
                clickhandle(intermediate_b[0], intermediate_b[1], b_x, b_y, set_to_intermediate)
                clickhandle(hard_b[0], hard_b[1], b_x, b_y, set_to_hard)
                clickhandle(leave_b[0], leave_b[1], leave_b[2], leave_b[3], pygame.quit)
            if gamestate == "endscreen":
                clickhandle(0.5 * WIDTH, 0.75 * HEIGHT, 0.2 * WIDTH, 0.1 * HEIGHT, set_to_menu)

        if (event.type == pygame.USEREVENT + 1 and gamestate == "ingame") or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            gamestate = "endscreen"
                    # this one checks for the window being closed
        if event.type == pygame.QUIT:
            pygame.quit()

#main loop
    screen.fill(BGCOLOR)

    gamemode[gamestate]()
    # after drawing, flip the display
    pygame.display.flip()

# close the window
pygame.quit()