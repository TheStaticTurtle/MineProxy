import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class Effect(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'effect_id': common.types.common.Integer,
			'location': common.types.complex.Position,
			'data': common.types.common.Integer,
			'disable_relative_volume': common.types.common.Boolean,
		}
	STRUCTURE_REPR_HIDDEN_FIELDS = ["data"]

	def __init__(self, context):
		super().__init__(context)
		self.effect_id = None
		self.location = None
		self.data = None
		self.disable_relative_volume = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x21
		if self.context.protocol_version == 47:
			return 0x28
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
