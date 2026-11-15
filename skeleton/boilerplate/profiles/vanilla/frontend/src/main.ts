import "./static/css/styles.css"

const body = document.querySelector("body");

if (!body) {
    throw new Error("<body> element not found");
}

const root = document.createElement("div");

body.appendChild(root);

const h = document.createElement("h1");

h.innerText = "Skeleton + FastAPI + Vanilla + WebPack"

root.appendChild(h);
