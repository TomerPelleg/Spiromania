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


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

s0 = [(0, 0), (5, 0), (6, 6), (3, 8), (1, 4), (2, 2)]
s1 = [(-1,1), (4,-4), (5,-2), (11,1), (10,5), (3,15)]

#create regular polygon, with right most vertex in (0,0)
# x vertices, and edge length of length
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
					dtype=np.float64)*10 + (450,311)
	outside_shape = np.asarray(create_regular_polygon(7, 3),
					dtype=np.float64)*10 + (450,311)
	inside_Shape = Shape(inside_shape)
	outside_Shape = Shape(outside_shape)
	outside_Polygon = Polygon(outside_Shape.cur_points)

	pygame.init()
	screen = pygame.display.set_mode((width, height))

	screen.fill((255,255,255))
	inside_Shape.draw_shape(screen)
	outside_Shape.draw_shape(screen)

	pygame.display.update()
	clock = pygame.time.Clock()

	esc_button = button.BoolButton(pos=(width-210, 10), size=(200, 100), color=(15,150,200), text="Main Screen", elevation=5)
	button_one = button.BoolButton(pos=(10, 10), size=(200, 100), color=(15,150,200), text="General Shapes", elevation=5)
	regular_button = button.BoolButton(pos = (10, 150), size =(200, 100), color = (15,150,200), text = "Regular Shapes", elevation=5)
	speed_slider = button.Slider(pos=(width-275, height-50), length=250, min_val=10, max_val=100, name="speed", start_val=20)
	hidden_buttons = [0]*4
	hidden_buttons[0] = button.Slider(pos = (width//3-150, height//3-50), length=250, min_val=3, max_val=20, name = "Outside Shape Edges", start_val=8)
	hidden_buttons[1] = button.Slider(pos = (2*width//3-150, height//3-50), length=250, min_val=1, max_val=10, name = "Outside Shape Length")
	hidden_buttons[2] = button.Slider(pos = (width//3-150, 2*height//3-50), length=250, min_val=3, max_val=22, name = "Inside Shape Edges")
	hidden_buttons[3] = button.Slider(pos = (2*width//3-150, 2*height//3-50), length=250, min_val=1, max_val=10, name= "Inside Shape Length")
	go_button = button.BoolButton(pos=(width-225, height-125), size=(200,100), color=(50,125,150), text="Draw")
	buttons = [esc_button, button_one, speed_slider,regular_button]

	cntr = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				return False
			for element in buttons:
				element.process_clicked(event, screen)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_one.process_clicked(event, screen):
					# user specified polygons
					screen.fill((255,255,255))
					pygame.display.update()
					outside_shape = get_points(screen, 'Enter Outer Shape Vertices. Click on the vertices locations, and the app will auto-complete the last edge when you press enter')
					inside_shape = get_points(screen, 'Enter Inner Shape Vertices. Click on the vertices locations, and the app will auto-complete the last edge when you press enter')
					draw_point = get_points(screen, 'Enter point to follow. Click on the point!', skip_chinese=True)
					screen.fill((255,255,255))
					pygame.display.update()
					inside_Shape = Shape(inside_shape)
					inside_Shape.update_special_point(draw_point[0])
					outside_Shape = Shape(outside_shape)
					outside_Polygon = Polygon(outside_Shape.cur_points)
					inside_Shape.draw_shape(screen)
					outside_Shape.draw_shape(screen)
					pygame.display.update()

				if regular_button.process_clicked(event, screen): 		# insert polygons
					#user input regular shapes
					target_list = [None,None,None,None]
					clicked = -1
					screen.fill((255,255,255))
					finished = False
					while not finished:
						pygame.display.update()
						screen.fill((255,255,255))
						for j in range(4):
							hidden_buttons[j].draw(screen)
							hidden_buttons[j].check_hover()
						go_button.draw(screen)
						go_button.check_hover()
						for mini_event in pygame.event.get():
							for j in range(4):
								hidden_buttons[j].process_clicked(mini_event, screen)
							if go_button.process_clicked(event, screen):
								target_list = [hidden_buttons[i].get_val() for i in range(4)]
								finished = True
								break

					scale = 10
					outside_raw_polygon =create_regular_polygon(target_list[0], target_list[1])
					center = sum(outside_raw_polygon, start = (0,0))
					center = (center[0] /len(outside_raw_polygon),center[1] / len(outside_raw_polygon)) #vertex 0 of the polygon
					center = (center[0] - target_list[1] / sympy.sin(sympy.pi / target_list[0]), center[1]) #center of mass of polygon
					center = (int(center[0]), int(center[1]))
					print("here here")
					center = (center[0]*scale, center[1]*scale) #scale
					inside_shape = np.asarray(create_regular_polygon(target_list[2], target_list[3]),
											  dtype=np.float64) * scale + (width/2, height/2) - center
					outside_shape = np.asarray(outside_raw_polygon,
											   dtype=np.float64) * scale + (width/2, height/2) - center
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
		inside_Shape.draw_shape(screen, (0, 0, 255)) #draw inside shape (and rotate it)
		outside_Shape.draw_shape(screen) # draw outside shpae
		pygame.display.update()
		# clock.tick(500)
		time.sleep(0.1/speed_slider.get_val())
		cntr += 1


if __name__ == "__main__":
	poly_main()

# todo: add button for Main Screen
