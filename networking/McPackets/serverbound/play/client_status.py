import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ClientStatus(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'action': common.types.complex.ClientStatusActionsEnums
	}

	def __init__(self, context):
		super().__init__(context)
		self.action = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x03
		if self.context.protocol_version == 47:
			return 0x16
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")