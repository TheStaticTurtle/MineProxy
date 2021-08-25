from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Response(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Status
	STRUCTURE = {
		'response': types.JSONString,
	}

	def __init__(self, context):
		super().__init__(context)
		self.response = None

	@property
	def ID(self):
		return 0x00