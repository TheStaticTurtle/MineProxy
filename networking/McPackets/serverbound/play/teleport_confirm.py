import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class TeleportConfirm(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'teleport_id': common.types.common.VarInt,
		}

	def __init__(self, context):
		super().__init__(context)
		self.teleport_id = None

	@property
	def ID(self):
		return 0x00
