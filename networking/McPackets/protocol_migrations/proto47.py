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
		0x08: clientbound.play.PositionAndLook,
		0x09: clientbound.play.HeldItemChanged,
		0x0A: clientbound.play.UseBed,
		0x0B: clientbound.play.Animation,
		0x0C: clientbound.play.SpawnPlayer,
		0x0D: clientbound.play.CollectItem,
		0x0E: clientbound.play.SpawnObject,
		0x0F: clientbound.play.SpawnMob,
		0x10: clientbound.play.SpawnPainting,
		0x11: clientbound.play.SpawnExperienceOrb,
		0x12: clientbound.play.EntityVelocity,
		0x13: clientbound.play.DestroyEntities,
		0x14: clientbound.play.Entity,
		0x15: clientbound.play.EntityRelativeMove,
		0x16: clientbound.play.EntityLook,
		0x17: clientbound.play.EntityLookAndRelativeMove,
		0x18: clientbound.play.EntityTeleport,
		0x19: clientbound.play.EntityHeadLook,
		0x1A: clientbound.play.EntityStatus,
		0x1B: clientbound.play.AttachEntity,
		0x1C: clientbound.play.EntityMetadata,
		0x1D: clientbound.play.EntityEffect,
		0x1E: clientbound.play.RemoveEntityEffect,
		0x1F: clientbound.play.SetExperience,

		0x3f: clientbound.play.PluginMessage,
		0x40: clientbound.play.Disconnect,
		0x41: clientbound.play.ServerDifficulty,
	}
}

proto = {
	"clientbound": lut_clientbound,
	"serverbound": lut_serverbound,
}