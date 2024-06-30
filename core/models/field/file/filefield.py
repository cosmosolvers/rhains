from typing import Any, Optional
import os
import shortuuid
from werkzeug.utils import secure_filename

from ..field import Field

from core.config.conf import rhconf
from exceptions.core.models import field


filechoice = {
    'AudioField': 'audio',
    'ImageField': 'img',
    'MediaField': 'video',
    'FileField': 'file'
}


class MediaView:
    def __init__(self, url: str, size: float, ext: str) -> None:
        self.__url = url
        self.__size = size
        self.__ext = ext

    def __delete_file(self) -> None:
        if os.path.exists(self.__url):
            os.remove(self.__url)
        self.__url = None

    def remove(self) -> None:
        self.__delete_file()
        self.__url = None

    @property
    def url(self) -> str:
        return self.__url

    @property
    def size(self) -> int:
        return self.__size

    @property
    def format(self) -> str:
        return self.__ext.upper()

    @property
    def ext(self) -> str:
        return self.__ext


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

        self.__file = getattr(self.__media, filechoice.get(self.__class__.__name__))
        if not self.__file:
            self.__file = self.__media.file

        if not self.__file:
            raise field.FileFieldError('media file not found')

        # create folder if self.__file.local is true and file.path don't exists
        folder = os.path.join(rhconf.project.path, self.__file.path)
        if self.__file.local and not os.path.exists(folder):
            os.makedirs(folder)
            if self.__file.url:
                os.chdir(folder)
                pathlist = self.__file.url.split('/\\')
                for path in pathlist:
                    os.makedirs(path)
                    os.chdir(path)

        path = self.__file.path
        if not path:
            raise field.FieldMediaPathError("media file path not found in configuration file")

        self._upload = os.path.join(
            rhconf.project.path if self.__file.local else self.__file.url,
            path,
            upload_to if upload_to and upload_to != path else ''
        )
        default = os.path.join(self._upload, default) if default else None

        super().__init__(nullable=nullable, default=default)
        if not os.path.exists(self._upload):
            os.makedirs(self._upload)
        # taille du fichier
        self._size = 0
        self._ext = ''

    def __upload_file(self, file_content: bytes) -> str:
        filename = secure_filename(shortuuid.uuid()) + '.' + self._ext
        url = os.path.join(self._upload, filename)
        with open(url, 'wb') as f:
            f.write(file_content)
        self._size = os.path.getsize(url)
        SIZE = self.__file.prefered.size
        if SIZE != -1 and self._size > SIZE:
            os.remove(url)
            raise field.FieldFileSizeError(f"file size {self._size} is too large")
        self._value = url

    def __load_file(self, value: str) -> bytes:
        with open(value, 'rb') as f:
            return f.read()

    def load(self, value: str) -> str:
        if not os.path.exists(value):
            raise field.FieldFileNotFoundError(f"{value} not found")
        return self._value

    def dump(self, value) -> str:
        if not os.path.exists(value):
            raise field.FieldFileNotFoundError(f"{value} not found")
        return value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and isinstance(value, bytes)

    def __set__(self, instance, value: str):
        self._ext = value.split('.')[-1]
        format = self.__file.prefered.format
        if len(format) != 0 and self._ext not in format:
            raise field.FieldFieldFormatError(f'{self.__ext} not accepted')
        value = self.__load_file(value)
        self._validated(value)
        self.__upload_file(value)

    def __get__(self, instance, owner) -> MediaView:
        if not instance:
            return self
        return MediaView(self._value, self._size, self._ext)
