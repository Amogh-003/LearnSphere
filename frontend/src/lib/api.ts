import axios from "axios";
import Cookies from "js-cookie";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT token if present
api.interceptors.request.use((config) => {
  const token = Cookies.get("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const authApi = {
  register: (data: {
    email: string;
    username: string;
    password: string;
    full_name?: string;
  }) => api.post("/auth/register", data),

  login: (username: string, password: string) => {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);
    return api.post("/auth/login", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
  },

  me: () => api.get("/auth/me"),
};

// Rooms
export const roomsApi = {
  list: (params?: { q?: string; topic_id?: number; skip?: number; limit?: number }) =>
    api.get("/rooms/", { params }),

  get: (id: number) => api.get(`/rooms/${id}`),

  create: (data: {
    name: string;
    description?: string;
    topic_id?: number;
    tag_names?: string[];
  }) => api.post("/rooms/", data),

  toggleLike: (id: number) => api.post(`/rooms/${id}/toggle_like`),

  messages: (id: number) => api.get(`/rooms/${id}/messages`),

  postMessage: (id: number, body: string, parent_id?: number) =>
    api.post(`/rooms/${id}/messages`, { body, parent_id }),
};

// Courses
export const coursesApi = {
  list: (params?: {
    q?: string;
    category_id?: number;
    level?: string;
    skip?: number;
    limit?: number;
  }) => api.get("/courses/", { params }),

  get: (id: number) => api.get(`/courses/${id}`),

  create: (data: {
    title: string;
    description: string;
    category_id?: number;
    level?: string;
  }) => api.post("/courses/", data),

  enroll: (id: number) => api.post(`/courses/${id}/enroll`),

  lessons: (id: number) => api.get(`/courses/${id}/lessons`),

  review: (id: number, rating: number, comment?: string) =>
    api.post(`/courses/${id}/reviews`, { rating, comment }),
};

export default api;