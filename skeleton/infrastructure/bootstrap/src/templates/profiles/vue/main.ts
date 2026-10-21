import { createApp } from "vue";

const body = document.querySelector("body");

if (!body) {
    throw new Error("<body> element not found");
}

const root = document.createElement("div");

root.id = "root";

body.appendChild(root);

import App from "./App.vue";

createApp(App).mount("#root");