import io
from networking.McPackets import SimplePacket
from common import types


class LoginPluginResponse(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.message_id = 0
		self.success = False
		self.data = b""

	def __repr__(self):
		return f"<Serverbound/LoginPluginResponse message_id={self.message_id} success={self.success}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = LoginPluginResponse(packet.id, packet.data_lenght, packet.data)
		new_packet.message_id, a = types.VarInt.read(stream)
		new_packet.success, b = types.Boolean.read(stream)
		if (packet.data_lenght-a-b) > 0:
			new_packet.data = stream.read(packet.data_lenght-a-b)

		return new_packet
