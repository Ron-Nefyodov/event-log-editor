# This is a sample Python script.
import binascii
import struct

Signature_record = b'\x2a\x2a\x00\x00'
Signature_chunk_first_4byte = b'\x45\x6c\x66\x43'
Signature_chunk_last_4byte = b'\x68\x6e\x6b\x00'
position_start_of_chunk = -8
position_last_event_record_id = 32
position_event_records_checksum = 52
position_next_record_offset = 48
position_last_record_offset = 44
size_chunk = 65535


def rewrite_size_record(evtx):
    # read and write evtx file
    with open(evtx, 'r+b') as evtx_file:
        size = b''
        four_bytes = evtx_file.read(4)
        while four_bytes:
            four_bytes = evtx_file.read(4)
            if four_bytes == Signature_chunk_first_4byte:
                four_bytes = evtx_file.read(4)
                if four_bytes == Signature_chunk_last_4byte:
                    evtx_file.seek(position_start_of_chunk, 1)
                    evtx_file.seek(position_last_event_record_id, 1)
                    last_record_id = evtx_file.read(8)
                else:
                    evtx_file.seek(-4, 1)
            elif four_bytes == Signature_record:
                offset_start_records = evtx_file.tell() - 4
                size = evtx_file.read(4)
                record_id = evtx_file.read(8)
            elif four_bytes == size:
                if evtx_file.read(4) == Signature_record:
                    evtx_file.seek(-4, 1)
                    offset_end_records = evtx_file.tell()
                    new_size = struct.pack('<L', (offset_end_records - offset_start_records))
                    evtx_file.seek(offset_start_records + 4)
                    evtx_file.write(new_size)
                    evtx_file.seek(offset_end_records - 4)
                    evtx_file.write(new_size)
                else:
                    evtx_file.seek(-4, 1)
                    if last_record_id == record_id:
                        offset_end_records = evtx_file.tell()
                        new_size = struct.pack('<L', (offset_end_records - offset_start_records))
                        evtx_file.seek(offset_start_records + 4)
                        evtx_file.write(new_size)
                        evtx_file.seek(offset_end_records - 4)
                        evtx_file.write(new_size)
    evtx_file.close()


def rewrite_records_checksum(evtx_file):
    with open(evtx_file, 'r+b') as evtx_file:
        crc32 = b''
        all_records = b''
        offset_first_record = 0
        offset_last_record = 0
        offset_checksum = 0
        four_bytes = evtx_file.read(4)
        while four_bytes:
            four_bytes = evtx_file.read(4)
            if four_bytes == Signature_chunk_first_4byte:
                four_bytes = evtx_file.read(4)
                if four_bytes == Signature_chunk_last_4byte:
                    evtx_file.seek(position_start_of_chunk, 1)
                    offset_start_chunk = evtx_file.tell()
                    offset_checksum = evtx_file.tell() + position_event_records_checksum
                    evtx_file.seek(44, 1)
                    offset_last_record = (struct.unpack('<L', evtx_file.read(4)))[0] + offset_start_chunk
                evtx_file.seek(- 4, 1)

            # check if it is the start of record
            if four_bytes == Signature_record and offset_last_record != 0 and offset_checksum != 0:

                # check if it is the first record in chunk
                if offset_first_record == 0:
                    offset_first_record = evtx_file.tell() - 4
                    evtx_file.seek(offset_last_record + 4)
                    size = struct.unpack('<L', evtx_file.read(4))
                    evtx_file.seek(size[0] - 8, 1)
                    offset_end_record = evtx_file.tell()
                    evtx_file.seek((offset_first_record - offset_end_record), 1)
                    all_records = evtx_file.read(offset_end_record - offset_first_record)
                    crc32 = struct.pack('<L', binascii.crc32(all_records) % (1 << 32))
                    evtx_file.seek(offset_checksum)
                    evtx_file.write(crc32)
                    evtx_file.seek(offset_end_record)
                    offset_first_record = 0
                    offset_checksum = 0
                    offset_last_record = 0
    evtx_file.close()


def rewrite_chunk_header_checksum(evtx):
    with open(evtx, 'r+b') as evtx_file:
        crc32 = b''
        all_header = b''
        four_bytes = evtx_file.read(4)
        while four_bytes:
            four_bytes = evtx_file.read(4)
            if four_bytes == Signature_chunk_first_4byte:
                four_bytes = evtx_file.read(4)
                if four_bytes == Signature_chunk_last_4byte:
                    offset_checksum = evtx_file.tell() + 116
                    evtx_file.seek(position_start_of_chunk, 1)
                    all_header = evtx_file.read(120)
                    evtx_file.seek(8, 1)
                    all_header += evtx_file.read(384)
                    crc32 = struct.pack('<L', binascii.crc32(all_header) % (1 << 32))
                    evtx_file.seek(offset_checksum)
                    evtx_file.write(crc32)
                    evtx_file.seek(384, 1)
                else:
                    evtx_file.seek(- 4, 1)
    evtx_file.close()


def rewrite_last_record_offset(evtx):
    with open(evtx, 'r+b') as evtx_file:
        size = b''
        four_bytes = evtx_file.read(4)
        while four_bytes:
            four_bytes = evtx_file.read(4)
            if four_bytes == Signature_chunk_first_4byte:
                four_bytes = evtx_file.read(4)
                if four_bytes == Signature_chunk_last_4byte:
                    evtx_file.seek(position_start_of_chunk, 1)
                    offset_start_chunk = evtx_file.tell()
                    evtx_file.seek(position_last_record_offset, 1)
                    offset_of_offset_last_event_record = evtx_file.tell()
            if four_bytes == Signature_record:
                size = struct.unpack('<L', evtx_file.read(4))
                evtx_file.seek(size[0] - 8, 1)
                if evtx_file.read(4) != Signature_record:
                    evtx_file.seek(-4, 1)
                    current_pos = evtx_file.tell()
                    evtx_file.seek(-size[0], 1)
                    offset_last_record = evtx_file.tell()
                    evtx_file.seek(offset_of_offset_last_event_record)
                    evtx_file.write(struct.pack('<L', (offset_last_record - offset_start_chunk)))
                    evtx_file.seek(current_pos)
    evtx_file.close()


def rewrite_next_record_offset(evtx):
    with open(evtx, 'r+b') as evtx_file:
        size = b''
        four_bytes = evtx_file.read(4)
        while four_bytes:
            four_bytes = evtx_file.read(4)
            if four_bytes == Signature_chunk_first_4byte:
                four_bytes = evtx_file.read(4)
                if four_bytes == Signature_chunk_last_4byte:
                    evtx_file.seek(position_start_of_chunk, 1)
                    offset_start_chunk = evtx_file.tell()
                    evtx_file.seek(position_next_record_offset, 1)
                    offset_of_offset_next_event_record = evtx_file.tell()
            if four_bytes == Signature_record:
                size = struct.unpack('<L', evtx_file.read(4))
                evtx_file.seek(size[0] - 8, 1)
                if evtx_file.read(4) != Signature_record:
                    evtx_file.seek(-4, 1)
                    offset_next_event_record = evtx_file.tell()
                    evtx_file.seek(offset_of_offset_next_event_record)
                    evtx_file.write(struct.pack('<L', (offset_next_event_record - offset_start_chunk)))
                    evtx_file.seek(offset_next_event_record)
    evtx_file.close()


def append_to_pos_in_file(evtx, pos, data):
    with open(evtx, 'r+b') as evtx_file:
        evtx_file.seek(pos)
        end_file = evtx_file.read()
        evtx_file.seek(pos)
        evtx_file.write(data)
        evtx_file.write(end_file)
    evtx_file.close()


def pad_chunk(evtx):
    # work in proccess
    with open(evtx, 'r+b') as evtx_file:
        size = b''
        four_bytes = evtx_file.read(4)
        while four_bytes:
            four_bytes = evtx_file.read(4)
            if four_bytes == Signature_chunk_first_4byte:
                four_bytes = evtx_file.read(4)
                if four_bytes == Signature_chunk_last_4byte:
                    evtx_file.seek(position_start_of_chunk, 1)
                    offset_start_chunk = evtx_file.tell()
                    evtx_file.seek(position_next_record_offset, 1)
                    offset_next_record = (struct.unpack('<L', evtx_file.read(4)))[0] + offset_start_chunk
                    evtx_file.seek(offset_next_record)
                    while evtx_file.tell() - offset_start_chunk < size_chunk:
                        four_bytes = evtx_file.read(4)
                        evtx_file.seek(-4, 1)
                        if four_bytes == Signature_chunk_first_4byte:
                            four_bytes = evtx_file.read(4)
                            if four_bytes == Signature_chunk_last_4byte:
                                evtx_file.seek(position_start_of_chunk, 1)
                                append_to_pos_in_file(evtx, evtx_file.tell(), b'\x00')
                                evtx_file.seek(1, 1)

    evtx_file.close()


def create_xml_file(evtx):
    xml_data = b''
    with open(evtx, 'r+b') as evtx_file:
        four_bytes = evtx_file.read(4)
        while four_bytes:
            four_bytes = evtx_file.read(4)
            # check if it is the start of record
            if four_bytes == Signature_record:
                size_record = (struct.unpack('<L', evtx_file.read(4)))[0]
                evtx_file.seek(16, 1)
                xml_data +=  evtx_file.read(size_record - 28)
    with open("C:\\Users\\U227835\\Desktop\\xml.xml", "w+b") as xml:
        xml.write(xml_data)


# def load_xml_file_to_evtx(xml,evtx):
# def rewrite_first_record_number_and_identifier(evtx):
# def rewrite_last_record_number_and_identifier(evtx):
# def rewrite_first_chunk(evtx):
# def rewrite_last_chunk(evtx):
# def rewrite_number_chunks(evtx):
# def rewrite_file_header_checksum(evtx):
# def rewrite_next_record_identifier(evtx):
# def rewrite_number_of_chunks(evtx):

if __name__ == '__main__':
    create_xml_file("C:\\Users\\U227835\\Desktop\\security.evtx")
    # rewrite_size_record("C:\\Users\\U227835\\Desktop\\security.evtx")
    # rewrite_last_record_offset("C:\\Users\\U227835\\Desktop\\security.evtx")
    # rewrite_next_record_offset("C:\\Users\\U227835\\Desktop\\security.evtx")
    # pad_chunk("C:\\Users\\U227835\\Desktop\\security.evtx")
    # rewrite_records_checksum("C:\\Users\\U227835\\Desktop\\security.evtx")
    # rewrite_chunk_header_checksum("C:\\Users\\U227835\\Desktop\\security.evtx")
