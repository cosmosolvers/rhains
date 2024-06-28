from typing import Any, Optional
import os
import shortuuid
from werkzeug.utils import secure_filename

from ..field import Field

from security.conf import rhconf
from exception.core.models import field


__file = {
    'AudioField': 'audio',
    'ImageField': 'img',
    'MediaField': 'video'
}


class FileField(Field):
    """
    FILE FIELD
    ==========
    champ general de fichiers

    :param upload_to: repertoire de stockage
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut

    :raise FieldFileNotFoundError: si le fichier n'est pas trouvé
    :raise FieldFileSizeError: si la taille du fichier est trop grande

    :return: str
    """

    def __init__(
        self,
        upload_to: Optional[str] = None,
        nullable=True,
        default: Optional[str] = None
    ):
        self.__media = rhconf.media
        if not self.__media:
            raise field.FieldFileError('media file not found')

        self.__file = getattr(self.__media, __file.get(self.__class__.__name__))
        if not self.__file:
            self.__file = self.__media.file

        if not self.__file:
            raise field.FileFieldError('media file not found')

        path = self.__file.path
        if not path:
            raise field.FieldMediaPathError("media file path not found in configuration file")

        self._upload = upload_to if not self.__file.local else os.path.join(
            rhconf.project.path,
            path,
            upload_to or ''
        )
        default = os.path.join(self._upload, default) if default else None

        super().__init__(nullable=nullable, default=default)
        if not os.path.exists(self._upload):
            os.makedirs(self._upload)
        # taille du fichier
        self._size = 0

    def __upload_file(self, file_content: bytes) -> str:
        filename = secure_filename(shortuuid.uuid())
        url = os.path.join(self._upload, filename)
        with open(url, 'wb') as f:
            f.write(file_content)
        self._size = os.path.getsize(url)
        SIZE = self.__file.prefered.size
        if SIZE != -1 and self._size > SIZE:
            os.remove(url)
            raise field.FieldFileSizeError(f"file size {self._size} is too large")
        return url

    def __load_file(self, value: str) -> bytes:
        with open(value, 'rb') as f:
            return f.read()

    def __delete_file(self) -> None:
        if os.path.exists(self._value):
            os.remove(self._value)

    def load(self, value: str) -> str:
        if not os.path.exists(value):
            raise field.FieldFileNotFoundError(f"{value} not found")
        return self._value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and isinstance(value, bytes)

    def remove(self) -> None:
        self.__delete_file()
        self._value = None

    def size(self) -> int:
        return self._size

    def __set__(self, instance, value: bytes):
        value = self.__upload_file(value)
        return super().__set__(instance, value)
