import random
import pygame

pygame.init()

'''
- Структурирование кода
- Отрисовать динозавра
- Подтянуть коллизии
- Меню с обучением (?выбор перса, ?выбор фона)
- Музыка
- Сделать всё под фулл скрин
- Отчёт и юнит тесты
'''

# Всё по экрану
display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))  # изменить в будущем под фулл скрин
# фуллскрин, но пока не имеет смысла и мешает, перерисовка Land
# pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
pygame.display.set_caption('images/Student Dino')

icon = pygame.image.load('images/icon.png')  # изменить в будущем
pygame.display.set_icon(icon)

cactus_img = [pygame.image.load('images/Cactus0.png'), pygame.image.load('images/Cactus1.png'),
              pygame.image.load('images/Cactus2.png')]
cactus_options = [69, 449, 37, 410, 40, 420]

Dino0 = pygame.image.load('images/Dino0.png')
Dino1 = pygame.image.load('images/Dino1.png')
Dino2 = pygame.image.load('images/Dino2.png')
Dino3 = pygame.image.load('images/Dino3.png')
Dino4 = pygame.image.load('images/Dino4.png')
Dino0 = pygame.transform.scale(Dino0, (Dino0.get_width() // 3, Dino0.get_height() // 3))
Dino1 = pygame.transform.scale(Dino1, (Dino1.get_width() // 3, Dino1.get_height() // 3))
Dino2 = pygame.transform.scale(Dino2, (Dino2.get_width() // 3, Dino2.get_height() // 3))
Dino3 = pygame.transform.scale(Dino3, (Dino3.get_width() // 3, Dino3.get_height() // 3))
Dino4 = pygame.transform.scale(Dino4, (Dino4.get_width() // 3, Dino4.get_height() // 3))

dino_img = [Dino0, Dino1, Dino2, Dino3, Dino4]

img_counter = 0


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive = (10, 10, 10)
        self.active = (0, 0, 0)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, (166, 255, 253), (x, y, self.width, self.height))
            print_text(message=message + '<', x=x + 10, y=y + 10, font_color=self.active, font_size=font_size)
            if click[0] == 1:
                if action is not None:
                    action()
        else:
            pygame.draw.rect(display, (166, 255, 253), (x, y, self.width, self.height))
        print_text(message=message, x=x + 10, y=y + 10, font_color=self.inactive, font_size=font_size)


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))  #


# Всё по персу
user_width = 60
user_height = 100
user_x = display_width // 3
user_y = display_height - user_height - 100

# Всё по кактусам

clock = pygame.time.Clock()
make_jump = False
jump_counter = 30
scores = 0
max_scores = 0
above_cactus = False


def gameplay():
    global make_jump
    game = True
    cactus_arr = []
    cactus_arr = create_cactus_arr(cactus_arr)
    land = pygame.image.load('images/land.jpg')

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()
        if make_jump:
            jump()

        count_score(cactus_arr)

        display.blit(land, (0, 0))
        print_text('Score: ' + str(scores), 600, 10)
        draw_array(cactus_arr)
        draw_dino()

        if check_collision(cactus_arr):
            game = False

        pygame.display.update()
        clock.tick(90)  # fps
    return game_over()


def jump():
    global user_y, jump_counter, make_jump
    if jump_counter >= -30:
        user_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 100, height, width, img, speed=4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, speed=4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 700, height, width, img, speed=4))

    return array


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < user_width:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    if choice >= 4:
        radius += random.randrange(200, 300)
    else:
        radius += random.randrange(300, 400)

    return radius


def check_collision(barriers):
    if barriers is not None:
        for barrier in barriers:
            if barrier.y == 449:
                if not make_jump:
                    if barrier.x <= user_x + user_width - 30 <= barrier.x + barrier.width:
                        return True
                elif jump_counter >= 0:
                    if user_y + user_height - 5 >= barrier.y:
                        if barrier.x <= user_x + user_width - 15 <= barrier.x + barrier.width:
                            return True
                else:
                    if user_y + user_height - 10 >= barrier.y:
                        if barrier.x <= user_x <= barrier.x + barrier.width:
                            return True
            else:
                if not make_jump:
                    if barrier.x <= user_x + user_width - 5 <= barrier.x + barrier.width:
                        return True
                elif jump_counter >= 10:
                    if user_y + user_height - 5 >= barrier.y:
                        if barrier.x <= user_x + user_width - 5 <= barrier.x + barrier.width:
                            return True
                else:
                    if user_y + user_height - 30 >= barrier.y:
                        if barrier.x <= user_x + user_width - 10 <= barrier.x + barrier.width:
                            return True
                    else:
                        if user_y + user_height - 30 >= barrier.y:
                            if barrier.x <= user_x + user_width - 10 <= barrier.x + barrier.width:
                                return True
        return False


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]
            cactus.return_self(radius, height, width, img)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (user_x, user_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game paused. Space to continue', 160, 200)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over', 300, 200)
        print_text('Jump to start. Esc to menu.', 170, 250)
        print_text('Max score: ' + str(max_scores), 530, 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return True
        if keys[pygame.K_ESCAPE]:
            show_menu()

        pygame.display.update()
        clock.tick(15)


def count_score(barriers):
    global scores
    for cactus in barriers:
        if cactus.x <= user_x and jump_counter == -30:
            scores += 1


def show_menu():
    menu_background = pygame.image.load('Menu.jpg')
    show = True

    start_btn = Button(230, 60)
    quit_btn = Button(230, 60)

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_game()

        display.blit(menu_background, (0, 0))
        start_btn.draw(270, 150, 'Start game', start_game, 40)
        quit_btn.draw(270, 210, 'How to play', tutorial, 40)
        pygame.display.update()
        clock.tick(60)


def start_game():
    global scores, make_jump, jump_counter, user_y
    while gameplay():
        scores = 0
        make_jump = False
        jump_counter = 30
        user_y = display_height - user_height - 100


def tutorial():
    menu_background = pygame.image.load('Menu.jpg')
    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            show_menu()

        display.blit(menu_background, (0, 0))
        print_text('Space to jump', 275, 150)
        print_text('Esc to menu', 275, 200)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    show_menu()
    pygame.quit()
    quit()
