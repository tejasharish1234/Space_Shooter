def game_loop():
    #importing necessary modules
    import pygame
    import random

    #initializing pygame and fonts 
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

    #setting a font to be used to display text on screen
    font = pygame.font.SysFont('Comic Sans MS', 25)

    class rocket(object):
        
        def __init__(self): 
            '''These variables are initialized to all objects of this class. The values are independent 
            of other objects of the same class.'''
            self.x = random.randrange(200,900)      #rocket's co-ordinates
            self.y = 600
            self.vel = 10               #rocket velocity
            self.health = 100           #earth's health
            self.shoot_cooldown = 0     #variable to allow only one missile to be fired every 3 iterations
        
        def draw(self):                                             #fn called in maindraw
            screen.blit(rocketship, (self.x, self.y))               #displays the image on the screen at the x&y coordinates              
        
        def shoot(self):                                            #fn called every time space is pressed
            # case that missile has just been shot, the cooldown is set back to 3 so there is a gap between shots.(makes the animation smoother)
            if self.shoot_cooldown == 0:    
                self.shoot_cooldown =  3
                missile(self.x, self.y)                             #assigning initialization variables to a missile
        
        def life(self):                                             #fn called in maindraw
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

            self.name = name                        #asteroid's name = asteroid+no
            self.x = random.randint(100,900)        #asteroid's starting co-ordinates
            self.y = 20                                              
            self.vely = 5                           #asteroid's velocity

        def draw(self):                             #fn called in maindraw()
            nonlocal screen                         
            #since the function draw() is within another function game_loop(), to access variables defined in game_loop, we use nonlocal and not global.                     
            self.destroy()
            self.kill_earth()
            screen.blit(asteroid_img, (self.x, self.y))
            self.y += self.vely
        
        def destroy(self):                          #fn called in draw()
            nonlocal score, running_dict, missile_list_iterable
            #if the missile is within the coordinates of the asteroid, asteroid is terminated and is removed from the screen and game.
            #since we need to check for all missiles, we use a for loop
            for x in missile.missile_list:
                if (self.x < x[0] < self.x + 100) and (self.y < x[1] < self.y + 120):
                    #setting the value of asteroid key to None so it cannot be called/ drawn in the game again.
                    running_dict [self.name] = None 
                    #100 points increment per kill.
                    score += 100   
                    missile.missile_list.remove(x)      #the missile is removed from the list and iterable value is reduced by 1 to prevent index out of range error.
                    missile_list_iterable -= 1

        def kill_earth(self):                       #fn called in draw()
            if self.y > 550:                        #if the asteroid has crossed this y coordinate, then the asteroid will strike earth and so earth loses health
                    millenium_falcon.health -=25
                    running_dict[self.name] = None  #asteroid value is set to None and wont be drawn in the game again.

    #---------------------------------------------------------------------------

    class missile(object):
        
        missile_list = []       #list of missiles to be fired
        vel = 30                #missile velocity                       

        def __init__(self,px, py):
            #checking if the missile list has less than 5 missiles, proceeding to move missile.
            if len(self.missile_list) < 5:  
                
                #the missile is appended into missile list and queued for firing. The +48 is so that it animation looks like missile is coming from under the rocket.
                self.missile_list.append([px + 48 ,py + 80]) 
                
            else:
                #more than 5 missiles are not allowed to have a smoother animation.
                self.missile_list.pop()   

        def movebull(self,i):           #fn called in maindraw()
            #i is a missile in missile list. i[1] is the y coordinate which reduces as missile is moving upwards.
            i[1] -= self.vel 
            missile.delete(self,i) 
        

        def delete(self,i):             #fn called in delete()
            nonlocal missile_list_iterable
            #if missile hits the edges, it is deleted
            if i[0] > 1200 or i[1] > 800 or i[1] < 0 or i[0] < 0: 
                self.missile_list.remove(i)
                missile_list_iterable -=1

    #---------------------------------------------------------------------------

    #initializing all the objects
    millenium_falcon = rocket()
    asteroid0 = asteroid('asteroid0')
    running_dict = {'asteroid0':asteroid0}          #asteroids to be drawn on screen
    not_running_dict = {}                           #asteroids to be drawn on screen in the future

    #creating required number of asteroids
    for val in range(1,32):
        x = 'asteroid{}'.format(val)
        not_running_dict[x] = asteroid(x)

    health_text = font.render('Health: ', False, (0, 0, 0), (122,122,122))

    def maindraw():                                 #draws all objects on screen, called in while loop as this needs to run infinitely till the game is stopped.
        screen.blit(bg, (0,0))                      #draws the screen background
        for asteroid in running_dict:
            if running_dict[asteroid] != None:
                running_dict[asteroid].draw()

        millenium_falcon.draw()
        screen.blit(health_text, (0,40))
        rocket.life(millenium_falcon)
        score_text = font.render('Score: {}'.format(score), False, (0, 0, 0),(122,122,122))
        screen.blit(score_text, (0,0))
        timelabel = font.render("Time - {} s".format(seconds), False, (0,0,0), (122,122,122))
        screen.blit(timelabel, (1050,0))
        
        if len(missile.missile_list) != 0:
            i = missile.missile_list[missile_list_iterable]
            screen.blit(missile_img, (i[0], i[1]))                             
            missile.movebull(missile,i)                                  
        
        pygame.display.update()                     #updates screen to show all objects 

    clock = pygame.time.Clock()
    score = 0
    milliseconds = 0                            
    seconds = 0                                 
    new_asteroid_timer = 0                      #time after which new asteroid is displayed on the screen
    missile_list_iterable = 0                   #iterable to iterate through missile_list
    running = True                              #flag variable to start the game loop

    #---------------------------------------------------------------------------

    while running:                                                         #game loop
        clock.tick(32)                                                     #32 ms delay for better accuracy
            
        for event in pygame.event.get():                                
            if event.type == pygame.QUIT:                                  #if game is closed
                running = False                                            
            
        if millenium_falcon.health == 0:                                   #if the earth has no health
            running = False                                                

        if seconds >= 65:                                                 #if the earth survives the attack for the duration of the game
            running = False
        
        keys = pygame.key.get_pressed()                                    #dictionary of all keys on keyboard
        
        if keys [pygame.K_LEFT] or keys [pygame.K_a] :                     #when the left arrow key or 'a' is pressed,
            millenium_falcon.x -= millenium_falcon.vel                     #rocket moves left with velocity = 10
            
        elif keys [pygame.K_RIGHT] or keys [pygame.K_d]:
            millenium_falcon.x += millenium_falcon.vel
            
        if keys[pygame.K_SPACE]:                                           #when space is pressed, the shoot fn is called
            millenium_falcon.shoot()
            millenium_falcon.shoot_cooldown -= 1

        if missile_list_iterable < len(missile.missile_list) - 1:          #so that index does not go out of range
            missile_list_iterable += 1                                     #increment iterable
        else:
            missile_list_iterable = 0                                      #reset to 0 if it is out of range

        milliseconds += clock.tick_busy_loop(150)
        if milliseconds > 150:                                          
            seconds += 1                                                   #increment time
            new_asteroid_timer += 1                                        #variable for adding new player on screen
            milliseconds -= 150

        if seconds < 25:
            if new_asteroid_timer == 3:                              
                #every 3 seconds an asteroid is drawn onto the screen
                new_asteroid_timer = 0                                    #reset timer to 0
                x = not_running_dict.popitem()                            #remove them from not_running_dict
                running_dict [x[0]] = x[1]                                #and add to running_dict
            
        elif 25 <= seconds <= 45:
            if new_asteroid_timer == 2:
                #every 2 seconds an asteroid is drawn onto the screen
                new_asteroid_timer = 0                                    
                x = not_running_dict.popitem()                           
                running_dict [x[0]] = x[1]                               
            
            elif new_asteroid_timer > 2:                                  #in case the variable reached a limit from the previous block that isn't checked by
                new_asteroid_timer = 2                                    #this block, the variable is set back to a number that is within this block's limit

        elif 45 <= seconds <= 60:
            if new_asteroid_timer == 1:
                #every second an asteroid is drawn onto the screen
                new_asteroid_timer = 0      
                if not_running_dict:                            
                    x = not_running_dict.popitem()                           
                    running_dict [x[0]] = x[1]       

            elif new_asteroid_timer > 1:
                new_asteroid_timer = 1
        
        #boundary condn: so that rocket does not go out of bounds 
        if millenium_falcon.x <= 0 :                                                     
            millenium_falcon.x = 0

        elif millenium_falcon.x >= 1080:
            millenium_falcon.x = 1080

        screen.fill((0,0,0))
        maindraw()                                                         #all draw functions are called here
        
    pygame.quit()                                                          #closes pygame

    return score, seconds
