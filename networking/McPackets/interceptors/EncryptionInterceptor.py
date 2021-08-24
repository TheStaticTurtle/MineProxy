import zlib

from common.authentication import AuthenticationToken
from common import types, encryption as encryption_tools
from common.connection import Connection
from common.context import Context
from ..Buffer import Buffer
from ..clientbound import LoginEncryptionRequest
from ..serverbound import LoginEncryptionResponse
from ..SimplePacketInterceptor import SimplePacketInterceptor


class EncryptionInterceptor(SimplePacketInterceptor):
	NAME = "EncryptionInterceptor"
	packet_class = LoginEncryptionRequest

	def __init__(self, context: Context, connection: Connection, auth_token: AuthenticationToken):
		super().__init__(context)
		self.connection = connection
		self.auth_token = auth_token
		self.secret = None

	def _intercept(self, packet: LoginEncryptionRequest):
		self.log.info(f"Intercepted {packet}, crafting response")
		self.secret = encryption_tools.generate_shared_secret()
		token, encrypted_secret = encryption_tools.encrypt_token_and_secret(packet.public_key, packet.verify_secret, self.secret)

		# A server id of '-' means the server is in offline mode
		if packet.server_id != '-':
			server_id = encryption_tools.generate_verification_hash(packet.server_id, self.secret, packet.public_key)
			if self.auth_token is not None:
				self.auth_token.join(server_id)

		encryption_response = LoginEncryptionResponse()
		encryption_response.shared_secret = encrypted_secret
		encryption_response.verify_secret = token

		buffer = Buffer()

		x = encryption_response.craft(self.context.protocol_version)
		buffer.write(x)

		if self.context.compression_threshold is not None:
			if len(buffer.get_writable()) > self.context.compression_threshold != -1:
				# compress the current payload
				uncompressed_data = buffer.get_writable()
				compressed_data = zlib.compress(uncompressed_data)
				buffer.reset()
				# write out the length of the compressed payload
				buffer.write(types.VarInt.write(len(uncompressed_data)))
				# write the compressed payload itself
				buffer.write(compressed_data)
			else:
				# write out a 0 to indicate uncompressed data
				packet_data = buffer.get_writable()
				buffer.reset()
				buffer.write(types.VarInt.write(0))
				buffer.write(packet_data)

		data = types.VarInt.write(len(buffer.get_writable()))  # Packet Size
		data = data + buffer.get_writable()

		self.connection.socket.send(data)

		self.log.info(f"Responded with {encryption_response}")

		cipher = encryption_tools.create_AES_cipher(self.secret)
		encryptor = cipher.encryptor()
		decryptor = cipher.decryptor()

		self.connection.socket = encryption_tools.EncryptedSocketWrapper(self.connection.socket, encryptor, decryptor)
		self.connection.file = encryption_tools.EncryptedFileObjectWrapper(self.connection.file, decryptor)
		self.log.debug(f"Connection socket updated")
