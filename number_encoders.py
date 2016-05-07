class unary:

	def get_alphabet():
		return [0]

	def encode(number):
		ret = []
		i = 0
		while (i<=number):
			ret.append(0)
			i+=1
		return ret

	def decode(output):
		ret = None
		for char in output:
			if str(char)=="0":
				if ret==None:
					ret = 0
				else:
					ret+=1
			else:
				break
		return ret

class binary:

	def get_alphabet():
		return [0, 1]

	def encode(number):
		return list(map(int, list(bin(number)[2:])))

class ternary:

	def get_alphabet():
		return [0, 1, 2]

	def encode(number):
		ret = ""
		while(True):
			ret += str(number % 3)
			number = number // 3
			if(number == 0):
				break
		ret = list(ret)
		ret.reverse()
		return ret
