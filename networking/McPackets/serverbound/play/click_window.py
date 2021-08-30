import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ClickWindow(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		out = {
			'window_id': common.types.common.UnsignedByte,
			'slot': common.types.common.Short,
			'button': common.types.common.Byte,
			'action_number': common.types.common.Short,
			'mode': common.types.common.Byte,
			'clicked_slot': common.types.complex.Slot,
		}
		if self.context.protocol_version >= 107:
			out["mode"] = common.types.common.VarInt
		return out

	def __init__(self, context):
		super().__init__(context)
		self.window_id = None
		self.slot = None
		self.button = None
		self.action_number = None
		self.mode = None
		self.clicked_slot = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x07
		if self.context.protocol_version == 47:
			return 0x0E
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
