# import the pygame module, so you can use it
import pygame
import Task_objects
import random
random.seed(2001)
 
# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    
    # Initialise the font module
    pygame.font.init()
    
    # Set caption
    pygame.display.set_caption("Working memory task")
     
    # create a surface on screen that has the size of 240 x 180
    display_width = 1020 
    display_height = 560
    screen = pygame.display.set_mode((display_width,display_height))
    
    screen.fill((255,255,255))
    
    questionAsker = Task_objects.QuestionAsker(pygame.font.Font('./CourierPrimeCodeRegular.ttf', 60),display_width,display_height, screen)
    
    questionAsker.beginning()
    
    for i in range (0,10):
        questionAsker.addTask(6, incorrectProbe = bool(random.randint(0,1)), alphabetic = True)
    
    questionAsker.runTasks()
    
    questionAsker.finished()
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()