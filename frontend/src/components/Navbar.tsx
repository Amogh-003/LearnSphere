"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, Users, Home, LogIn } from "lucide-react";
import clsx from "clsx";

const links = [
  { href: "/", label: "Home", icon: Home },
  { href: "/rooms", label: "Study Rooms", icon: Users },
  { href: "/courses", label: "Courses", icon: BookOpen },
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-700/80 bg-slate-900/90 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 font-semibold text-primary-400">
          <span className="text-xl">◎</span>
          <span>LearnSphere</span>
        </Link>

        <nav className="flex items-center gap-1">
          {links.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm transition-colors",
                pathname === href || pathname.startsWith(href + "/")
                  ? "bg-slate-800 text-primary-400"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              )}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
          <Link
            href="/login"
            className="ml-2 flex items-center gap-1.5 rounded-lg bg-primary-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-primary-700"
          >
            <LogIn size={16} />
            Login
          </Link>
        </nav>
      </div>
    </header>
  );
}