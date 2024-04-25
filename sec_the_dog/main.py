import pygame
from pygame.font import SysFont

pygame.init()
#
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600
# display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
# pygame.display.set_caption("MAIN")
# font = SysFont('Georgia',60,bold=True)
# font_for_the_buttons = SysFont('Georgia',40,bold=True)
# credits_font = SysFont('Georgia',20,bold=True)
#
# title_surf = font.render('SEC THE DOG ',True,'orange')
# title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150))
#
# # the dog logo
# dog_title_surf = pygame.image.load("dog_right.png")
# dog_title_rect = dog_title_surf.get_rect()
# dog_title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
#
# # the buttons
# new_game_surf = font_for_the_buttons.render('PLAY',True,'white')
# new_game_button = pygame.Rect(WINDOW_WIDTH//2-50,WINDOW_HEIGHT//2+80,140,40)
#
# credits_surf = credits_font.render('BY DATSANITY',True,'orange')
# credits_rect = credits_surf.get_rect(bottomleft=(10,WINDOW_HEIGHT-10))
#
#
# def activate_button():
#     pygame.init()
#     a,b = pygame.mouse.get_pos()
#     if new_game_button.x <= a <= new_game_button.x + 110 and new_game_button.y <= b <= new_game_button.y + 60:
#         # colors the text if it satisfies the condition
#         pygame.draw.rect(display_surface, (180, 180, 180), (WINDOW_WIDTH//2-70,WINDOW_HEIGHT//2+80,130,60))
#     else:
#         # if it dose not satisty, draw a rect at this coordinates and color
#         pygame.draw.rect(display_surface, (110, 110, 110), (WINDOW_WIDTH//2-70,WINDOW_HEIGHT//2+80,130,60))
#
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#
#             GAMEON = Game(WINDOW_WIDTH,WINDOW_HEIGHT,display_surface)
#             GAMEON.run_game()
#
#
#     activate_button()
#     display_surface.blit(title_surf,title_rect)
#     display_surface.blit(dog_title_surf,dog_title_rect)
#     display_surface.blit(new_game_surf, (new_game_button.x - 20, new_game_button.y + 5))
#     display_surface.blit(credits_surf,credits_rect)
#     pygame.display.update()
#
# pygame.quit()
class MainMenu:
    def __init__(self):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("MAIN")
        self.font = SysFont('Georgia', 60, bold=True)
        self.font_for_the_buttons = SysFont('Georgia', 40, bold=True)
        self.credits_font = SysFont('Georgia', 20, bold=True)

        self.title_surf = self.font.render('SEC THE DOG ', True, 'orange')
        self.title_rect = self.title_surf.get_rect(center=(self.WINDOW_WIDTH // 2, 150))

        # the dog logo
        self.dog_title_surf = pygame.image.load("dog_right.png")
        self.dog_title_rect = self.dog_title_surf.get_rect()
        self.dog_title_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)

        # the buttons
        self.new_game_surf = self.font_for_the_buttons.render('PLAY', True, 'white')
        self.new_game_button = pygame.Rect(self.WINDOW_WIDTH // 2 - 50, self.WINDOW_HEIGHT // 2 + 80, 140, 40)

        self.credits_surf = self.credits_font.render('BY DATSANITY', True, 'orange')
        self.credits_rect = self.credits_surf.get_rect(bottomleft=(10, self.WINDOW_HEIGHT - 10))

    def activate_button(self):
        a, b = pygame.mouse.get_pos()
        if self.new_game_button.x <= a <= self.new_game_button.x + 110 and self.new_game_button.y <= b <= self.new_game_button.y + 60:
            # colors the text if it satisfies the condition
            pygame.draw.rect(self.display_surface, (180, 180, 180), (self.WINDOW_WIDTH // 2 - 70, self.WINDOW_HEIGHT // 2 + 80, 130, 60))
        else:
            # if it dose not satisfy, draw a rect at these coordinates and color
            pygame.draw.rect(self.display_surface, (110, 110, 110), (self.WINDOW_WIDTH // 2 - 70, self.WINDOW_HEIGHT // 2 + 80, 130, 60))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_on = Game(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.display_surface)
                    game_on.run_game()

            self.activate_button()
            self.display_surface.blit(self.title_surf, self.title_rect)
            self.display_surface.blit(self.dog_title_surf, self.dog_title_rect)
            self.display_surface.blit(self.new_game_surf, (self.new_game_button.x - 20, self.new_game_button.y + 5))
            self.display_surface.blit(self.credits_surf, self.credits_rect)
            pygame.display.update()

        pygame.quit()

# Usage
if __name__ == "__main__":
    pygame.init()
    main_menu = MainMenu()
    main_menu.run()