import bpy
import struct
import zlib
from io import BytesIO

class RenderResult:
    def __init__(self, request_id, pixels):
        self.request_id = request_id
        self.pixels = pixels

    @classmethod
    def from_dict(cls, data):
        request_id = data["request_id"]
        width, height, channels, raw_data = decode_png(data["image"])
        if channels == 3:
            rgba_data = bytearray()
            for i in range(0, len(raw_data), 3):
                rgba_data.extend(raw_data[i:i+3])
                rgba_data.append(255)
            raw_data = rgba_data
            channels = 4
        # Convert raw_data (bytearray) into a list of lists, each inner list representing one RGBA pixel.
        pixels = []
        for i in range(0, len(raw_data), 4):
            pixels.append([float(raw_data[i+j]) / 255.0 for j in range(4)])
        return cls(request_id, pixels)

def decode_png(png_bytes):
    byte_stream = BytesIO(png_bytes)
    if byte_stream.read(8) != b'\x89PNG\r\n\x1a\n':
        raise ValueError("Invalid PNG file.")

    chunks = []
    width = height = bit_depth = color_type = None
    while True:
        length_data = byte_stream.read(4)
        if not length_data:
            break
        length = struct.unpack(">I", length_data)[0]
        chunk_type = byte_stream.read(4)
        chunk_data = byte_stream.read(length)
        byte_stream.read(4)  # Skip CRC.
        if chunk_type == b'IHDR':
            width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk_data[:10])
        elif chunk_type == b'IDAT':
            chunks.append(chunk_data)
        elif chunk_type == b'IEND':
            break

    if width is None or height is None:
        raise ValueError("Invalid PNG file: Missing IHDR chunk.")
    if bit_depth != 8:
        raise ValueError("Unsupported bit depth: {}".format(bit_depth))
    if color_type == 2:
        channels = 3
    elif color_type == 6:
        channels = 4
    else:
        raise ValueError("Unsupported color type: {}".format(color_type))

    decompressed = zlib.decompress(b''.join(chunks))
    stride = width * channels
    expected_size = (stride + 1) * height
    if len(decompressed) < expected_size:
        raise ValueError("Decompressed data is smaller than expected: {} < {}".format(len(decompressed), expected_size))

    raw_data = bytearray()
    prev_scanline = bytearray(stride)
    offset = 0

    for y in range(height):
        if offset >= len(decompressed):
            raise ValueError("Scanline out of range: {} >= {}".format(offset, len(decompressed)))
        filter_type = decompressed[offset]
        scanline = decompressed[offset + 1:offset + 1 + stride]
        offset += stride + 1

        filtered = bytearray(stride)
        if filter_type == 0:  # None.
            filtered[:] = scanline
        elif filter_type == 1:  # Sub.
            for i in range(stride):
                left = filtered[i - channels] if i >= channels else 0
                filtered[i] = (scanline[i] + left) & 0xFF
        elif filter_type == 2:  # Up.
            for i in range(stride):
                filtered[i] = (scanline[i] + prev_scanline[i]) & 0xFF
        elif filter_type == 3:  # Average.
            for i in range(stride):
                left = filtered[i - channels] if i >= channels else 0
                up = prev_scanline[i]
                filtered[i] = (scanline[i] + ((left + up) >> 1)) & 0xFF
        elif filter_type == 4:  # Paeth.
            for i in range(stride):
                left = filtered[i - channels] if i >= channels else 0
                up = prev_scanline[i]
                up_left = prev_scanline[i - channels] if i >= channels else 0
                filtered[i] = (scanline[i] + paeth_predictor(left, up, up_left)) & 0xFF
        else:
            raise ValueError("Unsupported PNG filter type: {}".format(filter_type))
        
        raw_data.extend(filtered)
        prev_scanline[:] = filtered

    return width, height, channels, raw_data

def paeth_predictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c
