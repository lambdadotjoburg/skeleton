import { createRoot } from "react-dom/client";

const body = document.querySelector("body");

if (!body) {
    throw new Error("<body> element not found");
}

const root = document.createElement("div");

body.appendChild(root);

createRoot(root).render(
    <h1>Skeleton + FastAPI + React + WebPack</h1>
);