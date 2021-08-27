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
		0x00: serverbound.play.KeepAlive,
		0x01: serverbound.play.ChatMessage,
		0x02: serverbound.play.UseEntity,
		0x03: serverbound.play.Player,
		0x04: serverbound.play.PlayerPosition,
		0x05: serverbound.play.PlayerLook,
		0x06: serverbound.play.PlayerLookAndPosition,
		0x07: serverbound.play.PlayerDigging,
		0x08: serverbound.play.PlayerBlockPlacement,
		0x09: serverbound.play.HeldItemChange,
		0x0A: serverbound.play.Animation,
		0x0B: serverbound.play.EntityAction,
		0x0C: serverbound.play.SteerVehicle,
		0x0D: serverbound.play.CloseWindow,
		0x0E: serverbound.play.ClickWindow,
		0x0F: serverbound.play.ConfirmTransaction,
		0x10: serverbound.play.CreativeInventorAction,
		0x11: serverbound.play.EnchantItem,
		0x12: serverbound.play.UpdateSign,
		0x13: serverbound.play.PlayerAbilities,
		0x14: serverbound.play.TabComplete,
		0x15: serverbound.play.ClientSettings,
		0x16: serverbound.play.ClientStatus,
		0x17: serverbound.play.PluginMessage,
		0x18: serverbound.play.Spectate,
		0x19: serverbound.play.ResourcePackStatus,
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
		0x20: clientbound.play.EntityProperties,
		0x21: clientbound.play.ChunkData,
		0x22: clientbound.play.MultiBlockChange,
		0x23: clientbound.play.BlockChange,
		0x24: clientbound.play.BlockAction,
		0x25: clientbound.play.BlockBreakAnimation,
		# 0x26: clientbound.play., # TODO: Nope not tonight see: map chunk bulk
		0x27: clientbound.play.Explosion,
		0x28: clientbound.play.Effect,
		0x29: clientbound.play.SoundEffect,
		0x2A: clientbound.play.Particle,
		0x2B: clientbound.play.ChangeGameState,
		0x2C: clientbound.play.SpawnGlobalEntity,
		0x2D: clientbound.play.OpenWindow,
		0x2E: clientbound.play.CloseWindow,
		0x2F: clientbound.play.SetSlot,
		0x30: clientbound.play.WindowItems,
		0x31: clientbound.play.WindowProperty,
		0x32: clientbound.play.ConfirmTransaction,
		0x33: clientbound.play.UpdateSign,
		# 0x34: clientbound.play., # TODO: Nope not tonight see: map
		0x35: clientbound.play.UpdateBlockEntity,
		0x36: clientbound.play.OpenSignEditor,
		0x37: clientbound.play.Statistics,
		# 0x38: clientbound.play., # TODO: Nope not tonight see: player list item
		0x39: clientbound.play.PlayerAbilitites,
		0x3A: clientbound.play.TabComplete,
		0x3B: clientbound.play.ScoreboardObjective,
		0x3C: clientbound.play.UpdateScore,
		0x3D: clientbound.play.DisplayScoreboard,
		0x3E: clientbound.play.Teams,
		0x3F: clientbound.play.PluginMessage,
		0x40: clientbound.play.Disconnect,
		0x41: clientbound.play.ServerDifficulty,
		0x42: clientbound.play.CombatEvent,
		0x43: clientbound.play.Camera,
		# 0x44: clientbound.play., # TODO: Nope not tonight see: world border
		# 0x45: clientbound.play., # TODO: Nope not tonight see: title
		0x46: clientbound.play.SetCompression,
		0x47: clientbound.play.PlayerListHeaderAndFooter,
		0x48: clientbound.play.RessourcePackSend,
		0x49: clientbound.play.UpdateEntityNBT,
	}
}

proto = {
	"clientbound": lut_clientbound,
	"serverbound": lut_serverbound,
}