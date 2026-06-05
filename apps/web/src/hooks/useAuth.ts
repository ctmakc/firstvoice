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
    // Check for demo session or cookie
    // For MVP: read from localStorage demo user
    const demoUser = localStorage.getItem("demo_user");
    if (demoUser) {
      setUser(JSON.parse(demoUser));
    }
    setLoading(false);
  }, []);

  const login = async (email: string) => {
    // Demo login — creates a viewer user
    const demoUser = { id: "demo", email, role: "viewer" };
    localStorage.setItem("demo_user", JSON.stringify(demoUser));
    setUser(demoUser);
  };

  const logout = () => {
    localStorage.removeItem("demo_user");
    setUser(null);
  };

  return { user, loading, login, logout };
}
