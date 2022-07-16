import cmath
from copy import deepcopy

import numpy as np
import pygame
from spiro import Spiro
import button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PI = cmath.pi
width, height = (1000, 700)
start = np.asarray((width // 2, height // 2))


def create_function(points):
	xs = np.linspace(-1*PI, PI-2*PI/(np.shape(points)[0]), (np.shape(points)[0]))
	ys = points[:,0] + points[:,1] * 1j
	return xs, ys


def num(k):
	return (-1) ** k * (k + 1) // 2


def calc_coeffs(xs, ys, k):
	cfs = np.zeros(k, dtype=complex)
	for n in range(k):
		y_cpy = np.array([cmath.exp(-1j * num(n) * xs[ni]) for ni in range(len(xs))])
		cfs[n] = sum(ys * y_cpy) / (len(xs) - 1)
	return cfs

def draw(ps, i, circle_num):
	ps = ps[:i] - start
	xs, ys = create_function(ps)
	coeffs = calc_coeffs(xs, ys, circle_num)
	speeds = np.array([num(ki) for ki in range(circle_num)])
	s = Spiro(speeds, coeffs, screen, ps[:i] + start)
	print("no")
	return fourier_main()

def fourier_main():
	print("here")
	pygame.init()
	global screen
	screen = pygame.display.set_mode((1000, 700))

	screen.fill(WHITE)
	# pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,50,50))
	pygame.display.update()

	ps = np.full((10000, 2), 0, dtype=float)
	i = 0
	circle_num = 5
	is_drawing = False
	add_to_arr = False
	circle_num_slider = button.Slider(pos = (width - 300, 50), length = 280, min_val=5, max_val=100, start_val=50)
	draw_button = button.BoolButton(pos=(0, 0), size=(200, 100), color=(100, 15, 100), text="Start Draw", elevation=5)
	elephent_button = button.BoolButton(pos=(0, 150), size=(200, 100), color=(100, 15, 100), text="Elephent", elevation=5)
	bird_button = button.BoolButton(pos=(0, 300), size=(200, 100), color=(100, 15, 100), text="Elephent?", elevation=5)
	buttons = [draw_button, elephent_button, bird_button]
	while True:
		for s_button in buttons:
			s_button.check_hover()
		circle_num_slider.check_hover()
		for event in pygame.event.get():
			for s_button in buttons:
				s_button.process_clicked(event, screen)
			circle_num_slider.process_clicked(event, screen)
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				return

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:		# IF ENTER IS PRESSED
					return draw(ps, i, circle_num)

					# rs = np.array(coeffs, dtype=int) ** 2 + np.array(-1j * coeffs, dtype=int) ** 2
					# s = OldSpiro(, [150,-35], , screen)

			if event.type == pygame.MOUSEBUTTONDOWN and is_drawing:
				ps = np.full((1000, 2), 0, dtype=float)
				i = 0
				add_to_arr = True

			if event.type == pygame.MOUSEBUTTONUP:
				if len(ps[:i])<2:
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
				ps[i] = pos
				for j in range(len(ps)):
					pygame.draw.rect(screen, (0, 0, 175), pygame.Rect(ps[j], (5, 5)))
				print(pos)
				i += 1

		for s_button in buttons:
			s_button.draw(screen)
		circle_num_slider.draw(screen)
		circle_num = circle_num_slider.get_val()
		is_drawing = draw_button.get_val()
		if elephent_button.get_val():
			ps = np.load('true_elephent.npy')
			last_elemnt = 1
			for j in range(len(ps)):
				if not (ps[j][0]==0 and ps[j][1]==0):
					last_elemnt = j
			return draw(ps, last_elemnt, circle_num)

		if bird_button.get_val():
			ps = np.load('true_elephent.npy')
			last_elemnt = 1
			for j in range(len(ps)):
				if not (ps[j][0]==0 and ps[j][1]==0):
					last_elemnt = j
			return draw(ps, last_elemnt, circle_num)

		pygame.display.update()


# pygame.draw.lines(screen, (0,0,0), True, ps[:i], width=5)


if __name__ == '__main__':
	fourier_main()