# This is a sample Python script.
import binascii
import struct


def rewrite_size_record(evtx):
    with open(evtx, 'r+b') as f:
        size = b''
        four_bytes = f.read(4)
        while four_bytes:
            four_bytes = f.read(4)
            if four_bytes == b'\x45\x6c\x66\x43':
                four_bytes = f.read(4)
                if four_bytes == b'\x68\x6e\x6b\x00':
                    f.seek(24,1)
                    last_record_id = f.read(8)
                    f.seek(-32,1)
                f.seek(-4,1)
            if four_bytes == b'\x2a\x2a\x00\x00':
                offset_first_size = f.tell() - 4
                size = f.read(4)
                record_id = f.read(8)
            if four_bytes == size:
                if f.read(4) == b'\x2a\x2a\x00\x00':
                    f.seek(-4, 1)
                    offset_second_size = f.tell()
                    new_size = struct.pack('<L', (offset_second_size - offset_first_size))
                    f.seek(offset_first_size + 4)
                    f.write(new_size)
                    f.seek(offset_second_size - 4)
                    f.write(new_size)
                else:
                    f.seek(-4, 1)
                    if(last_record_id == record_id):
                        offset_second_size = f.tell()
                        new_size = struct.pack('<L', (offset_second_size - offset_first_size))
                        f.seek(offset_second_size - 4)
                        f.write(new_size)

        f.close()


def rewrite_records_checksum(evtx_file):
    with open(evtx_file, 'r+b') as f:
        crc32 = b''
        all_records = b''
        offset_first_record = 0
        offset_last_record = 0
        offset_checksum = 0
        four_bytes = f.read(4)
        while four_bytes:
            four_bytes = f.read(4)
            if four_bytes == b'\x45\x6c\x66\x46':
                four_bytes = f.read(4)
                if four_bytes == b'\x69\x6c\x65\x00':
                    offset_start_chunk = f.tell()-8
                    offset_checksum = f.tell() + 44
                    f.seek(36, 1)
                    offset_last_record = (struct.unpack('<L', f.read(4)))[0]+offset_start_chunk
                    f.seek(-40, 1)
                f.seek(- 4, 1)
            if four_bytes == b'\x2a\x2a\x00\x00' and offset_last_record != 0 and offset_checksum != 0:
                # check if it is the first time
                if offset_first_record == 0:
                    offset_first_record = f.tell() - 4
                    f.seek(offset_last_record)
                    print(f.read(4))
                    size = struct.unpack('<L', f.read(4))
                    f.seek(size[0]-8, 1)
                    offset_end_record = f.tell()
                    print(offset_last_record)
                    print(offset_end_record)
                    print(offset_first_record)
                    f.seek((offset_first_record - offset_end_record), 1)
                    all_records = f.read(offset_end_record - offset_first_record)
                    crc32 = struct.pack('<L', binascii.crc32(all_records) % (1 << 32))
                    f.seek(offset_checksum)
                    f.write(crc32)
                    f.seek(offset_end_record)
                    offset_first_record = 0
                    offset_checksum = 0
                    offset_last_record = 0
        f.close()


def rewrite_chunk_header_checksum(evtx):
    with open(evtx, 'r+b') as f:
        crc32 = b''
        all_header = b''
        four_bytes = f.read(4)
        while four_bytes:
            four_bytes = f.read(4)
            if four_bytes == b'\x45\x6c\x66\x43':
                four_bytes = f.read(4)
                if four_bytes == b'\x68\x6e\x6b\x00':
                    offset_checksum = f.tell() + 116
                    f.seek(- 8, 1)
                    all_header = f.read(120)
                    f.seek(8, 1)
                    all_header += f.read(384)
                    crc32 = struct.pack('<L', binascii.crc32(all_header) % (1 << 32))
                    f.seek(offset_checksum)
                    f.write(crc32)
                    f.seek(384, 1)
                else:
                    f.seek(- 4, 1)
        f.close()

def rewrite_last_record_offset(evtx):
    with open(evtx, 'r+b') as f:
        size = b''
        four_bytes = f.read(4)
        while four_bytes:
            four_bytes = f.read(4)
            if four_bytes == b'\x45\x6c\x66\x43':
                four_bytes = f.read(4)
                if four_bytes == b'\x68\x6e\x6b\x00':
                    f.seek(-8,1)
                    offset_start_chunk = f.tell()
                    f.seek(44,1)
                    offset_of_offset_last_event_record = f.tell()
            if four_bytes == b'\x2a\x2a\x00\x00':
                size = struct.unpack('<L', f.read(4))
                f.seek(size[0] - 8, 1)
                if f.read(4) != b'\x2a\x2a\x00\x00':
                    f.seek(-4, 1)
                    current_pos = f.tell()
                    f.seek(-size[0], 1)
                    offset_last_record = f.tell()
                    f.seek(offset_of_offset_last_event_record)
                    f.write(struct.pack('<L',(offset_last_record-offset_start_chunk)))
                    f.seek(current_pos)




# def rewrite_first_record_number_and_identifier(evtx):
# def rewrite_last_record_number_and_identifier(evtx):
# def rewrite_first_chunk(evtx):
# def rewrite_last_chunk(evtx):
# def rewrite_number_chunks(evtx):
# def rewrite_file_header_checksum(evtx):
# def rewrite_next_record_identifier(evtx):
# def rewrite_number_of_chunks(evtx):

if __name__ == '__main__':
    rewrite_size_record("C:\\Users\\Desktop\\security.evtx")
    rewrite_last_record_offset("C:\\Users\\Desktop\\security.evtx")
    rewrite_records_checksum("C:\\Users\\Desktop\\security.evtx")
    rewrite_chunk_header_checksum("C:\\Users\\Desktop\\security.evtx")
