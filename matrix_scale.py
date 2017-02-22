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

input_matrix = np.array([[1,1,0,0], [0,1,0,1], [1,0,0,0]])
scale = ImageScale(input_matrix)
print scale.nearestNeighbor(2,4)
				
		
