import bpy
import json
from math import radians
import os

os.chdir("E:/Script To Animation/")
BaseDir = "Database/"
sourceFolder = "ParaInfo/"

def LoadModel(ObjData):
    path = BaseDir + str(ObjData["Name"]) +".fbx"
    bpy.ops.import_scene.fbx( filepath = path)
    obj  = bpy.context.active_object
    if obj == None:
        obj = bpy.context.selected_objects[0]
    obj.location=ObjData["Location"]
    obj.rotation_euler = ObjData["Rotation"]
    if ObjData["Scale"]!=-1:
        obj.scale = ObjData["Scale"]
    return obj

def set_floor(color=None):
    bpy.ops.mesh.primitive_plane_add(location=[0,0,0])
    Floor = bpy.context.active_object
    Floor.scale = 3*[100] 
    if color != None:
        mat = bpy.data.materials.new("Floor_color")
        mat.diffuse_color = color
        Floor.data.materials.append(mat)
        for face in Floor.data.polygons:
            face.material_index = face.index % 3
    return Floor

def clearCanvas():
    try:
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.data.objects['Camera'].select_set(False)
        bpy.data.objects['Light'].select_set(False)
        bpy.ops.object.delete()
    finally:
        return 

if __name__ == "__main__":
    files = os.listdir(sourceFolder)
    for i in range(len(files)) :
        file = files[i]
        canvas = clearCanvas()
        
        #set floor on scene
        #Floor = set_floor(color=(0.486,0.988,0,0))
        Floor = set_floor()

        #------------------Animation Process Begins----------------#
        #read data from file
        dataFile = open(sourceFolder + file)
        Data = json.load(dataFile)
        dataFile.close()

        objects = []
        for ObjData in Data[::-1]:
            try:
                objects.append(LoadModel(ObjData))
            except RuntimeError:
                print("\n" + ObjData["Name"] + " model in not loaded...\n")

            
        #bpy.context.scene.render.filepath = 'E:/Script To Animation/VideoOut/'
        #bpy.ops.render.render(animation=True)
        break



