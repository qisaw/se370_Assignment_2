'''
Created on 27/08/2013

This is where you do your work.
Not only do you need to fill in the methods but you can also add any other classes, 
methods or functions to this file to make your system pass all of the tests.

@author: YOUR UPI
'''

from drive import Drive

class A2File(object):
    '''
    One of these gets returned from Volume open.
    '''
    
    def __init__(self, params):
        '''
        Initializes an A2File object.
        Not called from the test file but you should call this from the
        Volume.open method.
        You can use as many parameters as you need.
        '''
        pass
    
    def size(self):
        '''
        Returns the size of the file in bytes.
        '''
        pass
    
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

    @staticmethod
    def format(drive, name):
        '''
        Creates a new volume in a disk.
        Puts the initial metadata on the disk.
        The name must be at least one byte long and not include "\n".
        Raises an IOError if after the allocation of the volume information
        there are not enough blocks to allocate the root directory and at least
        one block for a file.
        Returns the volume.
        '''
        pass
    
    def name(self):
        '''
        Returns the volumes name.
        '''
        pass
    
    def volume_data_blocks(self):
        '''
        Returns the number of blocks at the beginning of the drive which are used to hold
        the volume information.
        '''
        pass
        
    def size(self):
        '''
        Returns the number of blocks in the underlying drive.
        '''
        pass
    
    def bitmap(self):
        '''
        Returns the volume block bitmap.
        '''
        pass
    
    def root_index(self):
        '''
        Returns the block number of the first block of the root directory.
        Always the last block on the drive.
        '''
        pass
    
    @staticmethod
    def mount(drive_name):
        '''
        Reconnects a drive as a volume.
        Any data on the drive is preserved.
        Returns the volume.
        '''
        pass
    
    def unmount(self):
        '''
        Unmounts the volume and disconnects the drive.
        '''
        pass
    
    def open(self, filename):
        '''
        Opens a file for read and write operations.
        If the file does not exist it is created.
        Returns an A2File object.
        '''
        pass
