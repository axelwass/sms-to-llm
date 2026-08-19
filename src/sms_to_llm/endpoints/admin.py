from fastapi import APIRouter, Depends

from sms_to_llm.auth.authorization import require_admin_key
from sms_to_llm.database.factory import create_database
from sms_to_llm.schema.conversation import ConversationMessage

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin_key)])


@router.get("/conversations/{phone_number}", response_model=list[ConversationMessage])
def list_conversations(phone_number: str) -> list[ConversationMessage]:
    database = create_database()
    return database.get_conversation(phone_number)
