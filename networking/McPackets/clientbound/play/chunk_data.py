import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class ChunkDataV47(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'chunk_x': common.types.common.Integer,
			'chunk_z': common.types.common.Integer,
			'ground_up_continuous': common.types.common.Boolean,
			'primary_bit_mask': common.types.common.UnsignedShort,
			'data': common.types.common.VarIntPrefixedByteArray,
		}

	STRUCTURE_REPR_HIDDEN_FIELDS = ["data"]

	def __init__(self, context):
		super().__init__(context)
		self.chunk_x = None
		self.chunk_z = None
		self.ground_up_continuous = None
		self.primary_bit_mask = None
		self.data = None

	@property
	def ID(self):
		if self.context.protocol_version == 47:
			return 0x21
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")


class ChunkDataV107(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'chunk_x': common.types.common.Integer,
			'chunk_z': common.types.common.Integer,
			'ground_up_continuous': common.types.common.Boolean,
			'primary_bit_mask': common.types.common.UnsignedShort,
			'data': common.types.common.VarIntPrefixedByteArray,
			'biomes': common.types.common.ByteArray,
		}

	STRUCTURE_REPR_HIDDEN_FIELDS = ["data", "biomes"]

	def __init__(self, context):
		super().__init__(context)
		self.chunk_x = None
		self.chunk_z = None
		self.ground_up_continuous = None
		self.primary_bit_mask = None
		self.data = None
		self.biomes = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x20
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")


	@classmethod
	def from_basic_packet(cls, packet):
		if isinstance(packet, Packet):
			buffer = Buffer()
			buffer.write(packet.raw_data)
			buffer.reset_cursor()

			new_packet = cls(packet.context)

			new_packet.chunk_x, _ = new_packet.STRUCTURE["chunk_x"].read(packet.context, buffer)
			new_packet.chunk_z, _ = new_packet.STRUCTURE["chunk_z"].read(packet.context, buffer)
			new_packet.ground_up_continuous, _ = new_packet.STRUCTURE["ground_up_continuous"].read(packet.context, buffer)
			new_packet.primary_bit_mask, _ = new_packet.STRUCTURE["primary_bit_mask"].read(packet.context, buffer)
			new_packet.data, _ = new_packet.STRUCTURE["data"].read(packet.context, buffer)
			if new_packet.ground_up_continuous:
				new_packet.biomes, _ = new_packet.STRUCTURE["biomes"].read(packet.context, buffer)

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
				buffer  = self.STRUCTURE["chunk_x"].write(self.context, self.chunk_x)
				buffer += self.STRUCTURE["chunk_z"].write(self.context, self.chunk_z)
				buffer += self.STRUCTURE["ground_up_continuous"].write(self.context, self.ground_up_continuous)
				buffer += self.STRUCTURE["primary_bit_mask"].write(self.context, self.primary_bit_mask)
				buffer += self.STRUCTURE["data"].write(self.context, self.data)
				if self.ground_up_continuous:
					buffer += self.STRUCTURE["biomes"].write(self.context, self.biomes)

			except Exception as e:
				raise RuntimeError(f"{self.NAME}: Error while writing key: {str(e)}")

			return common.types.common.VarInt.write(self.context, self.ID) + buffer