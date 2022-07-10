import pygame

pygame.font.init()
nice_font = pygame.font.SysFont('Comic Sans MS', 30)

class Button:
    def __init__(self, pos, size, color='#475F77', text="Hi", elevation = 5):
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.bottom_color = '#354B5E'
        self.elevation = elevation

        self.rect = pygame.Rect(pos, size)
        self.down_rect = pygame.Rect((self.x, self.y+self.elevation), (self.width, self.height))
        self.text = text
        self.text_surface = nice_font.render(text, False, (0, 0, 0))

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = nice_font.render(new_text, False, (0, 0, 0))


    def check_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    return True
        return False

    def get_user_input(self, screen):
        txt = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # for finishing (enter)
                        ret = "".join([c for c in txt if c.isalnum()])
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





    def process(self, event, screen):
        if self.check_clicked(event):
            self.get_user_input(screen)




    def draw(self, screen):
        #draw down rectanle for nicer view
        pygame.draw.rect(screen, self.bottom_color, self.down_rect, border_radius = 12)
        #draw up rectangle
        pygame.draw.rect(screen, self.color, self.rect, border_radius = 12)
        #draw text
        screen.blit(self.text_surface, self.text_surface.get_rect(center = self.rect.center))
        pygame.display.update()

