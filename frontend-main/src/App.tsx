import { RouterProvider } from "react-router-dom";
import router from "@/router";

export default function App() {
  return (
    <div className="flex justify-center w-full min-h-screen bg-gray-100">
      <div className="relative w-full max-w-[480px] min-h-screen bg-sky-200 shadow-xl overflow-hidden">
        <RouterProvider router={router} />
      </div>
    </div>
  )
}