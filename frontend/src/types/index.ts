export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string | null;
  headline?: string | null;
  bio?: string | null;
  avatar_url?: string | null;
  points: number;
  is_active: boolean;
  created_at: string;
}

export interface UserPublic {
  id: number;
  username: string;
  full_name?: string | null;
  headline?: string | null;
  avatar_url?: string | null;
  points: number;
}

export interface Topic {
  id: number;
  name: string;
}

export interface Tag {
  id: number;
  name: string;
}

export interface Room {
  id: number;
  name: string;
  description?: string | null;
  topic_id?: number | null;
  is_pinned: boolean;
  scheduled_for?: string | null;
  max_participants?: number | null;
  host: UserPublic;
  topic?: Topic | null;
  tags: Tag[];
  participant_count: number;
  like_count: number;
  is_liked: boolean;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  room_id: number;
  body: string;
  parent_id?: number | null;
  user: UserPublic;
  created_at: string;
  replies?: Message[];
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  thumbnail_url?: string | null;
  level: string;
  is_published: boolean;
  instructor: UserPublic;
  category?: Category | null;
  average_rating?: number | null;
  enrollment_count: number;
  created_at: string;
  updated_at: string;
}

export interface Lesson {
  id: number;
  course_id: number;
  title: string;
  content?: string | null;
  video_url?: string | null;
  order: number;
  duration_minutes?: number | null;
  created_at: string;
}