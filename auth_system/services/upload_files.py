import datetime
import uuid
from django.core.validators import RegexValidator, ValidationError

FILE_TYPES = {
    r'^(jpg|jpeg|png|JPG)$': 'images',
    r'^(pdf)$': 'documents',
    r'^(mp4)$': 'videos'
}


def upload_name(instance, filename):
    file_type = filename.split('.')[-1]
    date = datetime.datetime.now().strftime('%Y/%m/%d')

    for regex, folder in FILE_TYPES.items():
        try:
            RegexValidator(regex).__call__(file_type)
            instance.type = folder
            return '%s/%s/%s/%s.%s' % (folder, instance._meta.model_name, date, uuid.uuid4(), file_type)
        except ValidationError:
            pass
    raise ValidationError('File type is unacceptable')
