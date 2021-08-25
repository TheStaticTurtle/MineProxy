from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Success(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'uuid': types.String,
		'username': types.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.uuid = None
		self.username = None

	@property
	def ID(self):
		return 0x02
