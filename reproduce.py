class Meta:
	def __init__(self, cls):
		self.cls = cls
		self.instances = []
		self.populate()

	def populate(self):
		for i in range(10):
			self.instances.append(self.cls())

class Object:
	def __init__(self):
		self.foo = 'bar'

m = Meta(Object)
