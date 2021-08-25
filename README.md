# MineProxy

MineProxy is a tool designed to proxy Minecraft packets from a client to a server while decoding them. This tool could be used for a lot of things (for example, packet logging).

This proxy isn't a simple TCP tunnel, it fully implements the base of the Minecraft protocol (compression and encryption).

The proxy uses Minecraft protocol [47](https://wiki.vg/index.php?title=Protocol&oldid=7368) as it's base, but will be updated to more recent versions

## About compression

This tool fully supports the compression of Minecraft packets, it will automatically adjust it's setting if it receives a `SetCompression` packet (It will proxy this packet back to the client)

## About encryption
This tool allows connecting to servers in online mode. Since after a few packets, the network traffic becomes encrypted by the client, you can't just decode it. 
This tool intercepts a `EncryptionRequest` packet, generate its own secrets and craft a `EncryptionResponse` packet to send to the server.
The Minecraft client has no idea that the traffic is being encrypted since it never received the request

Generating a`EncryptionRequest` packet and login into online server does mean that the tools needs to authenticate to Mojang servers, meaning that you have to enter your logins not in the Minecraft client but in the proxy itself. This is done via environment variable (or a .env file)

## What's implemented right now?

Right now, all the basics allowing for packet decoding / encoding / compression and network encryption is implemented.
A part of the protocol V47, you can see the packets in the `networking/McPackets/protocol_migration/proto47.py`. The goal being having it completely implemented

### Protocols migration ?
The base is V47 but let's imagine we want to support packets from protocol V109, instead of rewriting the entire packet table for the V109 we can just ignore packets like Handshake and don't add them in the V109 table. Instead, the script will find the closest version, in this case it's the V47 one

A packet was removed from V47 in V109? Just set the packet ID to None, and it will be like it's not there.

## License
See LICENSE.md