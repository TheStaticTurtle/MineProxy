import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, CombatEventEvent
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class CombatEvent(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'event': common.types.complex.CombatEventEventEnum,
		'duration': common.types.common.VarInt,
		'player_id': common.types.common.VarInt,
		'entity_id': common.types.common.Integer,
		'message': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.event = None
		self.duration = None
		self.player_id = None
		self.entity_id = None
		self.message = None

	@property
	def ID(self):
		return 0x42

	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		try:
			new_packet.event, _ = cls.STRUCTURE["event"].read(packet.context, buffer)
			if new_packet.event == CombatEventEvent.EndCombat:
				new_packet.duration, _ = cls.STRUCTURE["duration"].read(packet.context, buffer)
			if new_packet.event == CombatEventEvent.EntityDead:
				new_packet.player_id, _ = cls.STRUCTURE["player_id"].read(packet.context, buffer)
			if new_packet.event in [CombatEventEvent.EndCombat, CombatEventEvent.EntityDead]:
				new_packet.entity_id, _ = cls.STRUCTURE["entity_id"].read(packet.context, buffer)
			if new_packet.event == CombatEventEvent.EntityDead:
				new_packet.message, _ = cls.STRUCTURE["message"].read(packet.context, buffer)

		except Exception as e:
			raise RuntimeError(f"{new_packet.NAME}: Error while writing key: {str(e)}")

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""

		try:
			buffer += self.STRUCTURE["event"].write(self.context, self.event)
			if self.event == CombatEventEvent.EndCombat:
				buffer += self.STRUCTURE["duration"].write(self.context, self.duration)
			if self.event == CombatEventEvent.EntityDead:
				buffer += self.STRUCTURE["player_id"].write(self.context, self.player_id)
			if self.event in [CombatEventEvent.EndCombat, CombatEventEvent.EntityDead]:
				buffer += self.STRUCTURE["entity_id"].write(self.context, self.entity_id)
			if self.event == CombatEventEvent.EntityDead:
				buffer += self.STRUCTURE["message"].write(self.context, self.message)

		except Exception as e:
			raise RuntimeError(f"{self.NAME}: Error while writing key: {str(e)}")

		return common.types.common.VarInt.write(self.context, self.ID) + buffer