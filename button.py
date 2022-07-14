import pygame

pygame.font.init()
nice_font = pygame.font.SysFont('Comic Sans MS', 30)

class Button:
    def __init__(self, pos, size, color='#475F77', text="Hi", elevation = 5, print_text = True):
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.bottom_color = '#354B5E'
        self.elevation = elevation
        self.print_text = print_text

        self.rect = pygame.Rect((self.x, self.y-self.elevation), size)
        self.down_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.text = text
        self.text_surface = nice_font.render(text, False, (0, 0, 0))

        self.extra_init_steps()

    def extra_init_steps(self):
        pass

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = nice_font.render(new_text, False, (0, 0, 0))

    def update_rect(self):
        self.rect = pygame.Rect((self.x, self.y-self.elevation), (self.width, self.height))
        self.down_rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def check_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                if self.down_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    return True
        return False

    def click_func(self, screen):
        pass

    def process_clicked(self, event, screen):
        if self.check_clicked(event):
            return self.click_func(screen)

    def check_hover(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if self.down_rect.collidepoint(mouse_pos_x, mouse_pos_y):
            self.elevation = 1
        else:
            self.elevation =5
        self.update_rect()

    def draw(self, screen):
        #callee must do pygame.display.update()

        #draw down rectanle for nicer view
        pygame.draw.rect(screen, self.bottom_color, self.down_rect, border_radius = 12)
        #draw up rectangle
        pygame.draw.rect(screen, self.color, self.rect, border_radius = 12)
        #draw text
        if(self.print_text):
            screen.blit(self.text_surface, self.text_surface.get_rect(center = self.rect.center))


class TextButton(Button):
    def click_func(self, screen):
        txt = []
        self.update_text("".join(txt))
        self.draw(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # for finishing (enter)
                        ret = "".join(txt)
                        if ret:
                            return ret
                        else:
                            return "" #behaviour for empty input
                    if event.key == pygame.K_BACKSPACE:  # for removing (backspace)
                        if len(txt):
                            txt = txt[:-1]
                    if(event.unicode.isalnum()):
                        txt.append(event.unicode)
                    self.update_text("".join(txt))
                    self.draw(screen)
                    pygame.display.update()

class IntTextButton(Button):
    def click_func(self, screen):
        txt = []
        self.update_text("".join(txt))
        self.draw(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # for finishing (enter)
                        ret = "".join(txt)
                        if not ret:
                            ret = "0"
                            self.update_text("0")
                        ret = int(ret)
                        if ret:
                            return ret
                        else:
                            return "" #behaviour for empty input
                    if event.key == pygame.K_BACKSPACE:  # for removing (backspace)
                        if len(txt):
                            txt = txt[:-1]
                    if(event.unicode.isdigit()):
                        txt.append(event.unicode)
                    self.update_text("".join(txt))
                    self.draw(screen)
                    pygame.display.update()


class BoolButton(Button):
    def extra_init_steps(self):
        self.print_text = False

    def process_clicked(self, event, screen):
        if self.check_clicked(event):
            return True
        else:
            return False