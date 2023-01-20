import sys, pygame, copy
from pygame import *
pygame.init()

DISPLAYSURF = pygame.display.set_mode((1400, 700))
pygame.display.set_caption('Knight_OOP')

goblins = []
platforms = []

player_sprite_sheet = pygame.image.load('AnimationSheet_Character.png').convert_alpha()
backroundimage = pygame.transform.scale(pygame.image.load('entrance.png'), (1400, 700))
backround_rect = (0, 0, 1400, 700)

# Create a 2D array to represent the tile map (20 tiles by 10 tiles)
tile_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]




tile_images = [pygame.transform.scale(pygame.image.load('platformobject_045.png').convert_alpha(), (70, 70)),
              pygame.transform.scale(pygame.image.load('platform_009.png').convert_alpha(), (70, 70)),
              pygame.transform.scale(pygame.image.load('platform_004.png').convert_alpha(), (70, 70))]



def extractSprites(rows, columns, sprite_width, sprite_height, sprites, name_of_sprite_sheet_file, xsize, ysize):
    sprite_sheet = pygame.image.load(name_of_sprite_sheet_file).convert_alpha()
    for row in range(rows):
        for column in range(columns):
            x = column * sprite_width
            y = row * sprite_height
            width = sprite_width
            height = sprite_height

            # Use subsurface to extract the sprite
            sprite = sprite_sheet.subsurface((x, y, width, height))
            scaled_sprite = pygame.transform.scale(sprite, (xsize, ysize))

            # Add the sprite to the list
            sprites.append(scaled_sprite)




dog_spawn = USEREVENT + 7
goblin_spawn = USEREVENT + 8
damage_cooldown_period_over = USEREVENT + 9
#pygame.time.set_timer(dog_spawn, 4000) un comment if you want the dog
dogimage = pygame.transform.scale((pygame.image.load('pitbull_2.0 (1).png')), (250, 250)).convert_alpha()
dog_rect = pygame.Rect(-200, 100, 150, 150)
# sky_rect = pygame.Rect(0, 0, 1400, 700)
# skyimage = pygame.transform.scale((pygame.image.load('Sky.png')), (1400, 700))


UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
NONE = 'none'
white = (255, 255, 255)
black = (0, 0, 0)


fpsClock = pygame.time.Clock()
FPS = 60
idlechange = USEREVENT + 1
running_change = USEREVENT + 2
sprite_update = USEREVENT + 3
goblin_update = USEREVENT + 4
pygame.time.set_timer(idlechange, 450)
pygame.time.set_timer(running_change, 50)

class Platform(pygame.sprite.Sprite):
    
    def __init__(self, topleftx, toplefty, width, height):
        self.rect = pygame.Rect(topleftx, toplefty, width, height)
        self.image = pygame.transform.scale(pygame.image.load('platformobject_091.png').convert_alpha(), (width, height))
        self.mask = pygame.mask.from_surface(self.image)



class Player(pygame.sprite.Sprite):
    current_sprite = 0
    

        # Define the width and height of each sprite
    sprite_width = 32
    sprite_height = 32

    # Define the number of sprites in the sheet (rows and columns)
    rows = 9
    columns = 8

    # Create an empty list to store the sprites
    sprites = []

    # Loop through the rows and columns to extract each sprite
    for row in range(rows):
        for column in range(columns):
            x = column * sprite_width
            y = row * sprite_height
            width = sprite_width
            height = sprite_height

            # Use subsurface to extract the sprite
            sprite = player_sprite_sheet.subsurface((x, y, width, height))
            scaled_sprite = pygame.transform.scale(sprite, (100, 100))

            # Add the sprite to the list
            sprites.append(scaled_sprite)

   
    zsprites = [None]*50

    # idle sprites
    zsprites[0] = sprites[0]
    zsprites[1] = sprites[1]
    zsprites[2] = sprites[8]
    zsprites[3] = sprites[9]

    # running sprites
    zsprites[4] = sprites[24]
    zsprites[5] = sprites[25]
    zsprites[6] = sprites[26]
    zsprites[7] = sprites[27]
    zsprites[8] = sprites[28]
    zsprites[9]= sprites[29]
    zsprites[10] = sprites[30]
    zsprites[11] = sprites[31]

    # jumpign sprites
    zsprites[12] = sprites[40]
    zsprites[13] = sprites[41]
    zsprites[14] = sprites[42]
    zsprites[15] = sprites[43]
    zsprites[16] = sprites[44]
    zsprites[17] = sprites[45]
    zsprites[18] = sprites[46]
    zsprites[19] = sprites[47]
    
    # attack sprites
    zsprites[20] = sprites[64]
    zsprites[21] = sprites[65]
    zsprites[22] = sprites[66]
    zsprites[23] = sprites[67]
    zsprites[24] = sprites[68]
    zsprites[25] = sprites[69]
    zsprites[26] = sprites[70]
    zsprites[27] = sprites[71]
    
    rect = pygame.Rect(200, 200, 100, 100)
    rect.bottom = 560
    image = zsprites[0]
    mask = pygame.mask.from_surface(image)
    gravity = 0
    on_ground = True
    
    is_idling = True
    
    above_platform = False
    direction_facing = RIGHT
    already_flipped = False
    health = 10
    no_x_movement = True
    attacking = False
    health = 5
    damage_cooldown_period = False

    def attack(self):
        self.attacking = True

    def jump(self):
        self.gravity = -15
        self.on_ground = False

    def damaged(self):
        self.health -= 1
        self.damage_cooldown_period = True
        pygame.time.set_timer(damage_cooldown_period_over, 1000)

    def updateimage(self):

        if self.attacking == True:
            if self.current_sprite > 26 or self.current_sprite < 20:
                self.current_sprite = 20
            elif self.current_sprite == 26:
                self.current_sprite = 27
                self.attacking = False
            else:
                self.current_sprite += 1

            self.image = self.zsprites[self.current_sprite]
            pygame.time.set_timer(sprite_update, 50)
            self.already_flipped = False

        elif self.is_idling:
            if self.current_sprite >= 3: # the index of the fourth and final sprite in the idle animation
                self.current_sprite = 0
                self.image = self.zsprites[self.current_sprite]
                
            else:
                
                self.current_sprite += 1
                self.image = self.zsprites[self.current_sprite]

            pygame.time.set_timer(sprite_update, 300)
            self.already_flipped = False
        elif self.on_ground == False:
            if self.current_sprite >= 19 or self.current_sprite < 12:
                self.current_sprite = 12
                self.image = self.zsprites[self.current_sprite]
            else:
                self.current_sprite += 1
                self.image = self.zsprites[self.current_sprite]
            pygame.time.set_timer(sprite_update, 200)
            self.already_flipped = False
        else:
            if self.current_sprite >= 11 or self.current_sprite < 4: # the 8th and final frame in the running animation
                self.current_sprite = 4
                self.image = self.zsprites[self.current_sprite]
            else:
                self.current_sprite += 1
                self.image = self.zsprites[self.current_sprite]
                
            pygame.time.set_timer(sprite_update, 120)
            self.already_flipped = False

    def CheckIfOnGround(self, platforms, floorlevel):
        for i in range(len(platforms)):
            if self.rect.bottom >= floorlevel:
                self.rect.bottom = floorlevel
                return True

            elif pygame.sprite.collide_mask(self, platforms[i]) and self.gravity >= 0 and self.rect.bottom > (platforms[i].rect.top - 25)  and (self.rect.bottom < platforms[i].rect.top + 25):
                return  True

        
        return False

    

class Goblin(pygame.sprite.Sprite):

    sprite_width = 150
    sprite_height = 150
    sprites = []
    widthOfGoblin = 300
    heightOfGoblin = 300
    
    extractSprites(1, 8, sprite_width, sprite_height, sprites, 'Run.png', widthOfGoblin, heightOfGoblin)
    extractSprites(1, 4, sprite_width, sprite_height, sprites, 'Idle.png', widthOfGoblin, heightOfGoblin)
    extractSprites(1, 4, sprite_width, sprite_height, sprites, 'Death.png', widthOfGoblin, heightOfGoblin)
    extractSprites(1, 8, sprite_width, sprite_height, sprites, 'Attack.png', widthOfGoblin, heightOfGoblin)
    extractSprites(1, 4, sprite_width, sprite_height, sprites, 'Take Hit.png', widthOfGoblin, heightOfGoblin)

    already_flipped = False
    direction_facing = LEFT
    dying = False
    
    current_sprite = 0
    image = sprites[0]
    pygame.time.set_timer(goblin_update, 1500)
    

    
    def __init__(self, *args):
        if len(args) > 0:
            self.rect = pygame.Rect(200, 200, 300, 300)
            self.rect.bottom = 400
            self.image = self.sprites[0]
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.rect = pygame.Rect(1400, 700, 300, 300)
            self.rect.bottom = 665
            self.image = self.sprites[0]
            self.mask = pygame.mask.from_surface(self.image)
        
        

    def updateimage(self):
        if self.dying == True:
            if self.current_sprite > 15 or self.current_sprite < 12:
                self.current_sprite = 12
            elif self.current_sprite == 15:
                goblins.remove(self)
            else:
                self.current_sprite += 1

            self.image = self.sprites[self.current_sprite]
            pygame.time.set_timer(goblin_update, 100)
            self.already_flipped = False

        else:
            if self.current_sprite >= 7:
                self.current_sprite = 1
            else:
                self.current_sprite += 1
            self.image = self.sprites[self.current_sprite]
            pygame.time.set_timer(goblin_update, 100)
            self.already_flipped = False

    def advance_goblin(self):
        self.rect.x -= 3

    

        
class app():
    player = Player()
    goblins.append(Goblin())
    platforms.append(Platform(4 * 70, 5 * 70, 70 * 4, 70))
    platforms.append(Platform(700, 200, 200 , 200))
    platforms.append(Platform(1000, 300, 300, 50))

    

    #goblins.append(Goblin(500, 400))
    pygame.time.set_timer(sprite_update, 100)
    
    pygame.time.set_timer(goblin_spawn, 2000)
    
    
   

    while True:

        #player_rect_at_start = player.rect.copy() # we will use this later to check if there was movement (to know if the player is idling)
        player.mask = pygame.mask.from_surface(player.image) # we will use this for collisions

        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_RIGHT]:
            player.rect.x += 10
            player.direction_facing = RIGHT
            player.no_x_movement = False
            
        elif keysPressed[pygame.K_LEFT]:
            player.rect.x -= 10
            player.direction_facing = LEFT
            player.no_x_movement = False
            

        else: 
            player.no_x_movement = True

        if keysPressed[pygame.K_r]:
            player.attack()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and player.on_ground == True:
                if event.key == K_UP:
                    player.jump()
                    
            if event.type == sprite_update:
                player.updateimage()
                if player.direction_facing == LEFT:
                    player.image = pygame.transform.flip(player.image, True, False)

            if event.type == goblin_update:
                for goblin in goblins:
                    goblin.updateimage()
                    if goblin.direction_facing == LEFT:
                        goblin.image = pygame.transform.flip(goblin.image, True, False)

            if event.type == goblin_spawn:
                
                goblins.append(Goblin())
                
                
                pygame.time.set_timer(goblin_spawn, 6000)

            if event.type == dog_spawn:
                dog_rect.x = 1600
                dog_rect.bottom = 470
                # if dog_speed_multiplier <= 3.5:
                #     #dog_speed_multiplier = dog_speed_multiplier + .33
                # else: 
                #     #dog_speed_multiplier = 3.5

            if event.type == damage_cooldown_period_over:
                player.damage_cooldown_period = False
                
 
        # collisions
    
        for goblin in goblins:
            if pygame.sprite.collide_mask(player, goblin) and player.damage_cooldown_period == False:
                player.damaged()
                #goblins.remove(goblin)
                goblin.dying = True
                
            
            
        
        if player.on_ground == False:
            player.gravity += .5
            player.rect.y += player.gravity
        else:
            player.gravity = 0


        player.on_ground = player.CheckIfOnGround(platforms, 560)
       


        if player.rect.right > 1400:
            player.rect.right = 1400

        if player.rect.left < 0:
            player.rect.left = 0

       

        if player.no_x_movement == True and player.on_ground == True:
            player.is_idling = True
        else:
            player.is_idling = False

        if pygame.Rect.colliderect(player.rect, dog_rect) and player.damage_cooldown_period == False:
            player.damaged()
            #pygame.mixer.Sound.play(barkSound)

        dog_rect.x -= 10 

        for i in range(len(goblins)):
            goblins[i].advance_goblin()


        
        text = (f"""{player.direction_facing}, gravity: ,{player.gravity} , on_ground: {player.on_ground},
         idling: {player.is_idling}, current_sprite: {player.current_sprite}, goblins:  {len(goblins)}
        , player.health = {player.health}""")
        

       
        textSurf = pygame.font.Font('Pixeltype.ttf', 40).render(text, True, white, black)
        text_rect = textSurf.get_rect()
        text_rect.center = (600, 25)

        
        

        DISPLAYSURF.blit(backroundimage, backround_rect)


        # cells = [None*10][None*20]   
        # for row in range(len(tile_map)):
        #     for col in range(len(tile_map[row])):
        #         cell[row][col] = pygame.Rect(col*70, row*70, 70, 70)
                



        for row in range(len(tile_map)):
            for col in range(len(tile_map[row])):
                tile_type = tile_map[row][col]
                tile_image = tile_images[tile_type]
                DISPLAYSURF.blit(tile_image, (col * 70, row * 70))


        DISPLAYSURF.blit(textSurf, text_rect)
        DISPLAYSURF.blit(dogimage, dog_rect)
        
        

        for i in range(len(goblins)):
            DISPLAYSURF.blit(goblins[i].image, goblins[i].rect)

        for i in range(len(platforms)):
            DISPLAYSURF.blit(platforms[i].image, platforms[i].rect)

        DISPLAYSURF.blit(player.image, player.rect)
        
        pygame.display.update()
        fpsClock.tick(FPS)
        

