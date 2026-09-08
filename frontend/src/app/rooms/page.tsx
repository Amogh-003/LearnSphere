"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { roomsApi } from "@/lib/api";
import type { Room } from "@/types";
import { Users, Heart, Pin } from "lucide-react";

export default function RoomsPage() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    roomsApi
      .list({ q: search || undefined })
      .then((res) => setRooms(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [search]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold">Study Rooms</h1>
        <div className="flex gap-2">
          <input
            type="search"
            placeholder="Search rooms..."
            className="input max-w-xs"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <Link href="/rooms/new" className="btn-primary whitespace-nowrap">
            Create Room
          </Link>
        </div>
      </div>

      {loading ? (
        <p className="text-slate-400">Loading rooms...</p>
      ) : rooms.length === 0 ? (
        <div className="card text-center text-slate-400">
          No rooms found. Be the first to create one!
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {rooms.map((room) => (
            <Link
              key={room.id}
              href={`/rooms/${room.id}`}
              className="card transition hover:border-primary-600 hover:bg-slate-800"
            >
              <div className="flex items-start justify-between gap-2">
                <h2 className="font-semibold line-clamp-1">{room.name}</h2>
                {room.is_pinned && (
                  <Pin size={16} className="shrink-0 text-primary-400" />
                )}
              </div>
              {room.topic && (
                <span className="mt-1 inline-block rounded bg-slate-700 px-2 py-0.5 text-xs text-slate-300">
                  {room.topic.name}
                </span>
              )}
              <p className="mt-2 line-clamp-2 text-sm text-slate-400">
                {room.description || "No description"}
              </p>
              <div className="mt-4 flex items-center gap-4 text-xs text-slate-500">
                <span className="flex items-center gap-1">
                  <Users size={14} /> {room.participant_count}
                </span>
                <span className="flex items-center gap-1">
                  <Heart size={14} /> {room.like_count}
                </span>
                <span className="ml-auto">@{room.host.username}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}