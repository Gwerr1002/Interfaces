class Series(object):
	def gen_n(self,n):
		return list(range(1,n+1))

	def gen_2(self,n):
		return [i**2 for i in range(1,n+1)]

	def gen_fibo(self,n):
		if self.__check_fibo(n):
			aux = 0
			l = [1]
			for _ in range(n):
				aux = aux + l[-1]
				l.append(aux)
				aux = l[-2]
			return l

	def __check_fibo(self,n):
		if isinstance(n,int):
			return n>-1
		else:
			return False
