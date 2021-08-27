import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class EntityAction(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'action_id': common.types.complex.EntityActionActionEnum,
		'action_parameter': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.action_id = None
		self.action_parameter = None

	@property
	def ID(self):
		return 0x0B
