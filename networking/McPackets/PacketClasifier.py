from networking.McPackets import serverbound
from common.types import McState
from networking.McPackets.luts import proto47

class LutManager:
	DEFAULT_CLIENTBOUND_LUT = {
		McState.Handshaking: {},
		McState.Status: {},
		McState.Login: {},
		McState.Play: {}
	}
	DEFAULT_SERVERBOUND_LUT = {
		McState.Handshaking: {
			0x00: serverbound.Handshake,
			0xFE: serverbound.LegacySeverPing
		},
		McState.Status: {},
		McState.Login: {},
		McState.Play: {}
	}

	def __init__(self):
		self.luts = {
			47: proto47.proto
		}

	def get_luts_for_protocol_version(self, version):
		if version not in self.luts.keys():
			raise RuntimeError(f"Protocol {version} is not supported at this time")

		return self.luts[version]["serverbound"] , self.luts[version]["clientbound"]

class Classifier:

	def __init__(self):
		self.manager = LutManager()
		self.lut_serverbound = LutManager.DEFAULT_SERVERBOUND_LUT
		self.lut_clientbound = LutManager.DEFAULT_CLIENTBOUND_LUT

		self.protocol = None
		self.state = None

	def set_protocol(self, version):
		self.lut_serverbound, self.lut_clientbound = self.manager.get_luts_for_protocol_version(version)
		self.protocol = version

	def set_state(self, state):
		self.state = state

	def classify_clientbound(self, packet):
		if self.state in self.lut_clientbound.keys():
			if packet.id in self.lut_clientbound[self.state].keys():
				P = self.lut_clientbound[self.state][packet.id]
				return P.from_basic_packet(packet, self.protocol), True
		return packet, False

	def classify_serverbound(self, packet):
		if self.state in self.lut_serverbound.keys():
			if packet.id in self.lut_serverbound[self.state].keys():
				P = self.lut_serverbound[self.state][packet.id]
				return P.from_basic_packet(packet, self.protocol), True
		return packet, False