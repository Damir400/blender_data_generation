from datetime import datetime 
import os
import bpy



rendersStr  = 'renders'
scriptsStr  = 'scripts'
scenesStr   = 'scenes'
imagesStr   = 'images'
masksStr    = 'masks'

imgSubName      = 'img_'
maskSubName     = 'mask_'
annotationsSubName  = 'annotations_'

datetimeFormat = '%Y.%m.%d_%H.%M.%S'





def getDirs():

    rootDir = os.getcwd()
    rendersDir = os.path.join(rootDir, f'{rendersStr}/')
    scriptsDir = os.path.join(rootDir, f'{scriptsStr}/')
    scenesDir = os.path.join(rootDir, f'{scenesStr}/')
    curRendersDir = getCurrentRendersDir(rendersDir = rendersDir,
                                         rendersFolderName = f'{rendersStr}_',
                                         datetimeFormat = datetimeFormat)
    curImagesDir = os.path.join(curRendersDir, f'{imagesStr}/')
    curMasksDir = os.path.join(curRendersDir, f'{masksStr}/')
    
    print(f'')
    print(f'Получение путей директорий:...')
    print(f'\t проект:                      {rootDir}')
    print(f'\t все результаты генератора:   {rendersDir}')
    print(f'\t скрипты:                     {scriptsDir}')
    print(f'\t сцены:                       {scenesDir}')
    print(f'\t текущий запуска генератора:  {curRendersDir}')
    print(f'\t\t изображения:               {curImagesDir}')
    print(f'\t\t маски:                     {curMasksDir}')
    
    print(f'')

    return {
        'rootDir': rootDir,
        'rendersDir': rendersDir,
        'scriptsDir': scriptsDir,
        'scenesDir': scenesDir,
        'curRendersDir':curRendersDir,
        'curImagesDir': curImagesDir,
        'curMasksDir': curMasksDir,
    }



def getCurrentRendersDir(rendersDir: str,
                         rendersFolderName: str,
                         datetimeFormat: str):
    datetimeStr = datetime.now().strftime(datetimeFormat)
    currentRendersDir = os.path.join(rendersDir, f'{rendersFolderName}{datetimeStr}')

    return currentRendersDir



def createDirs(dirs: dict):
    print(f'\nПроверка наличия директории...')

    for dir in dirs:
        print(f'Проверка наличия директория: {dirs[dir]} ...')

        if not os.path.exists(dirs[dir]):
            os.makedirs(dirs[dir])
            print(f'\t УСПЕШНО создана директория!')
        else:
            print(f'\t ПРЕДУПРЕЖДЕНИЕ: данная директория уже существует!')



def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

    

def cameraViewBounds2d(scene, cam_ob, me_ob):
    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            # if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return (
        round(min_x * dim_x),            # X
        round(dim_y - max_y * dim_y),    # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    )