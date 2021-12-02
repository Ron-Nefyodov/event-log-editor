# event-log-editor
This project contitans severl parts:

1.python script that chech the crc32 and update here

2.format xmls from evtx

record size = locate(\*\*) to next locat(\*\*)

chunk header records checksum = crc32(first_in_chunk(\*\*) to second(last_in_chunk(\*\*)+ 4 bytes))

chunk header checksum = crc32(locate(ElfChnk) to locate(ElfChnk + 120) +  locate(ElfChnk + 128) to locate(ElfChnk + 512)

file header checksum = crc32(locate(ElfFile) to locate(ElfFile+120))

