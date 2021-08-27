import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class UpdateScore(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'score_name': common.types.common.String,
		'action': common.types.common.Byte,
		'objective_name': common.types.common.String,
		'value': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.score_name = None
		self.action = None
		self.objective_name = None
		self.value = None

	@property
	def ID(self):
		return 0x3C


	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		try:
			new_packet.score_name, _ = cls.STRUCTURE["score_name"].read(packet.context, buffer)
			new_packet.action, _ = cls.STRUCTURE["action"].read(packet.context, buffer)
			new_packet.objective_name, _ = cls.STRUCTURE["objective_name"].read(packet.context, buffer)
			if new_packet.action != 1:
				new_packet.value, _ = cls.STRUCTURE["value"].read(packet.context, buffer)

		except Exception as e:
			raise RuntimeError(f"{new_packet.NAME}: Error while writing key: {str(e)}")

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""

		try:
			buffer += self.STRUCTURE["score_name"].write(self.context, self.score_name)
			buffer += self.STRUCTURE["action"].write(self.context, self.action)
			buffer += self.STRUCTURE["objective_name"].write(self.context, self.objective_name)

			if self.action != 1:
				buffer += self.STRUCTURE["value"].write(self.context, self.value)

		except Exception as e:
			raise RuntimeError(f"{self.NAME}: Error while writing key: {str(e)}")

		return common.types.common.VarInt.write(self.context, self.ID) + buffer