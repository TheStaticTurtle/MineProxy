class Type(object):
	@staticmethod
	def read(context, file_object):
		raise NotImplementedError("Read method is not implemented")

	@staticmethod
	def write(context, value):
		raise NotImplementedError("Write method is not implemented")