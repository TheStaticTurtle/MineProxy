import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Response(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Status
	
	@property
	def STRUCTURE(self):
		return {
		'response': common.types.complex.JSONString,
	}

	def __init__(self, context):
		super().__init__(context)
		self.response = None

	@property
	def ID(self):
		return 0x00