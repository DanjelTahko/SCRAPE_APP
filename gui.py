import pygame
import time

from hitta_scrape import HittaScrape
from settings import *

class GUI:

    def __init__(self) -> None:
        
        # Surface and font init
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont('arial', 20)
        self.cursor = pygame.Rect(133, 48, 3, 23)
        self.user_text = ''

        # Searchbar
        self.searchbar_bool = False
        self.searchbar_border = pygame.Rect(128-5, 40-5, 1024+10, 40+10)
        self.searchbar        = pygame.Rect(128, 40, 1024, 40)

        # Button (SÖK | STARTA)
        self.button_border = pygame.Rect(597-5, 643-5, 86+10, 34+10)
        self.button_bar    = pygame.Rect(597, 643, 86, 34)

        self.state = 0

        self.scrape = HittaScrape()
        self.scrape_bool = False

        self.time = 0

    def inputs(self):
        
        mouse = pygame.mouse.get_pressed()

        if (mouse[0]):
            pos = pygame.mouse.get_pos()
            # check if click on input bar to search
            if (self.searchbar.collidepoint(pos)):
                self.searchbar_bool  = True
            # check if click on button to press button
            elif (self.button_bar.collidepoint(pos)):
                self.searchbar_bool = False
                print("Button pressed")
            else:
                self.searchbar_bool  = False
                
    def functions(self):

        if (self.runnable == 1):
            url = self.scrape.searchIndustry(self.user_text)
            self.scrape.scrapeSearch(url)
            self.search_button_color = BASE_COLOR

        elif (self.runnable == 2):
            pass 

        self.runnable = 0

    def scrapeApp(self):
        scrape_str = f"Hittade {self.scrape.companys} företag på {self.scrape.pages} sidor"
        companys = self.font.render(scrape_str, True, COLOR4)
        self.surface.blit(companys, (405,350))

    def drawBottom(self):

        if (self.state == 0):
            pygame.draw.rect(self.surface, COLOR4, self.button_border, border_radius=5)
            pygame.draw.rect(self.surface, COLOR2, self.button_bar, border_radius=5)
            # button = (597, 643, 86, 34)
            # SÖK    = (618 ,649 , 43, 22)
            text_search = self.font.render("SÖK", True, COLOR1)
            self.surface.blit(text_search, (618,649))

        elif (self.state == 1):
            pygame.draw.rect(self.surface, COLOR4, self.button_border, border_radius=5)
            pygame.draw.rect(self.surface, COLOR2, self.button_bar, border_radius=5)
            # button = (597, 643, 86, 34)
            # STARTA = (602 ,649 , 76, 23)
            text_search = self.font.render("STARTA", True, COLOR1)
            self.surface.blit(text_search, (602,649))

    def draw(self):

        current_time = pygame.time.get_ticks()

        # Draw Top & Bottom Bar
        pygame.draw.rect(self.surface, COLOR3, pygame.Rect(0, 0, 1280, 120))
        pygame.draw.rect(self.surface, COLOR3, pygame.Rect(0, 600, 1280, 120))

        # Draw Searchbar
        pygame.draw.rect(self.surface, COLOR4, self.searchbar_border, border_radius=5)
        pygame.draw.rect(self.surface, COLOR2, self.searchbar, border_radius=5)

        # Draw text on searchbar
        text_surface = self.font.render(self.user_text, True, COLOR1)
        text_rect    = text_surface.get_rect()
        text_rect.left = 133

        # If input to long..
        while(text_surface.get_width() > 1020):
            self.user_text = self.user_text[:-1]
            text_surface = self.font.render(self.user_text, True, COLOR1)
        
        self.surface.blit(text_surface, (133,48))
        if (self.searchbar_bool):
            #if (current_time - self.time >= 1000):
            if (time.time() % 1 > 0.5):
                self.cursor.left = text_rect.right
                pygame.draw.rect(self.surface, COLOR1, self.cursor)
                self.time = current_time
         
        # Middle box       
        pygame.draw.rect(self.surface, COLOR4, pygame.Rect(30, 150, 1220, 420), border_radius=5)
        pygame.draw.rect(self.surface, COLOR2, pygame.Rect(30+5, 150+5, 1220-10, 420-10), border_radius=5)

    def update(self):
        self.draw()
        self.drawBottom()
        self.inputs()
        #self.functions()
        