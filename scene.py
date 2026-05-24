import pygame
import sys
import splashscreen_engine as splash # For Video Playing | pip install splashscreen-engine


pygame.init()
loadimg = pygame.image.load
pygame.display.set_caption("My Story")
pygame.mixer.init()

is_mute = False
class GameOverScene:
    def __init__(self, width, height,mute=is_mute):
        global is_mute
        window= splash.Screen(title_bar=True)
        window.size(width,height)
        window.start()
        window.title("GameOver")

        skip_text = splash.Text(window,"Press `Space` to Skip.","lucida handwriting",30,"down")
        skip_text.show()
        bg_vid = splash.BackgroundVideo(window,"assets/Scenes/gameOverVid.mp4",fps=60)
        bg_vid.play()

        window.wait(0.5)
        sound1 = pygame.mixer.Channel(0)
        sound1.set_volume(0)
        if not mute:
            sound1.set_volume(0.2)
        gameOverSound = pygame.mixer.Sound("assets/Scenes/gameOverSound.mp3")
        sound1.play(gameOverSound)
        while bg_vid.is_playing:

            for event in pygame.event.get():
                # Handle window close
                if event.type == pygame.QUIT:
                    sound1.stop()
                    window.stop()
                    sys.exit()  # Safely exits the entire Python script
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:

                        if mute:
                            mute = False
                            sound1.set_volume(0.2)
                        else:
                            mute = True
                            sound1.set_volume(0)
                        is_mute = mute
                    if event.key == pygame.K_SPACE:
                        sound1.stop()
                        window.stop(quit_pygame=False)
                        pygame.display.update()
                        return

        window.stop(quit_pygame=False)


class GameStartScene:
    def __init__(self, width, height,mute=is_mute):
        global is_mute

        window= splash.Screen(title_bar=True)
        window.size(width, height)
        window.start()


        window.title("Rocket Game")

        bg_vid = splash.BackgroundVideo(window,"assets/Scenes/gameStartVid.mp4",fps=60)
        bg_vid.play()
        skip_text = splash.Text(window, "Press `Space` to Skip.", "lucida handwriting", 30,"down")
        skip_text.show()



        # window.wait(1)
        sound1 = pygame.mixer.Channel(0)
        sound1.set_volume(0)
        if not mute:
            sound1.set_volume(100)
        gameStartSound = pygame.mixer.Sound("assets/Scenes/gameStartSound.mp3")
        sound1.play(gameStartSound)
        while bg_vid.is_playing:

            for event in pygame.event.get():
                # Handle window close
                if event.type == pygame.QUIT:
                    sound1.stop()
                    window.stop()
                    sys.exit()  # Safely exits the entire Python script
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:

                        if mute:
                            mute = False
                            sound1.set_volume(100)
                        else:
                            mute = True
                            sound1.set_volume(0)
                        is_mute = mute
                    if event.key == pygame.K_SPACE:
                        sound1.stop()
                        window.stop(quit_pygame=False)
                        pygame.display.update()
                        return
        sound1.fadeout(3)

        window.stop(quit_pygame=False)

