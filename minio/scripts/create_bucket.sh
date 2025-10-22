#!/bin/sh

/usr/bin/mc alias set dockerminio $MINIO_ENDPOINT $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Создать бакет (флаг -p - только если еще не существует)
/usr/bin/mc mb -p dockerminio/$MINIO_BUCKET_NAME

/usr/bin/mc anonymous set download dockerminio/$MINIO_BUCKET_NAME

exit 0
