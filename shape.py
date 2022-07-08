from math import *

import numpy as np
import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Shape:
	def __init__(self, these_points):
		self.orig_points = these_points
		self.cur_points = these_points
		# self.cur_point_index = 0
		self.axis_point = self.cur_points[0]

		self.special_point = [1 / 3, 1 / 3, 1 / 3]
		self.trace = []

	# self.cur_point_position
	# self.cur_angle = 0

	def calc_rotated(self, big_shape_points: list = None, big_shape_poly: Polygon = None, alpha=0.01):
		# cur_point = self.cur_points[self.cur_point_index]
		new_points = [self.cur_points[i] for i in range(len(self.cur_points))]
		for i in range(len(self.cur_points)):
			if tuple(self.cur_points[i]) == tuple(self.axis_point):
				continue
			point = np.array([self.cur_points[i][0], self.cur_points[i][1]])
			point -= self.axis_point
			point = (point[0] * cos(alpha) - point[1] * sin(alpha),
					 point[1] * cos(alpha) + point[0] * sin(alpha))
			point += self.axis_point
			new_points[i] = point

		for p in new_points:
			point = Point(p)
			if not big_shape_poly.contains(point) and tuple(self.axis_point) != tuple(p):
				self.axis_point = p
				return False

		our_poly = Polygon(self.cur_points)
		for ext_p in big_shape_points:
			if tuple(self.axis_point) == tuple(ext_p):
				continue
			if our_poly.contains(Point(ext_p)):
				self.axis_point = np.array([ext_p[0], ext_p[1]])
				return False

		self.cur_points = new_points
		self.trace.append(np.dot(self.special_point, self.cur_points[:len(self.special_point)]))
		return True

	def draw_shape(self, screen, color=(255,0,0)):
		# shape
		pygame.draw.lines(screen, (0, 0, 0), True, self.cur_points, width=2)
		# trace
		if len(self.trace) > 1:
			pygame.draw.lines(screen, color, False, self.trace, width=2)
