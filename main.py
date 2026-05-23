# GAME SETTING
speed = 4
difficulty = 20  # Maximum Blocks On Screen | DON'T PUT LESS THAN 6
heart_rate = 60  # 1 / heart_rate blocks is heart
comet_rate = 8# 1 / comet_rate blocks is comet
FPS = 30
screen_width = 750
screen_height = 600
life = 3
paused = False
mute = False
current_score = 0




import scene    # All the scenes are made in scene.py file
import splashscreen_engine as splash # pip install splashscreen-engine

l_screen = splash.Screen()
l_screen.start()


loadingVid = splash.BackgroundVideo(l_screen,"assets\\loadingVid.mp4",loop=True)
loadingVid.play()
loadingBar = splash.LoadingBar(loadingVid)
loadingBar.place()
loadingBar.set_progress(5)


def update_bar(x):
    loadingBar.set_progress(x)
    l_screen.wait(0.2)
update_bar(10)



import os
import random
import pygame # pip install pygame
import threading


os.environ['SDL_VIDEO_CENTERED'] = '1'  # TO Centralize The Screen

pygame.init()

info = pygame.display.Info()

load_font = pygame.font.SysFont("Raleway Bold", 25)
loading = load_font.render("Loading", 1, (255, 255, 255))
update_bar(16)

# Sounds
pygame.mixer.init()

start_sound = pygame.mixer.Sound("assets\\Start_Sound.mp3")
game_over_sound = pygame.mixer.Sound("assets\\gameover_sound.mp3")
menu_cound = pygame.mixer.Sound("assets\\menu_sound.mp3")
bg_music = pygame.mixer.Sound("assets\\bg_music.mp3")
collide_sound = pygame.mixer.Sound("assets\\hit.mp3")
life_added_sound = pygame.mixer.Sound("assets\\life_added.mp3")
levelUp_sound = pygame.mixer.Sound("assets\\Level_Up.mp3")

# Messages
messages = [
    "W,A,S,D to control the Rocket",
    "Press SPACE to Pause",
    "Press `m` to Mute sounds.",
    "Collect Hearts To Gain Life",
    "Avoid Hitting Obstacles",
    "Made By Naman Chhabra",
    "Is this game Easy?",
    "Can you really reach 1 Lakh score?",
    "Difficulty increases over time."
]

pygame.display.set_caption("Protect The Rocket ~ Made By Naman")
icon = pygame.image.load("assets\\icon.ico").convert_alpha()
pygame.transform.scale(icon, (60, 60))
pygame.display.set_icon(icon)
update_bar(25)

heart_chances = [True]
for i in range(0, heart_rate):
    heart_chances.append(False)



clock = pygame.time.Clock()


def high_score():
    with open("assets\\Highest_score.txt", "r") as feee:
        return int(feee.read().strip())


high_scr = high_score()

update_bar(30)

# Chances of spawning a comet
def update_comet_rate(rate):
    global comet_rate
    comet_rate = rate
    comet_chances = [True]

    for _ in range(0, comet_rate):
        comet_chances.append(False)
    return comet_chances
update_comet_rate(comet_rate)

def save_score(score_now):
    with open("assets\\Highest_score.txt", "r") as f:
        a = int(f.read().strip())
        if a < score_now:
            with open("assets\\Highest_score.txt", "w") as fe:
                fe.write(f"{int(score_now)}")

update_bar(35)
def show_score(lifes, score, window):
    font = pygame.font.SysFont("Segoe UI Emoji", 20)
    text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    window.blit(text, (10, 10))

    text2 = font.render('❤️' * lifes, True, (255, 255, 255))
    window.blit(text2, (screen_width - 100, screen_height - 30))

update_bar(40)
asteroid = pygame.image.load("assets\\asteroid.png").convert_alpha()
asteroid = pygame.transform.scale(asteroid, (100, 100))
update_bar(45)
heart = pygame.image.load("assets\\life.png").convert_alpha()
heart = pygame.transform.scale(heart, (70, 70))

comet = pygame.image.load("assets\\comet.png").convert_alpha()
comet = pygame.transform.scale(comet, (60, 60))

update_bar(50)

last_cometScore_update = 3000

stars = pygame.image.load("assets\\Moving_Back.png").convert()
stars.set_alpha(50)

def level_up():
    global asteroid,stars
    obstacles_path = r"assets/Obstacles"
    file_count_obstacles = len([f for f in os.listdir(obstacles_path) if os.path.isfile(os.path.join(obstacles_path, f))])
    obstacle_number = random.randint(1,file_count_obstacles)
    asteroid = pygame.image.load(f"assets\\Obstacles\\{obstacle_number}.png").convert_alpha()
    asteroid = pygame.transform.scale(asteroid, (100, 100))

    bg_path = r"assets/Backgrounds"
    file_count_bg = len([f for f in os.listdir(bg_path) if os.path.isfile(os.path.join(bg_path, f))])
    star_number = random.randint(1,file_count_bg)
    stars = pygame.image.load(f"assets\\Backgrounds\\{star_number}.png").convert()
    stars.set_alpha(70)
    stars = pygame.transform.scale(stars, (screen_width, screen_height))

    def level_up_thread():
        if not mute:
            levelUp_sound.play()
        level_font = pygame.font.Font(None, 100)
        level_txt = level_font.render("LEVEL UP!", 1, (255,255,255))
        level_txt_rect = level_txt.get_rect(center=(screen_width//2,screen_height//2))
        for _ in range(0,100):
            screen.blit(level_txt,level_txt_rect)
            clock.tick(60)

    threading.Thread(target=level_up_thread).start()





class Block:

    def __init__(self, width):
        global screen, asteroid, last_cometScore_update,comet_rate
        self.isheart = random.choice(heart_chances)
        self.iscomet = False

        self.x = random.randint(0, width - 50)
        self.y = -200
        self.speed = random.randint(1, 5)
        self.screen = screen
        if self.isheart:
            self.block_mask = pygame.mask.from_surface(heart)
            return
        self.turn = random.choice([False, True])

        # If the last saved score (for comet) is less than current score, than update comet rate, store next score update in `last_cometScore_update` i.e. current_score + 800
        if last_cometScore_update < current_score:
            last_cometScore_update = current_score + 3000
            level_up()
            comet_rate -= 1
            if comet_rate < 0:
                comet_rate = random.randint(5, 8)
        if current_score > 5000:
            self.comet_chance = update_comet_rate(comet_rate)
            self.iscomet = random.choice(self.comet_chance)
            if self.iscomet:
                self.turn = True
                self.x = screen_width
                self.y = random.randint(-500,250)
                self.speed = random.randint(7, 10)
                self.block_mask = pygame.mask.from_surface(comet)
                _size = random.randint(5,15)
                self.aster = pygame.transform.scale(comet, (_size,_size))
                self.x_speed = random.randint(6, 9)
                return

        self.size = random.randint(40, 150)
        self.aster = pygame.transform.scale(asteroid, (self.size, self.size))
        self.block_mask = pygame.mask.from_surface(self.aster)

    def move(self):
        self.y += self.speed
        if not self.isheart:
            if self.turn:
                if self.iscomet:
                    self.x-= self.x_speed
                self.x -= 1
            else:
                self.x += 1

    def draw(self):
        if self.isheart:
            screen.blit(heart, (self.x, self.y))
            return
        if self.iscomet:
            screen.blit(comet, (self.x, self.y))
            return

        screen.blit(self.aster, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
update_bar(60)

def play():
    global paused, life, difficulty, mute, current_score , stars

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

    masks = [rocketL_mask, rocket_mask, rocketR_mask]
    rockets = [rocket_L, rocket, rocket_R]
    number = 1  # 0 for left, 1 for Straight, 2 for right

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
    game_over_image = pygame.transform.scale(game_over_image, (screen_width // 2, screen_height // 2))
    for _ in range(3):  # number of blocks
        blocks.append(Block(screen_width))

    showhit = 0
    font = pygame.font.Font(None, 300)

    font2 = pygame.font.Font(None, 20)

    def blit_message(msg):
        screen.blit(msg, (20, screen_height - 20))

    next_block_after = 100
    after = 600

    stars = pygame.transform.scale(stars, (screen_width, screen_height))
    stars_y = 0
    gap = -1 * stars.get_height()
    stars_y2 = gap

    ## Play Scene-1 and store new value of mute
    scene.GameStartScene(screen_width, screen_height,mute)
    mute = scene.is_mute

    if not mute:
        start_sound.play()

    bg_music.set_volume(0)
    channel2 = bg_music.play()


    if mute:
        channel2.pause()
    bg_music.set_volume(70)


    game_over_vid_playOneTime = True
    while running:
        if (not channel2.get_busy()) and not game_over and not mute:
            channel2.play(bg_music)

        message_text = font2.render(f"{messages[current_message]}", True, (255, 255, 255))

        if (score - temp_score3) >= 600:
            if current_message == max_message - 1:
                current_message = 0
            else:
                current_message += 1
            temp_score3 = score

        if not blocks:  # If there are no asteriods on the screen, don't stop further calculation
            blit_message(message_text)

            next_block_after -= 1
            score += 0.5
            current_score = score
            if next_block_after <= 0:
                blocks.append(Block(screen_width))  # create new

                next_block_after = random.randint(0, int(after))
            continue
        if not paused:
            screen.fill((0, 0, 0))
            screen.blit(stars, (0, stars_y))
            screen.blit(stars, (0, stars_y2))

            stars_y += 6
            stars_y2 += 6
            if stars_y >= stars.get_height():
                stars_y = gap
            if stars_y2 >= stars.get_height():
                stars_y2 = gap

            screen.blit(rockets[number], (x, y))

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

            offset = (block.x - x, block.y - y)
            if masks[number].overlap(block.block_mask, offset):
                if block.isheart:
                    if life < 3:
                        life += 1
                    if not mute:
                        life_added_sound.play()
                    blocks.remove(block)

                # Game Over
                elif life <= 1:
                    # Play Game Over Scene
                    if not paused and not mute:
                        channel2.fadeout(2000)
                    if game_over_vid_playOneTime:

                        # Play Scene-2 and store new value of mute | I forogot to use `if __name__ == '__main__':`
                        scene.GameOverScene(screen_width,screen_height,mute)
                        mute = scene.is_mute
                        game_over_vid_playOneTime = False
                    if not paused and not mute:
                        game_over_sound.play()
                    paused = True
                    game_over = True
                    save_score(score)

                else:
                    if not mute:
                        collide_sound.play()
                    blocks.remove(block)
                    life -= 1
                    showhit = 5  # For 5 frames

            # Hitting boundries changes Asteroids direction
            if not block.isheart and not block.iscomet:
                if block.x <= -30:
                    block.turn = False
                elif block.x >= screen_width - 80:
                    block.turn = True

            if not paused:
                score += 0.5
                current_score = score
                if block:
                    block.move()
            if block and not game_over:
                block.draw()
            if block:
                if block.y > screen_height:
                    blocks.remove(block)  # destroy asteroid
            if next_block_after <= 0:
                if len(blocks) < random.randint(4, lvl_difficult):  # to avoid too many obstacles on screen
                    blocks.append(Block(screen_width))  # create new asteroid

                next_block_after = random.randint(0, int(after))
            next_block_after -= 1
            if not paused:
                if (score - temp_score2) == 1000:
                    lvl_difficult += 1
                    if difficulty < lvl_difficult:
                        lvl_difficult = 5
                    temp_score2 = score
                if (score - temp_score) >= 50:
                    after -= random.randint(0, 50)
                    temp_score = score
                if after <= 50:
                    after += 500

        # Show Red Screen On Hit
        if showhit != 0:
            rect_curface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            rect_curface.fill((255, 0, 0, 70))
            screen.blit(rect_curface, (0, 0))

            hit_text = font.render("HIT", 1, (255, 255, 255))
            screen.blit(hit_text, (screen_width // 2 - 180, screen_height // 2 - 100))
            showhit -= 1

        if paused and game_over:
            screen.blit(game_over_image, (screen_width // 4, screen_height // 4))
        else:
            show_score(life, score, screen)
        if game_over:
            ismax_score = high_score()
            font = pygame.font.Font(None, 40)
            final_score = font.render(f"{int(score)}", True, (255, 255, 255))
            screen.blit(final_score, final_score.get_rect(center=(screen_width / 2, screen_height / 2 + 20)))
            max_score = font.render(f"{ismax_score if ismax_score > score else int(score)}", True, (255, 255, 255))
            screen.blit(max_score, max_score.get_rect(center=(screen_width // 2, screen_height // 2 + 90)))
        if not paused:
            blit_message(message_text)

        # Window Management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    running = False
                    paused = False
                    life = save_life
                    starting_screen()
                elif event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                    else:
                        paused = True
                if event.key == pygame.K_m:

                    if mute:
                        channel2.unpause()
                        mute = False
                    elif not mute:
                        channel2.pause()
                        mute = True



        else:
            clock.tick(FPS)
            pygame.display.update()

update_bar(70)
starting_bg = pygame.image.load("assets\\Background_Start.jpg")
starting_bg = pygame.transform.scale(starting_bg, (screen_width, screen_height))

randx, randy = 0, 0

update_bar(80)
def starting_screen():
    global randx, randy, mute
    pygame.event.clear()
    On = True
    angle = 0
    menu_cound.set_volume(0)
    channel = menu_cound.play()
    if mute:
        channel.pause()
    menu_cound.set_volume(100)
    while On:
        if not channel.get_busy() and not mute:
            channel.play(menu_cound)

        barder = random.randint(5, 13)

        angle += 10
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
                        channel.unpause()
                        mute = False
                    elif not mute:
                        channel.pause()
                        mute = True

        if not On:
            break

        # Making Some Animation
        colors = [(255, 255, 255), (0, 255, 255), (255, 255, 0)]

        for _ in range(10):
            # time.sleep(0.01)
            color = random.choice(colors)
            randx = random.randint(0, screen_width - 50)
            randy = random.randint(0, screen_height - 50)
            size = random.randint(1, 3)
            pygame.draw.circle(screen, color, (randx, randy), size)

        pygame.draw.rect(screen, (255, 255, 255), ((screen_width // 2 - 230), (screen_height // 2 - 150), 460, 290),
                         barder)

        txt = "Controls: W,A,S,D or Arrow Keys"
        control_text = load_font.render(txt, 1, (255, 255, 100))
        screen.blit(control_text, control_text.get_rect(center=(screen_width // 2, screen_height // 2 + 250)))

        clock.tick(7)
        pygame.display.update()
update_bar(100)

l_screen.stop(quit_pygame=False)
while l_screen.running:
    l_screen.wait(0.5)
pygame.display.update()
screen = pygame.display.set_mode((screen_width, screen_height))
starting_screen()

pygame.quit()
