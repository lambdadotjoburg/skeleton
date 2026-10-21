const body = document.querySelector("body");

if (!body) {
    throw new Error("<body> element not found");
}

const root = document.createElement("div");

body.appendChild(root);

const App = {
    render() {
        return h(
            "h1",
            "Skeleton + FastAPI + Vue + Webpack"
        );
    },
};

createApp(App).mount(root);