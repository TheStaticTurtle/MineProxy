import io

class _SocketEmulation:
    def __init__(self):
        pass

    def write(self, value):
        pass

    def send(self, value):
        self.write(value)

    def read(self, length):
        return b""

    def recv(self, length):
        return self.read(length)

class Buffer(_SocketEmulation):
    def __init__(self):
        _SocketEmulation.__init__(self)
        self.bytes = io.BytesIO()

    def write(self, value):
        if value:
            self.bytes.write(value)

    def read(self, length):
        return self.bytes.read(length)

    def read_all(self):
        return self.bytes.read()

    def reset(self):
        self.bytes = io.BytesIO()

    def tell(self):
        return self.bytes.tell()

    def peek(self, count):
        all_bytes = self.bytes.getvalue()
        current_pos = self.bytes.tell()
        return all_bytes[current_pos:current_pos+count]

    def reset_cursor(self):
        self.bytes.seek(0)

    def get_writable(self):
        return self.bytes.getvalue()
