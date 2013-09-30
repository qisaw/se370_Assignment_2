'''
Created on 27/08/2013

This is where you do your work.
Not only do you need to fill in the methods but you can also add any other classes, 
methods or functions to this file to make your system pass all of the tests.

@author: wkas533
'''

from drive import Drive
import collections
import math 


class A2File(object):
    '''
    One of these gets returned from Volume open.
    '''
    
    def __init__(self, fileName, usedDrives,drive):
        self.name = fileName
        self.data = b''
        self.usedDrives = usedDrives
        self.locationsOfData = collections.OrderedDict()
        self.drive = drive
        #look for the first unused Directory and set it as root
        self.rootDir = -1
        for i in range(len(self.usedDrives)):
            if self.usedDrives[i]==False:
                self.rootDir = i
                self.usedDrives[i] = True
                break 
        self.createDirectory()
        
        '''
        Initializes an A2File object.
        Not called from the test file but you should call this from the
        Volume.open method.
        You can use as many parameters as you need.
        '''


    def getMetaData(self):
        metaData = self.name + b'\n'+ str(len(self.data)).encode()+b'\n'+str(self.rootDir).encode()+b'\n'
        return metaData

    
    def createDirectory(self):
        #to create the directory, we must overrite the root directory
        #to get the values of the directories used, we only need the self.locations of data-
        usedForData = []
        for key in self.locationsOfData.keys():
            if not key == self.rootDir:
                usedForData.append(key)
        #clear whatever is in the root directory atm
        #then rewrite
        self.locationsOfData[self.rootDir]= b''
        for i in range(len(usedForData)):
            self.locationsOfData[self.rootDir]+= str(usedForData[i]).encode()+b'\n'
            #print("there is data at :"+ str(usedForData[i]))
        i=0
        numberOfSpaces = Drive.BLK_SIZE-len(self.locationsOfData[self.rootDir])%Drive.BLK_SIZE
        self.locationsOfData[self.rootDir] +=b' '*numberOfSpaces
            
        #print("file completed")
        #then rewirte all data
    
    def size(self):
        return len(self.data)
    
    def write(self, location, data):
        if(location>len(self.data)):
            self.data+=b' '*(location-len(self.data))
        self.data = self.data[:location]+data
        #allocate each of the data blocks to a piece of data
        keysToDelete=[]
        for key in self.locationsOfData.keys():
            if not (key==self.rootDir):
                self.usedDrives[key]= False
                keysToDelete.append(key)
                
        for key in keysToDelete:
            del(self.locationsOfData[key])
            
        #set these to false
        
        metaData = self.data
        #print (len(self.data))
        #print (self.data)
        numberOfSpaces = Drive.BLK_SIZE-len(metaData)%Drive.BLK_SIZE
        if numberOfSpaces == 64:
            numberOfSpaces = 0
        metaData +=b' '*numberOfSpaces
        
        #write the metadata
        i=0;
        while i < len(metaData)/Drive.BLK_SIZE:
            #find an emptyBlock
            emptyblknum = -1
            for j in range(len(self.usedDrives)):
                if self.usedDrives[j]==False:
                    emptyblknum = j
                    break
            #put it in that locationofData
            self.locationsOfData[emptyblknum] = metaData[i*Drive.BLK_SIZE:i*Drive.BLK_SIZE + Drive.BLK_SIZE]
            self.usedDrives[emptyblknum]=True
            i = i +1
            
        #allocate the spots
        
        #put the data into the appropriate length
        
        self.createDirectory()
        
        '''
        Writes data to a file at a specific byte location.
        If location is greater than the size of the file the file is extended
        to the location with spaces. 
        '''
    def read (self,location,amount):
        if(location<0)or(amount<0):
            raise IOError
        if (location>len(self.data))or(location+amount)>len(self.data):
            raise IOError
        
        return self.data[location:location+amount]
    
        '''
        Reads from a file at a specific byte location.
        An exception is thrown if any of the range from
        location to (location + amount - 1) is outside the range of the file.
        Areas within the range of the file return spaces if they have not been written to.
        '''

class Volume(object):
    '''
    A volume is the disk as it appears to the file system.
    The disk structure is to be entirely stored in ASCII so that it
    can be inspected easily. It must contain:
        Volume data blocks: the number of contiguous blocks with the volume data - as a string, ends with "\n"
        Name: at least one character plus "\n" for end of name)
        Size: as a string terminated with "\n"
        Free block bitmap: drive.num_blocks() + 1 bytes ("x" indicates used, "-" indicates free, ends with "\n")
        First block of root directory (called root_index) : as a string terminated with "\n" - always the last
            block on the drive.
    '''
    

    def __init__(self,drive,name,rootDir,usedDrives,numOfDataBlocks):
        self.drive = drive
        self.driveName = name
        self.rootDir = rootDir
        #initially all the drives are free
        self.usedDrives=usedDrives
        #number of data blocks used by the header
        self.numOfDataBlocks = numOfDataBlocks
        self.directory = Directory(self.usedDrives)
        #each of the datablocks are marked as used
        

    @staticmethod
    def format(drive, name):
        numOfBlocksForRootDir = int(math.ceil(drive.num_blocks()/Drive.BLK_SIZE))
        if (len(name)<1) or (len(name)>(drive.num_blocks()-numOfBlocksForRootDir)*Drive.BLK_SIZE):
            raise ValueError
        elif ("/" in name.decode()) or ("\n" in name.decode()):
            raise ValueError
        #there can only be drive.blk_size 0's in one block
        
        #initially all the drives are free
        usedDrives = [False]*drive.num_blocks()
        numOfDataBlocks = Volume.calculate_volume_data_blocks(name, drive, drive.num_blocks()-1 )
        for i in range(numOfDataBlocks):
            usedDrives[i]=True
        usedDrives[drive.num_blocks()-1]=True
        volume = Volume(drive,name,drive.num_blocks()-1,usedDrives,numOfDataBlocks)
        
        '''
        Creates a new volume in a disk.
        Puts the initial metadata on the disk.
        The name must be at least one byte long and not include "\n".
        Raises an IOError if after the allocation of the volume information
        there are not enough blocks to allocate the root directory and at least
        one block for a file.
        Returns the volume.
        '''
        return volume
    
    def name(self):
        '''
        Returns the volumes name.
        '''
        return self.driveName
    
    def volume_data_blocks(self):
        '''
        Returns the number of blocks at the beginning of the drive which are used to hold
        the volume information.
        '''
        '''
        to get the number of blocks used by the header we must:
        check the length of the information then
        divide by the Drive.blk_size
        and get the value given there
        round it up to the nearest whole number
        '''
        return self.numOfDataBlocks
    
    @staticmethod
    def calculate_volume_data_blocks(name,drive,rootDir):
        #length of the title
        titleLength = len(name) +1 #for the '/n'
        #length of bitmao is drive.numblocks +1
        bitmapLength = drive.num_blocks()+1
        #length of size
        sizeLength = len(str(drive.num_blocks()))+1
        #length of the root directory
        lenRoot = len(str(rootDir))+1
        #length of the volume data blocks, usually two but could be three
        ''' how am i going to get the size of the volume_data_blocks without actually calculating volume data blocks?
        esitmate how much it is and then add this to the volume data blocks, then check again.
        '''
        estimatedLength = (titleLength+bitmapLength+sizeLength + lenRoot)/Drive.BLK_SIZE
        estimatedLength = int(math.ceil(estimatedLength))
        lengthOfestimate = len(str(estimatedLength))+1
        finalLength = (titleLength+bitmapLength+sizeLength + lenRoot + lengthOfestimate)/Drive.BLK_SIZE
        return int(math.ceil(finalLength))
    
    def size(self):
        '''
        Returns the number of blocks in the underlying drive.
        '''
        return self.drive.num_blocks()
    
    def bitmap(self):
        '''
        Returns the volume block bitmap.
        '''
        bitmap = b''
        for i in range(len(self.usedDrives)):
            if self.usedDrives[i]==True:
                bitmap+=b'x'
            else:
                bitmap+=b'-'
        return bitmap
    
    def root_index(self):
        '''
        Returns the block number of the first block of the root directory.
        Always the last block on the drive.
        '''
        return self.rootDir
    
    @staticmethod
    def mount(drive_name):
        drive = Drive.reconnect(drive_name)
        allVolumeData = drive.read_block(0).decode()
        numOfBlocksUsed = allVolumeData.split('\n',1)[0]
        if int(numOfBlocksUsed)>1:
            for i in range(1,int(numOfBlocksUsed)):
                allVolumeData+=drive.read_block(i).decode() 
                
        data = allVolumeData.split('\n')
        numOfBlocksUsed=int(data[0])
        name = data[1]
        #dont need this
        numOfBlocksInDrive = int(data[2])
        bitmap = data[3]
        rootIndex = int(data[4])
        usedDrives=[False]*numOfBlocksInDrive
        Volume.calculate_volume_data_blocks(name, drive, rootIndex)
        numOfDataBlocks = Volume.calculate_volume_data_blocks(name, drive, rootIndex )
        for i in range(numOfDataBlocks):
            usedDrives[i]=True
        usedDrives[rootIndex]=True
        volume = Volume(drive, name.encode(), rootIndex, usedDrives, numOfBlocksUsed)
        #read the rootdirectory
        rootString = drive.read_block(rootIndex).decode()
        root= rootString.split('\n')
        for i in range(len(root)):
            if root[i].isdigit():
                if int(root[i])!=0:

                    fileData =  volume.drive.read_block(int(root[i])).decode().split('\n')
                    for i in range(0,len(fileData)-1,3):
                        fileName = fileData[i]
                        fileDataLength =  fileData[i+1]
                        fileStart = fileData[i + 2]
                        #then go into the fileStart
                        fileDirectory = volume.drive.read_block(int(fileStart))
                        fileDirectory = fileDirectory.decode().split('\n')
                        dataLocations = []
                        for j in range(len(fileDirectory)):
                            if fileDirectory[j].isdigit():
                                dataLocations.append(fileDirectory[j])
                        #now that we have all the locations of the data, we can read all the locations and concatinate them
                        dataOnFile = b''
                        for k in range(len(dataLocations)):
                            dataOnFile+=volume.drive.read_block(int(dataLocations[k]))
                        #only want the first n bits
                        dataOnFile = dataOnFile[:int(fileDataLength)]    
                        file = volume.open(fileName.encode())
                        file.write(0, dataOnFile)
                        print (file.data)
                    
        #print (root)
        
        return volume
        '''
        Reconnects a drive as a volume.
        Any data on the drive is preserved.
        Returns the volume.
        '''
    
    def unmount(self):
        #add the name and bitmap etc
        #self.drive.write_block(0,data)
        self.writeVolumeDataBlock()
        self.writeRootDirectoryStuff()
        self.writeFiles()
        self.drive.disconnect()
        
        
    def writeRootDirectoryStuff(self):
        self.directory.getAllMetaData()
        blocksUsedForMetaData = self.directory.metaData
        #then create the rootDirectory
        
        rootDirData = b''
        for key in blocksUsedForMetaData.keys():
            self.drive.write_block(key,blocksUsedForMetaData[key])
            rootDirData += str(key).encode()+b'\n'
        #fill the rest with zeros
        numberOfZeros = int(self.drive.num_blocks()-(len(rootDirData)/2))
        rootDirData +=b'0\n'*numberOfZeros
        #write this to the root directory
        #numberOfleftover spaces
        numberOfSpaces = Drive.BLK_SIZE-len(rootDirData)%Drive.BLK_SIZE
        rootDirData+=(b' '*numberOfSpaces)
        i = 0
        while i < len(rootDirData)/Drive.BLK_SIZE:
            self.drive.write_block(self.rootDir,rootDirData[i*Drive.BLK_SIZE:i*Drive.BLK_SIZE+Drive.BLK_SIZE])
            i+=1
    
    def writeVolumeDataBlock(self):
        dataVolumeSize = str(self.numOfDataBlocks).encode()+b'\n'+self.driveName+b'\n'+str(self.size()).encode()+b'\n'+self.bitmap()+b'\n'+str(self.rootDir).encode()+b'\n'
        '''make it divisible by Drive.blksize and then split the array'''
        numberOfSpaces = Drive.BLK_SIZE-len(dataVolumeSize)%Drive.BLK_SIZE
        dataVolumeSize+=(b' '*numberOfSpaces)
        i=0;
        while i < len(dataVolumeSize)/Drive.BLK_SIZE:
            #slice the array 
            self.drive.write_block(i,dataVolumeSize[i*Drive.BLK_SIZE:i*Drive.BLK_SIZE+Drive.BLK_SIZE])
            i= i +1

    def writeFiles(self):
        for file in self.directory.fileList:
            for fileKey in file.locationsOfData.keys():
                self.drive.write_block(fileKey,file.locationsOfData[fileKey])
        
    def open(self, filename):
        '''
        Opens a file for read and write operations.
        If the file does not exist it is created.
        Returns an A2File object.
        '''
        if('\n' in filename.decode())or('/'in filename.decode()):
            raise ValueError
        for i in range(len(self.directory.fileList)):
            if self.directory.fileList[i].name == filename:
                return self.directory.fileList[i]
        file = self.directory.addNewFile(filename,self.drive)
        return file
    
    
class Directory(object):
    def __init__(self, usedDrives):
        self.usedDrives = usedDrives
        self.fileList=[]
        self.metaData = {}
    
    def chooseMetaDataBlock(self):
        for i in range(len(self.usedDrives)):
            if self.usedDrives[i]==False:
                self.usedDrives[i]=True
                return i
            
                
        
    def addNewFile(self, fileName,drive):
        
        #create the file using the last free metaDataFile
        file = A2File(fileName, self.usedDrives,drive)
        self.fileList.append(file)
        self.getAllMetaData()
#         metaDataofFile = file.getMetaData()
#         if len(self.metaDataDictionary[self.currentDrive]+metaDataofFile)>Drive.BLK_SIZE:
#             #add whatever fits
#             
#             #choose the new block
#             #put the rest of the metaData in
#             pass
#         else :
#             self.metaDataDictionary[self.currentDrive]+=metaDataofFile
        return file
        
        #find an empty place in the used drives
    
    def getAllMetaData(self):
        for key in self.metaData.keys():
            self.usedDrives[key]=False
        #create new MetadataDictionary
        self.metaData = {}
        data = b''
        for i in range(len(self.fileList)):
            data += self.fileList[i].getMetaData()
            
        if len(data)>0:
        #make the data blockSized
            numberOfSpaces = Drive.BLK_SIZE-len(data)%Drive.BLK_SIZE
            data+=(b' '*numberOfSpaces)
            i = 0
            while i < len(data)/Drive.BLK_SIZE:
                chosenBlock = self.chooseMetaDataBlock()
                self.metaData[chosenBlock] = data[i*Drive.BLK_SIZE:i*Drive.BLK_SIZE+Drive.BLK_SIZE]
                i=i+1
