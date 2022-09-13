# -*- coding: utf-8 -*-
import os
import re
import shutil
import unicodedata
from typing import List, Optional
from uuid import uuid4

import magic
from fastapi import HTTPException
from starlette.datastructures import UploadFile
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from msaSDK.models.files import MSAFile

archive_unpack_formats = shutil.get_unpack_formats()
archive_pack_formats = shutil.get_archive_formats()
_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = (
    "CON",
    "AUX",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "LPT1",
    "LPT2",
    "LPT3",
    "PRN",
    "NUL",
)


def secure_filename(filename: str) -> str:
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.
    On windows systems the function also makes sure that the file is not
    named after one of the special device files.

    Example:
        ```Python
        secure_filename("My cool movie.mov")
        'My_cool_movie.mov'
        secure_filename("../../../etc/passwd")
        'etc_passwd'
        secure_filename('i contain cool \xfcml\xe4uts.txt')
        'i_contain_cool_umlauts.txt'
        ```

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.
    .. versionadded:: 0.5

    Args:
        filename: the filename to secure

    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename


class ServerHTTPException(HTTPException):
    def __init__(self, error: str = None):
        super(ServerHTTPException, self).__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error
        )


class InvalidResource(ServerHTTPException):
    """
    raise when has invalid resource
    """


class NoSuchFieldFound(ServerHTTPException):
    """
    raise when no such field for the given
    """


class FileMaxSizeLimit(ServerHTTPException):
    """
    raise when the upload file exceeds the max size
    """


class FileExtNotAllowed(ServerHTTPException):
    """
    raise when the upload file ext not allowed
    """


def nameGen(uid, file):
    return str(uid) + "_" + file.filename


class FileUpload:
    """FileUpload Class

    Args:
        filesize: int, size in bytes
        root_path: str = dirname of the file
        uploads_dir: str = "data/uploads", where to store the file
        not_allow_extensions: Optional[List[str]] = None, exclude file extensions from upload ability
        max_size: int = 150000000, max allowed filesize in bytes for upload
        createUIDSubFolders: bool = False, if enabled the system creates Subfolders by the UID

    """
    def __init__(
            self,
            filesize: int,
            root_path: str = os.path.join(os.path.dirname(__file__)),
            uploads_dir: str = "data/uploads",
            not_allow_extensions: Optional[List[str]] = None,
            max_size: int = 150000000,
            createUIDSubFolders: bool = False
    ):
        self.max_size = max_size
        self.not_allow_extensions = not_allow_extensions
        self.uploads_dir = uploads_dir
        self.filename_generator = nameGen
        self.root_path = root_path
        self.uid = str(uuid4())
        self.name = ""
        self.content_type = ""
        self.createSubFolders = createUIDSubFolders
        self.file_size = filesize
        self.magic_desc = ""
        self.magic_type = ""
        self.fullpath = ""

    async def save_file(self, filename: str, ufile: UploadFile):
        """Save the file

        Args:
            filename: the name of the file it should be saved uner
            ufile: UploadFile instance of the file to save

        """
        targetfolder = os.path.join(self.root_path, self.uploads_dir)
        try:
            os.makedirs(targetfolder, exist_ok=True)
        except Exception as e:
            pass
        struct = None
        if self.createSubFolders:
            struct = os.path.join(targetfolder, self.uid)
            os.makedirs(struct, exist_ok=True)
        else:
            struct = self.uploads_dir

        filen = os.path.join(struct, filename)
        self.fullpath = filen
        f = open(f'{filen}', 'wb')
        ufile.file.seek(0)
        with f as buffer:
            shutil.copyfileobj(ufile.file, buffer)
        self.magic_desc = magic.from_file(filen)
        self.magic_type = magic.from_file(filen, mime=True)
        return str(filename)

    async def upload(self, file: UploadFile):
        """upload the file

        Args:
            file: The UploadFile instance of the file for upload.

        """
        self.name = file.filename
        self.content_type = file.content_type

        filename = self.filename_generator(self.uid, file)

        if self.file_size > self.max_size:
            raise FileMaxSizeLimit(f"File size {self.file_size} exceeds max size {self.max_size}")
        if self.not_allow_extensions:
            for ext in self.not_allow_extensions:
                if filename.endswith(ext):
                    raise FileExtNotAllowed(
                        f"File ext {ext} is not allowed of {self.not_allow_extensions}"
                    )
        return await self.save_file(filename, file)


class FileDelete:
    """File Delete Class

    Args:
        uid: str , the GUID of the file
        root_path: str, dirname of the file
        uploads_dir: str, the folder the file was uploaded to.
    """
    def __init__(
            self,
            uid: str,
            root_path: str = os.path.join(os.path.dirname(__file__)),
            uploads_dir: str = "data/uploads",

    ):
        self.uid = uid
        self.uploads_dir = uploads_dir
        self.root_path = root_path

    async def delete_files(self):
        targetfolder = os.path.join(self.root_path, self.uploads_dir, self.uid)
        ret = str("{ \"Success\": \"deleted " + self.uid + "\"}")
        if os.path.exists(targetfolder):
            try:
                shutil.rmtree(targetfolder)
            except OSError as e:
                ret = str("{ \"Error\": \"%s - %s." % (e.filename, e.strerror) + "\"}")
        else:
            targetfolder = os.path.join(self.root_path, self.uploads_dir)
            hit = False
            for fname in os.listdir(targetfolder):
                if fname.startswith(self.uid):
                    targetfile = os.path.join(self.root_path, self.uploads_dir, fname)
                    os.remove(targetfile)
                    hit = True
            if hit is False:
                ret = str("{ \"Error\": \" no such file or batch exists for " + self.uid + "\"}")
        return ret


async def checkIfFileIsArchive(file: UploadFile):
    """Check if File is an Archive like zip or tar"""
    if not file:
        return False
    list_extensions = []
    for entry in archive_unpack_formats:
        subl = entry[1]
        list_extensions.extend([sub_ntry for sub_ntry in subl])

    filename, file_extension = os.path.splitext(file.filename)
    if file_extension in list_extensions:
        return True
    return False


async def createMSAFile(file: UploadFile, up: FileUpload) -> MSAFile:
    """Create an MSAFile Instance for the provided file

    Args:
        file: is the UploadFile
        up: is the FileUpload Instance

    Returns:
        mf: New MSAFile instance.

    """
    result = await up.upload(file)
    mf: MSAFile = MSAFile()
    mf.uid = up.uid
    mf.filename = secure_filename(up.name)
    mf.size = up.file_size
    mf.content_type = up.content_type
    mf.type_raw = up.magic_type
    mf.type_description = up.magic_desc
    return mf  # .copy()


async def createMSAFileFromUnpacked(filepath: str, processuid: str) -> MSAFile:
    """Create an MSAFile Instance for a file from an archive, and keep them under one group by the processuid

    Args:
        filepath: str of the file path
        processuid: str of the group process id (GUID)

    Returns:
        mf: New MSAFile instance.

    """
    mf: MSAFile = MSAFile()
    mf.uid = processuid
    mf.filename = filepath
    mf.size = os.path.getsize(filepath)
    mf.content_type = magic.from_file(filepath, mime=True)
    mf.type_raw = mf.content_type
    mf.type_description = magic.from_file(filepath)
    return mf  # .copy()
