import math

import pygame
import time
import numpy as np
from math import cos, sin, pi
from time import sleep
import cmath
from button import Button, TextButton, IntTextButton, BoolButton, Slider

# POSITIVE RADIUS MEANS OUTSIDE

# optimizations:
# https://stackoverflow.com/questions/70092416/pygame-efficient-way-to-draw-traceline-of-moving-object
# also, pygame.display.update() can receive a rect to update instead of the entire screen

#class to draw fourier circles

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
TRK = (0, 180, 120)
BLUE = (0, 0, 255)
alpha = 0

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = (pygame.display.Info().current_w, pygame.display.Info().current_h)
start = np.asarray((width // 2, height // 2))


def rep(z):
	return (z.real, z.imag)


class Spiro:
	def __init__(self, speeds, cfs, screen=None, ps = None):
		pygame.init()
		if screen is None:
			self.screen = pygame.display.set_mode((width, height))
		else:
			self.screen = screen

		self.screen.fill(WHITE)

		trace_l = int(1e5)
		trace = np.full((trace_l, 2), (0, 0))  # point
		t_step = (1e-2)
		t, i = 0, 0
		rotator = [cmath.exp(1.j * speeds[n] * t_step) for n in range(len(cfs))]

		return_button = BoolButton(pos = (10, 10), size =(200, 100), color = "#775F47", text = "Draw Again!", fg_color="#FFFFFF", elevation=5)
		draw_circles_button = BoolButton(pos = (10, 160), size =(200, 100), color = "#775F47", text = "Show Circles", fg_color="#FFFFFF", elevation=5, extra_parameters=["Hide Circles"])
		draw_original_button = BoolButton(pos = (10, 310), size =(200, 100), color = "#775F47", text = "Show Original Drawing", fg_color="#FFFFFF", elevation=5, extra_parameters=["Hide Original Drawing"])

		slider = Slider(pos = (300, 20), length = 400, min_val = 10, max_val= 100, name = "speed")
		buttons = [return_button, draw_circles_button, draw_original_button]
		while True:
			if return_button.get_val():
				return
			for button in buttons:
				button.check_hover()
				slider.check_hover()
			for event in pygame.event.get():
				for button in buttons:
					button.process_clicked(event, self.screen)
				slider.process_clicked(event, self.screen)

				if event.type == pygame.QUIT:
					pygame.display.quit()
					pygame.quit()
					exit()

				if event.type == pygame.QUIT:
					pygame.display.quit()
					pygame.quit()
					return

			pygame.display.update()
			self.screen.fill(WHITE)

			# LINES WE USED TO HAVE. WE NEED THEM IF WE WANT TO DRAW CIRCLES
			# partial_sum = [sum(cfs[:w]) for w in range(len(cfs))]
			# partial_sum = [rep(jj) for jj in partial_sum]
			# centers = [partial_sum[2*w] for w in range(len(cfs)//2)]
			# fixed_points = [partial_sum[2*w+1] for w in range(len(cfs)//2)]

			cfs *= rotator
			sum_v = width // 2 + 1.j * (height // 2) + cfs[0] #cfs[0] is the offset - no need to draw

			for q in cfs[1:]:
				#calculate each circles new position
				pygame.draw.lines(self.screen, BLUE, False, [rep(sum_v),rep(q+sum_v)], width=2)
				if draw_circles_button.get_val():
					#draw circles
					pygame.draw.circle(self.screen, BLUE, rep(sum_v), abs(q), width=1)
				sum_v += q
			trace[i] = rep(sum_v)

			if i > 2:
				for j in range(len(ps)):
					if ps is not None and draw_original_button.get_val():
						#draw original drawing
						pygame.draw.rect(self.screen, (0, 0, 175), pygame.Rect(ps[j], (3, 3)))
				for idx in range(int(max(0, i- 1.9 * math.pi / t_step)), i):
					#draw trace
					decay_factor = 0.5 + (idx - max(0, i- 1.9 * math.pi / t_step)) * 0.5 / (i - max(0, i- 1.9 * math.pi / t_step))
					decay_red = int(decay_factor * 255)
					pygame.draw.line(self.screen, (decay_red, 0, decay_red), trace[idx], trace[idx+1], width=4)

			t += t_step
			i = (i + 1) % trace_l
			if i==0:
				print("yo")
			time.sleep(0.1 / slider.get_val())

			for button in buttons:
				button.draw(self.screen)
			slider.draw(self.screen)

