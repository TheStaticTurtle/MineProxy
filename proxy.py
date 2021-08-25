import logging
import socket
import threading

import networking.McPackets as McPackets
from common.authentication import AuthenticationToken
from common.connection import Connection
from common.context import Context
from common.types import McState
from networking.McPackets.PacketPassthrought import PacketPassthrough
from networking.McPackets.interceptors.EncryptionInterceptor import EncryptionInterceptor
from networking.McPackets.interceptors.HandshakeInterceptor import HandshakeInterceptor
from networking.McPackets.interceptors.LoginStartInterceptor import LoginStartInterceptor


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

		self.context = Context()
		self.context.current_state = McState.Handshaking

		self.server_connection = Connection(self.context, upstreamSock)
		self.client_connection = Connection(self.context, self.__client_sock)
		self.server_bound_passthrought = PacketPassthrough(self.context, self.client_connection)
		self.client_bound_passthrought = PacketPassthrough(self.context, self.server_connection)

		self.interceptors = [
			HandshakeInterceptor(self.context, self.__client_addr, self.__server_addr),
			EncryptionInterceptor(self.context, self.server_connection, self.auth_token),
			LoginStartInterceptor(self.context, self.auth_token.profile),
		]
		self.packet_classifier = McPackets.PacketClasifier(self.context)

	def run(self):
		while True:
			try:
				packet = self.server_bound_passthrought.read_one()
				if packet:
					packet, packet_decoded = self.packet_classifier.classify_serverbound(packet)

					for interceptor in self.interceptors:
						if isinstance(packet, interceptor.packet_class):
							packet = interceptor.intercept(packet)

					if isinstance(packet, McPackets.serverbound.handshaking.Handshake):
						self.context.protocol_version = packet.protocol_version
						self.context.current_state = packet.next_state

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
					packet, packet_decoded = self.packet_classifier.classify_clientbound(packet)

					for interceptor in self.interceptors:
						if isinstance(packet, interceptor.packet_class):
							packet = interceptor.intercept(packet)

					if isinstance(packet, McPackets.clientbound.login.SetCompression):
						self.log.debug(f"Encrypted:{'✔' if self.server_connection.encrypted else '❌'}  {packet}")
						# Send the compression packet before setting the threshold otherwise it would send a compressed packet instead of the uncompressed one
						self.client_connection.socket.send(self.client_bound_passthrought.build_packet(packet))
						self.context.compression_threshold = packet.threshold
						packet = None

					if isinstance(packet, McPackets.clientbound.login.Success):
						self.context.current_state = McState.Play

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
