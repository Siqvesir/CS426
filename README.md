# CS426
Final Project Info for CS426

Project Recreation Guide (plus notes):

IMPORTANT DOWNLOAD AND STEPS TO TAKE BEFORE RUNNING THE CODE: 

In order to recreate the project the User must have ExifTool, OpenStego, and zsteg (which require Ruby to also be downloaded on the system to run properly)
as stegonagraphy tools to be functional. Additionally, the code requires the paths for ExifTool and OpenStego to be added to variables labled within the code
due to issues getting Windows to recognize them despite the use of shell=True and adding their paths to the PATH directory.

PFolders All-EncData, All-DecData, and the reportData.txt (the latter most of which does not need to be created initially) all need to be added to the same folder the code is stored.
The names of folders must match the above exactly!!!!!

PROJECT RECREATION STEPS
Note: Basic parameters from Encryption Steg tools were used - ie. no passwords and no changing defaults.
Exception: SilentEye had to output BMP files to work with file sizes

Encryption:
1) Keep the Images in Clean without any Steganography
2) Embed the Images with Img in the SilentEye (downloaded stego tool) folder with the Emb files using SilentEye. The corresponding files used in the test can be found in CS426_ProjectNotes.
3) Repeat Step 2 using the Stego folder (Stego is a browser-based stego tool)
4) Repeat Step 2 using the StegoCrypt folder (StegoCrypt is a browser-based stego tool)
5) Put All Encrypted files in a folder called All-EncData 

Decryption:
1) Create a Folder to store steg.py, All-EncData, and All-DecData in (it must be the same folder)
2) Run steg.py
3) Input the number of images to run through (60 images if following the same experiment)
4) steg.py will output data extracted from images in All-EncData into All-DecData (these will not be the images input unless they were OpenStego,
they will be .bin for zsteg, or .txt for ExifTool)
5) reportData.txt will also be generated and viewable with information on each of the files iterated through from what tool Decrypted them to the result (skipped or Y/N on hidden files found).
This data will be stored in a table

Other:
Currently in the repository All-DecData and the reportData.txt hold information from my own running of the code
This data is what is used in the Report folder for the Excel analysis of the code, the Slides, and the video.
