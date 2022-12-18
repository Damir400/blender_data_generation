from datetime import datetime
import json
from json import JSONEncoder


class AnnotationsJsonEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__



class DatasetInfo:
    def __init__(self, 
                 year=datetime.now().year,
                 version='1.0.0', 
                 description='Training Dataset', 
                 contributor='ML Engineer', 
                 url='', 
                 date_created=datetime.now().strftime('%d-%m-%Y')):
        self.year = year
        self.version = version
        self.description = description
        self.contributor = contributor
        self.url = url
        self.date_created = date_created



class DatasetLicense:
    def __init__(self, 
                 id: int,
                 name: str,
                 url = ''):
        self.id = id
        self.name = name
        self.url = url


class ObjectCategory:
    def __init__(self, 
                 id: int,
                 name: str,
                 supercategory: str = None):
        self.id = id
        self.name = name
        self.supercategory = supercategory


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

    def __init__(self):
        self.info = ''
        self.licenses = []
        self.categories = []
        self.images = []
        self.annotations = []


