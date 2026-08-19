from .admin import router as admin_router
from .health import router as health_router
from .sms_hook import router as sms_router
from .sms_hook import test_router
from .version import router as version_router

__all__ = [
    "admin_router",
    "health_router",
    "sms_router",
    "test_router",
    "version_router",
]
