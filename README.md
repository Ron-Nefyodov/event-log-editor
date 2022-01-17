# event-log-editor

This project contains severl parts:

1.python script that check evtx and update

2.format xmls from evtx,edit the xml and put it back 

# EVTX
Log file created by the Windows 7 Event Viewer; contains a list of events recorded by Windows; saved in a proprietary binary format that can only be viewed within the Event Viewer program
![image](https://user-images.githubusercontent.com/48227040/149736678-e077667d-cc11-4bf2-944b-b03e164f7974.png)

![image](https://user-images.githubusercontent.com/48227040/149730000-bc3b1ef7-9332-4716-81da-0ac5f0f0f6b9.png)

TODO:In file header i need to recaculte the first chunk number and last chunk number

TODO:next record identifier

TODO:num of chunks

TODO:recalc chunksum
![image](https://user-images.githubusercontent.com/48227040/149730085-24a9ea43-a16a-4faa-9935-752ea79dcc12.png)

TODO:first event record number

TODO:last event record number

TODO:first record id

TODO:last record id

done:last event record data offset

done:free sapace offset

done:event records checksum

done:chunk heser checksum
![image](https://user-images.githubusercontent.com/48227040/149730112-3a41697a-ee86-420c-bf5d-5b51a86c2892.png)

done:recaculte size and put in to both places

done:format binary xml to xml file

done:pad chunks after puting records back in 

TODO:format xml to binary xml and put it back to place
 
TODO:xml editor

thanks to svch0st for thew images 
