import numpy as np
import pygame
from shape import Shape
import time
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from inputshape import get_points
import button
import math
import sympy

s0 = [(0, 0), (5, 0), (6, 6), (3, 8), (1, 4), (2, 2)]
s1 = [(-1,1), (4,-4), (5,-2), (11,1), (10,5), (3,15)]

def create_regular_polygon(x, length):
	listo = []
	radius = length / sympy.sin(sympy.pi/x)
	for i in range(x):
		listo.append((radius*sympy.cos(2*i*sympy.pi/x) - radius, radius*sympy.sin(2*i*sympy.pi/x)))
	return listo

square = [(0,0),(3,0),(3,3),(0,3)]
triangle = [(0,0),(0.5,(3**0.5)/2),(1,0)]
pentagon = [(0,0), (2,0), (2.62,1.9), (1,3.08), (-0.62,1.9)]
hexagon = [(0,0), (6,0), (9,5.2), (6, 10.4), (0,10.4), (-3, 5.2)]


def poly_main():
	inside_shape = np.asarray(create_regular_polygon(4, 3),
					dtype=np.float64)*10 + (300,300)
	outside_shape = np.asarray(create_regular_polygon(7, 3),
					dtype=np.float64)*10 + (300,300)
	inside_Shape = Shape(inside_shape)
	outside_Shape = Shape(outside_shape)
	outside_Polygon = Polygon(outside_Shape.cur_points)

	pygame.init()
	screen = pygame.display.set_mode((720, 500))

	screen.fill((255,255,255))
	inside_Shape.draw_shape(screen)
	outside_Shape.draw_shape(screen)

	pygame.display.update()
	clock = pygame.time.Clock()

	esc_button = button.BoolButton(pos=(500, 10), size=(200, 100), color=(70,70,200), text="main screen", elevation=5)
	button_one = button.BoolButton(pos=(10, 10), size=(200, 100), color=(150, 150, 15), text="draw shapes", elevation=5)
	buttons = [esc_button, button_one]

	cntr = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_one.process_clicked(event, screen):
					screen.fill((255,255,255))
					pygame.display.update()
					outside_shape = get_points(screen)
					inside_shape = get_points(screen)
					screen.fill((255,255,255))
					pygame.display.update()
					inside_Shape = Shape(inside_shape)
					outside_Shape = Shape(outside_shape)
					outside_Polygon = Polygon(outside_Shape.cur_points)
					inside_Shape.draw_shape(screen)
					outside_Shape.draw_shape(screen)
					pygame.display.update()
				if esc_button.process_clicked(event, screen):
					return True
		for i in range(5):
			inside_Shape.calc_rotated(outside_Shape.cur_points, outside_Polygon)

		screen.fill((255,255,255))
		for s_button in buttons:
			s_button.check_hover()
			s_button.draw(screen)
		inside_Shape.draw_shape(screen, (0, 0, 255))
		outside_Shape.draw_shape(screen)
		pygame.display.update()
		clock.tick(500)
		cntr += 1


if __name__ == "__main__":
	poly_main()

# todo: add button for main screen
