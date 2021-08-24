import socket
from common import encryption
from common.context import Context


class Connection:
	def __init__(self, context: Context, s: socket.socket):
		self.context = context
		self.socket = s
		self.file = s.makefile("rb", 0)

	def close(self):
		self.file.close()
		self.socket.close()

	@property
	def encrypted(self):
		return isinstance(self.file, encryption.EncryptedFileObjectWrapper)