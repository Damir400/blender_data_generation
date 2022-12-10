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

print(f'Импорт модуля "blenderConfig.py"...')
import blenderConfig
importlib.reload(blenderConfig)

print(f'Попытка включения GPU для процесса рендеринга...')
blenderConfig.enableGPUs("CUDA")


print(f'\n\n****** ЗАВЕРШЕНИЕ РАБОТЫ ГЕНЕРАТОРА ******\n')