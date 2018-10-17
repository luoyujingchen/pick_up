import datetime
import hashlib
import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import get_valid_filename

import file_handler.default_settings as DEFAULTS

# Create your models here.
class BaseAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    upload_time = models.DateTimeField(auto_created=True,blank=True)
    update_time = models.DateTimeField(auto_now=True)

    def save(self, *args,**kwargs):
        if not self.upload_time:
            self.upload_time = datetime.datetime.now()
        super().save(*args,**kwargs)


class Img(BaseAttachment):
    def _upload_to(self,filename):
        upload_path = getattr(settings,'IMG_UPLOAD_FOLDER',DEFAULTS.IMG_UPLOAD_FOLDER)

        if upload_path[-1] != '/':
            upload_path += '/'

        filename = get_valid_filename(os.path.basename(filename))
        filename, ext = os.path.splitext(filename)
        hash = hashlib.sha1(str(datetime.time()).encode('utf-8')).hexdigest()
        fullpath = os.path.join(upload_path, "%s.%s%s" % (filename, hash, ext))

        return fullpath

    file = models.FileField(upload_to=_upload_to, max_length=255)

