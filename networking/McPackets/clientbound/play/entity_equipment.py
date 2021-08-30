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
		'slot': common.types.common.Short,
		'item': common.types.complex.Slot,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.slot = None
		self.item = None

	@property
	def ID(self):
		return 0x04