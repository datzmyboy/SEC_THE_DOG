import pygame, random,time,json


from pygame.font import SysFont

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("SEC THE DOG")


class Game:
    def __init__(self,WINDOW_WIDTH,WINDOW_HEIGHT,display_surface):
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.display_surface = display_surface
        self.FPS = 60
        self.clock = pygame.time.Clock()
        # self.draw = Draw()
        self.text = Text()
        self.dog = Dog()
        self.colors = Colors()
        self.burger = Burger(self.dog)
        self.to_display = False
        self.sound = Sounds()
    def update_text(self):
        self.text.eaten_text = self.text.font.render("Burgers eaten: "+ str(self.burger.burgers_eaten), True, 'orange')
        self.text.score_text = self.text.points_font.render("Score: " + str(self.burger.score), True, 'orange')
        self.text.lives_text = self.text.font.render("Lives: " + str(self.dog.dog_lives), True, 'orange')
        self.text.points_text = self.text.points_font.render("Burger points: " + str(self.burger.burger_points), True, 'orange')
        self.text.boost_text = self.text.font.render("Boost: " + str(self.dog.boost_level), True, 'orange')
    def update_score(self):
        user = read_players()
        my_user = user[0]
        my_score = my_user["player_score"]
        if self.burger.score > my_score:
            update_player("USER_DATA",self.burger.score)
            self.to_display = True

    def game_over(self):
        if self.dog.dog_lives == 0:
            self.display_surface.fill(self.colors.black)
            self.text.gameover_text = self.text.font.render("Final score : " + str(self.burger.score), True, 'orange')
            display_surface.blit(self.text.gameover_text,self.text.gameover_rect)
            display_surface.blit(self.text.continue_text, self.text.continue_rect)
            pygame.display.update()
            self.update_score()
            if self.to_display:
                self.display_surface.fill(self.colors.black)
                gameover_rect_adjusted = self.text.gameover_rect.move(-20, -50)
                display_surface.blit(self.text.gameover_text, gameover_rect_adjusted)
                # self.text.gameover_text = self.text.font.render("Final score : " + str(self.burger.score), True,'orange')
                display_surface.blit(self.text.greet_text,self.text.greet_rect)
                display_surface.blit(self.text.continue_text, self.text.continue_rect)
                self.text.high_score_text = self.text.points_font.render("High Score : "+str(self.burger.score) , True,'orange')

            pygame.display.update()
            pygame.mixer.music.stop()

            is_pause = True
            while is_pause:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.burger.score = 0
                        self.burger.burgers_eaten = 0
                        self.dog.dog_lives = self.dog.dog_starting_lives
                        self.dog.boost_level = self.dog.dog_starting_boost_level
                        self.burger.burger_velocity = self.burger.starting_burger_velocity
                        pygame.mixer.music.play()
                        is_pause = False
                    if event.type == pygame.QUIT:
                        is_pause = False
                        return False

    def run_game(self):
        pygame.mixer.music.play()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.display_surface.fill(self.colors.black)
            self.dog.dog_movement()
            self.dog.draw_dog()
            self.burger.draw_burger()
            self.burger.move_burger()
            self.burger.check_for_collision()
            self.burger.miss_burger()
            self.text.draw_texts()
            self.update_text()
            if self.game_over() == False:
                running = False
            pygame.display.update()
            self.clock.tick(self.FPS)
        pygame.quit()



class Dog:
    def __init__(self):
        self.dog_starting_lives = 3
        self.dog_normal_velocity = 5
        self.dog_boost_velocity = 10
        self.dog_starting_boost_level = 100

        self.dog_lives = self.dog_starting_lives
        self.dog_velocity = self.dog_normal_velocity
        self.boost_level = self.dog_starting_boost_level

        self.dog_left_text = pygame.image.load("dog_left.png")

        self.dog_right_text = pygame.image.load("dog_right.png")


        self.dog_image = self.dog_left_text
        self.dog_image_rect = self.dog_image.get_rect()

        self.dog_image_rect.centerx = WINDOW_WIDTH//2
        self.dog_image_rect.bottom = WINDOW_HEIGHT
        self.dog_bool = False
        # self.burger = Burger()

    def draw_dog(self):
        display_surface.blit(self.dog_image, self.dog_image_rect)

    def dog_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.dog_image_rect.left > 0:
            self.dog_image_rect.x -= self.dog_velocity
            self.dog_image = self.dog_left_text
            # print("moving")
        if keys[pygame.K_RIGHT] and self.dog_image_rect.right < WINDOW_WIDTH:
            self.dog_image_rect.x += self.dog_velocity
            self.dog_image = self.dog_right_text
            # print("moving")
        if keys[pygame.K_UP] and self.dog_image_rect.top > 100:
            self.dog_image_rect.y -= self.dog_velocity

        if keys[pygame.K_DOWN] and self.dog_image_rect.bottom < WINDOW_HEIGHT:
            self.dog_image_rect.y += self.dog_velocity
        #####
        #engage boost
        if keys[pygame.K_SPACE] and self.boost_level > 0 :
            self.dog_velocity = self.dog_boost_velocity
            self.boost_level-= 1
        else:
                self.dog_velocity = self.dog_normal_velocity

    def reposition_dog(self):
        self.dog_image_rect.centerx = WINDOW_WIDTH//2
        self.dog_image_rect.bottom = WINDOW_HEIGHT
        self.boost_level = self.dog_starting_boost_level
        print("nasdnjasndjasn,jdansdn,msand,mnas,dmn,asnd,masnd,mnas,dmnas,")



class Burger:
    def __init__(self,dog):
        self.starting_burger_velocity = 3
        self.burger_velocity = self.starting_burger_velocity
        self.burger_acceleration = .25
        self.burger_points = 0
        self.burgers_eaten = 0
        self.buffer_distance = 100
        self.score = 0

        self.buger_image = pygame.image.load("burger.png")
        self.buger_rect = self.buger_image.get_rect()
        self.buger_rect.topleft = (random.randint(0,WINDOW_WIDTH-32),-self.buffer_distance)
        # self.buger_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)
        self.dog = dog
        self.sound = Sounds()

    def draw_burger(self):
        display_surface.blit(self.buger_image, self.buger_rect)

    def move_burger(self):
        self.buger_rect.y += self.burger_velocity
        self.burger_points = int(self.burger_velocity * (WINDOW_HEIGHT - self.buger_rect.y + 100))

    def check_for_collision(self):
        if self.buger_rect.colliderect(self.dog.dog_image_rect):
            self.sound.play_bark_sound()
            self.buger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -self.buffer_distance)
            self.burger_velocity += self.burger_acceleration
            self.burgers_eaten+=1
            # print(f"the burgers eaten {self.burgers_eaten}")
            self.score +=self.burger_points
            # print(f"the score is {self.dog.score}")
            self.dog.boost_level += 25
            if self.dog.boost_level > self.dog.dog_starting_boost_level:
                self.dog.boost_level = self.dog.dog_starting_boost_level
            print(f"the boost level is {self.dog.boost_level}")
    #
    def miss_burger(self):
        if self.buger_rect.y > WINDOW_HEIGHT:
            self.dog.reposition_dog()
            self.dog.dog_lives -= 1
            print(self.dog.dog_lives)
            self.sound.play_miss_sound()
            # print("play")

            self.buger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -self.buffer_distance)
            self.burger_velocity = self.starting_burger_velocity







class Colors:
    def __init__(self):
        self.orange = (246,170,54)
        self.black = (0,0,0)
        self.white = (255,255,255)




class Text:
        def __init__(self):
            self.dog = Dog()
            self.burger = Burger(self.dog)
            self.colors = Colors()

            # self.font = pygame.font.Font('C:/path/to/Georgia.ttf', 32)
            self.font = SysFont('Georgia', 32, bold=True)
            self.points_font = SysFont('Georgia', 25, bold=True)

            self.points_text = self.points_font.render("Burger points: " + str(self.burger.burger_points), True, 'orange')
            self.points_rect = self.points_text.get_rect()
            self.points_rect.topleft = (10, 10)

            self.score_text = self.font.render("Score: " + str(self.burger.score), True, 'orange')
            self.score_rect = self.score_text.get_rect()
            self.score_rect.topleft = (10, 50)

            self.title_text = self.font.render("Sec the Dog", True, 'orange')
            self.title_rect = self.title_text.get_rect()
            self.title_rect.centerx = WINDOW_WIDTH // 2
            self.title_rect.y = 10

            self.eaten_text = self.font.render("Burgers eaten: "+ str(self.burger.burgers_eaten), True, 'orange')
            self.eaten_rect = self.eaten_text.get_rect()
            self.eaten_rect.centerx = WINDOW_WIDTH // 2
            self.eaten_rect.y = 50

            self.lives_text = self.font.render("Lives: " + str(self.dog.dog_lives), True, 'orange')
            self.lives_rect = self.lives_text.get_rect()
            self.lives_rect.topright = (WINDOW_WIDTH - 10, 10)

            self.boost_text = self.font.render("Boost: " + str(self.dog.boost_level), True, 'orange')
            self.boost_rect = self.boost_text.get_rect()
            self.boost_rect.topright = (WINDOW_WIDTH - 10, 50)

            self.gameover_text = self.font.render("Final score : " + str(self.burger.score), True, 'orange')
            self.gameover_rect = self.gameover_text.get_rect()
            self.gameover_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

            self.continue_text = self.font.render("Press any key to play again  " , True,'orange')
            self.continue_rect = self.continue_text.get_rect()
            self.continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

            get_score = read_players()
            user_data = get_score[0]
            high_score = user_data["player_score"]

            self.high_score_text = self.points_font.render("High Score : "+str(high_score) , True,'orange')
            self.high_score_rect = self.high_score_text.get_rect()
            self.high_score_rect.bottomleft = (5,WINDOW_HEIGHT)

            self.greet_text = self.font.render("Congatulations you got a high score! " , True,'orange')
            self.greet_rect = self.greet_text.get_rect()
            self.greet_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 10)


        def draw_texts(self):
            display_surface.blit(self.points_text, self.points_rect)
            display_surface.blit(self.score_text, self.score_rect)
            display_surface.blit(self.title_text, self.title_rect)
            display_surface.blit(self.eaten_text, self.eaten_rect)
            display_surface.blit(self.lives_text, self.lives_rect)
            display_surface.blit(self.boost_text, self.boost_rect)
            pygame.draw.line(display_surface, self.colors.white, (0, 100), (WINDOW_WIDTH, 100), 3)
            display_surface.blit(self.high_score_text,self.high_score_rect)





class Sounds:
    def __init__(self):
        self.bark_sound = pygame.mixer.Sound("bark_sound.wav")
        self.miss_sound = pygame.mixer.Sound("miss_sound - Copy.wav")
        pygame.mixer.music.load("bd_background_music.wav")
    def play_miss_sound(self):
        self.miss_sound.set_volume(9)
        self.miss_sound.play()
        print("playing")
        # time.sleep(.9)
    def play_bark_sound(self):
        self.bark_sound.play()

# save data section
#############################################
def create_player_json(player_name):
    try:
        # Attempt to read the existing player data from the file
        with open("players.json", "r") as file:
            players = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, initialize players as an empty list
        players = []

    # Check if the player already exists
    for player in players:
        if player["player_name"] == player_name:
            print("Player already exists.")
            return False

    # Create new player data
    player_data = {
        "player_name": player_name,
        "player_score": 0,  # Initialize player score to 0
    }

    # Append the new player data to the list of players
    players.append(player_data)

    # Write the updated player data back to the file
    with open("players.json", "w") as file:
        json.dump(players, file, indent=4)

    print("Player created successfully.")
    return True

def read_players():
    try:
        with open("players.json", "r") as file:
            try:
                players = json.load(file)
                if not players:
                    print("The file is empty.")
                return players
            except json.decoder.JSONDecodeError:
                print("The file is empty or does not contain valid JSON data.")
                return []
    except FileNotFoundError:
        return []


def delete_player(player_name):
    players = read_players()
    players_count = len(players)
    new_set_of_players = []
    for player in players:
        if player["player_name"] != player_name:
            new_set_of_players.append(player)
    if len(new_set_of_players) < players_count:
        print("deleted")
    else:
         print("not deleted")
    with open("players.json", "w") as file:
        json.dump(new_set_of_players, file, indent=4)

def update_player(player_name, new_player_score):
    players = read_players()
    player_found = False  # Flag to track if player was found
    for player in players:
        if player["player_name"] == player_name:
            player["player_score"] = new_player_score
            player_found = True
            break  # No need to continue iterating if player is found

    if not player_found:
        print("Player not found.")

    with open("players.json", "w") as file:
        json.dump(players, file, indent=4)

#

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    a, b = pygame.mouse.get_pos()
                    if self.new_game_button.collidepoint(a, b):
                        game = Game(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.display_surface)
                        game.run_game()



            self.activate_button()
            self.display_surface.blit(self.title_surf, self.title_rect)
            self.display_surface.blit(self.dog_title_surf, self.dog_title_rect)
            self.display_surface.blit(self.new_game_surf, (self.new_game_button.x - 20, self.new_game_button.y + 5))
            self.display_surface.blit(self.credits_surf, self.credits_rect)
            pygame.display.update()

        pygame.quit()


#



# Usage
if __name__ == "__main__":
    pygame.init()
    main_menu = MainMenu()
    main_menu.run()

# GAMEON = Game(WINDOW_WIDTH,WINDOW_HEIGHT,display_surface)
# GAMEON.run_game()
pygame.quit()