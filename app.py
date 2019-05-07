import numpy as np
import pprint



class Calculus:
	'''
		Gets the weight of a given vector
	'''
	@staticmethod
	def weight(vector):
		toret = 0
		for bit in np.nditer(vector):
			toret += bit
		return toret

	@staticmethod
	def generateIdentity(dimension):
		# Generates base vector
		toret = np.array((list(bin((2**(dimension-1)) >> 0)[2:]),),dtype=int)
		vector = lambda i,dimension : np.array((list(''.zfill(dimension-i) +\
			bin(2**i >> 1)[2:]),),dtype=int)

		# Generates the matrix
		for i in range(dimension-1,0,-1):
			array = vector(i,dimension)
			toret = np.concatenate((toret,array), axis=0)

		return toret


class Golay:
	def __init__(self):
		# Words
		self.__source = np.zeros((12,),dtype=int) # Size 12
		self.__decoded = np.zeros((12,),dtype=int) # Size 12
		self.__encoded = np.zeros((24,),dtype=int) # Size 24
		self.__received = np.zeros((24,),dtype=int) # Size 24

		# Matrix
		self.__GMatrix = np.zeros((12,24),dtype=int) # Size 12x24
		self.__HTMatrix = np.zeros((12,24),dtype=int) # Size 24x12
		self.__AMatrix = np.array([[1,0,0,0,1,1,1,0,1,1,0,1],
								   [0,0,0,1,1,1,0,1,1,0,1,1],
								   [0,0,1,1,1,0,1,1,0,1,0,1],
								   [0,1,1,1,0,1,1,0,1,0,0,1],
								   [1,1,1,0,1,1,0,1,0,0,0,1],
								   [1,1,0,1,1,0,1,0,0,0,1,1],
								   [1,0,1,1,0,1,0,0,0,1,1,1],
								   [0,1,1,0,1,0,0,0,1,1,1,1],
								   [1,1,0,1,0,0,0,1,1,1,0,1],
								   [1,0,1,0,0,0,1,1,1,0,1,1],
								   [0,1,0,0,0,1,1,1,0,1,1,1],
								   [1,1,1,1,1,1,1,1,1,1,1,0]]) # Size 12x12
		self.__IMatrix = Calculus.generateIdentity(12) # Size 12x12

	# Getters
	@property
	def source(self):
		return self.__source

	@property
	def decoded(self):
		return self.__decoded

	@property
	def encoded(self):
		return self.__encoded

	@property
	def received(self):
		return self.__received

	@property
	def GMatrix(self):
		return self.__GMatrix

	@property
	def AMatrix(self):
		return self.__AMatrix

	@property
	def IMatrix(self):
		return self.__IMatrix



if __name__ == "__main__":
	g24 = Golay()
	pprint.pprint(g24.IMatrix)