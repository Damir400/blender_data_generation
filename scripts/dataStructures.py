class DatasetInfo:
    year = 0
    version = ''
    description = ''
    contributor = ''
    url = ''
    date_created = ''


class Datasetlicense:
    id = 0
    name = ''
    url = ''


class ObjectCategory:
    id = 0
    name = ''
    supercategory = ''


class ImageInfo:
    id = 0
    width = 0
    height = 0
    file_name = ''
    license = 0


# class SegmentationInfo:


class ImageAnnotation:
    id = 0
    image_id = 0
    category_id = 0
    segmentation = []
    area = 0.0
    bbox = []


class DatasetAnnotation:
    # Здесь содержится высокоуровневая информация о наборе данных.
    info = ''

    # содержит список лицензий на изображения, 
    # которые применяются к изображениям в наборе данных.
    licenses = []

    # содержит список категорий. 
    # Категории могут принадлежать суперкатегории
    categories = []

    # содержит всю информацию об изображении в наборе данных 
    # без ограничивающей рамки или информации о сегментации. 
    # идентификаторы изображений должны быть уникальными
    images = []

    # список аннотаций каждого отдельного объекта из каждого изображения 
    # в наборе данных.
    annotations = []

