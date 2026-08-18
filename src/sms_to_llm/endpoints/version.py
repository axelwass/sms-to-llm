from fastapi import APIRouter

from sms_to_llm.__about__ import __version__
from sms_to_llm.schema.common import VersionResponse

router = APIRouter()


@router.get("/version", response_model=VersionResponse)
def get_version() -> VersionResponse:
    return VersionResponse(version=__version__)
