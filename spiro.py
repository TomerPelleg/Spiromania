import pygame
import numpy as np
from math import cos, sin, pi
from time import sleep
import cmath
from button import Button, TextButton, IntTextButton, BoolButton

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

		text_test_button = TextButton(pos = (0, 10), size =(200, 100), color = (15,15,100), text = "Me Text!", elevation=5)
		test_int_button = IntTextButton(pos = (300, 10), size =(200, 100), color = (15,100,100), text = "Me Int!", elevation=5)
		test_bool_button = BoolButton(pos = (600, 10), size =(200, 100), color = (100,15,100), text = "Me Silent!", elevation=5)
		buttons = [test_int_button, test_bool_button, text_test_button]
		while True:
			for button in buttons:
				button.check_hover()
			for event in pygame.event.get():
				for button in buttons:
					button.process_clicked(event, screen)
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
				pygame.draw.lines(self.screen, RED, False, trace[:i], width=2)
			t += 1e-5
			i = (i + 1) % trace_l

			for button in buttons:
				button.draw(screen)

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