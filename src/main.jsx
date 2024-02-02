import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

import App from "./App";

import Home from "./components/Home";
const router = createBrowserRouter([
  {
    path: "/100107-DowellEmailExtractor",
    element: <App />,
    children: [
      {
        path: "/100107-DowellEmailExtractor/",
        element: <Home />,
      },
    ],
  },
]);
const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
