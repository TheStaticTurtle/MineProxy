import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class UpdateBlockEntity(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'location': common.types.complex.Position,
			'action': common.types.complex.UpdateEntityActionEnum,
			'nbt_data': common.types.complex.OptionalNBT,
		}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.action = None
		self.nbt_data = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x09
		if self.context.protocol_version == 47:
			return 0x35
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")