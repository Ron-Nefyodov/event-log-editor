# event-log-editor
This project contitans severl parts:

1.python script that check the crc32 and update here like this:

record size = locate(\*\*) to next locat(\*\*)

chunk header records checksum = crc32(first_in_chunk(\*\*) to second(last_in_chunk(\*\*)+ 4 bytes))

chunk header checksum = crc32(locate(ElfChnk) to locate(ElfChnk + 120) +  locate(ElfChnk + 128) to locate(ElfChnk + 512)

file header checksum = crc32(locate(ElfFile) to locate(ElfFile+120))

2.format xmls from evtx


![image](https://user-images.githubusercontent.com/48227040/149730000-bc3b1ef7-9332-4716-81da-0ac5f0f0f6b9.png)
![image](https://user-images.githubusercontent.com/48227040/149730085-24a9ea43-a16a-4faa-9935-752ea79dcc12.png)
![image](https://user-images.githubusercontent.com/48227040/149730112-3a41697a-ee86-420c-bf5d-5b51a86c2892.png)


thanks to svch0st for thew images 
