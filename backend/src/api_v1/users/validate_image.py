from fastapi import UploadFile, File, HTTPException, status
import filetype


ACCEPTED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
]
MAX_FILE_SIZE = 1 * 1024 * 1024


async def validate_content_type(file: UploadFile):
    """Проверка типа файла в хедере"""
    if file.content_type not in ACCEPTED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid file type. Only JPEG and PNG are accepted.",
        )
    await file.seek(0)


async def validate_file_type(file: UploadFile):
    """Проверка типа файла"""
    first_bytes = await file.read(2048)
    file_info = filetype.guess(first_bytes)
    await file.seek(0)
    if file_info is None or file_info.mime not in ACCEPTED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The actual file type is not a valid image.",
        )


async def validate_file_size(file: UploadFile):
    """Проверка размера файла"""
    file_size = len(await file.read())
    await file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The file is too large. The maximum file size is 1MB."
        )


async def validate_image(uploaded_file: UploadFile = File(...)) -> UploadFile:
    """Валидация изображения"""
    await validate_content_type(uploaded_file)
    await validate_file_type(uploaded_file)
    await validate_file_size(uploaded_file)
    return uploaded_file
