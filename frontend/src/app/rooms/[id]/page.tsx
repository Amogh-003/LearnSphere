"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { roomsApi } from "@/lib/api";
import type { Room, Message } from "@/types";
import { Heart, Users, Send } from "lucide-react";

export default function RoomDetailPage() {
  const params = useParams();
  const roomId = Number(params.id);
  const [room, setRoom] = useState<Room | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!roomId) return;
    Promise.all([roomsApi.get(roomId), roomsApi.messages(roomId)])
      .then(([roomRes, msgRes]) => {
        setRoom(roomRes.data);
        setMessages(msgRes.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [roomId]);

  const handleLike = async () => {
    if (!room) return;
    try {
      const res = await roomsApi.toggleLike(room.id);
      setRoom({
        ...room,
        is_liked: res.data.liked,
        like_count: res.data.like_count,
      });
    } catch (e) {
      console.error(e);
    }
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!body.trim() || !room) return;
    try {
      const res = await roomsApi.postMessage(room.id, body.trim());
      setMessages((prev) => [...prev, res.data]);
      setBody("");
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) return <p className="text-slate-400">Loading room...</p>;
  if (!room) return <p className="text-red-400">Room not found</p>;

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold">{room.name}</h1>
            {room.topic && (
              <span className="mt-1 inline-block rounded bg-slate-700 px-2 py-0.5 text-xs">
                {room.topic.name}
              </span>
            )}
            <p className="mt-2 text-slate-400">{room.description}</p>
            <p className="mt-2 text-sm text-slate-500">
              Hosted by @{room.host.username}
            </p>
          </div>
          <div className="flex flex-col items-end gap-2">
            <button
              onClick={handleLike}
              className={`btn flex items-center gap-1 ${
                room.is_liked ? "text-red-400" : "btn-ghost"
              }`}
            >
              <Heart size={18} fill={room.is_liked ? "currentColor" : "none"} />
              {room.like_count}
            </button>
            <span className="flex items-center gap-1 text-sm text-slate-400">
              <Users size={16} /> {room.participant_count}
            </span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="card space-y-4">
        <h2 className="font-semibold">Discussion</h2>
        <div className="max-h-96 space-y-3 overflow-y-auto">
          {messages.length === 0 && (
            <p className="text-sm text-slate-500">No messages yet. Start the conversation!</p>
          )}
          {messages.map((msg) => (
            <div key={msg.id} className="rounded-lg bg-slate-800/80 p-3">
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <span className="font-medium text-primary-400">
                  @{msg.user.username}
                </span>
                <span>{new Date(msg.created_at).toLocaleString()}</span>
              </div>
              <p className="mt-1 text-sm">{msg.body}</p>
            </div>
          ))}
        </div>

        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            className="input flex-1"
            placeholder="Write a message..."
            value={body}
            onChange={(e) => setBody(e.target.value)}
          />
          <button type="submit" className="btn-primary">
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}