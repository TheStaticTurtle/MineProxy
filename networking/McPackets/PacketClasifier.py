import logging
from common.context import Context
from networking.McPackets.protocol_migrations import proto47

def merge_dicts_rec(*kwarg):
	out = {}
	for t in kwarg:
		for key in t.keys():
			if key in out:
				if isinstance(t[key], dict) and isinstance(out[key], dict):
					out[key] = merge_dicts_rec(out[key], t[key])
				else:
					out[key] = t[key]
			else:
				out[key] = t[key]
	return out

class LutManager:
	def __init__(self):
		self.log = logging.getLogger("LutManager")
		self.lut_versions = [47]
		self.luts_serverbound = {
			47: proto47.lut_serverbound,
		}
		self.luts_clientbound = {
			47: proto47.lut_clientbound,
		}

	def get_highest_protocol_version(self, under=None):
		return max([v for v in self.lut_versions if under is None or v <= under])

	def get_lowest_protocol_version(self, over=None):
		return min([v for v in self.lut_versions if over is None or v >= over])

	def _get_all_luts_under_version(self, under, reverse=False):
		self.lut_versions.sort(reverse=reverse)
		versions = [v for v in self.lut_versions if v <= under]
		cb_luts = [self.luts_clientbound[version] for version in versions]
		sb_luts = [self.luts_serverbound[version] for version in versions]
		return cb_luts, sb_luts

	def get_luts_for_protocol_version(self, version):
		max_v = self.get_highest_protocol_version(under=version)

		if version not in self.luts_serverbound.keys() or version not in self.luts_clientbound.keys():
			self.log.warning(f"Protocol version {version} is not yet supported. Running on protocol version {max_v}. YOU MAY RUN INTO ISSUES")
			version = max_v

		self.log.info(f"Generaton clientbound and servbound luts for version {version}")
		cb_luts, sb_luts = self._get_all_luts_under_version(version, reverse=False)

		clientbound_lut = merge_dicts_rec(*cb_luts)
		serverbound_lut = merge_dicts_rec(*sb_luts)

		return serverbound_lut, clientbound_lut

class Classifier:
	def __init__(self, context: Context):
		self.context = context
		self.context.add_protocol_change_callback(self._update_lut)
		self.manager = LutManager()
		self._update_lut(version=self.manager.get_lowest_protocol_version())

	def _update_lut(self, version=None):
		if version:
			self.lut_serverbound, self.lut_clientbound = self.manager.get_luts_for_protocol_version(version)
		else:
			self.lut_serverbound, self.lut_clientbound = self.manager.get_luts_for_protocol_version(self.context.protocol_version)

	def classify_clientbound(self, packet):
		if self.context.current_state in self.lut_clientbound.keys():
			if packet.ID in self.lut_clientbound[self.context.current_state].keys():
				P = self.lut_clientbound[self.context.current_state][packet.ID]
				if P:
					return P.from_basic_packet(packet), True
		return packet, False

	def classify_serverbound(self, packet):
		if self.context.current_state in self.lut_serverbound.keys():
			if packet.ID in self.lut_serverbound[self.context.current_state].keys():
				P = self.lut_serverbound[self.context.current_state][packet.ID]
				if P:
					return P.from_basic_packet(packet), True
		return packet, False