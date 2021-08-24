import io
from networking.McPackets import SimplePacket
from common import types


class LoginStart(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.name = ""

	def __repr__(self):
		return f"<Serverbound/LoginStart name={self.name}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = LoginStart(packet.id, packet.data_lenght, packet.data)
		new_packet.name,_ = types.String.read(stream)
		return new_packet
