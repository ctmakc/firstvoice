"use client";

import { useState, useEffect } from "react";

interface User {
  id: string;
  email?: string;
  name?: string;
  role: string;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("demo_user");
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch {
        localStorage.removeItem("demo_user");
      }
    }
    setLoading(false);
  }, []);

  const getElderKey = () => localStorage.getItem("elder_key") || "";

  const logout = () => {
    localStorage.removeItem("demo_user");
    localStorage.removeItem("elder_key");
    setUser(null);
    window.location.reload();
  };

  return { user, loading, logout, getElderKey };
}
