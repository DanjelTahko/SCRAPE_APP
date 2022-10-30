import pygame, sys

from settings import *
from gui import GUI


class APP:

    def __init__(self) -> None:
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Prospect App")
        img = pygame.image.load('tahko_icon.png')
        pygame.display.set_icon(img)

        self.gui = GUI()

    def run(self):

        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # temp quit program
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if (self.gui.searchbar_bool == True):
                        # Clear all text if 'command' + 'return' pressed
                        if event.key == pygame.K_LCTRL:
                            self.gui.user_text = ''
                        # Remove last letter in user input if 'return' pressed
                        elif event.key == pygame.K_BACKSPACE:
                            if (len(self.gui.user_text) > 0):
                                self.gui.user_text = self.gui.user_text[:-1]
                        # Search for user_input if 'enter' pressed
                        elif event.key == pygame.K_RETURN:
                            self.gui.searchbar_bool = False
                            #self.gui.runnable = 1
                            #self.gui.scrape_bool = True
                        # Add letter to user_input if any other key pressed
                        else:
                            self.gui.user_text += event.unicode

            self.screen.fill(COLOR5)
            self.gui.update()
            pygame.display.update()
            self.clock.tick(FPS)

            
if __name__ == '__main__':
    app = APP()
    app.run()