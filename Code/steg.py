import subprocess #let python to use processes on comp (aka the steg tools)
import os #lets python do stuff like navigating files
from pathlib import Path #just taking Path not whole library so locations aren't just random strings to python
import sys #won't run w/o this to pair with last line calling main

class stegTools:
    #constructor (hopefully)
    #while searching found __init__ cool bit of python code known as a reserved keyword for the python version of
    #a constructor! Very cool -> self note: remember this
    def __init__(user, postDecryptionPath, dataPath):
        user.outDecDirP = Path(postDecryptionPath) #path defined where file output stored (aka extracted hidden img/text)
        user.dataP = Path(dataPath) #path defined where collected data (aka the report) stored
        user.outDecDirP.mkdir(exist_ok=True) #only creates the output folder if it doesn't already exist
    
    #help with formating
    def dataHelper(user, tool, img, hidden, contained):
        hadHidden = "Y" if hidden else "N"
        with open(user.dataP, "a") as fptr:
            #little f before "" is also cool python code to pair with the {} so its handled as code not words
            fptr.write(f"{tool:<15} | {img:<30} | {hadHidden:<10} | {contained}\n") #keep rows neat

def main():

    #could not get windows terminal find path on its own, so had to hard code it
    exifExePath = "C:/Users/Void/Desktop/CS426_Project/Steganography-Tools/Extract/Exiftool/exiftool.exe.exe"
    openExePath = "C:/Users/Void/Desktop/CS426_Project/Steganography-Tools/Extract/OpenStego/openstego.bat"

    print("Siri Siqveland CS426\n")
    print("Automated Steg Tool for Final Project\n")
    print("Works with Exiftool, OpenStego, and zsteg")

    #initialize variables
    inEncDirName = "./All-EncData" #where the input-ed Enc images are stored
    dataCollected = "reportData.txt" # name of report
    outDecDirName = "./All-DecData" #where output-ed Dec images stored

    EncDir = Path(inEncDirName) #path to the encryption directory aka where all the potentially encrypted files are stored

    allDataAvail = list(EncDir.glob("*")) #list of all files in directory, in case userImg > available files
    numImgUser = int(input("How many images will be used?")) #get user input and assign to number of images used

    #check to ensure user value is valid
    if numImgUser > len(allDataAvail) or numImgUser <= 0:
        print("Requested invalid value available in the folder")
        numImgUser = int(input("How many images will be used?"))

    user = stegTools(outDecDirName, dataCollected)

    allEncDataUsing = [] #hold all the encrypted data to be tested
    i = 0 #track current file
    #while-loop to get all the files in the folder ready to be fed into the steg tools
    while i < numImgUser:
        allEncDataUsing.append(allDataAvail[i])
        i +=1


    #set up the report
    with open(user.dataP, "w") as fptr:
        fptr.write("Steganography Report CS426\n")
        fptr.write("Siri Siqveland -- Final Project\n")
        fptr.write("Post-Steganography Collected Data in Table Below:\n")
        fptr.write(f"{'Steg Tool':<15} |{'Input Img Name':<30}| {'Contained file?':<10} | Hidden File Name \n")
        fptr.write("_____________________________________________________________________\n")
        
    #handle each of the 2 tools below,  update report after each img iteration in each tool use:

    #Exiftool
    print("Using ExifTool...\n")
    for curImg in allEncDataUsing: #for the current image, run cmd in terminal and update report

        #intialize as if nothing found
        hidden = False #was anything necrypted
        decName = "N/A" #name of decrypted file
           
        ogFile = set(os.listdir(user.outDecDirP)) #track how many files in Dec folder
        #new cmd to check for binary with exif (aka hidden images)
        #looked up most common places hidden data stored and used tags to specify search in cmd line
        #-b is binary so it just looks at the binary not txt, -u in unknown so look at unknown tags, -W is write the output, and -TrailerData is location so exif looks at the area around EoF
        exifBinCmd = [exifExePath, "-b", "-u","-W", f"{user.outDecDirP}/%f_E-Dec.%s", "-TrailerData", str(curImg)]
        subprocess.run(exifBinCmd, capture_output=True) #run cmd, hidden data saved to output directory aka outDecDirP
            
        #look at all files in cur Img to check if stuff is really hidden w/ a size check
        checkDecFile = set(os.listdir(user.outDecDirP)) - ogFile #check if post dec dir has = or > files than og to determine if anything was extracted
        for fTempName in checkDecFile: #as loops, temp name is the current file looking at in checkDecFile
            decPath = user.outDecDirP / fTempName
            if os.path.getsize(decPath) > 2048: 
                hidden = True #hidden data likely if file is larger than 2048 and stuff got captured
                decName = fTempName #temp name moved to decName to be held onto bc it found something
                break #something found, loop no longer needed
            else:
                os.remove(decPath) #removes file if less than 2048b, likely not important aka sorts out what's prob meta not hidden
    
        #if failed w/ physical files tacked on then move to metadata
        if hidden == False:
            #switched from list to string bc of playing w/ debugging
            #-s3 makes easier to read for python, -Comment -UserComment - Description are all common tags to hide data
            exifTxtCmd = f'"{exifExePath}" -s3 -Comment -UserComment -Description "{str(curImg)}"' #build cmd
            txtResult = subprocess.run(exifTxtCmd, capture_output=True, text=True) #run the cmd capture the output, have it as text
            text = txtResult.stdout.strip() #remove whitespace that may trigger more false positives

            #if text exists and it's not short
            if text and len(text) > 5: #5 chosen randomly ti ensure msg > 10 chars and avoid false positives
                decName = f"{curImg.stem}_E-Dec.txt" #set decName to whatever curImg is since data found
                with open(user.outDecDirP / decName, "w") as fptr: #save data as text to decName
                    fptr.write(text)
                hidden = True  
        user.dataHelper("Exiftool", curImg.name, hidden, decName) #add it to the report

    print("Using ExifTool...done\n")


    #OpenStego - no _Dec.filetype listed as OpenStego gives the enc files name
    print("Using OpenStego..,\n")
    for curImg in allEncDataUsing:
        #Only functions for no-password openstego imgs, as no enc data was initially openstego it doesn't detect anythinggg sajd, should have checked before
        #so much debugging and for nothing to show here sad sad 
        # extract -a = algorithm RandomLSB (the algorithm) -sf is soruce file (curImg) -xd is extract directory (outDecDirP)
        cmdLineTxt = [openExePath, "extract", "-a", "RandomLSB", "-sf", str(curImg), "-xd", str(user.outDecDirP)]

        #try-except added bc it kept stalling in an infinite wait ;-;
        try:
            #see files in folder pre-running code to compare w/ after to see if anything found
            ogFile = set(os.listdir(user.outDecDirP))
            #if something goes wrong, times out after 15 seconds to avoid forever stuck
            #input = \n in case subprocess wants the password to ensure it doesn't get stuck again
            openResult = subprocess.run(cmdLineTxt, input="\n", capture_output=True, text=True, timeout=15) #timeout not working well so implement try-except instead
            returnCode = openResult.returnCode #check if code returned 0 is yes 1 is
        except:
            returnCode = 1 #mark an error -> took too long aka no code returned

        #see if new files added bc OpenStego saves output after cmd line run
        checkDecFiles = set(os.listdir(user.outDecDirP)) - ogFile

        #check if code was returned and there's a new file int he folder (aka decrypted smth) and nothing went wrong (aka 0 is success, 1 is errror)
        if returnCode == 0 and checkDecFiles:
            #get file name from newest file in dec folder
            decName = list(checkDecFiles)[0]
            #update results by throwing data found in
            user.dataHelper("OpenStego", curImg.name, True, decName)
        else: #nothing found to decyrpt
            user.dataHelper("OpenStego", curImg.name, False, "N/A")

    print("Using OpenStego...done\n")

    #zsteg
    print("Using zsteg...\n")
    print("Note: only work with .png and .bmp input so .jpg/.jpeg will be skipped\n")
    for curImg in allEncDataUsing:
        #if ".png" not in curImg or ".bmp" not in curImg:
        if curImg.suffix.lower() not in ['.png', '.bmp']:
            user.dataHelper("zsteg", curImg.name, False, "Skipped")
            continue
        
        #set up assume nothing found
        hidden = False
        decName = "N/A"
        #call zsteg then -a for all to search all the img aka like everything in it channels, pixels, metadata, etc.
        zCmdTxt = ["zsteg", "-a", str(curImg)]
        #grab text from metadata, turn it into text, and run in cmd shell (not that it helped w/ exif or open, but it does with zsteg)
        zResult = subprocess.run(zCmdTxt, capture_output=True, text=True, shell=True)

        zText = zResult.stdout.lower() #lower case to make searching words easier bc had trouble w/ accuracy when this not added
        #if got a result, and not original aka the og img desc and longer than 20 to avoid false pos again
        if zText and "original" not in zText and len(zText) > 20: 
            decName = f"{curImg.stem}_Z-Dec.txt" #sets the decName to the name of the first part of curImg before .something and renames to mark for decryption
            with open(user.outDecDirP / decName, "w") as fptr: #opens the img path in the output directory to write
                fptr.write(zText) #write the found txt in the file to (hopefully) get reconstructed
            hidden = True #some data was found hidden, yay 

        #work to get the binary data
        if hidden == False: #if nothing found as txt
            #call zsteg again but to extract coordinate data aka b1 of rgb data, lest sign bit, and read from x to y
            extZCmd = f'zsteg -E b1,rgb,lsb,xy {str(curImg)}'

            tmpDecName = f"{curImg.stem}_Z-Dec.bin" #binary data so saved as .bin renamed after cur img
            tmpPath = user.outDecDirP / tmpDecName #temp path set to the name in case data actually steg-worthy
            with open(tmpPath, "wb") as fptr: #wb to write in binary at the location
                subprocess.run(extZCmd, stdout=fptr, shell=True) #subprocess when run outputs into tmpPath location
            if os.path.exists(tmpPath): #if a path actually exists, so no more issues getting here (hopefully)
                if os.path.getsize(tmpPath) > 60: #random value chose to try and ensure no more false data
                    hidden = True #set hidden to true and save the steg data
                    decName = tmpDecName
                else:
                    os.remove(tmpPath) #remove the path if not actually steg, no clutter
        user.dataHelper("zsteg", curImg.name, hidden, decName)    #throw into the records
    print("Using zsteg... done\n")

    #let user know where all the data stored
    print(f"Finished {numImgUser} for each tool and {dataCollected} generated. Hidden files found saved to {outDecDirName}")

#code would not run w/o this call bc python doesn't have a pre-built main ig
if __name__ == "__main__":
    sys.exit(main())
    