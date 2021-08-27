import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Spectate(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'target_player': common.types.complex.UUID
	}

	def __init__(self, context):
		super().__init__(context)
		self.target_player = None

	@property
	def ID(self):
		return 0x18