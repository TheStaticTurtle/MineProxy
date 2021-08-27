import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class UpdateSign(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': common.types.complex.Position,
		'line1': common.types.complex.JSONString,
		'line2': common.types.complex.JSONString,
		'line3': common.types.complex.JSONString,
		'line4': common.types.complex.JSONString,
	}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.line1 = None
		self.line2 = None
		self.line3 = None
		self.line4 = None

	@property
	def ID(self):
		return 0x12
