import sys
import os
import importlib
import bpy


print(f'\n\n****** НАЧАЛО РАБОТЫ ГЕНЕРАТОРА ******\n')

# currentDir = os.getcwd()
# print(f'Директория проекта: {currentDir}')

# rendersDir = os.path.join(currentDir, 'renders/')
# print(f'Директория с рендерами: {rendersDir}')

# scriptsDir = os.path.join(currentDir, 'scripts/')
# print(f'Директория со скриптами: {rendersDir}')

# scenesDir = os.path.join(currentDir, 'scenes/')
# print(f'Директория со сценами: {rendersDir}')

print(f'Построение пути подключаемых скриптов (*.py)...')
dir = os.path.dirname(bpy.data.filepath)
dir = os.path.join(dir, '../scripts/')
print(f'Путь к подключаемым скриптам: {dir}')

if not dir in sys.path:
    print(f'Добавление пути к текущей среде Python...')
    sys.path.append(dir)


print(f'Импорт модуля "helper.py"...')
import helper
importlib.reload(helper)

print(f'Импорт модуля "blenderConfig.py"...')
import blenderConfig
importlib.reload(blenderConfig)


# print(f'Попытка включения GPU для процесса рендеринга...')
# blenderConfig.enableGPUs("CUDA")

dirs = helper.getDirs()

helper.createDirs(dirs)
# currentRendersDir = helper.getCurrentRendersDir(dirs['rendersDir'])
# print(f'Директория текущего рендеринга: {currentRendersDir}')

# print(f'\nПроверка наличия директории для текущего рендеринга...')
# if not os.path.exists(currentRendersDir):
#     os.makedirs(currentRendersDir)
#     print(f'Создана директория для текущего рендеринга!')
# else:
#     print(f'ПРЕДУПРЕЖДЕНИЕ: уже существует директория для текущего рендеринга!')


print(f'\n\n****** ЗАВЕРШЕНИЕ РАБОТЫ ГЕНЕРАТОРА ******\n')