from fastapi import APIRouter

router = APIRouter(
    prefix='/sync',
    tags=['Sync']
)

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone
from typing import Annotated
from src.utils.db import get_db  # Ваша функция зависимости для сессии БД
from src.schemas import UpstreamSyncPayload, DownstreamSyncResponse
from src.model import TodoModel

router = APIRouter(prefix="/sync", tags=["Sync"])

# --- 1. UPSTREAM: Клиент отправляет свои оффлайн-изменения на сервер ---
@router.post("/upstream")
@router.post("/upstream/")
def sync_upstream(payload: UpstreamSyncPayload, db: Session = Depends(get_db)):
    if not payload.changes:
        return {"status": "ok", "processed": 0}

    # Подготавливаем данные для массовой вставки (Bulk Upsert)
    stmt_data = [change.model_dump() for change in payload.changes]
    
    # Используем специфичный для PostgreSQL ON CONFLICT DO UPDATE (Upsert)
    # Если такой UUID уже есть — обновляем все поля, кроме самого id
    insert_stmt = insert(TodoModel).values(stmt_data)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=[TodoModel.id],
        # set_={
        #     "title": insert_stmt.excluded.title,
        #     "is_completed": insert_stmt.excluded.is_completed,
        #     "updated_at": insert_stmt.excluded.updated_at,
        #     "is_deleted": insert_stmt.excluded.is_deleted,
        # }
    )
    
    db.execute(upsert_stmt)
    db.commit()
    
    return {"status": "ok", "processed": len(stmt_data)}


# --- 2. DOWNSTREAM: Клиент запрашивает обновления, появившиеся с момента последней синхронизации ---
@router.get("/downstream", response_model=DownstreamSyncResponse)
@router.get("/downstream/", response_model=DownstreamSyncResponse)
def sync_downstream(
    # Клиент передает ISO-строку времени, например: ?since=2026-05-18T10:00:00
    since: Annotated[datetime, Query(description="Дата последней успешной синхронизации клиента")],
    limit: int = Query(default=500, max_value=1000),
    db: Session = Depends(get_db)
):
    # Фиксируем текущее время сервера ДО запроса, чтобы вернуть его клиенту
    current_server_time = datetime.now(timezone.utc)

    # Выбираем всё, что изменилось на сервере позже, чем `since`
    changes = (
        db.query(TodoModel)
        .filter(TodoModel.updated_at > since)
        .order_by(TodoModel.updated_at.asc())
        .limit(limit)
        .all()
    )

    return DownstreamSyncResponse(
        changes=changes,
        server_time=current_server_time
    )