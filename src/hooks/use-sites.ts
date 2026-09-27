"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useSites() {
  return useQuery({
    queryKey: ["sites"],
    queryFn: () => api.getSites()
  });
}
