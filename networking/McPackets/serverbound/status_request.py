from networking.McPackets import SimplePacket


class StatusRequest(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)

	def __repr__(self):
		return "<Serverbound/StatusRequest>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		new_packet = StatusRequest(packet.id, packet.data_lenght, packet.data)
		return new_packet
