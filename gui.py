import pygame
import time
import threading

from scrape import Scrape
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
        self.searchbar_thread = False
        self.searchbar_border = pygame.Rect(128-5, 40-5, 1024+10, 40+10)
        self.searchbar        = pygame.Rect(128, 40, 1024, 40)

        # Button (SÖK | STARTA)
        self.button_border = pygame.Rect(597-5, 643-5, 86+10, 34+10)
        self.button_bar    = pygame.Rect(597, 643, 86, 34)

        # Loading Bar
        self.loading_bar_border = pygame.Rect(256-5, 650-5, 768+10, 20+10)
        self.loading_bar        = pygame.Rect(256, 650, 768, 20)
        self.last_time = 0
        self.array_last_time = []
        self.last_scraped = -1


        self.state = 0

        self.scrape = Scrape()
        self.scrape_bool = False

        self.time = 0
        self.button_cooldown = 100

    def inputs(self):

        current_time = pygame.time.get_ticks()
        
        mouse = pygame.mouse.get_pressed()

        # button pressed
        if (mouse[0]):

            # debounce button cooldown
            if (current_time -  self.time >= self.button_cooldown):

                self.time = current_time

                print("\n")
                print("mouse clicked")

                # mouse position when pressed
                pos = pygame.mouse.get_pos()

                # check if click on input bar to search
                if (self.searchbar.collidepoint(pos) and self.searchbar_thread == False):
                    print("searchbar clicked")
                    self.searchbar_bool  = True
                    self.state = 0       

                # check if click on button to press button
                elif (self.state == 0 and self.button_bar.collidepoint(pos)):
                    self.searchbar_bool = False
                    print("button - SÖK clicked")
                    self.searchButtonPressed()
                    self.state = 1
                
                elif (self.state == 1 and self.button_bar.collidepoint(pos)):
                    self.searchbar_bool = False
                    print("button - STARTA clicked")
                    self.startButtonPressed()
                    self.state = 2
       
                else:
                    print("else clicked")
                    self.searchbar_bool  = False
      
    def searchButtonPressed(self):
        self.scrape.total_companys = '-'
        self.search_thread = threading.Thread(target=self.scrape.TEST_search, name="Search", args=(self.user_text,))
        self.search_thread.start()
        self.searchbar_thread = True
    
    def startButtonPressed(self):

        self.scrape_thread = threading.Thread(target=self.scrape.scrapeMainPage, name="Scrape", args=(self.scrape.url,))
        self.scrape_thread.start()
        self.searchbar_thread = True

    def drawBox(self):
        # Är detta verkligen så smart??? kanske göra om den på något sätt?
        if (self.state == 1):
            self.searchbar_thread = False
            if (self.scrape.total_companys == '-'):
                scrape_str = f"Söker efter {self.user_text}..."
            elif (self.scrape.total_companys == None):
                scrape_str = f"404 : Något gick fel, saknas internetanslutning kanske?"
            else:
                scrape_str = f"Hittade {self.scrape.total_companys} företag på {self.scrape.total_pages} sidor"
            
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

        elif (self.state == 2):
            # Draw loading bar
            pygame.draw.rect(self.surface, COLOR4, self.loading_bar_border, border_radius=10)
            pygame.draw.rect(self.surface, COLOR5, self.loading_bar, border_radius=10)

            # Draw loaded in loading bar
            total = 25
            width = self.loading_bar.width
            per = width / total
            loading_width = per * self.scrape.total_scraped
            pygame.draw.rect(self.surface, COLOR1, pygame.Rect(256, 650, loading_width, 20), border_radius=10)
            
            # Draw time left for webscrape
            current_time = pygame.time.get_ticks()
            if (self.scrape.total_scraped !=  self.last_scraped):
                self.last_scraped = self.scrape.total_scraped
                self.last_time = current_time - self.last_time
                self.array_last_time.append(self.last_time)
            
            t = 0
            for i in self.array_last_time:
                t += i
            t = t / len(self.array_last_time)

            time_left = (t * (total - self.last_scraped)) / 60000 # to minutes
            time_left_text = self.font.render(f"> {int(time_left)} min", True, COLOR1)
            time_width = time_left_text.get_width()
            self.surface.blit(time_left_text, (246-time_width,650))

            p = (self.last_scraped / total) * 100
            percent_text = self.font.render(f"{int(p)} %", True, COLOR1)
            self.surface.blit(percent_text, (1034,650))




            

    def draw(self):

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
            if (time.time() % 1 > 0.5):
                self.cursor.left = text_rect.right
                pygame.draw.rect(self.surface, COLOR1, self.cursor)
         
        # Middle box       
        pygame.draw.rect(self.surface, COLOR4, pygame.Rect(30, 150, 1220, 420), border_radius=5)
        pygame.draw.rect(self.surface, COLOR2, pygame.Rect(30+5, 150+5, 1220-10, 420-10), border_radius=5)

    def update(self):
        self.inputs()
        self.draw()
        self.drawBottom()
        self.drawBox()


        