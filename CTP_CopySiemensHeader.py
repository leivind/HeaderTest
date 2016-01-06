# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 14:36:46 2016

@author: ela010
"""

#Small program to copy Siemens headerfiles to a new name based on "Content Time" Dicom-tag which makes 
#it easier to sort large series of files, and also erases non unicode to utf-8
#Tags: https://code.google.com/p/pydicom/source/browse/source/dicom/_dicom_dict.py?r=9eddba59e8f9967fed7916ff5c091184a5760be8
#to do: rad all tags, check utf8 compatability?
#compare reading and writing headers with pydicom (truncates Siemens special tags) with medpy
import dicom, os
from Tkinter import *
import tkFileDialog
import time
from dicom.filereader import InvalidDicomError #only for older than pydicom 0.9.8
import unicodedata
import pylab
from medpy.io import load, save
#from dicom.errors import InvalidDicomError #only for pydiocm 0.9.8 and newer

root = Tk()
root.withdraw()
input_files_tk = tkFileDialog.askopenfilenames(title="Velg DICOM-filer", multiple=1)
input_files = root.splitlist(input_files_tk)        
input_file_list = [os.path.abspath(k) for k in input_files]
lastFolder = os.path.abspath(str("\\".join(input_file_list[0].split("\\")[:-1])))
#first_file = input_file_list[0]
number_of_images = len(input_file_list)
folders_dict = {}
folders_dict[lastFolder + "\\"] = []
number_of_written = 0


 
for filename in input_file_list:
    try:
#        ds=dicom.read_file(filename, stop_before_pixels = False, force=True)
#        pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)    
#        pylab.show()
        ds=dicom.read_file(filename, stop_before_pixels = False, force=True)
       
        
        #list all keys for fun!        
        for key in ds.dir():        
            value = getattr(ds, key, '')
            if type(value) is dicom.UID.UID or key == "PixelData":
                continue
            print "%s: %s" % (key, value)
            print ds.__contains__('WindowCenter')
            #ds.
            #read 0033, 1013
            #if type(value) is dicom.UID.UID:
            #   print "%s:" % (key)
#        try:        
#            dstime=ds.ContentTime[0:6]
#            dsRPD=ds.RequestedProcedureDescription[:]
#            print 'RPD:', dsRPD
#            #dsRPD.encode('utf8')
#            #dsSPSD=ds.ScheduledProcedureStepDescription[:]
#            dsSPSD=ds.RequestAttributesSequence[:]
#            dsSPSDu=dsSPSD[0].ScheduledProcedureStepDescription[:]
#            print 'SPSDu:', dsSPSDu
#            dsSPSDu8=dsSPSDu.decode('utf-8', 'ignore')            
#            #print unicodedata.normalize('NFKD', dsRPD).encode('ascii','ignore')
#            #dsSPSD=unicodestring.encode("utf-8")
#            #dsRPDuc=dsRPD.decode('utf-8')
#            dsRPDu8=dsRPD.decode('utf-8', 'ignore')
#            print 'RPDu8', dsRPDu8
#            #print dsSPSD
#            print 'SPSDu8', dsSPSDu8
#        except AttributeError:
#            dstime=ds.AcquisitionTime[0:6]
#            
#        ds_data=dicom.read_file(filename, force=True)
#        ds_data.RequestedProcedureDescription=dsRPDu8
        ds_newname=lastFolder + "\\Test_pydicom.dcm"
#       
        if not os.path.isfile(ds_newname):
                ds.save_as(ds_newname)
                print "File written: "
                print ds_newname
#            number_of_written += 1
        else:
            print 'File already exists: ' 
            print ds_newname
        
        
        #print ds[0x0033,0x1013].value #name
        pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)    
        pylab.show()
        
                #folders_dict[lastFolder + "\\"].append(filename.split("\\")[-1]) #list of valid dicom-files
    except IOError:
        print 'No such file'
    except InvalidDicomError:
        print 'Invalid Dicom file!', filename    
    except AttributeError:
        print 'Invalid Dicom file/ Content Time ID / RPD / SPSD does not exist', filename
    except MemoryError:
        print 'Memory error, not Dicom-file', filename
    except OverflowError:
        print 'Overflow error, not Dicom-file', filename
    except KeyError: 
        print 'Key error'
    
        
print "   "        
print "Done! %d of %d selected files successfully read % ", number_of_written, number_of_images
image_data, image_header = load(filename)
print image_header 
ds_newname2=lastFolder + "\\Test_medpy.dcm"
save(image_data, ds_newname2, image_header)