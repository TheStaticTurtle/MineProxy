class Type(object):
	@staticmethod
	def read(context, file_object):
		raise NotImplementedError("Read method is not implemented")

	@staticmethod
	def write(context, value):
		raise NotImplementedError("Write method is not implemented")


class Bytes(object):
	@staticmethod
	def read(context, file_object):
		k = file_object.read(99999999999999999999)
		return k, len(k)

	@staticmethod
	def write(context, value):
		return value
