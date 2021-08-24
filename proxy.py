import logging
import socket
import threading

import networking.McPackets as McPackets
from networking.McPackets.PacketPassthrought import PacketPasstrought
from networking.McPackets.interceptors.EncryptionInterceptor import EncryptionInterceptor
from networking.McPackets.interceptors.HandshakeInterceptor import HandshakeInterceptor
from common.types import McState
from common import encryption
from common.authentication import AuthenticationToken
from common.connection import Connection

class MinecraftProxy(threading.Thread):
	def __init__(self, server_infos, client_socket_infos, auth_token: AuthenticationToken):
		threading.Thread.__init__(self)
		self.log = logging.getLogger("Proxy")
		self.log.info("Hellow world")
		self.auth_token = auth_token
		self.__client_sock, self.__client_addr = client_socket_infos
		self.__server_addr = server_infos

		self.current_state = McState.Handshaking
		self.protocol_version = 0

		self.log.info(f"New thread started for {self.__client_addr} bridging to {self.__server_addr}")

		upstreamSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			upstreamSock.connect(self.__server_addr)
		except ConnectionRefusedError:
			self.log.error(f"Cloud not connect to {self.__server_addr}")
			self.__client_sock.close()
			return

		self.server_connection = Connection(upstreamSock)
		self.client_connection = Connection(self.__client_sock)
		self.server_bound_passthrought = PacketPasstrought(self.client_connection)
		self.client_bound_passthrought = PacketPasstrought(self.server_connection)

		self.handshake_spoof_interceptor = HandshakeInterceptor(self.__client_addr, self.__server_addr)
		self.encryption_interceptor = EncryptionInterceptor(self.server_connection, self.auth_token)

	def run(self):
		packet_classifier = McPackets.PacketClasifier()
		packet_classifier.set_state(self.current_state)

		while True:
			try:
				packet = self.server_bound_passthrought.read_one()

				if packet:
					# if self.current_state == McState.Handshaking or self.current_state == McState.Login or self.current_state == McState.Status:
					packet, packet_decoded = packet_classifier.classify_serverbound(packet)

					if isinstance(packet, McPackets.serverbound.Handshake):
						packet = self.handshake_spoof_interceptor.intercept(packet)

						packet_classifier.set_protocol(packet.protocol_version)
						self.client_bound_passthrought.set_protocol_version(packet.protocol_version)
						self.server_bound_passthrought.set_protocol_version(packet.protocol_version)
						self.encryption_interceptor.set_protocol_version(packet.protocol_version)
						packet_classifier.set_state(packet.next_state)
						self.protocol_version = packet.protocol_version
						self.current_state = packet.next_state

					if packet:
						self.log.debug(f"Encrypted:{'✔' if self.server_connection.encrypted else '❌'}  {packet}")
						self.server_connection.socket.send(self.server_bound_passthrought.build_packet(packet))


			except BlockingIOError:
				pass
			except ConnectionAbortedError:
				self.log.error(f"{self.__client_addr} closed connection to {self.__server_addr}")
				self.client_connection.close()
				self.server_connection.close()
				return

			try:
				packet = self.client_bound_passthrought.read_one()
				if packet:
					# if self.current_state == McState.Handshaking or self.current_state == McState.Login or self.current_state == McState.Status:
					packet, packet_decoded = packet_classifier.classify_clientbound(packet)

					if isinstance(packet, McPackets.clientbound.LoginSetCompression):
						self.log.debug(f"Encrypted:{'✔' if self.server_connection.encrypted else '❌'}  {packet}")
						self.encryption_interceptor.set_compression_threshold(packet.threshold)
						self.client_connection.socket.send(self.client_bound_passthrought.build_packet(packet))
						self.client_bound_passthrought.set_compression_threshold(packet.threshold)
						self.server_bound_passthrought.set_compression_threshold(packet.threshold)
						packet = None

					if isinstance(packet, McPackets.clientbound.LoginSuccess):
						packet_classifier.set_state(McState.Play)
						self.current_state = McState.Play

					if isinstance(packet, McPackets.clientbound.LoginEncryptionRequest):
						packet = self.encryption_interceptor.intercept(packet)

					if packet:
						self.log.debug(f"Encrypted:{'✔' if self.server_connection.encrypted else '❌'}  {packet}")
						self.client_connection.socket.send(self.client_bound_passthrought.build_packet(packet))

			except BlockingIOError:
				pass
			except ConnectionAbortedError:
				self.log.error(f"{self.__client_addr} closed connection to {self.__server_addr}")
				self.client_connection.close()
				self.server_connection.close()
				return



class MinecraftProxyManager(threading.Thread):
	"""docstring for ClassName"""
	def __init__(self, server_ip, server_port=25565, listen_port=25565, auth_token=None):
		super(MinecraftProxyManager, self).__init__()
		self.log = logging.getLogger("Proxy/Manager")
		self.log.info("Hellow world")
		self.auth_token = auth_token
		self.server_ip = server_ip
		self.server_port = server_port
		self.listen_port = listen_port

	def run(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind(("0.0.0.0", self.listen_port))
		server.settimeout(1)
		self.log.info("Running waiting for clients")

		clients = []

		while True:
			try:
				server.listen()
				info = server.accept()
				client = MinecraftProxy((self.server_ip, self.server_port), info, self.auth_token)
				client.start()
				clients.append(client)
			except socket.timeout:
				pass
