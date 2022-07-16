import button
import pygame
import fourier
import old_spiro
import poly_main

fourier_button = button.BoolButton(pos = (50, 50), size =(300, 100), color = (70,70,200), text = "custom drawing", elevation=5)
old_spiro_button = button.BoolButton(pos = (450, 50), size =(300, 100), color = (15,200,15), text = "symmetric circles", elevation=5)
polygons_button = button.BoolButton(pos = (850, 50), size =(300, 100), color = (200,15,15), text = "draw polygons", elevation=5)
buttons = [fourier_button, old_spiro_button, polygons_button]

width, height = 1200, 500


def main_screen_main():
	pygame.init()
	screen = pygame.display.set_mode((width, height))

	while True:
		for button in buttons:
			button.check_hover()
			button.draw(screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()

			if fourier_button.process_clicked(event, screen):
				r = fourier.fourier_main()
				if r == False:
					exit()
				else:
					screen = pygame.display.set_mode((width, height))

			elif old_spiro_button.process_clicked(event, screen):
				r = old_spiro.old_spiro_main()
				if r == False:
					exit()
				else:
					screen = pygame.display.set_mode((width, height))

			elif polygons_button.process_clicked(event, screen):
				r = poly_main.poly_main()
				if r == False:
					exit()
				else:
					screen = pygame.display.set_mode((width, height))

		pygame.display.update()
		screen.fill((255,255,255))

if __name__ == '__main__':
	main_screen_main()
