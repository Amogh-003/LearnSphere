"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { coursesApi } from "@/lib/api";
import type { Course } from "@/types";
import { Star, Users } from "lucide-react";

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [level, setLevel] = useState("");

  useEffect(() => {
    coursesApi
      .list({ q: search || undefined, level: level || undefined })
      .then((res) => setCourses(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [search, level]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold">Courses</h1>
        <div className="flex flex-wrap gap-2">
          <input
            type="search"
            placeholder="Search courses..."
            className="input max-w-xs"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select
            className="input max-w-[140px]"
            value={level}
            onChange={(e) => setLevel(e.target.value)}
          >
            <option value="">All levels</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>

      {loading ? (
        <p className="text-slate-400">Loading courses...</p>
      ) : courses.length === 0 ? (
        <div className="card text-center text-slate-400">
          No published courses yet.
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {courses.map((course) => (
            <Link
              key={course.id}
              href={`/courses/${course.id}`}
              className="card transition hover:border-primary-600 hover:bg-slate-800"
            >
              <div className="mb-2 flex items-center gap-2">
                <span className="rounded bg-primary-900/60 px-2 py-0.5 text-xs capitalize text-primary-300">
                  {course.level}
                </span>
                {course.category && (
                  <span className="rounded bg-slate-700 px-2 py-0.5 text-xs text-slate-300">
                    {course.category.name}
                  </span>
                )}
              </div>
              <h2 className="font-semibold line-clamp-1">{course.title}</h2>
              <p className="mt-1 line-clamp-2 text-sm text-slate-400">
                {course.description}
              </p>
              <div className="mt-4 flex items-center gap-4 text-xs text-slate-500">
                {course.average_rating != null && (
                  <span className="flex items-center gap-1 text-amber-400">
                    <Star size={14} fill="currentColor" />{" "}
                    {course.average_rating}
                  </span>
                )}
                <span className="flex items-center gap-1">
                  <Users size={14} /> {course.enrollment_count}
                </span>
                <span className="ml-auto">@{course.instructor.username}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}