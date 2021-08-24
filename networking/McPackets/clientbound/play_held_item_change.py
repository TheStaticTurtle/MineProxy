import io
from networking.McPackets import SimplePacket
from common import types


class PlayHeldItemChanged(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.slot = None

	def __repr__(self):
		return f"<ClientBound/PlayHeldItemChanged slot={self.slot}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = PlayHeldItemChanged(packet.id, packet.data_lenght, packet.data)
		new_packet.slot,_ = types.Byte.read(stream)
		return new_packet
