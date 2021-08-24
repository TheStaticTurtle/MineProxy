import io
from networking.McPackets import SimplePacket
from common import types


class LoginSetCompression(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.threshold = -1

	def __repr__(self):
		return f"<ClientBound/LoginSetCompression threshold={self.threshold}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = LoginSetCompression(packet.id, packet.data_lenght, packet.data)
		new_packet.threshold, _ = types.VarInt.read(stream)
		return new_packet

	def craft(self, protocol_version):
		data = b""
		data += types.VarInt.write(self.id)
		data += types.VarInt.write(self.threshold)
		return data