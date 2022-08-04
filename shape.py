import math
from math import *

import numpy as np
import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#class to represent a polygon
class Shape:
	def __init__(self, these_points):
		self.orig_points = these_points #orignal points (not changed at all)
		self.cur_points = these_points #current points location (changed each time we rotate the shape)
		# self.cur_point_index = 0
		self.axis_point = self.cur_points[0] #center of rotation

		self.special_point = [1 / 3, 1 / 3, 1 / 3] # point to follow trace. Baricentric coordinates of the first three vertices
		self.trace = [] #trace of the point to draw
		self.contact = False #was contact made (if yes - switch axis point
		self.factor = 1 #scale factor to the rotation angle (see explanation in the report)

	# self.cur_point_position
	# self.cur_angle = 0

	def update_special_point(self, new_point):
		#set new point for trace
		#compute base matrix
		first_row = [self.cur_points[0][0], self.cur_points[0][1], 1]
		second_row = [self.cur_points[1][0], self.cur_points[1][1], 1]
		third_row = [self.cur_points[2][0], self.cur_points[2][1], 1]
		matrix = np.matrix([first_row, second_row, third_row])
		self.special_point = np.matmul([new_point[0], new_point[1], 1], np.linalg.inv(matrix))
		self.special_point = np.array(self.special_point)[0]

	def calc_rotated(self, big_shape_points: list = None, big_shape_poly: Polygon = None, alpha=0.01):
		#rotate by alpha angles (or change axis_point if impossible)
		alpha *= self.factor
		# cur_point = self.cur_points[self.cur_point_index]
		new_points = [self.cur_points[i] for i in range(len(self.cur_points))]
		for i in range(len(self.cur_points)):
			# calculate new positions of points
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
				# check for intersectoin
				if(self.factor > 1/(2**40)):
					# if intersected with outside polygon - try again with smaller scale
					self.factor/=2
					return False
				self.axis_point = self.cur_points[idx] #if the scale is small enought, change axis_point
				if not self.contact:
					self.trace = []
				self.contact = True
				self.factor = 1
				return False

		for ext_p in big_shape_points:
			#check for intersection such the new axis point is a point of the outside shape
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
		pygame.draw.lines(screen, color=(0, 0, 0), points=self.cur_points, width=2, closed=True)
		# trace
		if len(self.trace) > 1:
			pygame.draw.circle(screen, (255, 0, 0), mid_point, radius=5)
			pygame.draw.lines(screen, color=color, points=self.trace, width=2, closed=False)
