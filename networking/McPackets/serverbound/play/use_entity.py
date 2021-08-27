import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, UseEntityType
from networking.McPackets import SimplePacket
from common import types
from networking.McPackets.Buffer import Buffer


class UseEntity(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'target': common.types.common.VarInt,
		'type': common.types.complex.UseEntityTypeEnum,
		'target_x': common.types.common.Float,
		'target_y': common.types.common.Float,
		'target_z': common.types.common.Float,
	}

	def __init__(self, context):
		super().__init__(context)
		self.target = None
		self.type = None
		self.target_x = None
		self.target_y = None
		self.target_z = None

	@property
	def ID(self):
		return 0x02


	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		try:
			new_packet.target, _ = cls.STRUCTURE["target"].read(packet.context, buffer)
			new_packet.type, _ = cls.STRUCTURE["type"].read(packet.context, buffer)
			if new_packet.type == UseEntityType:
				new_packet.target_x, _ = cls.STRUCTURE["target_x"].read(packet.context, buffer)
				new_packet.target_y, _ = cls.STRUCTURE["target_y"].read(packet.context, buffer)
				new_packet.target_z, _ = cls.STRUCTURE["target_z"].read(packet.context, buffer)
		except Exception as e:
			raise RuntimeError(f"{new_packet.NAME}: Error while writing key: {str(e)}")

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""

		try:
			buffer += self.STRUCTURE["target"].write(self.context, self.target)
			buffer += self.STRUCTURE["type"].write(self.context, self.type)
			if self.type == UseEntityType:
				buffer += self.STRUCTURE["target_x"].write(self.context, self.target_x)
				buffer += self.STRUCTURE["target_y"].write(self.context, self.target_y)
				buffer += self.STRUCTURE["target_z"].write(self.context, self.target_z)

		except Exception as e:
			raise RuntimeError(f"{self.NAME}: Error while writing key: {str(e)}")

		return common.types.common.VarInt.write(self.context, self.ID) + buffer
