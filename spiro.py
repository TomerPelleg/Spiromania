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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
TRK = (0, 180, 120)
BLUE = (0, 0, 255)
alpha = 0

width, height = (1000, 700)
start = np.asarray((width // 2, height // 2))


def rep(z):
	return (z.real, z.imag)


class Spiro:
	def __init__(self, speeds, cfs, screen=None):
		pygame.init()
		if screen is None:
			self.screen = pygame.display.set_mode((width, height))
		else:
			self.screen = screen

		self.screen.fill(WHITE)

		trace_l = int(1e5)
		trace = np.full((trace_l, 2), (0, 0))  # point
		t, i = 0, 0

		return_button = BoolButton(pos = (0, 0), size =(200, 100), color = (100,15,100), text = "Draw Again!", elevation=5)
		slider = Slider(pos = (300, 20), length = 400, min_val = 1, max_val= 1000)
		buttons = [return_button]
		while True:
			if return_button.get_val():
				return
			for button in buttons:
				button.check_hover()
				slider.check_hover()
			for event in pygame.event.get():
				for button in buttons:
					button.process_clicked(event, screen)
				slider.process_clicked(event, screen)

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

			sum_v = width // 2 + 1.j * (height // 2)
			rotator = [cmath.exp(1.j * speeds[n] * t) for n in range(len(cfs))]
			cfs *= rotator

			for q in cfs:
				pygame.draw.lines(self.screen, BLUE, False, [rep(sum_v),rep(q+sum_v)], width=2)
				sum_v += q
			trace[i] = rep(sum_v)

			if i > 2:
				for idx in range(int(max(0, i- 2 * math.pi / t)), i):
					decay_factor = 0.5 + (idx - max(0, i- 2 * math.pi / t)) * 0.5 / (i - max(0, i- 2 * math.pi / t))
					decay_red = int(decay_factor * 255)
					pygame.draw.line(self.screen, (decay_red, 0, decay_red), trace[idx], trace[idx+1], width=2)
			t += 1e-5
			i = (i + 1) % trace_l
			time.sleep(0.01 / slider.get_val())

			for button in buttons:
				button.draw(screen)
			slider.draw(screen)

# def new_draw_spiro(self, centers, fixed_points, alpha=0.5):
	# 	dist = (centers - fixed_points) ** 2
	# 	dist = (dist[:, 0] + dist[:, 1]) ** 0.5
	# 	radii = dist
	#
	# 	centers += start
	# 	fixed_points += start
	#
	# 	for i, r in enumerate(radii):
	# 		pygame.draw.circle(self.screen, BLACK, centers[i], r, width=3)
	# 		if i > 0:
	# 			pygame.draw.line(self.screen, GREY, centers[i], fixed_points[i], width=3)
	# 	return alpha * centers[-1] + (1 - alpha) * fixed_points[-1]