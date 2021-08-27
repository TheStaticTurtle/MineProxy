import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class UpdateSign(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': common.types.complex.Position,
		'line1': common.types.common.String,
		'line2': common.types.common.String,
		'line3': common.types.common.String,
		'line4': common.types.common.String,
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
		return 0x33