import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class Particle(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'particle_id': common.types.common.Integer,
			'long_distance': common.types.common.Boolean,
			'x': common.types.common.Float,
			'y': common.types.common.Float,
			'z': common.types.common.Float,
			'offset_x': common.types.common.Float,
			'offset_y': common.types.common.Float,
			'offset_z': common.types.common.Float,
			'particle_data': common.types.common.Float,
			'particle_count': common.types.common.Integer,
		}

	def __init__(self, context):
		super().__init__(context)
		self.particle_id = None
		self.long_distance = None
		self.x = None
		self.y = None
		self.z = None
		self.offset_x = None
		self.offset_y = None
		self.offset_z = None
		self.particle_data = None
		self.particle_count = None
		self.data = []

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x22
		if self.context.protocol_version == 47:
			return 0x2A
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")

	def __repr__(self):
		return f"<{self.NAME} particle_id={self.particle_id} long_distance={self.long_distance} x={self.x} y={self.y} z={self.z} offset_x={self.offset_x} offset_y={self.offset_y} offset_z={self.offset_z} particle_data={self.particle_data} particle_count={self.particle_count} data={self.data}>"

	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		for key in new_packet.STRUCTURE.keys():
			try:
				value, _ = new_packet.STRUCTURE[key].read(packet.context, buffer)
				new_packet.__setattr__(key, value)
			except Exception as e:
				raise RuntimeError(f"{new_packet.NAME}: Error while writing key {key} for type {new_packet.STRUCTURE[key].__class__.__name__}: {str(e)}")

		data_varint_count = 0
		if new_packet.particle_id in [36]:
			data_varint_count = 2
		if new_packet.particle_id in [37, 38]:
			data_varint_count = 1

		for i in range(data_varint_count):
			v, _ = common.types.common.VarInt.read(packet.context, buffer)
			new_packet.data.append(v)

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""
		for key in self.STRUCTURE.keys():
			try:
				value = self.__getattribute__(key)
				buffer += self.STRUCTURE[key].write(self.context, value)
			except Exception as e:
				raise RuntimeError(f"{self.NAME}: Error while writing key {key} for type {self.STRUCTURE[key].__class__.__name__}: {str(e)}")

		for value in self.data:
			buffer += common.types.common.VarInt.write(self.context, value)

		return common.types.common.VarInt.write(self.context, self.ID) + buffer

