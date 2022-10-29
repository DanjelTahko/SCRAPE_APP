import pygame

from hitta_scrape import HittaScrape
from settings import *

class GUI:

    def __init__(self) -> None:
        
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont('arial', 20)

        self.user_text = ''
        self.search_bar_bool        = False
        self.search_bar_color       = 'dark grey'
        self.search_bar_rect        = pygame.Rect(400, 25, 450, 30)
        self.search_bar_rect_border = pygame.Rect(390, 15, 470, 50) #390+470=860
        self.search_button_color    = BASE_COLOR
        self.search_button          = pygame.Rect(870, 25, 52, 30)
        self.search_button_border   = pygame.Rect(860, 15, 72, 50)

        self.scrape = HittaScrape()
        self.scrape_bool = False
        self.runnable = 0

    def inputs(self):
        
        mouse = pygame.mouse.get_pressed()
        if (mouse[0]):
            pos = pygame.mouse.get_pos()
            # check if click on input bar to search
            if (self.search_bar_rect.collidepoint(pos)):
                self.search_bar_bool  = True
                self.search_bar_color = 'white'

            elif(self.search_button.collidepoint(pos)):
                self.search_bar_color = 'dark grey'
                self.search_bar_bool  = False

                self.search_button_color = BASE_COLOR_TEST
                self.runnable = 1
                self.scrape_bool = True
            else:
                self.search_bar_bool  = False
                self.search_bar_color = 'dark grey'

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
        companys = self.font.render(scrape_str, True, (0,0,0))
        self.surface.blit(companys, (405,350))


    def draw(self):
        
        # Search Bar
        pygame.draw.rect(self.surface, BASE_COLOR_TEST, self.search_bar_rect_border)
        pygame.draw.rect(self.surface, self.search_bar_color, self.search_bar_rect)
        pygame.draw.rect(self.surface, BASE_COLOR_TEST, self.search_button_border)
        pygame.draw.rect(self.surface, self.search_button_color, self.search_button)
        
        text_surface = self.font.render(self.user_text, True, (0,0,0))

        while(text_surface.get_width() > 432):
            self.user_text = self.user_text[:-1]
            text_surface = self.font.render(self.user_text, True, (0,0,0))

        self.surface.blit(text_surface, (405,28))
        #self.search_bar_rect.w = max(100, text_surface.get_width()+10)

        button_surface = self.font.render("SÖK", True, (0,0,0))
        self.surface.blit(button_surface, (875,28))

        if (self.scrape_bool):
            self.scrapeApp()


    def update(self):
        self.inputs()
        self.draw()
        self.functions()
        