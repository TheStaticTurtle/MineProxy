import io
from networking.McPackets import SimplePacket
from common import types


class LoginEncryptionRequest(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.server_id = ""
		self.public_key_lenght = 0
		self.public_key = b""
		self.verify_secret_lenght = 0
		self.verify_secret = b""

	def __repr__(self):
		return f"<ClientBound/LoginEncryptionRequest server_id={self.server_id} public_key_lenght={self.public_key_lenght} verify_secret_lenght={self.verify_secret_lenght}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = LoginEncryptionRequest(packet.id, packet.data_lenght, packet.data)

		new_packet.server_id, _ = types.String.read(stream)
		new_packet.public_key_lenght, _ = types.VarInt.read(stream)
		new_packet.public_key = stream.read(new_packet.public_key_lenght)
		new_packet.verify_secret_lenght, _ = types.VarInt.read(stream)
		new_packet.verify_secret = stream.read(new_packet.verify_secret_lenght)
		return new_packet
