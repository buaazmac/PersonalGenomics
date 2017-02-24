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
		return result

input_matrix = np.array([[1,1,0,0], [0,1,0,1], [1,0,0,0]])
scale = ImageScale(input_matrix)
print scale.nearestNeighbor(2,4)
print '#'
print scale.bilinearInterpolation(2,4)
print '#'
print scale.bilinearInterpolation(6,4)
print '#'
print scale.bilinearInterpolation(7,4)
				
		
