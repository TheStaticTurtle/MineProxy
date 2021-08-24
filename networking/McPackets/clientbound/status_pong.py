import io
from networking.McPackets import SimplePacket
from common import types


class StatusPong(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.payload = 0

	def __repr__(self):
		return f"<ClientBound/StatusPong payload={self.payload}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = StatusPong(packet.id, packet.data_lenght, packet.data)
		new_packet.payload,_ = types.Long.read(stream)
		return new_packet
