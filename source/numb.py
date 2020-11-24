class Separator(object):

	def __init__(self, value):
		self.NUMBER = str(value)

	def sep(self):

		self.count = 0
		self.output = list()

		if len(self.NUMBER.split('.')) == 1:
			self.a = self.NUMBER.split('.')[0]	
		elif len(self.NUMBER.split('.')) == 2:
			self.a = self.NUMBER.split('.')[0]
			self.b = self.NUMBER.split('.')[1]
			
		for char in reversed(self.a):
			if self.count == 3:
				self.output.append(',')
				self.count = 0
			self.output.append(char)
			self.count += 1

		if len(self.NUMBER.split('.')) == 1:
			self.fixed = ''.join(self.output)[::-1]
		elif len(self.NUMBER.split('.')) == 2:
			self.fixed = ''.join(self.output)[::-1] + '.' + self.b
			
		return self.fixed