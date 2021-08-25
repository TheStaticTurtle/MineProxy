from networking.McPackets import serverbound, clientbound
from common.types.enums import McState

lut_serverbound = {
	McState.Handshaking: {
		0x00: serverbound.handshaking.Handshake,
		0xFE: serverbound.handshaking.LegacySeverPing
	},
	McState.Status: {
		0x00: serverbound.status.Request,
		0x01: serverbound.status.Ping
	},
	McState.Login: {
		0x00: serverbound.login.Start,
		0x01: serverbound.login.EncryptionResponse,
	},
	McState.Play: {
		0x17: serverbound.play.PluginMessage,
	}
}

lut_clientbound = {
	McState.Handshaking: {
	},
	McState.Status: {
		0x00: clientbound.status.Response,
		0x01: clientbound.status.Pong,
	},
	McState.Login: {
		0x00: clientbound.login.Disconnect,
		0x01: clientbound.login.EncryptionRequest,
		0x02: clientbound.login.Success,
		0x03: clientbound.login.SetCompression,
	},
	McState.Play: {
		0x00: clientbound.play.KeepAlive,
		0x01: clientbound.play.JoinGame,
		0x02: clientbound.play.ChatMessage,
		0x03: clientbound.play.TimeUpdate,
		0x04: clientbound.play.EntityEquipment,
		0x05: clientbound.play.SpawnPosition,
		0x06: clientbound.play.UpdateHealth,
		0x07: clientbound.play.Respawn,
		# 0x08: clientbound.play.,
		0x09: clientbound.play.HeldItemChanged,
		0x41: clientbound.play.ServerDifficulty,
		0x3f: clientbound.play.PluginMessage,
		0x40: clientbound.play.Disconnect,
	}
}

proto = {
	"clientbound": lut_clientbound,
	"serverbound": lut_serverbound,
}