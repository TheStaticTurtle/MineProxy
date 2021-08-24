from networking.McPackets import serverbound, clientbound
from common.types import McState

lut_serverbound = {
	McState.Handshaking: {
		0x00: serverbound.Handshake,
		0xFE: serverbound.LegacySeverPing
	},
	McState.Status: {
		0x00: serverbound.StatusRequest,
		0x01: serverbound.StatusPing
	},
	McState.Login: {
		0x00: serverbound.LoginStart,
		0x01: serverbound.LoginEncryptionResponse,
		0x02: serverbound.LoginPluginResponse,
	},
	McState.Play: {
		0x17: serverbound.PlayPluginMessage,
	}
}

lut_clientbound = {
	McState.Handshaking: {
	},
	McState.Status: {
		0x00: clientbound.StatusResponse,
		0x01: clientbound.StatusPong,
	},
	McState.Login: {
		0x00: clientbound.LoginDisconnect,
		0x01: clientbound.LoginEncryptionRequest,
		0x02: clientbound.LoginSuccess,
		0x03: clientbound.LoginSetCompression,
		0x04: clientbound.LoginPluginRequest,
	},
	McState.Play: {
		0x01: clientbound.PlayJoinGame,
		0x41: clientbound.PlayServerDifficulty,
		0x05: clientbound.PlaySpawnPosition,
		0x3f: clientbound.PlayPluginMessage,
		0x09: clientbound.PlayHeldItemChanged,
		0x40: clientbound.PlayDisconnect,
	}
}

proto = {
	"clientbound": lut_clientbound,
	"serverbound": lut_serverbound,
}