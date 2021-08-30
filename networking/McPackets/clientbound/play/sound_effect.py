import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class SoundEffectV47(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'sound_name': common.types.common.String,
			'x': common.types.common.Integer,
			'y': common.types.common.Integer,
			'z': common.types.common.Integer,
			'volume': common.types.complex.Float,
			'pitch': common.types.common.UnsignedByte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.sound_name = None
		self.x = None
		self.y = None
		self.z = None
		self.volume = None
		self.pitch = None

	@property
	def ID(self):
		if self.context.protocol_version == 47:
			return 0x29
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")


class SoundEffectV107(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'sound_name': common.types.common.String,
			'sound_category': common.types.complex.SoundCategoryEnum,
			'x': common.types.complex.FixedPointInteger3B,
			'y': common.types.complex.FixedPointInteger3B,
			'z': common.types.complex.FixedPointInteger3B,
			'volume': common.types.common.Float,
			'pitch': common.types.common.UnsignedByte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.sound_name = None
		self.sound_category = None
		self.x = None
		self.y = None
		self.z = None
		self.volume = None
		self.pitch = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x19
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")