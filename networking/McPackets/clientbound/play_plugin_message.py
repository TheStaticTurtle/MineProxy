import io
from networking.McPackets import SimplePacket
from common import types


class PlayPluginMessage(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.channel = None
		self.channel_data = None

	def __repr__(self):
		return f"<ClientBound/PlayPluginMessage channel={self.channel} channel_data={self.channel_data}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = PlayPluginMessage(packet.id, packet.data_lenght, packet.data)
		new_packet.channel,_ = types.String.read(stream)
		new_packet.channel_data = stream.read()

		return new_packet
