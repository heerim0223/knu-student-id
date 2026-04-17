import { createBrowserRouter } from "react-router-dom";
import Home from "@/pages/Home";
// 객체 기반 라우팅
const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
])

export default router;
