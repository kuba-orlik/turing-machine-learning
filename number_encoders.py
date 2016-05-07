class unary:

	def get_alphabet():
		return [0]

	def encode(number):
		ret = []
		while (i<=number):
			ret.append(0)
		return ret

class binary:

	def get_alphabet():
		return [0, 1]

	def encode(number):
		return list(bin(number)[2:])

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
