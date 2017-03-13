# This is the class for image scaling
# Input: matrix ( N * M )
# Methods: NearestNeighbor, Bilinear Interpolation, Bicubic Interpolation...(still on work)
import numpy as np
	
class ImageScale:
	def __init__(self, matrix):
		self.matrix = matrix
		self.width = matrix.shape[0]
		self.height = matrix.shape[1]
		# Output a warning when height is not 4
		if self.height != 4:
			print '[Value Warning] Height of matrix should be 4! Please check your matrix'

	# Input: width and height for new matrix
	# 	 background value for grid has no reference (maybe useful.. or not )
	# Output: new matrix
	def nearestNeighbor(self, new_width, new_height, background_v = 0):
		x_ratio = (self.width << 16) / new_width + 1
		y_ratio = (self.height << 16) / new_height + 1
		result = []
		for i in range(new_width):
			col = []
			for j in range(new_height):
				px = int((i * x_ratio) >> 16)
				py = int((j * y_ratio) >> 16)
				col.append(self.matrix[px][py])
			result.append(col)
		return np.array(result)

	# Bilinear Interpolation
	def bilinearInterpolation(self, new_width, new_height, background_v = 0):
		x_ratio = float(self.width - 1) / float(new_width - 1)
		y_ratio = float(self.height - 1) / float(new_height - 1)
		result = []
		for i in range(new_width):
			col = []
			for j in range(new_height):
				px = float(i * x_ratio)
				py = float(j * y_ratio)

				x1 = int(px)
				x2 = x1 + 1
				y1 = int(py)
				y2 = y1 + 1

				if x2 >= self.width:
					x2 = self.width - 1
					x1 = x2 - 1
				if y2 >= self.height:
					y2 = self.height - 1
					y1 = y2 - 1

				q11 = float(self.matrix[x1][y1])
				q12 = float(self.matrix[x1][y2])
				q21 = float(self.matrix[x2][y1])
				q22 = float(self.matrix[x2][y2])

				a1 = (float(x2) - px) / (float(x2) - float(x1))
				a2 = (px - float(x1)) / (float(x2) - float(x1))

				f_x_y1 = a1 * q11 + a2 * q21 
				f_x_y2 = a1 * q12 + a2 * q22 
				f_x_y = (float(y2) - py) / (float(y2) - float(y1)) * f_x_y1 \
					+ (py - float(y1)) / (float(y2) - float(y1)) * f_x_y2
				col.append(f_x_y)
			result.append(col)
		return np.array(result)
	# Linear Interpolation for 1D data
	def linearInterpolation(self, new_width, new_height, background_v = 0):
		x_ratio = float(self.width - 1) / float(new_width - 1)
		result = []
		for i in range(new_width):
			col = []
			for j in range(new_height):
				px = float(i * x_ratio)

				x1 = int(px)
				x2 = x1 + 1
				
				if x2 >= self.width:
					x2 = self.width - 1
					x1 = x2 - 1

				q1 = float(self.matrix[x1][j])
				q2 = float(self.matrix[x2][j])
				fx1 = (px - x1) / (x2 - x1)
				val = q1 * (1.0 - fx1) + q2 * fx1
				col.append(val)
			result.append(col)
		return np.array(result)
	# Cubic Interpolation for 1D data
	def cubicInterpolation(self, new_width, new_height, background_v = 0):
		x_ratio = float(self.width - 1) / float(new_width - 1)
		result = []
		def h00(t):
			return 2.0 * pow(t, 3) - 3.0 * pow(t, 2) + 1
		def h10(t):
			return pow(t, 3) - 2.0 * pow(t, 2) + t
		def h01(t):
			return -2.0 * pow(t, 3) + 3.0 * pow(t, 2)
		def h11(t):
			return pow(t, 3) - pow(t, 2)
		for i in range(new_width):
			col = []
			for j in range(new_height):
				px = float(i * x_ratio)

				x1 = int(px)
				x2 = x1 + 1
				
				if x2 >= self.width:
					x2 = self.width - 1
					x1 = x2 - 1

				q1 = float(self.matrix[x1][j])
				q2 = float(self.matrix[x2][j])
				x0 = x1 - 1
				q0 = q1
				x3 = x2 + 1
				q3 = q2
				if x1 > 0:
					x0 = x1 - 1
					q0 = float(self.matrix[x0][j])
				if x2 < self.width - 1:
					x3 = x2 + 1
					q3 = float(self.matrix[x3][j])
				m1 = 0.5 * ((q2 - q1) + (q1 - q0))
				m2 = 0.5 * ((q3 - q2) + (q2 - q1))
				t = px - float(x1)
				val = h00(t) * q1 + h10(t) * m1 + h01(t) * q2 + h11(t) * m2

				col.append(val)
			result.append(col)
		return np.array(result)
		

input_matrix = np.array([[1,1,0,0], [0,1,0,1], [1,0,0,0]])
scale = ImageScale(input_matrix)
print "nearest neighbor"
print scale.nearestNeighbor(4,4)
print "bilinear interpolation"
print scale.bilinearInterpolation(4,4)
print "linear interpolation"
print scale.linearInterpolation(4,4)
print "cubic interpolation"
print scale.cubicInterpolation(4,4)
				
		
