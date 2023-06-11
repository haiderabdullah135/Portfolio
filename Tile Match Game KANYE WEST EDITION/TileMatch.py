import pygame, cv2, random, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x , y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('images/aliens/' + filename)

        self.back_image = pygame.image.load('images/aliens/' + filename)
        pygame.draw.rect(self.back_image, Gold_LV, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False


#contains all logic for the Game
class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False

        #aliens

        self.all_aliens = [f for f in os.listdir('images/aliens') if os.path.join('Images/Aliens', f)]

        self.img_width, self.img_height = [128, 128]
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()



        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate lvel design first level
        self.generate_level(self.level)


        #initialize background video

        self.is_video_playing = True
        self.play =  pygame.image.load('Images/play.png').convert_alpha()
        self.stop =  pygame.image.load('Images/stop.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright = ((windowHeight + 507), 60))
        self.get_video()

        # initialize music
        self.is_music_playing = True
        self.sound_on = pygame.image.load('Images/sound.png').convert_alpha()
        self.sound_off = pygame.image.load('Images/mute.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright = (windowWidth - 10 , 10))

        # load music randomly
        randomMusicFile = random.choice(all_mp3)
        pygame.mixer.music.load(randomMusicFile)
        pygame.mixer.music.play()


# background video code . success is that the video was found properly and img means all the frames are stored in img. self capture read.
    def get_video(self):
        self.cap = cv2.VideoCapture('Video/earth.mp4')
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]


#all the cards flipping and level changes basically action of the game toggling of buttons
    def update(self, event_list):
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)


    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                #event.button 1 is LMB 2 is scroll wheel button and 3 is RMB
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # iteration for tiles in the tile group
                    for tile in self.tiles_group:
                        #each tile is assigned a rect to react to the mouse button for action
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            # make sure there are 2 images and if you have 2 images then make sure they are 2 different images. if they are the same to block the game so that you cannot click on the images again. basically youve matched them so do not click them again. this is basically a temp array in which only 2 images can go at the same time. so following code will be if the images are not the same therefore game will not block these images and they will be reflipped in a sense.
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break

# frame count += 1 is for to add a time break in between choosing tiles.
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False
                # is to check the tiles in flipped arrays which always have 2 tiles and hide them and then reset the flipped array so the next 2 images can come in.
                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []





    def generate_level(self, level):
        self.aliens = self.select_random_aliens(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.aliens)

    def generate_tileset(self, aliens):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        #tiles alignment code
        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2

        #generating tiles code
        tiles = []
        self.tiles_group.empty()
# for loop for generating tiles

        for i in range(len(aliens)):
            #x and y determine each tiles position
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(aliens[i], x, y)
            self.tiles_group.add(tile)



    def select_random_aliens(self, level):
        # random sample will randomly select from a list which is self.all_aliens and the sub brackts will select a specific number of items here self.level = 1 so 1 plus 1 plus 2 = 4 so first level is 4 images. then next level will be 2 so 2 plus 2 + 2 equals to 6 so second level will have 6 images and so on
        aliens = random.sample(self.all_aliens, (self.level + self.level + 2))
        aliens_copy = aliens.copy()
        aliens.extend(aliens_copy)
        random.shuffle(aliens)
        return aliens




    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()

                if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):

                    if self.is_video_playing:
                        self.is_video_playing = False
                        self.video_toggle = self.stop
                    else:
                        self.is_video_playing = True
                        self.video_toggle = self.play

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level =+ 1
                    if self.level >= 6:
                        self.level = 1
                    self.generate_level(self.level)


# level is not advancing to the next stage. also see why video is not looping. and add more icons like drakes album or kanyes faces

#is to be used to draw all the images video and text// total user interface code
    def draw(self):
        screen.fill(Brown_LV)

        #fonts
        title_font = pygame.font.Font('Fonts/futur.ttf', 48)
        content_font = pygame.font.Font('Fonts/futur.ttf', 24)
        secondTitle_font = pygame.font.Font('Fonts/futur.ttf', 38)
        level_font = pygame.font.Font('Fonts/futur.ttf', 34)

        #text
        title_text = title_font.render('MEMORY GAME', True, Gold_LV)
        secondTitle_text = secondTitle_font.render('KANYE WEST EDITION', True, Gold_LV)

        #rectanglar text box for title to help position it. it factors the entire screen not a separate box.
        title_rect = title_text.get_rect(midtop = (windowWidth // 2, 15))
        title_rect2 = secondTitle_text.get_rect(midtop = (windowWidth // 2, 67))

                                                                #true is for Anti Aliasing parameter
        level_text = level_font.render('LEVEL ' + str(self.level), True, Gold_LV)
        level_rect = level_text.get_rect(midtop = (windowWidth // 2, 110))


        info_text = content_font.render('Find 2 of Each Tile', True, Gold_LV)
        info_rect = info_text.get_rect(midtop = (windowWidth // 2, 152))

# background video frames are represendted as stream of bytes. we conveert those bytes into an image. then dimension (self.shape). blue green red is used instead of rgb because cv package used to capture video uses this color scheme. last parammter is the rectangle

        if self.is_video_playing:
            if self.success:
                screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))
            # loop video code
            else:
                self.get_video
        else:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))




        if not self.level == 5:
            next_text = content_font.render('Level complete! Press "SPACE" for the next level', True, Gold_LV)
        else:
            next_text = content_font.render('Congrats! GAME OVER BITCH', True, Gold_LV)

        next_rect = next_text.get_rect(midbottom = (windowWidth // 2, windowHeight - 40))

        #this code is used to display text in game screen
        screen.blit(title_text, title_rect)
        screen.blit(secondTitle_text, title_rect2)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)

        #code for drawing a rectangle around the toggle buttons to bring contrast to game
        pygame.draw.rect(screen, Gold_LV, (windowHeight + 455, 0, 65, 110))

        screen.blit(self.music_toggle, self.music_toggle_rect)
        screen.blit(self.video_toggle, self.video_toggle_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()



        if self.level_complete:
            screen.blit(next_text, next_rect)


pygame.init()

windowWidth = 1280
windowHeight = 760
screen = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Memory Game")


Brown_LV = (69, 54, 48)
Gold_LV = (155, 126, 75)
BLACK = (0, 0, 0)
RED = (225, 0, 0)


FPS = 60
clock = pygame.time.Clock()

#randomly pick songs from file code // ZZZ is random variable
path_music_files = (r"C:\Users\Haider Abdullah\Desktop\py4e\projects that need to be done\Tile Match Game\Sounds")
all_mp3 = [os.path.join(path_music_files, ZZZ) for ZZZ in os.listdir(path_music_files) if ZZZ.endswith('.mp3')]



game= Game()

#main init code for starting game
running = True
while running:
    event_list = pygame.event.get()
    #coding for quitting the game // also for the quit button.
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False


    game.update(event_list)



    pygame.display.update()
    clock.tick(FPS)



pygame.quit()
