import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityEffect(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'entity_id': common.types.common.VarInt,
		'effect_id': common.types.common.Byte,
		'amplifier': common.types.common.Byte,
		'duration': common.types.common.VarInt,
		'hide_particle': common.types.common.Boolean,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.effect_id = None
		self.amplifier = None
		self.duration = None
		self.hide_particle = None

	@property
	def ID(self):
		return 0x1D
