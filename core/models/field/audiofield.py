from typing import Optional
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import shortuuid
import io
import os

from .filefield import FileField

from security.conf import rhconf
from exception.core.models import field


class AudioField(FileField):
    """
    AUDIO FIELD
    ===========
    field pour les fichiers audio
    """

    def __init__(
        self,
        upload_to: Optional[str] = None,
        nullable=True,
        default: Optional[str] = None
    ):
        super().__init__(upload_to=upload_to, nullable=nullable, default=default)
        self._format = ''
        if 'audio' in rhconf.get('media'):
            self._format = rhconf.get('media').get('audio').get('prefered').get('format')
        else:
            raise field.FieldMediaFormatError("media audio format not found in configuration file")

    def __upload_file(self, file_content: bytes) -> str:
        audio = AudioSegment.from_file(io.BytesIO(file_content))
        # Régler le taux d'échantillonnage si nécessaire
        audio = audio.set_frame_rate(44100)
        # Régler le nombre de canaux si nécessaire
        audio = audio.set_channels(2)
        fielname = secure_filename(shortuuid.uuid()) + '.' + self._format
        url = os.path.join(self._upload, fielname)

        self._size = os.path.getsize(url)
        SIZE = rhconf.get('media').get('prefered').get('size')
        if SIZE != -1 and self._size > SIZE:
            os.remove(url)
            raise field.FieldFileSizeError(f"file size {self._size} is too large")
        audio.export(url, format=self._format)
        return url
