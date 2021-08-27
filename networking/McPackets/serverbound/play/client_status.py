import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ClientStatus(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'action': common.types.complex.ClientStatusActionsEnums
	}

	def __init__(self, context):
		super().__init__(context)
		self.action = None

	@property
	def ID(self):
		return 0x16