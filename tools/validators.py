import mimetypes
import os

VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
VALID_BOOK_EXTENSIONS = [".pdf"]
VALID_BOOK_MIMETYPES = ["application/pdf"]
VALID_IMAGE_MIMETYPES = ["image/jpeg", "image/jpg", "image/png"]
MAX_SIZE = 4*1024*1024


def valid_file_extension(file, extension_list):
    if extension_list == "image":
        extension_list = VALID_IMAGE_EXTENSIONS
    else:
        extension_list = VALID_BOOK_EXTENSIONS
    return any([file.endswith(e) for e in extension_list])


def valid_file_mimetype(file, mimetype_list):
    if mimetype_list == "image":
        mimetype_list = VALID_IMAGE_MIMETYPES
    else:
        mimetype_list = VALID_BOOK_MIMETYPES
    mime_type, encoding = mimetypes.guess_type(file)
    if mime_type:
        return any([mime_type.startswith(m) for m in mimetype_list])
    else:
        return False


def get_file_name(file):
    file_name, ext = os.path.splitext(str(file))
    return str(file_name)


def get_file_extension(file):
    file_name, ext = os.path.splitext(str(file))
    return ext


def valid_lecture_extension(file):
    VALID_LECTURE_EXTENSIONS = [".pdf", ".ppt", ".pptx", ".docx", ".doc", ".zip", ".rar"]
    return any([file.endswith(e) for e in VALID_LECTURE_EXTENSIONS])


def valid_lecture_mimetype(file):
    VALID_LECTURE_MIMETYPES = ["application/pdf",
                               "application/x-rar-compressed",
                               "application/zip",
                               "application/msword",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               "application/vnd.ms-powerpoint",
                               "application/vnd.openxmlformats-officedocument.presentationml.presentation"]
    mime_type, encoding = mimetypes.guess_type(file)
    if mime_type:
        return any([mime_type.startswith(m) for m in VALID_LECTURE_MIMETYPES])
    else:
        return False


def get_file_mimetype(file):
    mime_type, encoding = mimetypes.guess_type(file)
    if mime_type:
        return mime_type
