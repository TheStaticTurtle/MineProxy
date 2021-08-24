import io
from networking.McPackets import SimplePacket
from common import types


class LoginEncryptionResponse(SimplePacket.Packet):

	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.shared_secret = b""
		self.verify_secret = b""

	def __repr__(self):
		return f"<Serverbound/LoginEncryptionResponse shared_secret_lenght={len(self.shared_secret)} verify_secret_lenght={len(self.verify_secret)}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = LoginEncryptionResponse(packet.id, packet.data_lenght, packet.data)
		new_packet.shared_secret, _ = types.VarIntPrefixedByteArray.read(stream)
		new_packet.verify_secret, _ = types.VarIntPrefixedByteArray.read(stream)
		return new_packet

	def craft(self, protocol_version):
		data = b""
		data += types.VarInt.write(self.id)
		data += types.VarIntPrefixedByteArray.write(self.shared_secret)
		data += types.VarIntPrefixedByteArray.write(self.verify_secret)

		return data
