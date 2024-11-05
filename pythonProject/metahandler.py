import xml.etree.ElementTree as ET
import os
import csv
import itertools
import datetime
from matplotlib.backend_bases import NonGuiException



def getVoxelDimensions(datapath):
   #find properties file
   frametime = 1
   frametimeStr = None
   for root, dirs, files in os.walk(datapath):
      for file in files:
         if not file.endswith('Properties.xml'):
            continue
         metadatapath = (os.path.join(root, file))

   voxelDim = {}
   root = ET.parse(metadatapath).getroot()
   for type_tag in root.findall('Image/ImageDescription/Dimensions/DimensionDescription'):
      voxelDim[type_tag.get('DimID')] = type_tag.get('Voxel')
      value = type_tag.get('DimID')
      if value == "T":
         voxelDim[type_tag.get('DimID')] = type_tag.get('Voxel')[:-2]

   for i, j in voxelDim.items():
      voxelDim[i] = float(j)
   return voxelDim

def getShapeDimensions(datapath):
   #find properties file
   shapeDim = {}
   frametime = 1
   frametimeStr = None
   for root, dirs, files in os.walk(datapath):
      for file in files:
         if not file.endswith('Properties.xml'):
            continue
         metadatapath = (os.path.join(root, file))


   root = ET.parse(metadatapath).getroot()
   for type_tag in root.findall('Image/ImageDescription/Dimensions/DimensionDescription'):
      voxelDim[type_tag.get('DimID')] = type_tag.get('NumberOfElements')

   for i, j in voxelDim.items():
      shapeDim[i] = int(j)

   return shapeDim


def getTimeDifference(metapath, echempath):
   #find properties file
   startConf = None
   startEchem = None

   for root, dirs, files in os.walk(metapath):
      for file in files:
         if not file.endswith('Properties.xml'):
            continue
         metadatapath = (os.path.join(root, file))

   root = ET.parse(metadatapath).getroot()
   for type_tag in root.findall('./Image/ImageDescription'):
      for child in type_tag:
         if child.tag == "StartTime":
            startConf = child.text

   with open(echempath) as tsv:
      for line in csv.reader(tsv, dialect="excel-tab"):
         if line[0] == "DATE":
            startEchem = line[2]
         if line[0] == "TIME":
            startEchem = startEchem + " " + line[2]

   timeStartConf = datetime.datetime.strptime(startConf, "%m/%d/%Y %I:%M:%S.%f %p")
   timeStartEchem = datetime.datetime.strptime(startEchem, "%d.%m.%Y %H:%M:%S")

   timeDiff = timeStartEchem - timeStartConf
   return timeDiff.total_seconds()


def getElectricData(filepath):
   data = []
   returnList = []
   with open(filepath) as tsv:
      for line in csv.reader(tsv, dialect="excel-tab"):
         if line[0] == "" and len(line) > 2:
            data.append(line)
   returnList = (list(map(list, itertools.zip_longest(*data, fillvalue=None)))[1:])

   with open(filepath) as tsv:
      for line in csv.reader(tsv, dialect="excel-tab"):
         if line[0] == "TAG":
            returnList.insert(0, line[1])

   return returnList