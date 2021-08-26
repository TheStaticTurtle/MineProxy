import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket


class PositionAndLook(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'x': common.types.common.Double,
		'y': common.types.common.Double,
		'z': common.types.common.Double,
		'yaw': common.types.common.Float,
		'pitch': common.types.common.Float,
		'flags': common.types.common.Byte,
	}

	FLAG_REL_X = 0x01
	FLAG_REL_Y = 0x02
	FLAG_REL_Z = 0x04
	FLAG_REL_YAW = 0x08
	FLAG_REL_PITCH = 0x10

	def __init__(self, context):
		super().__init__(context)
		self.x = None
		self.x_relative = None
		self.y = None
		self.y_relative = None
		self.z = None
		self.z_relative = None
		self.yaw = None
		self.yaw_relative = None
		self.pitch = None
		self.pitch_relative = None
		self.flags = None

	@property
	def ID(self):
		return 0x08

	def apply_meta_fields(self):
		self.x_relative = bool(self.flags & self.FLAG_REL_X)
		self.y_relative = bool(self.flags & self.FLAG_REL_Y)
		self.z_relative = bool(self.flags & self.FLAG_REL_Z)
		self.yaw_relative = bool(self.flags & self.FLAG_REL_YAW)
		self.pitch_relative = bool(self.flags & self.FLAG_REL_PITCH)

	def __repr__(self):
		x_str = ("~" if self.x_relative else "")+str(self.x)
		y_str = ("~" if self.y_relative else "")+str(self.y)
		z_str = ("~" if self.z_relative else "")+str(self.z)
		yaw_str = ("~" if self.yaw_relative else "")+str(self.yaw)
		pitch_str = ("~" if self.pitch_relative else "")+str(self.pitch)
		return f"<{self.NAME} x={x_str} y={y_str} z={z_str} yaw={yaw_str} pitch={pitch_str}>"
