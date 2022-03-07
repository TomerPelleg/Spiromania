import pygame
import numpy as np
from math import cos, sin, pi
from time import sleep
import cmath

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
# start = np.asarray((width//2, height//2),dtype=float)
start = np.asarray((width // 2, height // 2))

def rep(z):
	return (z.real, z.imag)

class Spiro:
	def __init__(self, radii, init_degrees, speeds=None, screen=None, cfs=None):
		pygame.init()
		if screen is None:
			self.screen = pygame.display.set_mode((width, height))
		else:
			self.screen = screen

		self.screen.fill(WHITE)

		if speeds is None:
			speeds = np.ones(np.shape(radii))
		self.rs = np.array(radii)
		init_degrees = np.array(init_degrees)
		self.betas = np.array(init_degrees)

		# point = self.draw_spiro(alpha=0)

		trace_l = int(1e5)
		trace = np.full((trace_l, 2), (0,0)) # point
		trace2 = np.full((trace_l, 2), (0,0)) # point
		t, i = 0, 0

		# betas = np.copy(self.rs)
		# print(self.rs)
		# for i in range(len(self.rs)-1,0,-1):
		# betas[i] /= betas[i-1]

		# clock = pygame.time.Clock()
		# t2 = pygame.time.get_ticks()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.display.quit()
					pygame.quit()
					return

			pygame.display.update()
			self.screen.fill(WHITE)

			# self.betas = 10*t * self.rs[0] / self.rs + init_degrees
			self.betas = t*speeds + init_degrees
			# self.betas = 100*t + init_degrees

			#point = self.draw_spiro(alpha=0)
			partial_sum = [sum(cfs[:w]) for w in range(len(cfs))]
			partial_sum = [rep(jj) for jj in partial_sum]
			centers = [partial_sum[2*w] for w in range(len(cfs)//2)]
			fixed_points = [partial_sum[2*w+1] for w in range(len(cfs)//2)]
			# point = self.new_draw_spiro(0, centers, fixed_points)
			sum_v = width//2 + 1.j*(height//2)
			rotator = [cmath.exp(1.j*speeds[n]*t) for n in range(len(cfs))]
			cfs *= rotator

			for q in cfs:
				pygame.draw.lines(self.screen, BLUE, False, [rep(sum_v),rep(q+sum_v)], width=2)
				sum_v+=q
			trace[i] = rep(sum_v) # point
			# trace2[i] = point
			if i > 2:
				pygame.draw.lines(self.screen, RED, False, trace[:i], width=2)
				pygame.draw.lines(self.screen, TRK, False, trace2[:i], width=2)
			t += 1e-3
			i = (i + 1) % trace_l

			# t1 = t2
			# t2 = pygame.time.get_ticks()
			# print(t2-t1)
			# clock.tick(2000)

	def new_draw_spiro(self, alpha=0.5, centers=None, fixed_points=None):
		if centers is None or fixed_points is None:
			centers, fixed_points = self.stack_spiro()
		# print('centers:', list(centers))
		# print('fixed:', list(fixed_points), end='\n\n')

		centers += start
		fixed_points += start
		dist = (centers-fixed_points)**2
		dist = (dist[:,0] + dist[:,1])**0.5
		self.rs = dist
		# rs = [complex(dkj-ksdf) for dkj,ksdf in zip(centers, fixed_points)]

		for i, r in enumerate(self.rs):
			pygame.draw.circle(self.screen, BLACK, centers[i], r, width=3)
			if i > 0:
				pygame.draw.line(self.screen, GREY, centers[i], fixed_points[i], width=3)
				# moving_p =
				# pygame.draw.line(self.screen, BLACK, centers[i], moving_p, width=3)
		return alpha * centers[-1] + (1 - alpha) * fixed_points[-1]

	def draw_spiro(self, alpha=0.5, centers=None, fixed_points=None):
		if centers is None or fixed_points is None:
			centers, fixed_points = self.stack_spiro()
		# print('centers:', list(centers))
		# print('fixed:', list(fixed_points), end='\n\n')

		centers += start
		fixed_points += start

		for i, r in enumerate(self.rs):
			pygame.draw.circle(self.screen, BLACK, centers[i], r, width=3)
			if i > 0:
				pygame.draw.line(self.screen, GREY, centers[i], fixed_points[i], width=3)
				# moving_p =
				# pygame.draw.line(self.screen, BLACK, centers[i], moving_p, width=3)
		return alpha * centers[-1] + (1 - alpha) * fixed_points[-1]

	def stack_spiro(self):
		num = len(self.rs)
		centers = np.full((num, 2), 0.)
		fixed_points = np.full((num, 2), 0.)
		fixed_points[0] = (self.rs[0] * cos(self.betas[0]), self.rs[0] * sin(self.betas[0]))

		c, f = centers[0], fixed_points[0]
		for i in range(1, num):
			c = c * self.rs[i] - f * (self.rs[i - 1] + self.rs[i])
			c = c / (-self.rs[i - 1])
			centers[i] = c

			new_p = f - c
			# new_p *= cos(betas[i])+i*sin(betas[i])
			new_p = np.array([new_p[0] * cos(self.betas[i]) - new_p[1] * sin(self.betas[i]),
							  new_p[0] * sin(self.betas[i]) + new_p[1] * cos(self.betas[i])])
			new_p = new_p + c
			f = new_p
			fixed_points[i] = f
		return centers, fixed_points

# if __name__ == '__main__':
# 	radii = np.array([64,32,64,32,16])
# 	# radii = np.array([20, 90, 50])
# 	# radii = np.array([150,-35])
# 	# init_degrees = np.deg2rad(np.array([0,0,0]))
# 	init_degrees = np.zeros(radii.shape)
#
# 	s = Spiro(radii, init_degrees)
