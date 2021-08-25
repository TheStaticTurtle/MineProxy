from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class KeepAlive(SimplePacket.Packet):
	ID = 0x00
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'keep_alive_id': types.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.keep_alive_id = None
