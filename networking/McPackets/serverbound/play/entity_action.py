import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class EntityAction(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		out = {
			'entity_id': common.types.common.VarInt,
			'action_id': common.types.complex.EntityActionActionEnum,
			'action_parameter': common.types.common.VarInt,
		}
		if self.context.protocol_version >= 107:
			del out["action_parameter"]
			out["jump_boost"] = common.types.common.VarInt
			out["action_id"] = common.types.complex.EntityActionActionV107Enum

		return out

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.action_id = None
		if self.context.protocol_version >= 107:
			self.jump_boost = None
		if self.context.protocol_version == 47:
			self.action_parameter = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x14
		if self.context.protocol_version == 47:
			return 0x0B
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
