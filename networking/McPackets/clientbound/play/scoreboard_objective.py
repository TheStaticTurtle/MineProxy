import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class ScoreboardObjective(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
		'objective_name': common.types.common.String,
		'mode': common.types.common.Byte,
		'objective_value': common.types.common.String,
		'type': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.objective_name = None
		self.mode = None
		self.objective_value = None
		self.type = None

	@property
	def ID(self):
		return 0x3B


	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		try:
			new_packet.objective_name, _ = new_packet.STRUCTURE["objective_name"].read(packet.context, buffer)
			new_packet.mode, _ = new_packet.STRUCTURE["mode"].read(packet.context, buffer)
			if new_packet.mode in [0, 2]:
				new_packet.objective_value, _ = new_packet.STRUCTURE["objective_value"].read(packet.context, buffer)
				new_packet.type, _ = new_packet.STRUCTURE["type"].read(packet.context, buffer)

		except Exception as e:
			raise RuntimeError(f"{new_packet.NAME}: Error while writing key {key} for type {new_packet.STRUCTURE[key].__class__.__name__}: {str(e)}")

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""

		try:
			buffer += self.STRUCTURE["objective_name"].write(self.context, self.objective_name)
			buffer += self.STRUCTURE["mode"].write(self.context, self.mode)

			if self.mode in [0, 2]:
				buffer += self.STRUCTURE["objective_value"].write(self.context, self.objective_name)
				buffer += self.STRUCTURE["type"].write(self.context, self.type)

		except Exception as e:
			raise RuntimeError(f"{self.NAME}: Error while writing key {key} for type {self.STRUCTURE[key].__class__.__name__}: {str(e)}")

		return common.types.common.VarInt.write(self.context, self.ID) + buffer