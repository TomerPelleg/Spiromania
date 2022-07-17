import math

import pygame

pygame.font.init()

class Button:
    def __init__(self, pos, size, color='#475F77', text="Hi", elevation = 5, print_text = True):
        self.nice_font = pygame.font.SysFont('Comic Sans MS', 20)
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.bottom_color = '#354B5E'
        self.elevation = elevation
        self.print_text = print_text
        self.is_clicked = False

        self.rect = pygame.Rect((self.x, self.y-self.elevation), size)
        self.down_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.text = text
        self.text_surface = self.nice_font.render(text, False, (0, 0, 0))

        self.extra_init_steps()

    def extra_init_steps(self):
        pass

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.nice_font.render(new_text, False, (0, 0, 0))

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
        else:
            return None

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
            screen.blit(self.text_surface, self.text_surface.get_rect(center = self.down_rect.center))


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
                    elif event.key == pygame.K_BACKSPACE:  # for removing (backspace)
                        if len(txt):
                            txt = txt[:-1]
                    # if(event.unicode.isalnum()):
                    #     txt.append(event.unicode)
                    else:
                        txt.append(event.unicode)
                    self.update_text("".join(txt))
                    self.draw(screen)
                    pygame.display.update()

class IntTextButton(Button):
    def check_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                if self.down_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    self.is_clicked = True
        return self.is_clicked

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
        self.is_clicked = False

    def get_val(self):
        return self.is_clicked

    def process_clicked(self, event, screen):
        if self.check_clicked(event):
            self.is_clicked = not self.is_clicked
            return True
        else:
            return False

class Slider:
    def __init__(self, pos, length, min_val=5, max_val=50, start_val = 5, circ_color='#FF0000', bar_color = '#354B5E', radius = 10, name = ""):
        self.nice_font = pygame.font.SysFont('Comic Sans MS', 15)
        self.x = pos[0]
        self.y = pos[1]
        self.length = length
        self.min_val = min_val
        self.max_val = max_val
        self.circ_color = circ_color
        self.bar_color = bar_color
        self.val = start_val
        self.name = name
        self.circle_center = (pos[0] + int((min(max(start_val, min_val), max_val) - min_val) * length / (max_val-min_val)), pos[1]+radius/2)
        self.radius = radius
        self.is_clicked = False
        self.min_center = (self.x + 5, self.y + self.radius + 10)
        self.max_center = (self.x+self.length - 5, self.y +self.radius + 10)

        self.rect = pygame.Rect((self.x, self.y), (self.length, self.radius))
        self.min_text = self.nice_font.render(str(self.min_val), False, (0, 0, 0))
        self.max_text = self.nice_font.render(str(self.max_val), False, (0, 0, 0))
        self.val_text = self.nice_font.render(str(self.val), False, (0, 0, 0))
        self.name_text = self.nice_font.render(str(self.name), False, (0, 0, 0))

        self.extra_init_steps()

    def extra_init_steps(self):
        pass

    def update_text(self):
        self.val_text = self.nice_font.render(str(self.val), False, (0, 0, 0))

    def update_val(self):
        self.val = int(self.min_val + (self.circle_center[0] - self.x)/float(self.length) * (self.max_val - self.min_val))
        self.update_text()

    def is_mouse_touching(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        return bool(math.sqrt((self.circle_center[0] - mouse_pos_x) ** 2 + (self.circle_center[1] - mouse_pos_y) ** 2)<=self.radius)

    def check_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.is_mouse_touching():
                    self.is_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False

    def process_clicked(self, event, screen):
        self.check_clicked(event)

    def check_hover(self):
        if self.is_clicked:
            self.circle_center = (min(max(pygame.mouse.get_pos()[0], self.x), self.x + self.length), self.circle_center[1])
            self.update_val()
        else:
            pass

    def get_val(self):
        return self.val

    def draw(self, screen):
        #callee must do pygame.display.update()

        #clean area for nicer draw
        pygame.draw.rect(screen, "#FFFFFF", pygame.Rect((self.x - 10, self.y - 20), (self.length + 20, self.radius + 40)))

        #draw down rectanle for nicer view
        pygame.draw.rect(screen, self.bar_color, self.rect, border_radius = 12)
        #draw up rectangle
        pygame.draw.circle(screen, self.circ_color, self.circle_center, self.radius)
        #draw texts
        screen.blit(self.val_text, self.val_text.get_rect(center = (self.x + self.length/2, self.y - 10)))
        screen.blit(self.min_text, self.min_text.get_rect(center = self.min_center))
        screen.blit(self.max_text, self.max_text.get_rect(center = self.max_center))
        screen.blit(self.name_text, self.name_text.get_rect(center = (self.x + self.length/2, self.y + self.radius + 10)))


