# GAME SETTING
speed = 4
difficulty = 20 # Maximum Blocks On Screen | DON'T PUT LESS THAN 6
heart_rate = 30 # 1 / heart_rate blocks is heart
FPS = 30
screen_width = 750
screen_height = 600
life = 3
paused = False

mute = False

import os
import random
import time
import pygame


os.environ['SDL_VIDEO_CENTERED'] = '1'   # TO Centralize The Screen

pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((200,200),pygame.NOFRAME) # For Loading Screen
load_font = pygame.font.SysFont("Raleway Bold", 25)
loading = load_font.render("Loading",1,(255,255,255))
screen.blit(loading,loading.get_rect(center=(100,100)))
pygame.display.update()
time.sleep(1)

# Sounds
pygame.mixer.init()

start_sound = pygame.mixer.Sound("assets\\Start_Sound.mp3")
game_over_sound = pygame.mixer.Sound("assets\\gameover_sound.mp3")
menu_cound = pygame.mixer.Sound("assets\\menu_sound.mp3")
bg_music = pygame.mixer.Sound("assets\\bg_music.mp3")
collide_sound = pygame.mixer.Sound("assets\\hit.mp3")
life_added_sound = pygame.mixer.Sound("assets\\life_added.mp3")

# Messages
messages = [
    "W,A,S,D to control the Rocket",
    "Press SPACE to Pause",
    "Press `m` to Mute sounds.",
    "Collect Hearts To Gain Life",
    "Avoid Hitting Asteroids",
    "Made By Naman Chhabra",
    "Can you really reach 1 Lakh score?",
    "Is this game Easy?",
    "Difficulty increases over time."
]


pygame.display.set_caption("Protect The Rocket ~ Made By Naman")
icon = pygame.image.load("assets\\icon.ico").convert_alpha()
pygame.transform.scale(icon,(60,60))
pygame.display.set_icon(icon)

heart_chances = [True]
for i in range(0,heart_rate):
    heart_chances.append(False)


clock = pygame.time.Clock()

def high_score():
    with open("assets\\Highest_score.txt", "r") as feee:
        return int(feee.read().strip())
high_scr = high_score()

def save_score(current_score):

    with open("assets\\Highest_score.txt", "r") as f:
        a = int(f.read().strip())
        if a < current_score:
            print("Big")
            with open("assets\\Highest_score.txt", "w") as fe:
                fe.write(f"{int(current_score)}")


def show_score(lifes,score,window):
    font = pygame.font.SysFont("Segoe UI Emoji", 20)
    text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    window.blit(text, (10,10))

    text2 = font.render('❤️'*lifes, True, (255, 255, 255))
    window.blit(text2,(screen_width-100,screen_height-30))

asteroid = pygame.image.load("assets\\asteroid.png").convert_alpha()
asteroid = pygame.transform.scale(asteroid,(100,100))

heart = pygame.image.load("assets\\life.png").convert_alpha()
heart = pygame.transform.scale(heart,(70,70))

class Block:

    def __init__(self,width):
        global screen,asteroid
        self.isheart = random.choice(heart_chances)
        self.x = random.randint(0,width-50)
        self.y = -200
        self.speed=random.randint(1,5)
        self.screen = screen
        if self.isheart:
            self.block_mask = pygame.mask.from_surface(heart)
            return
        self.turn = random.choice([False,True])
        self.size = random.randint(40, 150)
        self.aster = pygame.transform.scale(asteroid, (self.size, self.size))
        self.block_mask = pygame.mask.from_surface(self.aster)



    def move(self):
        self.y += self.speed
        if not self.isheart:
            if self.turn:
                self.x -= 1
            else:
                self.x +=1
    def draw(self):
        if self.isheart:
            screen.blit(heart, (self.x, self.y))
            return
            
        screen.blit(self.aster,(self.x,self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


def play():
    global paused,life,difficulty

    max_message = len(messages)
    current_message = 0

    rocket_L = pygame.image.load("assets\\Rocket_L.png").convert_alpha()
    rocket_L = pygame.transform.scale(rocket_L, (100, 100))
    rocketL_mask = pygame.mask.from_surface(rocket_L)
    rocket = pygame.image.load("assets\\Rocket.png").convert_alpha()
    rocket = pygame.transform.scale(rocket, (100, 100))
    rocket_mask = pygame.mask.from_surface(rocket)
    rocket_R = pygame.image.load("assets\\Rocket_R.png").convert_alpha()
    rocket_R = pygame.transform.scale(rocket_R, (100, 100))
    rocketR_mask = pygame.mask.from_surface(rocket_R)

    masks = [rocketL_mask,rocket_mask,rocketR_mask]
    rockets = [rocket_L,rocket,rocket_R]
    number = 1 # 0 for left, 1 for Straight, 2 for right

    lvl_difficult = 5

    temp_score = 0
    temp_score2 = 0
    temp_score3 = 0

    save_life = life
    game_over = False
    score = 0
    x, y = 350, 500
    running = True

    blocks = []
    
    game_over_image = pygame.image.load("assets\\Game_Over.png")
    game_over_image = pygame.transform.scale(game_over_image,(screen_width//2,screen_height//2))
    for _ in range(3):  # number of blocks
        blocks.append(Block(screen_width))

    showhit = 0
    font = pygame.font.Font(None, 300)

    font2 = pygame.font.Font(None, 20)
    def blit_message(msg):
        screen.blit(msg, (20, screen_height - 20))
    next_block_after = 100
    after = 600

    stars = pygame.image.load("assets\\Moving_Back.png").convert()
    stars.set_alpha(50)
    stars = pygame.transform.scale(stars, (screen_width, screen_height))
    stars_y = 0
    gap = -1*screen_height
    stars_y2 = gap

    start_sound.play()
    bg_music.set_volume(70)
    channel2 = bg_music.play()

    while running:
        if (not channel2.get_busy()) and not game_over and not mute:
            channel2.play(bg_music)

        message_text = font2.render(f"{messages[current_message]}", True, (255, 255, 255))

        if (score-temp_score3) >= 600:
            if current_message == max_message-1:
                current_message = 0
            else:
                current_message += 1
            temp_score3 = score

        if not blocks:  # If there are no asteriods on the screen, don't stop further calculation
            blit_message(message_text)
            
            next_block_after -= 1
            score+=0.5
            if next_block_after <=0:
                blocks.append(Block(screen_width))  # create new

                next_block_after = random.randint(0, int(after))
            continue
        if not paused:
            screen.fill((0,0,0))
            screen.blit(stars,(0,stars_y))
            screen.blit(stars,(0,stars_y2))

            stars_y += 6
            stars_y2 += 6
            if stars_y >= 500:
                stars_y = gap
            if stars_y2 >= 500:
                stars_y2 = gap

            screen.blit(rockets[number],(x,y))
     
        keys = pygame.key.get_pressed()
        if not paused:
            # Game Controls
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                y -= speed
                number = 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                y += speed
                number = 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                x -= speed
                number = 0
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                x += speed
                number = 2
            if not any(keys):
                number = 1

        # Boundaries
        if x < -30:
            x = -30
        if x > screen_width - 80:
            x = screen_width - 80
        if y < 0:
            y = 0
        if y > screen_height - 100:
            y = screen_height - 100
        if not paused:
            check_block = blocks[:]
        else:
            check_block = blocks
            
        for block in check_block:

            offset = (block.x-x,block.y-y)
            if masks[number].overlap(block.block_mask,offset):
                if block.isheart:
                    if life < 3 :
                        life+=1
                    life_added_sound.play()
                    blocks.remove(block)
                elif life <=1:
                    if not paused and not mute:
                        channel2.fadeout(2000)
                        game_over_sound.play()
                    paused = True
                    game_over = True
                    save_score(score)

                else:
                    if not mute:
                        collide_sound.play()
                    blocks.remove(block)
                    life-=1
                    showhit = 5  # For 5 frames
                    
            # Hitting boundries changes Asteroids direction
            if not block.isheart:
                if block.x <= -30:
                    block.turn = False
                elif block.x >= screen_width - 80:
                    block.turn = True

            if not paused:
                score += 0.5
                if block:
                    block.move()
            if block:
                block.draw()
            if block:
                if block.y > screen_height:
                    blocks.remove(block)  # destroy asteroid
            if next_block_after <=0:
                if len(blocks) < random.randint(4,lvl_difficult):  # to avoid too many obstacles on screen
                    blocks.append(Block(screen_width))  # create new asteroid

                next_block_after = random.randint(0, int(after))
                print("Nextblock will come after: ",next_block_after)
            next_block_after-=1
            if not paused:
                if (score - temp_score2) == 1000:
                    lvl_difficult+=1
                    if difficulty < lvl_difficult:
                        lvl_difficult = 5
                    temp_score2 = score
                if (score - temp_score) >=50:
                    after-= random.randint(0,50)
                    print("After: ",after)
                    temp_score = score
                if after <= 50:
                    after += 500
                    print("Reset to 1000")


        # Show Red Screen On Hit
        if showhit != 0:
            rect_curface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            rect_curface.fill((255, 0, 0, 70))
            screen.blit(rect_curface, (0, 0))

            hit_text = font.render("HIT", 1, (255, 255, 255))
            screen.blit(hit_text, (screen_width // 2 - 180, screen_height // 2-100))
            showhit -= 1

        if paused and game_over:
            screen.blit(game_over_image,(screen_width//4,screen_height//4))
        else:
            show_score(life,score, screen)
        if game_over:
            ismax_score = high_score()
            font = pygame.font.Font(None, 40)
            final_score = font.render(f"{int(score)}", True, (255, 255, 255))
            screen.blit(final_score, final_score.get_rect(center=(screen_width/2,screen_height/2+20)))
            max_score = font.render(f"{ismax_score if ismax_score > score else int(score)}", True, (255, 255, 255))
            screen.blit(max_score, max_score.get_rect(center=(screen_width//2,screen_height//2+90)))
        if not paused:
            blit_message(message_text)
            
        # Window Management ( TODO: Create seprate function for this )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    running = False
                    paused = False
                    life=save_life
                    starting_screen()
                elif event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                    else:
                        paused = True



        else:
            clock.tick(FPS)
            pygame.display.update()

starting_bg = pygame.image.load("assets\\Background_Start.jpg")
starting_bg = pygame.transform.scale(starting_bg,(screen_width,screen_height))


randx,randy = 0,0
def starting_screen():
    global randx,randy,mute
    On = True
    angle = 0
    channel = menu_cound.play()
    while On:
        if not channel.get_busy() and not mute:
            channel.play(menu_cound)

        barder = random.randint(5,13)
        # rotate_image = pygame.transform.rotate(circlestart,angle)
        angle+=10
        if angle == 360:
            angle = 0
        screen.blit(starting_bg, (0, 0))
        
        
        # Window Management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                On = False
                channel.fadeout(3000)
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    On = False
                    if not mute:
                        channel.fadeout(2000)
                    play()
                if event.key == pygame.K_m:

                    if mute:
                        print("Unpaused")
                        channel.unpause()
                        mute = False
                    elif not mute:
                        print("Paused")
                        channel.pause()
                        mute = True




        if not On:
            break
        # Making Some Animation

        colors = [(255,255,255),(0,255,255),(255,255,0)]

        for _ in range(10):
            # time.sleep(0.01)
            color = random.choice(colors)
            randx = random.randint(0,screen_width-50)
            randy = random.randint(0,screen_height-50)
            size = random.randint(1,3)
            pygame.draw.circle(screen,color,(randx,randy),size)
        
        pygame.draw.rect(screen,(255,255,255),((screen_width//2-230), (screen_height//2-150), 460, 290),barder)


        txt = "Controls: W,A,S,D or Arrow Keys"
        control_text = load_font.render(txt, 1, (255, 255, 100))
        screen.blit(control_text,control_text.get_rect(center=(screen_width//2,screen_height//2+250)))

        clock.tick(7)
        pygame.display.update()


pygame.display.update()
screen = pygame.display.set_mode((screen_width, screen_height))


starting_screen()

pygame.quit()
