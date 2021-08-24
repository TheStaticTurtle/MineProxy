from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types


class Request(SimplePacket.Packet):
	ID = 0x00
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Status
	STRUCTURE = {
	}