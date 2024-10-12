import xml.etree.ElementTree as ET
import os

def getFrameTime(datapath):
   #find properties file
   frametime = 1
   frametimeStr = None
   for root, dirs, files in os.walk(datapath):
      for file in files:
         if not file.endswith('Properties.xml'):
            continue
         metadatapath = (os.path.join(root, file))


   root = ET.parse(metadatapath).getroot()
   for type_tag in root.findall('Image/ImageDescription/Dimensions/DimensionDescription'):
      value = type_tag.get('DimID')
      if value == "T":
         frametimeStr =  (type_tag.get('Voxel'))

   frametime = float(frametimeStr[:-2])
   return frametime




