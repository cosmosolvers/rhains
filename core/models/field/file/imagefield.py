from typing import Optional
from PIL import Image
from werkzeug.utils import secure_filename
import shortuuid
import io
import os

from .filefield import FileField

from core.config.conf import rhconf
from exceptions.core.models import field


class ImageField(FileField):
    """
    IMAGE FIELD
    ===========
    field pour les images
    """

    def __init__(
        self,
        upload_to: Optional[str] = None,
        nullable=True,
        default: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        format: Optional[str] = None
    ):
        super().__init__(upload_to=upload_to, nullable=nullable, default=default)
        self._format = ''
        if 'img' in rhconf.get('media'):
            self._format = rhconf.get('media').get('img').get('prefered').get('format')
        else:
            raise field.FieldMediaFormatError("media image format not found in configuration file")
        self._width = width
        self._height = height
        self._format = format if format else self._format

    def __upload_file(self, file_content: bytes) -> str:
        image = Image.open(io.BytesIO(file_content))
        fielname = secure_filename(shortuuid.uuid()) + '.' + self._format
        url = os.path.join(self._upload, fielname)

        if self._width and self._height:
            image = image.resize((self._width, self._height))

        self._size = os.path.getsize(url)
        SIZE = rhconf.get('media').get('prefered').get('size')
        if SIZE != -1 and self._size > SIZE:
            os.remove(url)
            raise field.FieldFileSizeError(f"file size {self._size} is too large")
        image.save(url, format=self._format)
        return url
