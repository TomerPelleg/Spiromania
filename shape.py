import math
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
		self.contact = False
		self.factor = 1

	# self.cur_point_position
	# self.cur_angle = 0

	def calc_rotated(self, big_shape_points: list = None, big_shape_poly: Polygon = None, alpha=0.01):
		alpha *= self.factor
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

		our_poly = Polygon(new_points)
		for idx in range(len(new_points)):
			p = new_points[idx]
			point = Point(p)
			if not big_shape_poly.contains(point) and tuple(self.axis_point) != tuple(p):
				if(self.factor > 1/(2**40)):
					self.factor/=2
					return False
				self.axis_point = self.cur_points[idx]
				if not self.contact:
					self.trace = []
				self.contact = True
				self.factor = 1
				return False

		for ext_p in big_shape_points:
			if tuple(self.axis_point) == tuple(ext_p):
				continue
			if our_poly.contains(Point(ext_p)):
				if(self.factor >= 1/(2**40)):
					self.factor/=2
					return False
				self.axis_point = np.array([ext_p[0], ext_p[1]])
				if not self.contact:
					self.trace = []
				self.contact = True
				self.factor = 1
				return False

		self.cur_points = new_points
		mid_point = sum(self.cur_points) / len(self.cur_points)
		self.trace.append(np.dot(self.special_point, self.cur_points[:len(self.special_point)]))
		# self.trace.append(mid_point)
		return True

	def draw_shape(self, screen, color=(255,0,0)):
		# shape
		mid_point = np.dot(self.special_point, self.cur_points[:len(self.special_point)])
		pygame.draw.lines(screen, (0, 0, 0), True, self.cur_points, width=2)
		pygame.draw.circle(screen, (255, 0,0 ), mid_point, radius=5)
		# trace
		if len(self.trace) > 1:
			pygame.draw.lines(screen, color, False, self.trace, width=2)
