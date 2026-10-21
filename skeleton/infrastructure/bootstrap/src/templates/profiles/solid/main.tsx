import { render } from "solid-js/web";

const body = document.querySelector("body");

if (!body) {
    throw new Error("<body> element not found");
}

const root = document.createElement("div");

body.appendChild(root);

const App = () => (
    <h1>Skeleton + FastAPI + SolidJS + Webpack</h1>
);

render(
    () => <App />,
    root
);