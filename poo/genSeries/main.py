import series

class Display():
	def __init__(self, format='list'):
		self.format = format

	def show(self,sname,srs):
		print(f"\n{sname}")
		if isinstance(srs,list):
			if self.format =='list':
				print(srs)
			elif self.format == 'item':
				for n,s in enumerate(srs,1):
					print(f"f[{n}] = {s}")
			else:
				print("formato desconocido")
		else:
			print(srs)

class more_series(series.Series):
	def gen_pares(self,n):
		return list(range(2,n+1,2))


def main():
	srs=more_series()
	dsp=Display()
	r = srs.gen_n(10)
	n = srs.gen_2(10)
	f = srs.gen_fibo(10)
	p = srs.gen_pares(10)
	dsp.show('gen_n',r)
	dsp.show('gen_n2',n)
	dsp.show('gen_fibo',f)
	dsp.show('gen_pares',p)

if __name__=="__main__":
	main()
