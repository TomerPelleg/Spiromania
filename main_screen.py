from button import TextButton, BoolButton
import pygame
import fourier
import old_spiro
import poly_main

fourier_button = BoolButton(pos = (0, 10), size =(300, 100), color = (15,15,200), text = "custom drawing", elevation=5)
old_spiro_button = BoolButton(pos = (400, 10), size =(300, 100), color = (15,200,15), text = "symmetric circles", elevation=5)
polygons_button = BoolButton(pos = (800, 10), size =(300, 100), color = (200,15,15), text = "draw polygons", elevation=5)

buttons = [fourier_button, old_spiro_button, polygons_button]


def main_screen_main():
	pygame.init()
	screen = pygame.display.set_mode((1100, 700))

	while True:
		for button in buttons:
			button.check_hover()
		for event in pygame.event.get():
			if fourier_button.process_clicked(event, screen):
				fourier.fourier_main()
			elif old_spiro_button.process_clicked(event, screen):
				old_spiro.old_spiro_main()
			elif polygons_button.process_clicked(event, screen):
				poly_main.poly_main()

		pygame.display.update()
		screen.fill((255,255,255))
		for button in buttons:
			button.draw(screen)

if __name__ == '__main__':
	main_screen_main()
