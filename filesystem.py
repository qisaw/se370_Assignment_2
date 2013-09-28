'''
Created on 27/08/2013

This is where you do your work.
Not only do you need to fill in the methods but you can also add any other classes, 
methods or functions to this file to make your system pass all of the tests.

@author: wkas533
'''

from drive import Drive
import math

class A2File(object):
    '''
    One of these gets returned from Volume open.
    '''
    
    def __init__(self, fileName):
        self.name = fileName
        self.fileSize = 0
        '''
        Initializes an A2File object.
        Not called from the test file but you should call this from the
        Volume.open method.
        You can use as many parameters as you need.
        '''

    
    def size(self):
        return self.fileSize
    
    def write(self, location, data):
        '''
        Writes data to a file at a specific byte location.
        If location is greater than the size of the file the file is extended
        to the location with spaces. 
        '''
        pass
    
    def read(self, location, amount):
        '''
        Reads from a file at a specific byte location.
        An exception is thrown if any of the range from
        location to (location + amount - 1) is outside the range of the file.
        Areas within the range of the file return spaces if they have not been written to.
        '''
        pass

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
    

    def __init__(self,drive,name):
        self.drive = drive
        self.driveName = name
        self.rootDir = drive.num_blocks()-1
        #initially all the drives are free
        self.usedDrives=[[False]]*drive.num_blocks()
        #number of data blocks used by the header
        self.numOfDataBlocks = self.calculate_volume_data_blocks()
        #each of the datablocks are marked as used
        for i in range(self.numOfDataBlocks):
            self.usedDrives[i]=True
        #root directory is also  used
        self.usedDrives[self.rootDir]=True

    @staticmethod
    def format(drive, name):
        if (len(name)<1) or (len(name)>(drive.num_blocks()-1)*Drive.BLK_SIZE):
            raise ValueError
        elif ("/" in name.decode()) or ("\n" in name.decode()):
            raise ValueError
        volume = Volume(drive,name)
        
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
    
    def calculate_volume_data_blocks(self):
        #length of the title
        titleLength = len(self.name()) +1 #for the '/n'
        #length of bitmao is drive.numblocks +1
        bitmapLength = self.drive.num_blocks()+1
        #length of size
        sizeLength = len(str(self.drive.num_blocks()))+1
        #length of the root directory
        lenRoot = len(str(self.rootDir))+1
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
        
        '''
        Reconnects a drive as a volume.
        Any data on the drive is preserved.
        Returns the volume.
        '''
        pass
    
    def unmount(self):
        #add the name and bitmap etc
        #self.drive.write_block(0,data)
        self.writeVolumeDataBlock()
        self.drive.disconnect()
    
    def writeVolumeDataBlock(self):
        dataVolumeSize = str(self.numOfDataBlocks).encode()+b'\n'+self.driveName+b'\n'+str(self.size()).encode()+b'\n'+self.bitmap()+b'\n'+str(self.rootDir).encode()+b'\n'
        '''make it divisible by Drive.blksize and then split the array'''
        numberOfSpaces = Drive.BLK_SIZE-len(dataVolumeSize)%Drive.BLK_SIZE
            
        dataVolumeSize+=(b' '*numberOfSpaces)
        i=0;
        while i < len(dataVolumeSize)/Drive.BLK_SIZE:
            #slice the array 
            print(len(dataVolumeSize[i*Drive.BLK_SIZE:i*Drive.BLK_SIZE+Drive.BLK_SIZE]))
            self.drive.write_block(i,dataVolumeSize[i*Drive.BLK_SIZE:i*Drive.BLK_SIZE+Drive.BLK_SIZE])
            i= i +1

        
    def open(self, filename):
        '''
        Opens a file for read and write operations.
        If the file does not exist it is created.
        Returns an A2File object.
        '''
        pass
