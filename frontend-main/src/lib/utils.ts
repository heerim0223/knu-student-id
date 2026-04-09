import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

// Shadcn/UI 클래스 조합 함수
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
