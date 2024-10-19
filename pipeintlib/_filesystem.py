import contextlib
import logging
import os
import shutil
import stat
import uuid
from pathlib import Path
from typing import Callable

LOGGER = logging.getLogger(__name__)


def set_path_read_only(path: Path):
    """
    Remove write permissions for everyone on the given file without modifying other permissions.

    Reference: https://stackoverflow.com/a/38511116/13806195
    """
    # NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING
    NO_WRITING = ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions & NO_WRITING)


def rmtree(path: Path, ignore_errors=False):
    """
    Remove the directory and its content while handling any potential PermissionError.

    This function is copied from ``tempfile.TemporaryDirectory._rmtree``

    Args:
        path: filesystem path to an existing directory
        ignore_errors: do not raise if there is error during cleanup
    """

    def resetperms(path_):
        try:
            os.chflags(path_, 0)
        except AttributeError:
            pass
        os.chmod(path_, 0o700)

    def onerror(func, path_, exc_info):
        if issubclass(exc_info[0], PermissionError):
            try:
                if path_ != path_:
                    resetperms(os.path.dirname(path_))
                resetperms(path_)

                try:
                    os.unlink(path_)
                # PermissionError is raised on FreeBSD for directories
                except (IsADirectoryError, PermissionError):
                    rmtree(path_, ignore_errors=ignore_errors)
            except FileNotFoundError:
                pass
        elif issubclass(exc_info[0], FileNotFoundError):
            pass
        else:
            if not ignore_errors:
                raise

    shutil.rmtree(path, onerror=onerror)


@contextlib.contextmanager
def backupdir(src_dir: Path, logger: Callable[[str], None]):
    """
    Delete the given directory and make a backup out of it, restored if any error happen.
    """
    backup_path = src_dir.with_stem(f"{src_dir.stem}.backup")
    logger(f"creating backup '{backup_path}'")

    try:
        src_dir.rename(backup_path)
    except PermissionError:
        logger(f"warning: got permission error; trying a folder refresh")
        try:
            tmpfile = backup_path / ("tmppp" + uuid.uuid4().hex)
            tmpfile.write_text(
                "this is a hack to force the system to update the folder status"
            )
            tmpfile.unlink()
        except:
            pass

        # finally retry the renaming
        src_dir.rename(backup_path)

    try:
        yield
    except:
        logger(f"upcomming error: reverting to backup")
        rmtree(src_dir)
        backup_path.rename(src_dir)
        raise
    else:
        logger(f"removing backup '{backup_path}'")
        rmtree(backup_path)
