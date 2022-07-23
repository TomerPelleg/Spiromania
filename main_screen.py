import button
import pygame
import fourier
import old_spiro
import poly_main

width, height = 900, 200

fourier_button, old_spiro_button, polygons_button, buttons = [0]*4
def init_buttons():
	global fourier_button, old_spiro_button, polygons_button, buttons
	fourier_button = button.BoolButton(pos = (3*width//4-50, height//2-50), size =(200, 100), color = (60,200,140), text = "Custom Drawing", elevation=5)
	old_spiro_button = button.BoolButton(pos = (2*width//4-100, height//2-50), size =(200, 100), color = (100,200,100), text = "Symmetric Circles", elevation=5)
	polygons_button = button.BoolButton(pos = (width//4-150, height//2-50), size =(200, 100), color = (140,200,60), text = "Draw Polygons", elevation=5)
	buttons = [fourier_button, old_spiro_button, polygons_button]
init_buttons()


def main_screen_main():
	pygame.init()
	global width, height
	screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

	while True:
		for button in buttons:
			button.check_hover()
			button.draw(screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				return

			if event.type == pygame.VIDEORESIZE:
				screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
				width, height = event.size
				print(event.size)
				init_buttons()

			if fourier_button.process_clicked(event, screen):
				r = fourier.fourier_main()
				if r == False:
					exit()
				else:
					screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

			elif old_spiro_button.process_clicked(event, screen):
				r = old_spiro.old_spiro_main()
				if r == False:
					exit()
				else:
					screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

			elif polygons_button.process_clicked(event, screen):
				r = poly_main.poly_main()
				if r == False:
					exit()
				else:
					screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

		pygame.display.update()
		screen.fill((255,255,255))


if __name__ == '__main__':
	main_screen_main()
