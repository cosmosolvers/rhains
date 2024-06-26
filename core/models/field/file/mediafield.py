from typing import Optional
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
import shortuuid
import io
import os

from .filefield import FileField

from core.config.conf import rhconf
from exceptions.core.models import field


class MediaField(FileField):
    """
    VIDEO FIELD
    ===========
    field pour les videos
    """

    def __init__(
        self,
        upload_to: Optional[str] = None,
        nullable=True,
        default: Optional[str] = None
    ):
        super().__init__(upload_to=upload_to, nullable=nullable, default=default)
        self._format = ''
        if 'video' in rhconf.get('media'):
            self._format = rhconf.get('media').get('video').get('prefered').get('format')
        else:
            raise field.FieldMediaFormatError("media video format not found in configuration file")

    def __upload_file(self, file_content: bytes) -> str:
        video = VideoFileClip(io.BytesIO(file_content))
        fielname = secure_filename(shortuuid.uuid()) + '.' + self._format
        url = os.path.join(self._upload, fielname)

        self._size = os.path.getsize(url)
        SIZE = rhconf.get('media').get('prefered').get('size')
        if SIZE != -1 and self._size > SIZE:
            os.remove(url)
            raise field.FieldFileSizeError(f"file size {self._size} is too large")
        video.write_videofile(url, codec='libx264')
        return url
