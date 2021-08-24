import socket
from common import encryption


class Connection:
	def __init__(self, s: socket.socket):
		self.socket = s
		self.file = s.makefile("rb", 0)

	def close(self):
		self.file.close()
		self.socket.close()

	@property
	def encrypted(self):
		return isinstance(self.file, encryption.EncryptedFileObjectWrapper)