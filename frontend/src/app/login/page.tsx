"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Cookies from "js-cookie";
import { authApi } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    email: "",
    username: "",
    password: "",
    full_name: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (isRegister) {
        await authApi.register({
          email: form.email,
          username: form.username,
          password: form.password,
          full_name: form.full_name || undefined,
        });
      }
      const res = await authApi.login(
        isRegister ? form.username : form.username || form.email,
        form.password
      );
      Cookies.set("access_token", res.data.access_token, { expires: 1 });
      router.push("/");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-md">
      <div className="card">
        <h1 className="text-2xl font-bold text-center">
          {isRegister ? "Create account" : "Welcome back"}
        </h1>
        <p className="mt-1 text-center text-sm text-slate-400">
          {isRegister
            ? "Join LearnSphere and start learning"
            : "Sign in to your account"}
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          {isRegister && (
            <>
              <div>
                <label className="mb-1 block text-sm text-slate-300">Email</label>
                <input
                  type="email"
                  name="email"
                  required
                  className="input"
                  value={form.email}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label className="mb-1 block text-sm text-slate-300">
                  Full name
                </label>
                <input
                  type="text"
                  name="full_name"
                  className="input"
                  value={form.full_name}
                  onChange={handleChange}
                />
              </div>
            </>
          )}
          <div>
            <label className="mb-1 block text-sm text-slate-300">
              {isRegister ? "Username" : "Username or Email"}
            </label>
            <input
              type="text"
              name="username"
              required
              className="input"
              value={form.username}
              onChange={handleChange}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm text-slate-300">Password</label>
            <input
              type="password"
              name="password"
              required
              minLength={8}
              className="input"
              value={form.password}
              onChange={handleChange}
            />
          </div>

          {error && (
            <p className="rounded-lg bg-red-900/40 px-3 py-2 text-sm text-red-300">
              {error}
            </p>
          )}

          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "Please wait..." : isRegister ? "Register" : "Sign in"}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-slate-400">
          {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            type="button"
            onClick={() => {
              setIsRegister(!isRegister);
              setError("");
            }}
            className="text-primary-400 hover:underline"
          >
            {isRegister ? "Sign in" : "Register"}
          </button>
        </p>
      </div>
    </div>
  );
}