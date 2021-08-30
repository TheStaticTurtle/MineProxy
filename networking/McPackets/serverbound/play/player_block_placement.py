import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PlayerBlockPlacement(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		if self.context.protocol_version >= 107:
			return {
				'location': common.types.complex.Position,
				'face': common.types.common.VarInt,
				'hand': common.types.complex.UseEntityHandEnum,
				'cursor_position_x': common.types.common.UnsignedByte,
				'cursor_position_y': common.types.common.UnsignedByte,
				'cursor_position_z': common.types.common.UnsignedByte,
			}
		if self.context.protocol_version == 47:
			return {
				'location': common.types.complex.Position,
				'face': common.types.common.Byte,
				'held_item': common.types.complex.Slot,
				'cursor_position_x': common.types.common.Byte,
				'cursor_position_y': common.types.common.Byte,
				'cursor_position_z': common.types.common.Byte,
			}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.face = None
		if self.context.protocol_version >= 107:
			self.hand = None
		if self.context.protocol_version == 47:
			self.held_item = None
		self.cursor_position_x = None
		self.cursor_position_y = None
		self.cursor_position_z = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1C
		if self.context.protocol_version == 47:
			return 0x08
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
