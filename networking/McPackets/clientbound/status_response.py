import io
import json
from networking.McPackets import SimplePacket
from common import types


class StatusResponse(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.json = {}

	def __repr__(self):
		return f"<ClientBound/StatusResponse {json.dumps(self.json)}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = StatusResponse(packet.id, packet.data_lenght, packet.data)

		w,_ = types.String.read(stream)
		new_packet.json = json.loads(w)

		return new_packet
