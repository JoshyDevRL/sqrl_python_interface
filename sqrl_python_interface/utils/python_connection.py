
import win32file
import sys
import struct
import time

class NamedPipeClient:
    def __init__(self, pipe_name):
        self.pipe_name = pipe_name
        self.pipe = None

    def connect(self):
        for i in range(20):
            time.sleep(0.5)
            try:
                self.pipe = win32file.CreateFile(
                    self.pipe_name,
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None
                )
                return True
            except Exception as e:
                print(f"[PI] Failed to connect to the pipe")

    def write(self, message):
        if self.pipe:
            win32file.WriteFile(self.pipe, message)

    def read(self):
        if self.pipe:
            hr, data = win32file.ReadFile(self.pipe, 64*1024)
            return data

    def close(self):
        if self.pipe:
            win32file.CloseHandle(self.pipe)
            self.pipe = None


# SPEC
# 0-11 blue car physics (floats)
# 12 blue car boost (float)
# 13 blue car team (int)
# 14-18 blue car (bools)

# 19-30 orange car physics (floats)
# 31 orange car boost (float)
# 32 orange car team (int)
# 33-37 orange car (bools)

# 38 boost active (bool)
# 39 boost timer (float)
# * 34
# 106-114 ball physics (floats)
# 115 game time (float)
# 116 game time remaining (float)
# 117-118 game (bools)


def deserialize_gamestate(binary_data):
    state_dict = []
    offset = 0

    def read_vec():
        nonlocal offset
        vec = struct.unpack('3f', binary_data[offset:offset + 3 * 4])
        offset += 3 * 4
        return vec

    if binary_data == b'EXIT\x00':
        print("[PI] Received EXIT command.")
        exit(0)
    
    # Blue Car
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())
    state_dict.append(struct.unpack('f', binary_data[offset:offset + 4])[0])
    offset += 4
    state_dict.append(struct.unpack('i', binary_data[offset:offset + 4])[0])
    offset += 4
    for i in range(5):
        state_dict.append(struct.unpack('?', binary_data[offset:offset + 1])[0])
        offset += 1

    # Orange Car
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())
    state_dict.append(struct.unpack('f', binary_data[offset:offset + 4])[0])
    offset += 4
    state_dict.append(struct.unpack('i', binary_data[offset:offset + 4])[0])
    offset += 4
    for i in range(5):
        state_dict.append(struct.unpack('?', binary_data[offset:offset + 1])[0])
        offset += 1

    # Boost Pads
    for _ in range(34):
        state_dict.append(struct.unpack('?', binary_data[offset:offset + 1])[0])
        offset += 1
        state_dict.append(struct.unpack('f', binary_data[offset:offset + 4])[0])
        offset += 4

    # Ball
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())
    state_dict.extend(read_vec())

    # Game
    state_dict.append(struct.unpack('f', binary_data[offset:offset + 4])[0])
    offset += 4
    state_dict.append(struct.unpack('f', binary_data[offset:offset + 4])[0])
    offset += 4
    state_dict.append(struct.unpack('?', binary_data[offset:offset + 1])[0])
    offset += 1
    state_dict.append(struct.unpack('?', binary_data[offset:offset + 1])[0])
    offset += 1
    state_dict.append(struct.unpack('i', binary_data[offset:offset + 4])[0])
    offset += 4
    return state_dict

def serialize_data(floats, bools):
    assert len(floats) == 5
    assert len(bools) == 3

    binary_data = struct.pack('5f', *floats)
    binary_data += struct.pack('3?', *bools)
    return binary_data


class PythonInterface:
    def __init__(self, pipe_name_ext: str):
        self.pipe_name = r'\\.\pipe\PythonInterFace-' + pipe_name_ext
        self.pipe = None

    def start_connection(self):
        self.pipe = NamedPipeClient(self.pipe_name)
        if not self.pipe.connect():
            print("[PI] Could not connect to the pipe.")
            sys.exit(1)

    def read(self):
        state = self.pipe.read()
        game_state = deserialize_gamestate(state)
        return game_state

    def send(self, controller):
        serialized = serialize_data(controller.f(), controller.b())
        self.pipe.write(serialized)

    def close(self):
        self.pipe.close()
