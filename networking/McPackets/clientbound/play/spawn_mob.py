import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class SpawnMob47(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'type': common.types.common.UnsignedByte,
			'x': common.types.complex.FixedPointInteger5B,
			'y': common.types.complex.FixedPointInteger5B,
			'z': common.types.complex.FixedPointInteger5B,
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

class SpawnMob107(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'entity_uuid': common.types.common.UUID,
			'type': common.types.common.UnsignedByte,
			'x': common.types.complex.Double,
			'y': common.types.complex.Double,
			'z': common.types.complex.Double,
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
		self.entity_uuid = None
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
		return 0x03