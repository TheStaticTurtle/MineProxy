import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class SpawnObjectV47(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'type': common.types.common.Byte,
			'x': common.types.complex.FixedPointInteger5B,
			'y': common.types.complex.FixedPointInteger5B,
			'z': common.types.complex.FixedPointInteger5B,
			'pitch': common.types.complex.Angle,
			'yaw': common.types.complex.Angle,
			'data': common.types.common.Integer,
			'velocity_x': common.types.complex.VelocityShort,
			'velocity_y': common.types.complex.VelocityShort,
			'velocity_z': common.types.complex.VelocityShort,
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
		self.data = None
		self.velocity_x = None
		self.velocity_y = None
		self.velocity_z = None

	@property
	def ID(self):
		if self.context.protocol_version == 47:
			return 0x0E
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")

	@classmethod
	def from_basic_packet(cls, packet):
		if isinstance(packet, Packet):
			buffer = Buffer()
			buffer.write(packet.raw_data)
			buffer.reset_cursor()

			new_packet = cls(packet.context)

			new_packet.entity_id, _ = new_packet.STRUCTURE["entity_id"].read(packet.context, buffer)
			new_packet.type, _ = new_packet.STRUCTURE["type"].read(packet.context, buffer)
			new_packet.x, _ = new_packet.STRUCTURE["x"].read(packet.context, buffer)
			new_packet.y, _ = new_packet.STRUCTURE["y"].read(packet.context, buffer)
			new_packet.z, _ = new_packet.STRUCTURE["z"].read(packet.context, buffer)
			new_packet.pitch, _ = new_packet.STRUCTURE["pitch"].read(packet.context, buffer)
			new_packet.yaw, _ = new_packet.STRUCTURE["yaw"].read(packet.context, buffer)
			new_packet.data, _ = new_packet.STRUCTURE["data"].read(packet.context, buffer)

			if new_packet.data != 0:
				new_packet.velocity_x, _ = new_packet.STRUCTURE["velocity_x"].read(packet.context, buffer)
				new_packet.velocity_y, _ = new_packet.STRUCTURE["velocity_y"].read(packet.context, buffer)
				new_packet.velocity_z, _ = new_packet.STRUCTURE["velocity_z"].read(packet.context, buffer)

			new_packet.apply_meta_fields()

			return new_packet

		else:
			raise RuntimeError(f"Can't create {type(cls)} from {type(packet)} ")


	def craft(self):
		if self.ID is None:
			raise NotImplementedError("Can't craft packet")

		if self.raw_data is not None and len(self.raw_data) > 0:
			return common.types.common.VarInt.write(self.context, self.ID) + self.raw_data
		else:
			try:
				buffer  = self.STRUCTURE["entity_id"].write(self.context, self.entity_id)
				buffer += self.STRUCTURE["type"].write(self.context, self.type)
				buffer += self.STRUCTURE["x"].write(self.context, self.x)
				buffer += self.STRUCTURE["y"].write(self.context, self.y)
				buffer += self.STRUCTURE["z"].write(self.context, self.z)
				buffer += self.STRUCTURE["pitch"].write(self.context, self.pitch)
				buffer += self.STRUCTURE["yaw"].write(self.context, self.yaw)
				buffer += self.STRUCTURE["data"].write(self.context, self.data)

				if self.data != 0:
					buffer += self.STRUCTURE["velocity_x"].write(self.context, self.velocity_x)
					buffer += self.STRUCTURE["velocity_y"].write(self.context, self.velocity_y)
					buffer += self.STRUCTURE["velocity_z"].write(self.context, self.velocity_z)
			except Exception as e:
				raise RuntimeError(f"{self.NAME}: Error while writing key: {str(e)}")

			return common.types.common.VarInt.write(self.context, self.ID) + buffer


class SpawnObjectV107(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'object_uuid': common.types.common.UUID,
			'type': common.types.common.Byte,
			'x': common.types.complex.Double,
			'y': common.types.complex.Double,
			'z': common.types.complex.Double,
			'pitch': common.types.complex.Angle,
			'yaw': common.types.complex.Angle,
			'data': common.types.common.Integer,
			'velocity_x': common.types.complex.VelocityShort,
			'velocity_y': common.types.complex.VelocityShort,
			'velocity_z': common.types.complex.VelocityShort,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.object_uuid = None
		self.type = None
		self.x = None
		self.y = None
		self.z = None
		self.pitch = None
		self.yaw = None
		self.data = None
		self.velocity_x = None
		self.velocity_y = None
		self.velocity_z = None

	@property
	def ID(self):
		return 0x00