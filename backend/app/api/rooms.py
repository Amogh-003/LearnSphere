from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.user import User
from app.models.study import Room, Topic, Tag, Message, room_likes, room_participants
from app.schemas.study import (
    RoomCreate,
    RoomUpdate,
    RoomOut,
    MessageCreate,
    MessageOut,
    TopicOut,
    TagOut,
)
from app.schemas.user import UserPublic
from app.api.deps import get_current_user

router = APIRouter(prefix="/rooms", tags=["rooms"])


def room_to_out(room: Room, current_user: User | None = None) -> RoomOut:
    return RoomOut(
        id=room.id,
        name=room.name,
        description=room.description,
        topic_id=room.topic_id,
        is_pinned=room.is_pinned,
        scheduled_for=room.scheduled_for,
        max_participants=room.max_participants,
        host=UserPublic.model_validate(room.host),
        topic=TopicOut.model_validate(room.topic) if room.topic else None,
        tags=[TagOut.model_validate(t) for t in room.tags],
        participant_count=len(room.participants),
        like_count=len(room.likes),
        is_liked=current_user in room.likes if current_user else False,
        created_at=room.created_at,
        updated_at=room.updated_at,
    )


@router.get("/", response_model=list[RoomOut])
async def list_rooms(
    q: str | None = Query(None, description="Search by name or description"),
    topic_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    query = (
        select(Room)
        .options(
            selectinload(Room.host),
            selectinload(Room.topic),
            selectinload(Room.tags),
            selectinload(Room.participants),
            selectinload(Room.likes),
        )
        .order_by(Room.is_pinned.desc(), Room.updated_at.desc())
    )
    if q:
        query = query.where(
            (Room.name.ilike(f"%{q}%")) | (Room.description.ilike(f"%{q}%"))
        )
    if topic_id:
        query = query.where(Room.topic_id == topic_id)

    result = await db.execute(query.offset(skip).limit(limit))
    rooms = result.scalars().all()
    return [room_to_out(r, current_user) for r in rooms]


@router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_in: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = Room(
        host_id=current_user.id,
        name=room_in.name,
        description=room_in.description,
        topic_id=room_in.topic_id,
        is_pinned=room_in.is_pinned,
        scheduled_for=room_in.scheduled_for,
        max_participants=room_in.max_participants,
    )
    db.add(room)
    await db.flush()

    # Handle tags
    for name in room_in.tag_names:
        name = name.strip().lower()
        if not name:
            continue
        result = await db.execute(select(Tag).where(Tag.name == name))
        tag = result.scalar_one_or_none()
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
            await db.flush()
        room.tags.append(tag)

    room.participants.append(current_user)
    await db.flush()

    # Reload with relationships
    result = await db.execute(
        select(Room)
        .where(Room.id == room.id)
        .options(
            selectinload(Room.host),
            selectinload(Room.topic),
            selectinload(Room.tags),
            selectinload(Room.participants),
            selectinload(Room.likes),
        )
    )
    room = result.scalar_one()
    return room_to_out(room, current_user)


@router.get("/{room_id}", response_model=RoomOut)
async def get_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    result = await db.execute(
        select(Room)
        .where(Room.id == room_id)
        .options(
            selectinload(Room.host),
            selectinload(Room.topic),
            selectinload(Room.tags),
            selectinload(Room.participants),
            selectinload(Room.likes),
        )
    )
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room_to_out(room, current_user)


@router.post("/{room_id}/toggle_like")
async def toggle_like(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.likes))
    )
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if current_user in room.likes:
        room.likes.remove(current_user)
        liked = False
    else:
        room.likes.append(current_user)
        liked = True
    await db.flush()
    return {"liked": liked, "like_count": len(room.likes)}


@router.get("/{room_id}/messages", response_model=list[MessageOut])
async def list_messages(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Message)
        .where(Message.room_id == room_id, Message.parent_id.is_(None))
        .options(selectinload(Message.user), selectinload(Message.replies).selectinload(Message.user))
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()
    return messages


@router.post("/{room_id}/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def create_message(
    room_id: int,
    msg_in: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    message = Message(
        room_id=room_id,
        user_id=current_user.id,
        body=msg_in.body,
        parent_id=msg_in.parent_id,
    )
    db.add(message)

    # Auto-join room
    result = await db.execute(
        select(Room).where(Room.id == room_id).options(selectinload(Room.participants))
    )
    room = result.scalar_one()
    if current_user not in room.participants:
        room.participants.append(current_user)

    await db.flush()
    await db.refresh(message)

    result = await db.execute(
        select(Message)
        .where(Message.id == message.id)
        .options(selectinload(Message.user))
    )
    message = result.scalar_one()
    return message