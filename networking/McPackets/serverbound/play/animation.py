import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Animation(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
	}

	@property
	def ID(self):
		return 0x0A
