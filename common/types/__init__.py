class Type(object):
	@staticmethod
	def read(context, file_object):
		raise NotImplementedError("Base data type not serializable")

	@staticmethod
	def write(context, value):
		raise NotImplementedError("Base data type not serializable")