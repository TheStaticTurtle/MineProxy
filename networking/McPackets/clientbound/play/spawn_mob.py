import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class SpawnMob(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'type': common.types.common.UnsignedByte,
		'x': common.types.complex.FixedPointInteger,
		'y': common.types.complex.FixedPointInteger,
		'z': common.types.complex.FixedPointInteger,
		'pitch': common.types.complex.Angle,
		'yaw': common.types.complex.Angle,
		'head_pitch': common.types.complex.Angle,
		'velocity_x': common.types.complex.VelocityShort,
		'velocity_y': common.types.complex.VelocityShort,
		'velocity_z': common.types.complex.VelocityShort,
		'metadata': common.types.complex.EntityMetadata
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.type = None
		self.x = None
		self.y = None
		self.z = None
		self.pitch = None
		self.yaw = None
		self.head_pitch = None
		self.velocity_x = None
		self.velocity_y = None
		self.velocity_z = None
		self.metadata = None

	@property
	def ID(self):
		return 0x0F

	# @classmethod
	# def from_basic_packet(cls, packet):
	# 	if isinstance(packet, Packet):
	# 		buffer = Buffer()
	# 		buffer.write(packet.raw_data)
	# 		buffer.reset_cursor()
	#
	# 		new_packet = cls(packet.context)
	#
	# 		new_packet.entity_id, _ = cls.STRUCTURE["entity_id"].read(packet.context, buffer)
	# 		new_packet.type, _ = cls.STRUCTURE["type"].read(packet.context, buffer)
	# 		new_packet.x, _ = cls.STRUCTURE["x"].read(packet.context, buffer)
	# 		new_packet.y, _ = cls.STRUCTURE["y"].read(packet.context, buffer)
	# 		new_packet.z, _ = cls.STRUCTURE["z"].read(packet.context, buffer)
	# 		new_packet.pitch, _ = cls.STRUCTURE["pitch"].read(packet.context, buffer)
	# 		new_packet.yaw, _ = cls.STRUCTURE["yaw"].read(packet.context, buffer)
	# 		new_packet.head_pitch, _ = cls.STRUCTURE["head_pitch"].read(packet.context, buffer)
	# 		new_packet.velocity_x, _ = cls.STRUCTURE["velocity_x"].read(packet.context, buffer)
	# 		new_packet.velocity_y, _ = cls.STRUCTURE["velocity_y"].read(packet.context, buffer)
	# 		new_packet.velocity_z, _ = cls.STRUCTURE["velocity_z"].read(packet.context, buffer)
	#
	# 		new_packet.metadata = buffer.read(9999999999999)
	# 		print(new_packet.metadata)
	#
	# 		new_packet.apply_meta_fields()
	#
	# 		return new_packet
	#
	# 	else:
	# 		raise RuntimeError(f"Can't create {type(cls)} from {type(packet)} ")
	#
	# def craft(self):
	# 	if self.ID is None:
	# 		raise NotImplementedError("Can't craft packet")
	#
	# 	if self.raw_data is not None and len(self.raw_data) > 0:
	# 		return common.types.common.VarInt.write(self.context, self.ID) + self.raw_data
	# 	else:
	# 		try:
	# 			buffer  = self.STRUCTURE["entity_id"].write(self.context, self.entity_id)
	# 			buffer += self.STRUCTURE["type"].write(self.context, self.type)
	# 			buffer += self.STRUCTURE["x"].write(self.context, self.x)
	# 			buffer += self.STRUCTURE["y"].write(self.context, self.y)
	# 			buffer += self.STRUCTURE["z"].write(self.context, self.z)
	# 			buffer += self.STRUCTURE["pitch"].write(self.context, self.pitch)
	# 			buffer += self.STRUCTURE["yaw"].write(self.context, self.yaw)
	# 			buffer += self.STRUCTURE["head_pitch"].write(self.context, self.head_pitch)
	# 			buffer += self.STRUCTURE["velocity_x"].write(self.context, self.velocity_x)
	# 			buffer += self.STRUCTURE["velocity_y"].write(self.context, self.velocity_y)
	# 			buffer += self.STRUCTURE["velocity_z"].write(self.context, self.velocity_z)
	#
	# 			buffer += self.metadata
	#
	# 		except Exception as e:
	# 			raise RuntimeError(f"{self.NAME}: Error while writing key {key} for type {self.STRUCTURE[key].__class__.__name__}: {str(e)}")
	#
	# 		return common.types.common.VarInt.write(self.context, self.ID) + buffer