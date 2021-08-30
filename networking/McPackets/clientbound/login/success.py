import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Success(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	
	@property
	def STRUCTURE(self):
		return {
		'uuid': common.types.common.String,
		'username': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.uuid = None
		self.username = None

	@property
	def ID(self):
		return 0x02
