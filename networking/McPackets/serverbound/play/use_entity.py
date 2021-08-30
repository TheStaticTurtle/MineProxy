import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, UseEntityType
from networking.McPackets import SimplePacket
from common import types
from networking.McPackets.Buffer import Buffer


class UseEntity(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		out = {
			'target': common.types.common.VarInt,
			'type': common.types.complex.UseEntityTypeEnum,
			'target_x': common.types.common.Float,
			'target_y': common.types.common.Float,
			'target_z': common.types.common.Float,
		}
		if self.context.protocol_version >= 107:
			out["hand"] = common.types.complex.UseEntityHandEnum
		return out

	def __init__(self, context):
		super().__init__(context)
		self.target = None
		self.type = None
		self.target_x = None
		self.target_y = None
		self.target_z = None
		if self.context.protocol_version >= 107:
			self.hand = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x0A
		if self.context.protocol_version == 47:
			return 0x02
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")

	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		try:
			new_packet.target, _ = new_packet.STRUCTURE["target"].read(packet.context, buffer)
			new_packet.type, _ = new_packet.STRUCTURE["type"].read(packet.context, buffer)
			if new_packet.type == UseEntityType.InteractAt:
				new_packet.target_x, _ = new_packet.STRUCTURE["target_x"].read(packet.context, buffer)
				new_packet.target_y, _ = new_packet.STRUCTURE["target_y"].read(packet.context, buffer)
				new_packet.target_z, _ = new_packet.STRUCTURE["target_z"].read(packet.context, buffer)
			if new_packet.type == UseEntityType.InteractAt or new_packet.type == UseEntityType.Interact:
				if packet.context.protocol_version >= 107:
					new_packet.hand, _ = new_packet.STRUCTURE["hand"].read(packet.context, buffer)

		except Exception as e:
			raise RuntimeError(f"{new_packet.NAME}: Error while writing key: {str(e)}")

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""

		try:
			buffer += self.STRUCTURE["target"].write(self.context, self.target)
			buffer += self.STRUCTURE["type"].write(self.context, self.type)
			if self.type == UseEntityType.InteractAt:
				buffer += self.STRUCTURE["target_x"].write(self.context, self.target_x)
				buffer += self.STRUCTURE["target_y"].write(self.context, self.target_y)
				buffer += self.STRUCTURE["target_z"].write(self.context, self.target_z)
			if self.type == UseEntityType.InteractAt or self.type == UseEntityType.Interact:
				if self.context.protocol_version >= 107:
					buffer += self.STRUCTURE["hand"].write(self.context, self.hand)

		except Exception as e:
			raise RuntimeError(f"{self.NAME}: Error while writing key: {str(e)}")

		return common.types.common.VarInt.write(self.context, self.ID) + buffer
