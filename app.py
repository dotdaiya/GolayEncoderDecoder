import numpy as np
import pprint



class Calculus:

	'''
		Compare 2 given matrix
	'''
	def compareMatrix(mat1,mat2):
		return np.array_equal(mat1,mat2)



	'''
		Adds two given vector
	'''
	def vectorAddSub(vector1,vector2):
		binaryAddition = lambda x,y : (x + y) % 2
		typeDim = lambda v1,v2 : True if (isinstance(v1,np.ndarray) and\
			isinstance(v2,np.ndarray) and v1.shape[0] == v2.shape[0]) else False

		toret = np.zeros((vector1.shape[0]),dtype=int)

		if typeDim(vector1,vector2):
			for elem in range(0,(vector1.shape[0])):
				toret[elem] = binaryAddition(vector1[elem],vector2[elem])
		else:
			print("Wrong types or dimensions.")

		return toret


	'''
		Multiply two given matrix
	'''
	def matrixMultiplication(mat1,mat2):
		typeDim = lambda matrix1,matrix2 : True if (isinstance(matrix1,np.ndarray) and\
			isinstance(matrix2,np.ndarray) and matrix1.shape[1] == matrix2.shape[0]) else False
		binaryMultiplication = lambda x,y : (x * y) % 2  
		binaryAddition = lambda x,y : (x + y) % 2

		toret = np.zeros((mat1.shape[0],mat2.shape[1]),dtype=int)
		
		if typeDim(mat1,mat2):
			mat2T = np.transpose(mat2)
			for row1 in range(0,mat1.shape[0]):
				for row2 in range(0,mat2T.shape[0]):
					y = 0
					for column in range(0,mat1.shape[1]):
						x = binaryMultiplication(mat1[row1][column],mat2T[row2][column])
						y = binaryAddition(x,y)
					toret[row1][row2] = y
		else:
			print("Wrong types or dimensions.")

		return toret

	'''
		Gets the weight of a given vector
	'''
	@staticmethod
	def weight(vector):
		toret = 0
		for bit in np.nditer(vector):
			toret += bit
		return toret

	'''
		Generate and returns an identity matrix of given size
	'''
	@staticmethod
	def generateIdentity(dimension):
		# Generates base vector
		toret = np.array((list(bin((2**(dimension)) >> 1)[2:]),),dtype=int)

		# Generates base vector of given position and dimension
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
		self.__AMatrix = np.array([[1,1,0,1,1,1,0,0,0,1,0,1],
								   [1,0,1,1,1,0,0,0,1,0,1,1],
								   [0,1,1,1,0,0,0,1,0,1,1,1],
								   [1,1,1,0,0,0,1,0,1,1,0,1],
								   [1,1,0,0,0,1,0,1,1,0,1,1],
								   [1,0,0,0,1,0,1,1,0,1,1,1],
								   [0,0,0,1,0,1,1,0,1,1,1,1],
								   [0,0,1,0,1,1,0,1,1,1,0,1],
								   [0,1,0,1,1,0,1,1,1,0,0,1],
								   [1,0,1,1,0,1,1,1,0,0,0,1],
  								   [0,1,1,0,1,1,1,0,0,0,1,1],
  								   [1,1,1,1,1,1,1,1,1,1,1,0]]) # Size 12x12
		self.__IMatrix = Calculus.generateIdentity(12) # Size 12x12
		self.__HMatrix = np.concatenate((self.__IMatrix,self.__AMatrix),axis=1) # Size 12x24
		self.__GMatrix = np.concatenate((self.__AMatrix,self.__IMatrix),axis=1) # Size 12x24


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
	def HMatrix(self):
		return self.__GMatrix

	@property
	def AMatrix(self):
		return self.__AMatrix

	@property
	def IMatrix(self):
		return self.__IMatrix


	'''
		Encode a given word
	'''
	def encode(self,word):
		return Calculus.matrixMultiplication(word,self.GMatrix)


	'''
		Decode a encoded word
	'''
	def decode(self,received):
		eVector = self.decodeError(received)
		if isinstance(eVector,type(None)):
			print("Se requiere retransmisión.")
			return None
		else:
			return Calculus.vectorAddSub(received[0],eVector[0])


	'''
		Algorith to get the error of the codified word
	'''
	def decodeError(self,received):
		# Compute syndrome synd = received * HT
		synd = Calculus.matrixMultiplication(received,self.HMatrix.transpose())
		eVector = np.zeros((1,24),dtype=int) 
		zeroVector = np.zeros((1,12),dtype=int)


		if Calculus.weight(synd[0]) <= 3: # No errors
			return np.concatenate((synd,zeroVector),axis=1)

		for row in range(0,self.AMatrix.shape[0]): # 1 error
			x = Calculus.vectorAddSub(synd[0],self.AMatrix[row])
			if Calculus.weight(x) <= 2:
				# print(row)
				# print(x)
				# print(self.IMatrix[row])
				y = np.concatenate((self.IMatrix[row], x),axis=0)
				return y.reshape(1,24)

		# Compute second syndrome
		synd2 = Calculus.matrixMultiplication(synd,self.AMatrix)

		if Calculus.weight(synd2) <= 3:
			return np.concatenate((synd2,zeroVector),axis=1)

		for row in range(0,self.AMatrix.shape[0]): # 1 error
			x = Calculus.vectorAddSub(synd2[0],self.AMatrix[row])
			if Calculus.weight(x) <= 2:
				y = np.concatenate((x,self.IMatrix[row]),axis=0)
				return y.reshape(1,24)
		return None

	'''
		Introduce errors in a given codified word
	'''
	def introduceErrors(self):
		pass


def main():
	g = Golay()
	word = np.array((list("101111101011"),),dtype=int)	
	received = g.encode(word)
	print("Vector codificado: "+ str(received))
	received[0][7] = 0
	received[0][0] = 0
	received[0][18] = 0
	received[0][23] = 0
	print("Vector codificado c: "+ str(received))
	

	decoded = g.decode(received)
	print("Vector decodificado: "+ str(decoded))
	if Calculus.compareMatrix(received,decoded):
		print("equals")

if __name__ == "__main__":
	main()
