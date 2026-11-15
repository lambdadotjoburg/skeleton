import "./static/css/styles.css"

import { mount } from "svelte";

import App from "./App.svelte";

const body = document.querySelector("body");

if (!body) {
    throw new Error("<body> element not found");
}

const root = document.createElement("div");

root.id = "root";

body.appendChild(root);

mount(App, { target: root, });