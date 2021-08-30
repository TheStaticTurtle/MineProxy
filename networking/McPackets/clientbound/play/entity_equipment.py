import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class EntityEquipment(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'slot': common.types.common.VarInt if self.context.protocol_version >= 107 else common.types.common.Short,
			'item': common.types.complex.Slot,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.slot = None
		self.item = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x3C
		if self.context.protocol_version == 47:
			return 0x04
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")