from fastapi import HTTPException


def validate_response(status_code: int):
    if status_code == 404:
        raise HTTPException(
            status_code=status_code,
            detail="Not found",
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status_code,
            detail="Bad request",
        )
