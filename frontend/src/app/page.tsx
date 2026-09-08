import Link from "next/link";
import { BookOpen, Users, Trophy, MessageSquare } from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-16">
      {/* Hero */}
      <section className="text-center pt-8 pb-4">
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
          Learn together.{" "}
          <span className="text-primary-400">Grow faster.</span>
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-400">
          LearnSphere combines real-time topic-based study rooms with structured
          online courses, quizzes, and progress tracking — all in one platform.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link href="/rooms" className="btn-primary">
            Explore Study Rooms
          </Link>
          <Link href="/courses" className="btn-secondary">
            Browse Courses
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[
          {
            icon: Users,
            title: "Study Rooms",
            desc: "Join topic-based rooms, chat in real time, and learn with peers.",
          },
          {
            icon: BookOpen,
            title: "Online Courses",
            desc: "Structured lessons, video content, and instructor tools.",
          },
          {
            icon: MessageSquare,
            title: "Quizzes & Progress",
            desc: "Test your knowledge and track completion automatically.",
          },
          {
            icon: Trophy,
            title: "Leaderboard",
            desc: "Earn points from activity and climb the ranks.",
          },
        ].map(({ icon: Icon, title, desc }) => (
          <div key={title} className="card text-center">
            <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-primary-900/50 text-primary-400">
              <Icon size={24} />
            </div>
            <h3 className="font-semibold">{title}</h3>
            <p className="mt-1 text-sm text-slate-400">{desc}</p>
          </div>
        ))}
      </section>

      {/* CTA */}
      <section className="card bg-gradient-to-r from-primary-900/40 to-slate-800/60 text-center">
        <h2 className="text-2xl font-semibold">Ready to start learning?</h2>
        <p className="mt-2 text-slate-400">
          Create an account and join the community in seconds.
        </p>
        <Link href="/login" className="btn-primary mt-6 inline-flex">
          Get Started
        </Link>
      </section>
    </div>
  );
}