from fs import open_fs
from fs import *
from fs.base import *
from fs.compress import *
from fs.copy import *
from fs.enums import *
from fs.errors import *
from fs.glob import *
from fs.info import *
from fs.filesize import *
from fs.mirror import *
from fs.move import *
from fs.opener import *
from fs.opener.base import *
from fs.opener.parse import *
from fs.opener.registry import *
from fs.opener.errors import *
from fs.path import *
from fs.permissions import *
from fs.tools import *
from fs.tree import *
from fs.walk import *
from fs.wildcard import *
from fs.wrap import *
from fs.wrapfs import *
from typing import Union


class MSAFilesystem:
    """MSA Filesystem base class, provides a common interface to any filesystem.

    Opening a filesystem for a given protocol.

    Think of MSAFilesystem as the next logical step to Python’s file objects.
    In the same way that file objects abstract a single file, MSAFilesystem objects abstract an entire filesystem.

    **Paths**

    With the possible exception of the constructor, all paths in a filesystem are MSAFilesystem paths, which have the following properties:

    * Paths are ```str``` type in Python3, and ```unicode``` in Python2
    * Path components are separated by a forward slash (```/```)
    * Paths beginning with a ```/``` are absolute
    * Paths not beginning with a forward slash are relative
    * A single dot (```.```) means ‘current directory’
    * A double dot (```..```) means ‘previous directory’


    **FS URL's** are formatted in the following way:

    ```<protocol>://<username>:<password>@<resource>```

    The components are as follows:

    ```<protocol>``` Identifies the type of filesystem to create. e.g. osfs, ftp.

    ```<username>``` Optional username.

    ```<password>``` Optional password.

    ```<resource>``` A resource, which may be a domain, path, or both.


    **Builtin Filesystems:**

    * App Filesystems

        Manage filesystems in platform-specific application directories.
        These classes abstract away the different requirements for user data across platforms, which vary in their conventions. They are all subclasses of OSFS.

        ```Python
        Parameters:
        appname (str) – The name of the application.
        author (str) – The name of the author (used on Windows).
        version (str) – Optional version string, if a unique location per version of the application is required.
        roaming (bool) – If True, use a roaming profile on Windows.
        create (bool) – If True (the default) the directory will be created if it does not exist.

        # Examples
        open_fs('userdata://appname:author:version')
        open_fs('userconf://appname:author:version')
        open_fs('sitedata://appname:author:version')
        open_fs('siteconf://appname:author:version')
        open_fs('usercache://appname:author:version')
        open_fs('userlog://appname:author:version')
        ```

    * FTP Filesystem

        A FTP (File Transport Protocol) Filesystem.
        Optionally, the connection can be made securely via TLS. This is known as FTPS, or FTP Secure. TLS will be enabled when using the ftps:// protocol, or when setting the tls argument to True in the constructor.

        ```Python
        Parameters:
        host (str) – A FTP host, e.g. 'ftp.mirror.nl'.
        user (str) – A username (default is 'anonymous').
        passwd (str) – Password for the server, or None for anon.
        acct (str) – FTP account.
        timeout (int) – Timeout for contacting server (in seconds, defaults to 10).
        port (int) – FTP port number (default 21).
        proxy (str, optional) – An FTP proxy, or None (default) for no proxy.
        tls (bool) – Attempt to use FTP over TLS (FTPS) (default: False)

        # Examples
        open_fs('ftp://test.rebex.net')
        open_fs('ftps://demo.wftpserver.com')
        open_fs('ftp://demo:password@test.rebex.net')
        open_fs('ftp://ftp.ebi.ac.uk/?proxy=test.rebex.net')
        ```

    * Memory Filesystem

        A filesystem that stored in memory.
        Memory filesystems are useful for caches, temporary data stores, unit testing, etc. Since all the data is in memory, they are very fast, but non-permanent. The MemoryFS constructor takes no arguments.

        ```Python
        Parameters:
        None

        # Examples
        fs.open_fs('mem://')
        ```

    * Mount Filesystem

        A Mount FS is a virtual filesystem which can seamlessly map sub-directories on to other filesystems.

        ```Python
        A Mount FS is a virtual filesystem which can seamlessly map sub-directories on to other filesystems.

        Parameters:
        auto_close (bool) – If True (the default), the child filesystems will be closed when MountFS is closed.

        # Examples
        from fs.mountfs import MountFS
        combined_fs = MountFS()
        combined_fs.mount('config', config_fs)
        combined_fs.mount('resources', resources_fs)
        ```

    * Multi Filesystem

        A MultiFS is a filesystem composed of a sequence of other filesystems, where the directory structure of each overlays the previous filesystem in the sequence.
        One use for such a filesystem would be to selectively override a set of files, to customize behavior.

        ```Python
        Parameters for add_fs:
        name (str) – A unique name to refer to the filesystem being added.
        fs (FS or str) – The filesystem (instance or URL) to add.
        write (bool) – If this value is True, then the fs will be used as the writeable FS (defaults to False).
        priority (int) – An integer that denotes the priority of the filesystem being added. Filesystems will be searched in descending priority order and then by the reverse order they were added. So by default, the most recently added filesystem will be looked at first.

        # Examples
        # MultiFS()
        from fs.osfs import OSFS
        from fs.multifs import MultiFS

        theme_fs = MultiFS()
        theme_fs.add_fs('templates', OSFS('templates'))
        theme_fs.add_fs('theme', OSFS('theme'))
        ```

    * OS Filesystem

        Manage the filesystem provided by your OS.
        In essence, an OSFS is a thin layer over the io and os modules of the Python standard library.

        ```Python
        That's the default if you don't define another Filesystem Protokoll.

        # Examples
        fs.open_fs()
        ```

    * Sub Filesystem

        Manage a directory in a parent filesystem.
        A sub-directory on a parent filesystem.
        A SubFS is a filesystem object that maps to a sub-directory of another filesystem. This is the object that is returned by opendir.

        ```Python

        # Examples
        SubFS(parent_fs, path)
        ```

    * Tar Filesystem

        Read and write tar files.
        There are two ways to open a TarFS for the use cases of reading a tar file, and creating a new one.
        If you open the TarFS with write set to False (the default), then the filesystem will be a read only filesystem which maps to the files and directories within the tar file. Files are decompressed on the fly when you open them.

        ```Python
        Parameters:
        file (str or io.IOBase) – An OS filename, or an open file handle.
        write (bool) – Set to True to write a new tar file, or use default (False) to read an existing tar file.
        compression (str, optional) – Compression to use (one of the formats supported by tarfile: xz, gz, bz2, or None).
        temp_fs (str) – An FS URL or an FS instance to use to store data prior to tarring. Defaults to creating a new TempFS.

        # Examples
        with TarFS('foo.tar.gz') as tar_fs:
            readme = tar_fs.readtext('readme.txt')

        with TarFS('foo.tar.xz', write=True) as new_tar:
            new_tar.writetext(
                'readme.txt',
                'This tar file was written by PyFilesystem'
            )
        ```

    * Temporary Filesystem

        Manage filesystems in temporary locations.
        A temporary filesytem is stored in a location defined by your OS (/tmp on linux). The contents are deleted when the filesystem is closed.
        A TempFS is a good way of preparing a directory structure in advance, that you can later copy. It can also be used as a temporary data store.

        ```Python
        A temporary filesytem is stored in a location defined by your OS (/tmp on linux). The contents are deleted when the filesystem is closed.

        # Examples
        fs.open_fs("temp://")
        open_fs("temp://local_copy")
        ```

    * Zip Filesystem

        Read and write zip files.
        There are two ways to open a ZipFS for the use cases of reading a zip file, and creating a new one.
        If you open the ZipFS with write set to False (the default) then the filesystem will be a read-only filesystem which maps to the files and directories within the zip file. Files are decompressed on the fly when you open them.

        ```Python
        Parameters:
        file (str or io.IOBase) – An OS filename, or an open file object.
        write (bool) – Set to True to write a new zip file, or False (default) to read an existing zip file.
        compression (int) – Compression to use (one of the constants defined in the zipfile module in the stdlib).
        temp_fs (str or FS) – An FS URL or an FS instance to use to store data prior to zipping. Defaults to creating a new TempFS.

        # Examples
        with ZipFS('foo.zip') as zip_fs:
            readme = zip_fs.readtext('readme.txt')

        with ZipFS('foo.zip', write=True) as new_zip:
            new_zip.writetext(
                'readme.txt',
                'This zip file was written by PyFilesystem'
            )
        ```

    * SMB Filesystem

        A filesystem over SMB.

        ```Python
        https://github.com/althonos/fs.smbfs

        Parameters:
        host: either the host name (not the FQDN) of the SMB server, its IP address, or both in a tuple. If either the IP address or the host name is not given, NETBIOS is queried to get the missing data.
        user: the username to connect with, defaults to "guest" for anonymous connection.
        passwd: an optional password to connect with, defaults to "" for anonymous connection.
        timeout: the timeout, in seconds, for NetBIOS and TCP requests.
        port: the port the SMB server is listening on.
        name_port: the port the NetBIOS naming service is listening on.
        direct_tcp: set to True if the server is accessible directly through TCP, leave as False for maximum compatibility.
        domain: the network domain to connect with, i.e. the workgroup on Windows. Usually safe to leave as empty string, the default.

        Once created, the SMB filesystem behaves like any other filesystem

        # Examples
        open_fs('smb://username:password@SAMBAHOSTNAME:port/share')
        ```

    * WebDAV Filesystem

        A filesystem for WebDAV.
        Web Distributed Authoring and Versioning, which is an extension to HTTP that lets clients edit remote content on the web. In essence, WebDAV enables a web server to act as a file server, allowing authors to collaborate on web content.

        ```Python
        https://github.com/PyFilesystem/webdavfs

        # Examples
        open_fs('webdav://admin:admin@domain.com:22082/exist/webdav/db')
        open_fs('webdavs://admin:admin@domain.com/exist/webdav/db')
        ```

    * Azure Datalake Filesystem

        A filesystem for Azure Datalake storage.
        S3FS allows you to work with S3 in the same way as any other supported filesystem.

        ```Python
        https://github.com/emedgene/fs_dlk

        Parameters:
        tenant_id
        store


        # Examples
        open_fs("dlk://username:password@/store_name/path/to/remote")
        open_fs("dlk://username:password@tenant-id/store_name/path/to/remote")

        # Downloading files
        with open("local_file", "wb") as local_file:
            dlkfs.download("path/to/remote/file", local_file)

        # Uploading files
        with open("local_file", "wb") as local_file:
            dlkfs.upload("path/to/remote/file", local_file)

        ```

    * S3FS Filesystem

        A filesystem for Amazon S3 cloud storage.
        S3FS allows you to work with S3 in the same way as any other supported filesystem.

        ```Python
        https://github.com/PyFilesystem/s3fs

        Parameters:
        bucket_name (str) – The S3 bucket name.
        dir_path (str) – The root directory within the S3 Bucket. Defaults to "/"
        aws_access_key_id (str) – The access key, or None to read the key from standard configuration files.
        aws_secret_access_key (str) – The secret key, or None to read the key from standard configuration files.
        endpoint_url (str) – Alternative endpoint url (None to use default).
        aws_session_token (str) –
        region (str) – Optional S3 region.
        delimiter (str) – The delimiter to separate folders, defaults to a forward slash.
        strict (bool) – When True (default) S3FS will follow the PyFilesystem specification exactly. Set to False to disable validation of destination paths which may speed up uploads / downloads.
        cache_control (str) – Sets the ‘Cache-Control’ header for uploads.
        acl (str) – Sets the Access Control List header for uploads.
        upload_args (dict) – A dictionary for additional upload arguments. See https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Object.put for details.
        download_args (dict) – Dictionary of extra arguments passed to the S3 client.

        # Examples
        open_fs('s3://mybucket')
        open_fs('s3://mybucket', upload_args={"CacheControl": "max-age=2592000", "ACL": "public-read"})
        open_fs('s3://example?acl=public-read&cache_control=max-age%3D2592000%2Cpublic')

        ```

    * Google Cloud Storage (GCS) Filesystem

        A filesystem for Google Cloud Storage (GCS).
        With GCSFS, you can interact with Google Cloud Storage as if it was a regular filesystem.

        ```Python
        https://github.com/Othoz/gcsfs

        Parameters:
        project (str): Google Cloud project to use
        api_endpoint (str): URL-encoded endpoint that will be passed to the GCS client's client_options
        strict ("True" or "False"): Whether GCSFS will be opened in strict mode

        # Examples
        open_fs("gs://mybucket/root_path?project=test&api_endpoint=http%3A//localhost%3A8888&strict=False")

        ```

    * Google Drive Filesystem

        A filesystem for Google Drive.
        Interact with Google Drive as if it was a regular filesystem.

        ```Python
        https://github.com/rkhwaja/fs.googledrivefs

        Parameters:
        oauth2_access_token
        refresh_token
        token_uri
        client_id
        client_secret

        # Examples
        open_fs("googledrive:///?access_token=<oauth2 access token>&refresh_token=<oauth2 refresh token>&client_id=<oauth2 client id>&client_secret=<oauth2 client secret>")

        ```

    * Dropbox Filesystem

        A filesystem for Dropbox.
        Web Distributed Authoring and Versioning, which is an extension to HTTP that lets clients edit remote content on the web. In essence, WebDAV enables a web server to act as a file server, allowing authors to collaborate on web content.

        ```Python
        https://github.com/PyFilesystem/fs.dropboxfs

        # Examples
        open_fs('dropbox://dropbox.com?access_token=<dropbox access token>')
        ```

    * OneDrive Filesystem

        A filesystem for Dropbox.
        Web Distributed Authoring and Versioning, which is an extension to HTTP that lets clients edit remote content on the web. In essence, WebDAV enables a web server to act as a file server, allowing authors to collaborate on web content.

        ```Python
        https://github.com/rkhwaja/fs.onedrivefs

        Parameters:
        clientId: <your client id>,
        clientSecret: <your client secret>,
        token: <token JSON saved by oauth2lib>,
        SaveToken: <function which saves a new token string after refresh>
        driveId
        userId
        groupId
        siteId

        # Examples
        open_fs('onedrive://...')
        ```

    * YouTube Videos and Playlists Filesystem

        A filesystem for YouTube Videos and Playlists.

        ```Python
        https://github.com/media-proxy/fs.youtube

        Parameters:
        url: The Playlist/Video URL or simply use the YouTube ID
        playlist: If the ID or URL is one Video only, set this to False
        seekable: Use a seekable implementation to move inside the videofile.

        Once created, the YoutubeFS filesystem behaves like any other filesystem

        # Examples
        open_fs('youtube://youtubeplaylistid')
        ```

    * External Filesystems

        See the following wiki page for a list of filesystems not in the core library, and community contributed filesystems.
        https://www.pyfilesystem.org/page/index-of-filesystems/

    Args:
        fs_url (str) – A filesystem URL.
        parse_result (ParseResult) – A parsed filesystem URL.
        writeable (bool) – True if the filesystem must be writable.
        create (bool) – True if the filesystem should be created if it does not exist.
        cwd (str) – The current working directory (generally only relevant for OS filesystems).

    Raises:
        fs.opener.errors.OpenerError – If a filesystem could not be opened for any reason.

    Returns:
    A filesystem instance.

    """

    def __init__(self, fs_url: Union[FS, str], writeable: bool = True,
                 create: bool = True, cwd: str = "") -> None:

        super().__init__()
        self._fs_url: Union[FS, str] = fs_url
        self._writeable: bool = writeable
        self._create: bool = create
        self._cwd: str = cwd

        self.fs: FS = open_fs(self._fs_url, self._writeable, self._create, self._cwd)



