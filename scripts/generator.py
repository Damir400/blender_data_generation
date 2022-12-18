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


print(f'\nУстановка пути сохранения результата рендеринга кадра...')
C.scene.render.filepath = f'{dirs["curImagesDir"]}/img_'
print(f'\t путь: {dirs["curImagesDir"]}/img_')

annotationsFilepath = H.getAnnotationsFilepath(dirs['curRendersDir'])

curScene = C.scene
curCamera = C.scene.camera
curObject = C.scene.objects['Scratch_002']

imagesAnnotations = []

dataset = DS.DatasetAnnotation()
dataset.info = DS.DatasetInfo()



def frame_change_handler(scene):
    damageBbox = H.cameraViewBounds2d(curScene, curCamera, curObject)
    imagesAnnotations.append(damageBbox)

    H.writeAnnotations(annotationsFilepath, H.toJson(dataset, DS.AnnotationsJsonEncoder))
    print(damageBbox)


bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(frame_change_handler)
bpy.context.scene.frame_set(0)

print(f'\n\n****** ЗАВЕРШЕНИЕ РАБОТЫ ГЕНЕРАТОРА ******\n')