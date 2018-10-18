import datetime
import hashlib
import os
import uuid

from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.text import get_valid_filename
import file_handler.default_settings as DEFAULTS


class BaseFile(models.Model):
    created = models.DateField(auto_created=True,editable=False)
    modified = models.DateField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4().hex,primary_key=True)

    def save(self, *args,**kwargs):
        if not self.created:
            self.created = timezone.now()
        super().save(*args,**kwargs)


class TypeImg(BaseFile):
    def file_upload_dir(self,filename):
        upload_path = getattr(settings,'IMG_UPLOAD_FOLDER',DEFAULTS.IMG_UPLOAD_FOLDER)

        if upload_path[-1] != '/':
            upload_path += '/'

        filename = get_valid_filename(os.path.basename(filename))
        filename, ext = os.path.splitext(filename)
        hash = hashlib.sha1(str(datetime.time()).encode('utf-8')).hexdigest()
        fullpath = os.path.join(upload_path, "%s.%s%s" % (filename, hash, ext))

        return fullpath

    file = models.FileField(upload_to=file_upload_dir)