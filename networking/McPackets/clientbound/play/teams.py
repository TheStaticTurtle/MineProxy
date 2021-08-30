import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class Teams(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'team_name': common.types.common.String,
		'mode': common.types.common.Byte,
		'team_display_name': common.types.common.String,
		'team_prefix': common.types.common.String,
		'team_suffix': common.types.common.String,
		'friendly_fire': common.types.common.Byte,
		'name_tag_visibility': common.types.common.String,
		'color': common.types.common.Byte,
		'players': common.types.complex.VarIntStringArray,
	}

	def __init__(self, context):
		super().__init__(context)
		self.team_name = None
		self.mode = None
		self.team_display_name = None
		self.team_prefix = None
		self.team_suffix = None
		self.friendly_fire = None
		self.name_tag_visibility = None
		self.color = None
		self.players = None

	@property
	def ID(self):
		return 0x3E


	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		try:
			new_packet.team_name, _ = new_packet.STRUCTURE["team_name"].read(packet.context, buffer)
			new_packet.mode, _ = new_packet.STRUCTURE["mode"].read(packet.context, buffer)
			if new_packet.mode in [0, 2]:
				new_packet.team_display_name, _ = new_packet.STRUCTURE["team_display_name"].read(packet.context, buffer)
				new_packet.team_prefix, _ = new_packet.STRUCTURE["team_prefix"].read(packet.context, buffer)
				new_packet.team_suffix, _ = new_packet.STRUCTURE["team_suffix"].read(packet.context, buffer)
				new_packet.friendly_fire, _ = new_packet.STRUCTURE["friendly_fire"].read(packet.context, buffer)
				new_packet.name_tag_visibility, _ = new_packet.STRUCTURE["name_tag_visibility"].read(packet.context, buffer)
				new_packet.color, _ = new_packet.STRUCTURE["color"].read(packet.context, buffer)
			if new_packet.mode in [0, 3, 4]:
				new_packet.players, _ = new_packet.STRUCTURE["players"].read(packet.context, buffer)

		except Exception as e:
			raise RuntimeError(f"{new_packet.NAME}: Error while writing key: {str(e)}")

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""

		try:
			buffer += self.STRUCTURE["team_name"].write(self.context, self.team_name)
			buffer += self.STRUCTURE["mode"].write(self.context, self.mode)
			if self.mode in [0, 2]:
				buffer += self.STRUCTURE["team_display_name"].write(self.context, self.team_display_name)
				buffer += self.STRUCTURE["team_prefix"].write(self.context, self.team_prefix)
				buffer += self.STRUCTURE["team_suffix"].write(self.context, self.team_suffix)
				buffer += self.STRUCTURE["friendly_fire"].write(self.context, self.friendly_fire)
				buffer += self.STRUCTURE["name_tag_visibility"].write(self.context, self.name_tag_visibility)
				buffer += self.STRUCTURE["color"].write(self.context, self.color)
			if self.mode in [0, 3, 4]:
				buffer += self.STRUCTURE["players"].write(self.context, self.players)

		except Exception as e:
			raise RuntimeError(f"{self.NAME}: Error while writing key: {str(e)}")

		return common.types.common.VarInt.write(self.context, self.ID) + buffer