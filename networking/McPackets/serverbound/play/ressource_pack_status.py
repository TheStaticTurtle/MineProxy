import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ResourcePackStatus(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'hash': common.types.common.String,
		'result': common.types.complex.ResourcePackStatusResultEnum
	}

	def __init__(self, context):
		super().__init__(context)
		self.hash = None
		self.result = None

	@property
	def ID(self):
		return 0x19