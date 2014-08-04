################################################################################
# Copyright 2014 Ujaval Gandhi
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
################################################################################
from qgis.utils import iface
from PyQt4.QtCore import QVariant
import json , random , io
# Replace the values below with values from your layer.
# For example, if your identifier field is called 'XYZ', then change the line
# below to _NAME_FIELD = 'XYZ'
_NAME_FIELD = 'NAME'
# Replace the value below with the field name that you want to sum up.
# For example, if the # field that you want to sum up is called 'VALUES', then
# change the line below to _SUM_FIELD = 'VALUES'
_SUM_FIELD = 'POP_EST'

# Names of the new fields to be added to the layer
_NEW_NEIGHBORS_FIELD = 'NEIGHBORS'
_NEW_SUM_FIELD = 'SUM'

layer = iface.activeLayer()

# Create 2 new fields in the layer that will hold the list of neighbors and sum
# of the chosen field.
layer.startEditing()
#layer.dataProvider().addAttributes(        [QgsField(_NEW_NEIGHBORS_FIELD, QVariant.String),         QgsField(_NEW_SUM_FIELD, QVariant.Int)])layer.updateFields()
# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

# Build a spatial index
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)

print len(qgis.utils.iface.mapCanvas().layers()) , "layers"
layer_province=qgis.utils.iface.mapCanvas().layers()[1]
# Loop through all features and find features that touch each feature
counter = 0
for f in feature_dict.values():
    print 'Working on %s' % f[_NAME_FIELD]
    geom = f.geometry()
    # Find all features that intersect the bounding box of the current feature.
    # We use spatial index to find the features intersecting the bounding box
    # of the current feature. This will narrow down the features that we need
    # to check neighboring features.
    intersecting_ids = index.intersects(geom.boundingBox())
    # Initalize neighbors list and sum
    neighbors = []
    neighbors_sum = 0
    in_is = int(f[_SUM_FIELD]*0.35)
    in_gz = int(f[_SUM_FIELD]*0.14)
    in_ar = int(f[_SUM_FIELD]*0.48)
    in_ot = int(f[_SUM_FIELD]*0.03)
    rfg = int(f[_SUM_FIELD]*0.73)
    causalities = int(f[_SUM_FIELD]*0.0036)
    idz=[]
    idz.append(f["ID"])


    exp = QgsExpression("adm0_a3 = '"+f["adm0_a3"] +"' and st = 1")
    fields = layer_province.pendingFields()
    exp.prepare(fields)
    features = filter(exp.evaluate, layer_province.getFeatures())
    centroid = geom.centroid().asPoint()
    neighbors.append( {"type":"Feature","real_name":f[_NAME_FIELD]  , "name":"Israel" , "pop" :in_is , "x":centroid.x() , "y": centroid.y() ,"geometry" :  geom.exportToGeoJSON() ,"causalities": causalities ,"refugies": rfg  }  )
    centroid = features[0].geometry().centroid().asPoint()
    neighbors.append(   {"type":"Feature","name":"Gaza" , "pop" :in_gz  , "x":centroid.x() , "y": centroid.y(), "geometry" :features[0].geometry().exportToGeoJSON() } )
    ##neighbors.append( [  features[0].geometry().exportToGeoJSON()  , features[0]["ratio"] ] )
    for intersecting_id in intersecting_ids:
        # Look up the feature from the dictionary
        if intersecting_id != f["ID"]:
            intersecting_f = feature_dict[intersecting_id]
            centroid = intersecting_f.geometry().centroid().asPoint()
            neighbors.append(  {"type":"Feature","name":intersecting_f[_NAME_FIELD] , "pop" : in_ar/len(intersecting_ids)+random.uniform(-1,1)*0.01*f[_SUM_FIELD] , "x":centroid.x() , "y": centroid.y()  , "geometry" :  intersecting_f.geometry().exportToGeoJSON() }  )
            idz.append(intersecting_id)
        # For our purpose we consider a feature as 'neighbor' if it touches or
        # intersects a feature. We use the 'disjoint' predicate to satisfy
        # these conditions. So if a feature is not disjoint, it is a neighbor.
    
    feature_rand = feature_dict[random.sample(list(set(feature_dict.keys()) - set(idz)) , 1)[0]]
    centroid = feature_rand.geometry().centroid().asPoint()
    neighbors.append( {"type":"Feature","name": feature_rand[_NAME_FIELD]  , "pop" : in_ot+random.uniform(-1,1)*0.01*f[_SUM_FIELD] , "x":centroid.x() , "y": centroid.y(),"geometry" :  feature_rand.geometry().exportToGeoJSON() } )
    dic_ = {"type":"FeatureCollection" , "features":neighbors}
    ##print json.dumps(dic_)

    with io.open(f["iso_a2"]+'.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(dic_, ensure_ascii=False).replace('\\' , '').replace('}"' , '}').replace('"{' , '{')))
    #neighbors.append(intersecting_f[_NAME_FIELD])
    #neighbors_sum += intersecting_f[_SUM_FIELD]
    #f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
    #f[_NEW_SUM_FIELD] = neighbors_sum
    # Update the layer with new attribute values.
    #layer.updateFeature(f)
    counter+=1
    #if counter > 5 : break
layer.commitChanges()
print 'Processing complete.'
