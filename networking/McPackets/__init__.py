from . import serverbound
from . import clientbound

from .PacketClasifier import Classifier as PacketClasifier

# lut_serverbound = {
# 	McState.Handshaking: {
# 		0x00: serverbound.Handshake,
# 		0xFE: serverbound.LegacySeverPing
# 	},
# 	McState.Status: {
# 		0x00: serverbound.StatusRequest,
# 		0x01: serverbound.StatusPing
# 	},
# 	McState.Login: {
# 		0x00: serverbound.LoginStart,
# 		0x01: serverbound.LoginEncryptionResponse,
# 		0x02: serverbound.LoginPluginResponse,
# 	},
# 	McState.Play: {
# 	}
# }
#
# lut_clientbound = {
# 	McState.Handshaking: {
# 	},
# 	McState.Status: {
# 		0x00: clientbound.StatusResponse,
# 		0x01: clientbound.StatusPong
# 	},
# 	McState.Login: {
# 		0x00: clientbound.LoginDisconnect,
# 		0x01: clientbound.LoginEncryptionRequest,
# 		0x02: clientbound.LoginSuccess,
# 		0x03: clientbound.LoginSetCompression,
# 		0x04: clientbound.LoginPluginRequest,
# 	},
# 	McState.Play: {
# 		0x01: clientbound.PlayJoinGame
# 	}
# }

# def classify_packet(packet, state, protocol_version, is_clientbound):
# 	if is_clientbound:
# 		if state in lut_clientbound.keys():
# 			if packet.id in lut_clientbound[state].keys():
# 				P = lut_clientbound[state][packet.id]
# 				return P.from_basic_packet(packet, protocol_version), True
# 	else:
# 		if state in lut_serverbound.keys():
# 			if packet.id in lut_serverbound[state].keys():
# 				P = lut_serverbound[state][packet.id]
# 				return P.from_basic_packet(packet, protocol_version), True
# 	return packet, False