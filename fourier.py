import cmath
from copy import deepcopy

import numpy as np
import pygame
from spiro import Spiro

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PI = cmath.pi
width, height = (1000, 700)
start = np.asarray((width // 2, height // 2))


def create_function(points):
	xs = np.linspace(-1*PI, PI, np.shape(points)[0])
	ys = points[:,0] + points[:,1] * 1j
	return xs, ys


def num(k):
	return (-1) ** k * (k + 1) // 2


def calc_coeffs(xs, ys, k):
	cfs = np.zeros(k, dtype=complex)
	for n in range(k):
		y_cpy = np.array([cmath.exp(-1j * num(n) * xs[ni]) for ni in range(len(xs))])
		cfs[n] = sum(ys * y_cpy) / (len(xs)-1)
	return cfs


def main():
	pygame.init()
	global screen
	screen = pygame.display.set_mode((1000, 700))

	screen.fill(WHITE)
	# pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,50,50))
	pygame.display.update()

	ps = np.full((10000, 2), 0, dtype=float)
	i = 0
	k = 50
	add_to_arr = False
	r = pygame.Rect(0, 0, 10, 10)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				return

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:		# IF ENTER IS PRESSED
					ps = ps[:i]-start
					xs, ys = create_function(ps)
					coeffs = calc_coeffs(xs, ys, k)
					speeds = np.array([num(ki) for ki in range(k)])
					s = Spiro(speeds, coeffs, screen)

					rs = np.array(coeffs, dtype=int) ** 2 + np.array(-1j * coeffs, dtype=int) ** 2
					# s = OldSpiro(, [150,-35], , screen)

					pygame.display.quit()
					pygame.quit()
					return

			if event.type == pygame.MOUSEBUTTONDOWN:
				ps = np.full((1000, 2), 0, dtype=float)
				i = 0
				add_to_arr = True

			if event.type == pygame.MOUSEBUTTONUP:
				if len(ps)<2:
					add_to_arr = False
					continue
				pos = pygame.mouse.get_pos()
				add_to_arr = False
				screen.fill(WHITE)
				pygame.draw.lines(screen, (0, 0, 0), True, ps[:i], width=5)
				# for p in ps:
				# r.move_ip(pos)
				# pygame.surface
				# pygame.draw.rect(screen, (0,0,0), pygame.Rect(p, (50,50)))
				pygame.display.update()
			if add_to_arr:
				pos = pygame.mouse.get_pos()
				pygame.draw.rect(screen, (0, 0, 175), pygame.Rect(pos, (10, 10)))
				print(pos)
				ps[i] = pos
				i += 1
		# pygame.draw.lines(screen, (0,0,0), True, ps[:i], width=5)


if __name__ == '__main__':
	main()
