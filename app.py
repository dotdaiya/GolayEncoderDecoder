import numpy as np
import pprint
import sys
import time as time
import random as r


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
		self.__source = np.zeros((1,12),dtype=int) # Size 12
		self.__decoded = np.zeros((1,12),dtype=int) # Size 12
		self.__encoded = np.zeros((1,24),dtype=int) # Size 24
		self.__received = np.zeros((1,24),dtype=int) # Size 24

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

	# Setters
	@source.setter
	def source(self,value):
		self.__source = value

	@decoded.setter
	def decoded(self,value):
		self.__decoded = value

	@encoded.setter
	def encoded(self,value):
		self.__encoded = value

	@received.setter
	def received(self,value):
		self.__received = value

	@GMatrix.setter
	def GMatrix(self,value):
		self.__GMatrix = value

	@HMatrix.setter
	def HMatrix(self,value):
		self.__GMatrix = value

	@AMatrix.setter
	def AMatrix(self,value):
		self.__AMatrix = value

	@IMatrix.setter
	def IMatrix(self,value):
		self.__IMatrix = value


	'''
		Encode a word of 12 digits
	'''
	def encode(self):
		self.encoded = Calculus.matrixMultiplication(self.source,self.GMatrix)

	'''
		Decode a encoded word
	'''
	def decode(self):
		eVector = self.decodeError()
		if isinstance(eVector,type(None)):
			print("\n\n\nIt needs retransmision.")
			self.decoded = None
		else:
			self.decoded = np.copy(Calculus.vectorAddSub(self.received[0],eVector[0]))


	'''
		Algorithm to get the error of the codified word
		For more information check Readme
	'''
	def decodeError(self):
		# Compute syndrome synd = received * HT
		synd = np.copy(Calculus.matrixMultiplication(self.received,self.HMatrix.transpose()))
		eVector = np.zeros((1,24),dtype=int) 
		zeroVector = np.zeros((1,12),dtype=int)


		if Calculus.weight(synd[0]) <= 3: 
			return np.concatenate((synd,zeroVector),axis=1)

		for row in range(0,self.AMatrix.shape[0]):
			x = Calculus.vectorAddSub(synd[0],self.AMatrix[row])
			if Calculus.weight(x) <= 2:
				y = np.concatenate((self.IMatrix[row], x),axis=0)
				return y.reshape(1,24)

		# Compute second syndrome
		synd2 = np.copy(Calculus.matrixMultiplication(synd,self.AMatrix))

		if Calculus.weight(synd2) <= 3: 
			return np.concatenate((synd2,zeroVector),axis=1)

		for row in range(0,self.AMatrix.shape[0]): 
			x = Calculus.vectorAddSub(synd2[0],self.AMatrix[row])
			if Calculus.weight(x) <= 2:
				y = np.concatenate((x,self.IMatrix[row]),axis=0)
				return y.reshape(1,24)
		return None

	'''
		Introduce errors in a given codified word
	'''
	def introduceErrors(self):
		listRan = []
		self.received = np.copy(self.encoded)
		
		while True:
			n = int(input("Enter a number of errors [0-5]: "),10)
			if n >= 1 and n < 5:
				break
			if n == 0:
				return None

		for i in range(0,n):
			while True:
				ranPos = r.randint(0,23)
				if ranPos not in listRan:
					listRan.append(ranPos)
					break

			v = self.__received[0][ranPos]

			if v == 1:
				v = 0
			elif v == 0:
				v = 1
			else:
				print("Error.")
				return None
			
			self.__received[0][ranPos] = v



def main():
	g = Golay()

	while True:
		print_menu()
		choice = int(input("Enter your option [1-4]: "),10)

		if choice == 1:
			while True:
				x = input("Enter the word you want to codify [12 chars]")
				if bininput(x) and len(x) == 12:
					for i in range(0,12):
						g.source[0][i] = int(x[i],10)
					break

			print("\nSource word: " +  str(g.source))
			print("\nEncoding word...")
			g.encode()
			time.sleep(2)
			print("Encoded word: " + str(g.encoded) + "\n\n\n")
		elif choice == 2:
			g.introduceErrors()
		elif choice == 3:
			print("\nDecoding word...")
			g.decode()
			time.sleep(2)
			print("Source word: " + str(g.source))
			print("Encoded word: " + str(g.encoded))
			print("Received word: " + str(g.received))
			print("Decoded word: " + str(g.decoded) + "\n\n\n")
			print("Comparing received and encoded word:"+ "\n\n\n")
			print(str(g.encoded)[2:-2])
			print(str(g.received)[2:-2])

			print("\n\nComparing source word and decoded word:")
			print(str(g.source)[2:-2])
			print(str(g.decoded)[25:-1])
		elif choice == 4:
			sys.exit("\n\nClosing...")
		else:
			print("Enter a number [1-4].\n\n",flush=True)			


def bininput(input_string):
    for character in input_string:
        if character == '0':
            continue
        elif character == '1':
            continue
        else:
            return False
    return True


def print_menu():
	print(30*"-" + "MENU" + "-"*30)
	print("1: Codificar palabra.")
	print("2: Introducir errores (Opcional).")
	print("3: Decodificar palabra con n errores.")
	print("4: Salir.")
	print(30*"-" + "----" + "-"*30)


if __name__ == "__main__":
	main()
