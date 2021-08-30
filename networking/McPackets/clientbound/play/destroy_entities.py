import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class DestroyEntities(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'count': common.types.common.VarInt,
		}

	def __init__(self, context):
		super().__init__(context)
		self.count = None
		self.entity_ids = []

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x30
		if self.context.protocol_version == 47:
			return 0x13
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")

	@classmethod
	def from_basic_packet(cls, packet):
		if isinstance(packet, Packet):
			buffer = Buffer()
			buffer.write(packet.raw_data)
			buffer.reset_cursor()

			new_packet = cls(packet.context)

			new_packet.count, _ = new_packet.STRUCTURE["count"].read(packet.context, buffer)
			for i in range(new_packet.count):
				new_packet.entity_ids.append(common.types.common.VarInt.read(packet.context, buffer)[0])

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
			buffer  = self.STRUCTURE["count"].write(self.context, self.count)
			for value in self.entity_ids:
				buffer += common.types.common.VarInt.write(self.context, value)

			return common.types.common.VarInt.write(self.context, self.ID) + buffer