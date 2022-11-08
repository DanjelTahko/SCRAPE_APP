import pygame
import time
import threading

from scrape import Scrape
from settings import *
from config import *

class GUI:

    def __init__(self) -> None:

        #self.searchbar_thread = False ???
        # what does it do?
        # fix time in loading bar! total should be total companies chosen in filter

        
        # Surface and font init
        self.surface    = pygame.display.get_surface()
        self.font       = pygame.font.SysFont('arial', 20)
        self.cursor     = pygame.Rect(133, 48, 3, 23)
        self.user_text  = ''

        # Searchbar
        self.searchbar_bool     = False
        self.searchbar_thread   = False
        self.searchbar_border   = pygame.Rect(128-5, 40-5, 1024+10, 40+10)
        self.searchbar          = pygame.Rect(128, 40, 1024, 40)

        # Button (SÖK | STARTA)
        self.button_border      = pygame.Rect(597-5, 643-5, 86+10, 34+10)
        self.button_bar         = pygame.Rect(597, 643, 86, 34)

        # Loading Bar
        self.loading_bar_border = pygame.Rect(256-5, 650-5, 768+10, 20+10)
        self.loading_bar        = pygame.Rect(256, 650, 768, 20)
        self.last_time          = 0
        self.array_last_time    = []
        self.last_scraped       = -1

        # Arrows (change page)
        self.right_arrow      = None
        self.right_arrow_bool = False
        self.left_arrow       = None
        self.left_arrow_bool  = False

        # Filter search
        self.filter_pages   = 0
        self.filter_orgnum  = False
        self.filter_telnum  = False
        self.filter_website = False

        self.state = 0

        self.scrape = Scrape()
        self.scrape_bool = False

        self.time = 0
        self.button_cooldown = 250
        self.pressed = False

        # Industries (categories)
        self.dictionary = HITTA_INDUSTRY
        self.rect_industries_array = []
        self.surf_industries_array = []
        self.text_industries_array = []
        self.createList(self.dictionary)
        self.industry_pages = 1
        self.atm_page = 1

    
    def createList(self, dictionary_industries):
        """ Creates industry rect that you can click of dictionary"""
        # Creates text, surface and the rect

        self.rect_industries_array = []
        self.surf_industries_array = []
        self.text_industries_array = []

        x_text = 35
        y_text = 155+20
        # | 10 | T(390) | 10 | T(390) | 10 | T(390) | 10 |

        for index, industry in enumerate(dictionary_industries):
            
            companys_text = self.font.render(industry, True, COLOR4)
            self.surf_industries_array.append(companys_text)
            companys_rect = companys_text.get_rect(topleft=(x_text+10, y_text))
            self.rect_industries_array.append(companys_rect)
            self.text_industries_array.append(industry)
            y_text += 23 + 10

            if((index+1)%10 == 0):
                x_text += 10 + 390
                y_text = 155+20

            if ((index+1)%30 == 0):
                x_text = 35
                y_text = 155+20

        self.atm_page = 1

    def inputs(self):

        """
        STATES
        0 - Search (searchbar and industries/categories)
        1 - Filter (sets filters for starting web scrape)
        2 - Scrape (scraping pages)
        3 - Save   (save scraped to file)
        """

        current_time = pygame.time.get_ticks()
        
        mouse = pygame.mouse.get_pressed()

        # button pressed
        if (mouse[0]):

            # debounce button cooldown
            if (current_time -  self.time >= self.button_cooldown):

                self.time = current_time

                print("\n")
                print(f"mouse clicked - state:{self.state}")

                # mouse position when pressed
                pos = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(pos, (5,5))

                # collidelist return index that collides, if none -1
                if (self.state == 0 and mouse_rect.collidelist(self.rect_industries_array) >= 0):
                    # store index in variable to get industry value/text
                    index = mouse_rect.collidelist(self.rect_industries_array)
                    if (self.atm_page > 1):
                        index += 30 * (self.atm_page-1)
                    print(f"{self.text_industries_array[index]} - clicked")
                    # if dictionary value is not empty, create new dictionary with values as keys
                    if (self.dictionary[self.text_industries_array[index]]):
                        self.user_text = self.text_industries_array[index]
                        self.dictionary = self.dictionary[self.text_industries_array[index]]
                        self.createList(self.dictionary)
                    else:
                        # set user_text to clicked industry category 
                        self.user_text = self.text_industries_array[index]
                
                elif (self.right_arrow_bool and mouse_rect.colliderect(self.right_arrow)):
                    self.atm_page += 1

                elif (self.left_arrow_bool and mouse_rect.colliderect(self.left_arrow)):
                    self.atm_page -= 1
                    

                # check if click on input bar to search
                elif (self.searchbar.collidepoint(pos) and self.searchbar_thread == False): 
                    print("searchbar clicked")
                    self.searchbar_bool  = True
                    self.state = 0       
                    self.dictionary = HITTA_INDUSTRY
                    self.createList(self.dictionary)

                # check if click on SÖK button to press button
                elif (self.state == 0 and self.button_bar.collidepoint(pos)):
                    print("button - SÖK clicked")
                    self.searchbar_bool = False
                    self.searchButtonPressed()
                    self.state = 1
                
                # check if click on STARTA button to press button
                elif (self.state == 1 and self.button_bar.collidepoint(pos)):
                    print("button - STARTA clicked")
                    self.searchbar_bool = False
                    # can only press start button if search is complete and companies more than 0
                    if (not self.searchbar_thread and self.scrape.total_companys > 0):
                        self.startButtonPressed()
                        self.state = 2
       
                else:
                    print("else clicked")
                    self.searchbar_bool  = False
      
    def searchButtonPressed(self):
        self.searchbar_thread = True
        # Create & Start thread = Makes search with word to find number of companies and pages
        self.search_thread = threading.Thread(target=self.scrape.searchThread, name="Search Thread", args=(self.user_text,))
        self.search_thread.start()
        # Sets dictionary with industries to standard template
        self.dictionary = HITTA_INDUSTRY
        self.createList(self.dictionary)
    
    def startButtonPressed(self):
        
        pages = self.atm_page
        org = False
        num = False
        web = False
        csv = {}
        self.scrape_thread = threading.Thread(target=self.scrape.scrapeThread, name="Scrape thread", args=(pages, org, num, web, csv))
        self.scrape_thread.start()
        #self.searchbar_thread = True

    def drawBox(self):
        """
        Draws inside middlebox\n
        """
        # BOX = pygame.Rect(x=35, y=155, w=1210, h=410)
        # TEXT HEIGHT = 23 pixels
        # | 10 | T(390) | 10 | T(390) | 10 | T(390) | 10 |

        X = 35
        Y = 155
        
        # SEARCH STATE
        if (self.state == 0):

            # sets pages based on how many industries/sub industries and so on
            # e.g 1 page is 30 industries, so 31 industries will be 2 pages
            get_pages = lambda c : int(c/30) + 1 if (c % 30 > 0) else int(c/30)
            self.industry_pages = get_pages(len(self.text_industries_array))
            
            # sets start and stop range of array for showing industries at right page 
            # e.g page 2 will show industries in range [30 : 60]
            # but if array only contains 44 industries it will be [30 : 44]
            range_start = 0
            range_stop = 30
            if (self.industry_pages > 1):
                range_start += 30 * (self.atm_page-1)
                if (self.atm_page != self.industry_pages):
                    range_stop += 30 * (self.atm_page-1)
                else:
                    range_stop = range_start + len(self.text_industries_array) % 30
            else:
                range_stop = len(self.text_industries_array)

            # loops through range where index will be [range_start : range_stop]
            for index in range(range_start, range_stop):
                # sets surf,text and rect to right one 
                surf = self.surf_industries_array[index]
                text = self.text_industries_array[index]
                rect = self.rect_industries_array[index]
                # if text is too long (>540px) delete two last words 
                if (surf.get_width() > 540):
                    text_strip = text.split()
                    new_text = ' '.join(text_strip[:-2])
                    surf = self.font.render(new_text, True, COLOR4)
                # deletes only last word (textframe can only be max 390px)
                elif (surf.get_width() > 390):
                    text_strip = text.split()
                    new_text = ' '.join(text_strip[:-1])
                    surf = self.font.render(new_text, True, COLOR4)
                # draws text on surface 
                self.surface.blit(surf, rect)

            # draws page e.g 1/6
            pages_text = self.font.render(f"{self.atm_page}/{self.industry_pages}", True, COLOR4)
            pages_rect = pages_text.get_rect(midtop=(640, 520))
            self.surface.blit(pages_text, pages_rect)
            pages_width_r = pages_rect.width / 2

            # RIGHT ARROW (if theres more than one pages and if atm page is less than amount of pages)
            if (self.industry_pages > 1 and self.atm_page < self.industry_pages):
                # so we can click on next page
                self.right_arrow_bool = True
                # right of page number
                x = 645 + pages_width_r
                right_a = ((x, 520), (x, 520+20), (x+20, 520+10), (x, 520))
                self.right_arrow = pygame.Rect(x, 520, 20, 20)
                pygame.draw.polygon(self.surface, COLOR5, right_a)
            else:
                # sets to False so we cant change page to next (when theres only 1 page available or no next page)
                self.right_arrow_bool = False 

            # LEFT ARROW (if theres more than one pages and if atm page is more than first page)
            if (self.industry_pages > 1 and self.atm_page > 1):
                # so we can click on previous page
                self.left_arrow_bool = True
                # left of page number
                x = 635 - pages_width_r
                left_a = ((x, 520), (x, 520+20), (x-20, 520+10), (x, 520))
                self.left_arrow = pygame.Rect(x-20, 520, 20, 20)
                pygame.draw.polygon(self.surface, COLOR5, left_a)
            else:
                # sets to False so we cant change page (when theres only 1 page available or on page 1)
                self.left_arrow_bool = False

        # FILTER STATE
        elif (self.state == 1):
             
            if (self.scrape.total_companys == '-'):
                # Searching for companies 
                scrape_str = f"Söker efter {self.user_text}..."
            elif (self.scrape.total_companys == None):
                # Could not find anything probably because no internet 
                scrape_str = f"404 : Något gick fel, saknas internetanslutning kanske?"
                self.searchbar_thread = False
            else:
                # Companies found 
                if (self.scrape.total_pages == 1):
                    sida = 'sida'
                else:
                    sida = 'sidor'
                scrape_str = f"Hittade {self.scrape.total_companys} företag på {self.scrape.total_pages} {sida}"
                if (self.searchbar_thread):
                    self.atm_page = self.scrape.total_pages
                self.searchbar_thread = False
            
            # draws text at the top with underline 
            companys_text = self.font.render(scrape_str, True, COLOR4)
            companys_rect = companys_text.get_rect(midtop=(WIDTH/2, Y+7.5))
            self.surface.blit(companys_text, companys_rect)
            pygame.draw.rect(self.surface, COLOR4, pygame.Rect(X+5, Y+38, 1200, 2), border_radius=5)

            # if any companies found and if theres internet connection 
            if (not self.scrape.error and not self.searchbar_thread and self.scrape.total_companys > 0):

                # draws "Antal sidor :"
                filter_pages = self.font.render("Antal sidor :", True, COLOR4)
                filter_pages_rect = filter_pages.get_rect(topright=((WIDTH/2)-20, Y+60))
                self.surface.blit(filter_pages, filter_pages_rect)

                x = (WIDTH/2)+10
                y = Y+60

                # LEFT ARROW (if theres more than one pages and if atm page is more than first page)
                if (self.atm_page > 1):
                    # so we can click on previous page
                    self.left_arrow_bool = True
                    # left of page number
                    left_a = ((x, y), (x, y+20), (x-20, y+10), (x, y))
                    self.left_arrow = pygame.Rect(x-20, y, 20, 20)
                    pygame.draw.polygon(self.surface, COLOR5, left_a)
                else:
                    # sets to False so we cant change page (when theres only 1 page available or on page 1)
                    self.left_arrow_bool = False

                pages_amount = self.font.render(f"{self.atm_page}", True, COLOR4)
                pages_amount_rect = pages_amount.get_rect(topleft=(x+5, y))
                self.surface.blit(pages_amount, pages_amount_rect)
                _width = pages_amount_rect.width
                x += _width + 10

                # RIGHT ARROW (if theres more than one pages and if atm page is less than amount of pages)
                if (self.atm_page < self.scrape.total_pages):
                    # so we can click on next page
                    self.right_arrow_bool = True
                    # right of page number
                    right_a = ((x, y), (x, y+20), (x+20, y+10), (x, y))
                    self.right_arrow = pygame.Rect(x, y, 20, 20)
                    pygame.draw.polygon(self.surface, COLOR5, right_a)
                else:
                    # sets to False so we cant change page to next (when theres only 1 page available or no next page)
                    self.right_arrow_bool = False 
                

                # draws "Org-Nummer :"
                filter_orgnum = self.font.render("Org-nummer :", True, COLOR4)
                filter_orgnum_rect = filter_pages.get_rect(topright=((WIDTH/2)-20, Y+103))
                self.surface.blit(filter_orgnum, filter_orgnum_rect)

                x = (WIDTH/2)-20
                y = Y+103

                new_button = pygame.Rect(x+11, y+1, 20-1, 20-1)
                new_button_b = pygame.Rect(x+10, y, 20, 20)

                """ color change button [TRUE or FALSE] """

                pygame.draw.rect(self.surface, COLOR4, new_button_b, border_radius=5)
                pygame.draw.rect(self.surface, COLOR2, new_button, border_radius=5)
                text_search = self.font.render("TRUE / FALSE", True, COLOR1)
                self.surface.blit(text_search, (x,y))
                

                # draws "Telefonnummer :"
                filter_pages = self.font.render("Telefonnummer  :", True, COLOR4)
                filter_pages_rect = filter_pages.get_rect(topright=((WIDTH/2)-20, Y+146))
                self.surface.blit(filter_pages, filter_pages_rect)
                
                
                # draws "Hemsida :"
                filter_pages = self.font.render("Hemsida :", True, COLOR4)
                filter_pages_rect = filter_pages.get_rect(topright=((WIDTH/2)-20, Y+189))
                self.surface.blit(filter_pages, filter_pages_rect)

                # draws "Jämföra CSV? :"
                filter_pages = self.font.render("Importera csv :", True, COLOR4)
                filter_pages_rect = filter_pages.get_rect(topright=((WIDTH/2)-20, Y+232))
                self.surface.blit(filter_pages, filter_pages_rect)
                

                # draws Jämföra csv???
                #filter_pages = self.font.render("Antal sidor :", True, COLOR4)
                #filter_pages_rect = filter_pages.get_rect(midtop=(WIDTH/2, Y+40))
                #self.surface.blit(filter_pages, filter_pages_rect)
                #pygame.draw.rect(self.surface, COLOR4, pygame.Rect(X+5, Y+38, 1200, 2), border_radius=5)




    def drawBottom(self):

        if (self.state == 0 or self.state == 1):

            if (self.state == 0):
                button_text = 'SÖK'
                x,y = 618, 649
            elif (self.state == 1):
                button_text = 'STARTA'
                x,y = 602,649

            # Draw button 
            pygame.draw.rect(self.surface, COLOR4, self.button_border, border_radius=5)
            pygame.draw.rect(self.surface, COLOR2, self.button_bar, border_radius=5)
            text_search = self.font.render(button_text, True, COLOR1)
            self.surface.blit(text_search, (x,y))

        elif (self.state == 2):
            # Draw loading bar
            pygame.draw.rect(self.surface, COLOR4, self.loading_bar_border, border_radius=10)
            pygame.draw.rect(self.surface, COLOR5, self.loading_bar, border_radius=10)

            # Draw loaded in loading bar
            total = self.atm_page * 25 
            if (total > self.scrape.total_companys):
                total = self.scrape.total_companys

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

            #time_left = (t * (total - self.last_scraped)) / 60000 # to minutes
            time_left = (t * (total - self.last_scraped)) / 6000 # to seconds
            time_left_text = self.font.render(f"~ {int(time_left/60)} min {time_left%60:.0f} sec", True, COLOR1)
            time_width = time_left_text.get_width()
            self.surface.blit(time_left_text, (246-time_width,649))

            p = (self.last_scraped / total) * 100
            percent_text = self.font.render(f"{int(p)} %", True, COLOR1)
            self.surface.blit(percent_text, (1034,649))

    def drawBase(self):

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
        self.drawBase()
        self.drawBottom()
        self.drawBox()
        self.inputs()


        