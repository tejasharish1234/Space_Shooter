if __name__ == '__main__':
    def game_loop():
        #importing necessary modules
        import pygame
        import random

        pygame.init()
        pygame.font.init()

        #creating the screen
        screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Space Fighters")

        #importing images
        rocketship = pygame.image.load('images/fighter.png').convert_alpha()
        asteroid_img = pygame.image.load('images/fireball_1.png').convert_alpha() 
        missile_img = pygame.image.load('images/Bullet.png').convert_alpha()
        bg =  pygame.image.load('images/bg.jpg')

        class rocket(object):
            
            def __init__(self  ): 
                '''These variables are initialized to all objects of this class. The values are independent 
                of other objects of the same class.'''
                self.x = random.randrange(200,900)                      #rocket's co-ordinates: moves only horizontally, no vertical motion
                self.y = 600
                self.vel = 10               #rocket velocity
                self.health = 100           #earth's health
                #self.destroyed = False            #flag variable to check if earth has survived the attack or has been destroyed
                self.attack_cooldown = 0     #variable to allow only one missile to be fired every 3 iterations
            
            def draw(self):                                             #fn called in maindraw
                screen.blit(rocketship, (self.x, self.y))               #displays the image on the screen at the x&y coordinates              
            
            def attack(self):                                            #fn called every time space is pressed
                # case that missile has just been shot, the cooldown is set back to 3 so there is a gap between shots.(makes the animation smoother)
                if self.attack_cooldown == 0:    
                    self.attack_cooldown =  3
                    #assigning variables to the missile class
                    bulletss(self.x, self.y)
            
            def life(self):                       #fn called in maindraw
                #draw a shape (screen, color, shape(x,y,length, width))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(100, 45, 100, 20))
                
                if self.health == 100:
                    color = (0, 255, 0)       #green
                    pygame.draw.rect(screen, color, pygame.Rect(100, 45, self.health, 20))

                elif self.health == 75:
                    color = (255, 255, 0)     #yellow
                    pygame.draw.rect(screen,color, pygame.Rect(100, 45, self.health, 20))
                    
                elif self.health == 50:
                    color = (255, 165, 0)     #orange
                    pygame.draw.rect(screen,color, pygame.Rect(100, 45, self.health, 20))

                elif self.health == 25:
                    color = (255, 0, 0)       #red
                    pygame.draw.rect(screen,color, pygame.Rect(100, 45, self.health, 20))

                elif self.health == 0:
                    color = (0, 0, 0)         #black
                    pygame.draw.rect(screen,color, pygame.Rect(100, 45, self.health, 20))               

        #---------------------------------------------------------------------------

        class asteroid(object):
            def __init__(self,name): 

                self.name = name                        
                self.x = random.randint(100,900)        #asteroid's starting co-ordinates
                self.y = 20                                              
                self.vely = 5                           #asteroid's velocity
                self.check_hit = False                      #flag variable to check if asteroid has attacked earth

            def draw(self):                             #fn called in maindraw()
                nonlocal screen                                               
                self.destroy()
                self.kill_earth()
                screen.blit(asteroid_img, (self.x, self.y))                                #displayed on screen
                self.y += self.vely
            
            def destroy(self):                          #fn called in draw()
                nonlocal score, running_dict, bull_iterable
                #if the player is within the coordinates of the rival, rival is terminated and is removed from the screen and game.
                
                for x in bulletss.bullet_list:
                    if (self.x < x[0] < self.x + 100) and (self.y < x[1] < self.y + 120):
                        #setting the value of enemy key to none so it cannot be called/ drawn in the game again.
                        running_dict [self.name] = None 
                        #100 points increment per kill.
                        score += 100   
                        bulletss.bullet_list.remove(x)
                        bull_iterable -= 1

            def kill_earth(self):                       #fn called in draw()
                if self.check_hit == False:
                    if self.y > 550:
                        millenium_falcon.health -=25
                        self.hit = True
                        running_dict[self.name] = None

        #---------------------------------------------------------------------------

        class bulletss(object):
            #list of bullets queued to be fired
            bullet_list = []     
            #bullet velocity                       
            vel = 30   

            def __init__(self,px, py):
                #checking if the bullet list has less than 5 bullets, proceeding to move bullet.
                if len(self.bullet_list) < 5:  
                    
                    #the bullet with required configuration is appended into bullet list and queued for firing.
                    self.bullet_list.append([px + 48 ,py + 80]) 
                    
                else:
                    #if there are 5 bullets in the list the last bullet is removed from the list to make space for a new bullet on screen.
                    self.bullet_list.pop()   

            def movebull(self,i): 
                #i is the list containing the information about the configuration of that bullet.
                i[1] -= self.vel 
                #deleting bullets 
                bulletss.delete(self,i) 
            

            def delete(self,i):
                nonlocal bull_iterable
                #if bullet hits the edges, it is deleted
                if i[0] > 1200 or i[1] > 800 or i[1] < 0 or i[0] < 0: 
                    self.bullet_list.remove(i)
                    bull_iterable -=1
        #---------------------------------------------------------------------------

        #setting a font to be used to display text on screen
        font = pygame.font.SysFont('Comic Sans MS', 25)
        health_text = font.render('Health: ', False, (0, 0, 0), (122,122,122))
        millenium_falcon = rocket()
        rival0 = asteroid('rival0')
        running_dict = {'rival0':rival0}
        not_running_dict = {}

        for val in range(1,48):
            x = 'rival{}'.format(val)
            not_running_dict[x] = asteroid(x)

        def maindraw():                                 #draws all characters on screen}
            screen.blit(bg, (0,0))                      #draws the screen bg
            for enemy in running_dict:
                if running_dict[enemy] != None:
                    running_dict[enemy].draw()

            millenium_falcon.draw()
            rocket.life(millenium_falcon)
            score_text = font.render('Score: {}'.format(score), False, (0, 0, 0),(122,122,122))
            screen.blit(score_text, (0,0))
            screen.blit(health_text, (0,40))
            timelabel = font.render("Time - {} s".format(seconds), False, (0,0,0), (122,122,122))
            screen.blit(timelabel, (1050,0))
            
            if len(bulletss.bullet_list) != 0:
                i = bulletss.bullet_list[bull_iterable]
                screen.blit(missile_img, (i[0], i[1]))                             #displays bullet on screen
                bulletss.movebull(bulletss,i)                                  #fn to move bullet
            
            pygame.display.update()                     #updates screen to show all characters 

        clock = pygame.time.Clock()
        score = 0
        milliseconds = 0                            
        seconds = 0                                 #time in seconds
        new_guy_timer = 0                           #time in 
        bull_iterable = 0                                       #iterable to iterate through bullet_list
        running = True

        #---------------------------------------------------------------------------

        while running:                                                         #game loop
            clock.tick(32) 
                                                    #32 ms delay for better accuracy
                
            for event in pygame.event.get():                                
                if event.type == pygame.QUIT:                                  #if game is closed
                    running = False                                            #stop the game

                if event.type == pygame.KEYUP:                                 #if no key is pressed
                    millenium_falcon.dir = None                                             #moving in no direction
                
            if millenium_falcon.health == 0:                                                #if the player has no health
                running = False                                                #stop the game

            if seconds >= 120:
                running = False
            
            if bull_iterable < len(bulletss.bullet_list) - 1:                              #so that index does not go out of range
                bull_iterable += 1                                                         #increment iterable
            else:
                bull_iterable = 0                                                          #reset to 0 if it is out of range

            keys = pygame.key.get_pressed()                                    #list of all keys on keyboard
            
            if keys [pygame.K_LEFT] or keys [pygame.K_a] :                     #when the left arrow key or 'a' is pressed,
                millenium_falcon.x -= millenium_falcon.vel                     #rocket co-ordinate changes with assigned velocity,
                
            elif keys [pygame.K_RIGHT] or keys [pygame.K_d]  :
                millenium_falcon.x += millenium_falcon.vel
                
            if keys[pygame.K_SPACE]:
                millenium_falcon.attack()
                millenium_falcon.attack_cooldown -= 1


            milliseconds += clock.tick_busy_loop(150)
            if milliseconds > 150:                                          
                seconds += 1                                                #increment time
                new_guy_timer += 1                                          #variable for adding new player on screen
                milliseconds -= 150

            if seconds < 30:
                if new_guy_timer == 4:                              
                    # if more than 5s have elapsed and if there are enemies have not yet been displayed on screen
                    new_guy_timer = 0                                       #reset timer to 0
                    x = not_running_dict.popitem()                          #remove them from not_running_dict
                    running_dict [x[0]] = x[1]                                #and add to running_dict
            
            elif seconds >=30 and seconds <=60:
                
                if new_guy_timer == 3:
                    new_guy_timer = 0                                       #reset timer to 0
                    x = not_running_dict.popitem()                          #remove them from not_running_dict
                    running_dict [x[0]] = x[1]                                #and add to running_dict
                elif new_guy_timer > 3:
                    new_guy_timer = 2
            else:
                if new_guy_timer == 2:
                    new_guy_timer = 0                                       #reset timer to 0
                    x = not_running_dict.popitem()                          #remove them from not_running_dict
                    running_dict [x[0]] = x[1]                                #and add to running_dict
                elif new_guy_timer > 2:
                    new_guy_timer = 1
            
            #boundary condn: so that character does not go out of bounds 
            if millenium_falcon.x <= 0 :                                                     
                millenium_falcon.x = 0

            elif millenium_falcon.x >= 1080:
                millenium_falcon.x = 1080

            screen.fill((0,0,0))
            maindraw()                                                         #all draw functions are called here
            
        pygame.quit()                                                          #closes pygame

        return score, seconds
    game_loop()
