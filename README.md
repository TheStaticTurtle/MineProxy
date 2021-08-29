
# MineProxy  
  
MineProxy is a tool designed to proxy Minecraft packets from a client to a server while decoding them. This tool could be used for a lot of things (for example packet logging).  
  
This proxy isn't a simple TCP tunnel, it fully implements the base of the Minecraft protocol (compression and encryption).  
  
The proxy uses Minecraft protocol [47](https://wiki.vg/index.php?title=Protocol&oldid=7368) as it's base, but will be updated to more recent versions  
  
## Warning
This tool is still in construction things might change. Moreover packets are not all tested (most of them are tho).
If you disable play packets you might be able to use this tool for unsupported protocol versions
## Config  

Config is based on a python file named `config.py`, you can see an example in the `config.example.py` but here are what the values mean:

| Variable                         | Use | Type |
|----------------------------------|-----|------|
| MINEPROXY_PROXY_REMOTE_IP        | IP of the real server | String |
| MINEPROXY_PROXY_REMOTE_PORT      | Port of the real server | Int |
| MINEPROXY_PROXY_LISTEN_PORT      | Port of the proxy | Int |
| MINEPROXY_PARSE_PLAY_PACKETS     | Parse `Play` packets (disabling drastically increase performance) | Boolean |
| MINEPROXY_AUTH_USE_MICROSOFT     | Try and use microsoft (xbox live) authentication **Experimental** | Boolean |  
| MINEPROXY_AUTH_MINECRAFT_EMAIL   | Email used for authenticating to mojang servers |  String |
| MINEPROXY_AUTH_MINECRAFT_PASSWORD| Password used for the authentication | String |

## About authentication  
  
This tool should work just fine if you minecraft account is a mojang one.<br>
If your account is a microsoft account you can try to set `MINEPROXY_AUTH_USE_MICROSOFT` to `True` this feature is experimental as it's based on reading PrismarineJS and xbox-live-auth source code and some parts docs
  
## About compression  
  
This tool fully supports the compression of Minecraft packets, it will automatically adjust it's setting if it receives a `SetCompression` packet (It will proxy this packet back to the client)  
  
## About encryption  
This tool allows connecting to servers in online mode. Since after a few packets, the network traffic becomes encrypted by the client, you can't just decode it.   
This tool intercepts a `EncryptionRequest` packet, generate its own secrets and craft a `EncryptionResponse` packet to send to the server.  
The Minecraft client has no idea that the traffic is being encrypted since it never received the request  
  
Generating a `EncryptionRequest` packet and login into online server does mean that the tools needs to authenticate to Mojang servers, meaning that you have to enter your logins not in the Minecraft client but in the proxy itself. This is done via environment variable (or a .env file)  
  
## What's implemented right now?  
  
All the basics allowing for packet decoding / encoding / compression and network encryption are implemented. Here is what is implemented  
| Minecraft Version | Protocol Version | Coverage |  
|-------------------|------------------|----------|  
| 1.8 - 1.8.9       | [47](https://wiki.vg/index.php?title=Protocol&oldid=7368)               | Non-Play packets: 12/12<br>Serverbound packets: 32/32<br>Clientbound packets: 75/80<br>Missing packets:<br>- `MapChunkBulk`<br>- `Map`<br>- `PlayerListItem`<br>- `WorldBorder`<br>- `Title` |  
  
### Protocols migration ?  
The base is V47 but let's imagine we want to support packets from protocol V109, instead of rewriting the entire packet table for the V109 we can just ignore packets like Handshake and don't add them in the V109 table. Instead, the script will find the closest version, in this case it's the V47 one  
  
A packet was removed from V47 in V109? Just set the packet ID to None, and it will be like it's not there.  
  
## License  
See [LICENSE.md](https://github.com/TheStaticTurtle/MineProxy/blob/master/LICENSE.md)