import bpy

def enableGPUs(device_type, use_cpus=False):
    print(f'Получение настроек движка рендеринга Cycles...')
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cycles_preferences.refresh_devices()
    devices = cycles_preferences.devices

    if not devices:
        print(f'Не обнаружено устройство для рендеринга на движке Cycles!')
        raise RuntimeError("Unsupported device type")

    activated_gpus = []
    for device in devices:
        if device.type == "CPU":
            print(f'Использовать CPU для рендеринга: {use_cpus}')
            device.use = use_cpus
        else:
            print(f'Использовать GPU для рендеринга: {not use_cpus}')
            device.use = True
            activated_gpus.append(device.name)
            print(f'Используемое устройство для рендеринга: {device.name}')

    cycles_preferences.compute_device_type = device_type
    bpy.context.scene.cycles.device = "GPU"

    return activated_gpus