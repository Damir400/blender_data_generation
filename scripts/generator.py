import sys
import os
import importlib
import bpy

print(f'\n\n****** НАЧАЛО РАБОТЫ ГЕНЕРАТОРА ******\n')

print(f'Построение пути подключаемых скриптов (*.py)...')
dir = os.path.dirname(bpy.data.filepath)
dir = os.path.join(dir, '../scripts/')
print(f'Путь к подключаемым скриптам: {dir}')

if not dir in sys.path:
    print(f'Добавление пути к текущей среде Python...')
    sys.path.append(dir)

print(f'Импорт модуля "helper.py"...')
import helper as H
importlib.reload(H)

print(f'Импорт модуля "blenderConfig.py"...')
import blenderConfig
importlib.reload(blenderConfig)

print(f'Импорт модуля "dataStructures.py"...')
import dataStructures as DS
importlib.reload(DS)

print(f'Попытка включения GPU для процесса рендеринга...')
blenderConfig.enableGPUs("CUDA")

dirs = H.getDirs()
H.createDirs(dirs)
C = bpy.context
R = C.scene.render

print(f'\nУстановка пути сохранения результата рендеринга кадра...')
C.scene.render.filepath = f'{dirs["curImagesDir"]}/img_'
C.scene.node_tree.nodes['MaskOutput'].base_path = dirs['curMasksDir']
C.scene.node_tree.nodes['MaskOutput'].file_slots[0].path = H.maskSubName
print(f'\t путь: {dirs["curImagesDir"]}/img_')

annotationsFilepath = H.getAnnotationsFilepath(dirs['curRendersDir'])

curScene = C.scene
curCamera = C.scene.camera
stratchObj = C.scene.objects['Scratch']
rustObj = C.scene.objects['Rust']

# imagesAnnotations = []

dataset = DS.DatasetAnnotation()
dataset.info = DS.DatasetInfo()
dataset.info.imagesRelPath = os.path.relpath(dirs['curImagesDir'], dirs['curRendersDir'])
dataset.info.masksRelPath = os.path.relpath(dirs['curMasksDir'], dirs['curRendersDir'])
dataset.licenses.append(DS.DatasetLicense(1, 'MIT'))
dataset.categories.append(DS.ObjectCategory(1, 'scratch'))
dataset.categories.append(DS.ObjectCategory(2, 'rust'))

H.writeAnnotations(annotationsFilepath, H.toJson(dataset, DS.AnnotationsJsonEncoder))


def getMaskName(imgName):
    print(f'MaskOutput: {C.scene.node_tree.nodes["MaskOutput"].base_path}')
    print(f'MaskOutput: {C.scene.node_tree.nodes["MaskOutput"].inputs[0].name}')
    print(f'MaskOutput: {C.scene.node_tree.nodes["MaskOutput"].file_slots[0]}')
    print(f'MaskOutput: {C.scene.node_tree.nodes["MaskOutput"].file_slots[0].path}')
    return imgName.replace("img_", "mask_")


def getImageName(frame):
    return os.path.basename(R.frame_path(frame=frame))


def frame_change_handler(scene):
    curFrame = scene.frame_current
    dataset.info.imgCount += 1
    
    # damageBbox = H.cameraViewBounds2d(curScene, curCamera, curObject)
    # print(damageBbox)
    # imagesAnnotations.append(damageBbox)

    # H.writeAnnotations(annotationsFilepath, H.toJson(dataset, DS.AnnotationsJsonEncoder))

    imageInfo = DS.ImageInfo(id=dataset.info.imgCount, 
                             width=H.imgWidth,
                             height=H.imgHeight,
                             file_name=getImageName(curFrame),
                             mask_name=getMaskName(getImageName(curFrame)),
                             license=dataset.licenses[0].id)

    dataset.info.objCount += 1
    objBbox = H.cameraViewBounds2d(curScene, curCamera, stratchObj)
    stratchObjAnn = DS.ImageAnnotation(id=dataset.info.objCount,
                                        image_id=imageInfo.id,
                                        category_id=dataset.categories[0].id,
                                        bbox=objBbox)

    dataset.info.objCount += 1
    objBbox = H.cameraViewBounds2d(curScene, curCamera, rustObj)
    rustObjAnn = DS.ImageAnnotation(id=dataset.info.objCount,
                                    image_id = imageInfo.id,
                                    category_id=dataset.categories[1].id,
                                    bbox=objBbox)

    dataset.images.append(imageInfo)
    dataset.annotations.append(stratchObjAnn)
    dataset.annotations.append(rustObjAnn)

    H.writeAnnotations(annotationsFilepath, H.toJson(dataset, DS.AnnotationsJsonEncoder))



bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(frame_change_handler)
bpy.context.scene.frame_set(0)

print(f'\n\n****** ЗАВЕРШЕНИЕ РАБОТЫ ГЕНЕРАТОРА ******\n')