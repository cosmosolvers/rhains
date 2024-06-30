from typing import Optional
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import shortuuid
import io
import os

from .filefield import FileField

from exceptions.core.models import field


class AudioField(FileField):
    """
    AUDIO FIELD
    ===========
    champ de fichiers audio

    :param upload_to: repertoire de stockage
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut

    :raise FieldMediaFormatError: si le format audio n'est pas valide
    :raise FieldFileSizeError: si la taille du fichier est trop grande

    :return: str
    """

    def __init__(
        self,
        upload_to: Optional[str] = None,
        nullable=True,
        default: Optional[str] = None
    ):
        super().__init__(upload_to=upload_to, nullable=nullable, default=default)

    def __upload_file(self, file_content: bytes) -> str:
        audio = AudioSegment.from_file(io.BytesIO(file_content))
        # Régler le taux d'échantillonnage si nécessaire
        audio = audio.set_frame_rate(44100)
        # Régler le nombre de canaux si nécessaire
        audio = audio.set_channels(2)
        fielname = secure_filename(shortuuid.uuid()) + '.' + self._ext
        url = os.path.join(self._upload, fielname)

        self._size = os.path.getsize(url)
        SIZE = self.__file.prefered.size
        if SIZE != -1 and self._size > SIZE:
            os.remove(url)
            raise field.FieldFileSizeError(f"file size {self._size} is too large")
        audio.export(url, format=self._format)
        self._value = url
