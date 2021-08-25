from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types


class Request(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Status
	STRUCTURE = {
	}

	@property
	def ID(self):
		return 0x00