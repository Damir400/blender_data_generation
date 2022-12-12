from datetime import datetime 
import os



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
