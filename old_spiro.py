import pygame
import numpy as np
from math import cos, sin, pi
from time import sleep
from button import BoolButton
from button import Slider

# POSITIVE RADIUS MEANS OUTSIDE

# optimizations:
# https://stackoverflow.com/questions/70092416/pygame-efficient-way-to-draw-traceline-of-moving-object
# also, pygame.display.update() can receive a rect to update instead of the entire screen

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
TRK = (0, 180, 120)

alpha = 0

width, height = (1000, 700)
start = np.asarray((width // 2, height // 2))


class OldSpiro:
	def __init__(self, screen, radii, init_degrees, trace_l=int(1e5)):
		self.rs = np.array(radii)
		self.betas = np.array(init_degrees)
		self.screen = screen

		point = self.draw_spiro(alpha=0)

		# trace_l is is the maximal length of the trace
		self.trace_l = trace_l
		# the trace which follows the most inner circle
		self.trace = np.full((self.trace_l, 2), point)

	def draw(self, t, i):
		self.betas = t * self.rs[0] / self.rs + self.betas
		point = self.draw_spiro(alpha=0)
		self.trace[i] = point
		if i > 2:
			pygame.draw.lines(self.screen, RED, False, self.trace[:i], width=2)

	def draw_spiro(self, alpha=0.5):
		centers, fixed_points = self.stack_spiro()

		centers += start
		fixed_points += start

		for i, r in enumerate(self.rs):
			pygame.draw.circle(self.screen, BLACK, centers[i], abs(r), width=3)
			if i > 0:
				pygame.draw.line(self.screen, GREY, centers[i], fixed_points[i], width=3)
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


def old_spiro_main():
	# radii = np.array([64,32,64,32,16])
	# radii = np.array([20, 90, 50])
	# radii = np.array([150,-35])	# good

	radii = np.array([70, -25])
	init_degrees = np.zeros(radii.shape)

	pygame.init()
	screen = pygame.display.set_mode((width, height))
	screen.fill(WHITE)

	esc_button = BoolButton(pos = (700, 10), size =(300, 100), color = (70,70,200), text = "main screen", elevation=5)
	speed_slider = Slider(pos = (20, 30), length=400, start_val=1, min_val=1, max_val=100)
	count_slider = Slider(pos = (20, 110), length=400, start_val=2, min_val=2, max_val=10)

	elements = [esc_button, speed_slider, count_slider]
	buttons = [esc_button]
	for button in buttons:
		button.print_text = True

	trace_l = int(1e5)
	s = OldSpiro(screen, radii, init_degrees, trace_l)
	t,i = 0,0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				return False
			if esc_button.process_clicked(event, screen):
				return True
			speed_slider.process_clicked(event, screen)
			count_slider.process_clicked(event, screen)

			if count_slider.get_val() != len(s.rs):
				n = count_slider.get_val()
				radii = np.array([(-1)**i * (100- 30*i) for i in range(n)])

				init_degrees = np.zeros(radii.shape)
				s = OldSpiro(screen, radii, init_degrees, trace_l)
		pygame.display.update()
		screen.fill(WHITE)
		s.draw(t, i)

		for element in elements:
			element.check_hover()
			element.draw(screen)

		t += 0.01 * speed_slider.get_val()
		i = (i + 1) % trace_l


if __name__ == '__main__':
	old_spiro_main()

