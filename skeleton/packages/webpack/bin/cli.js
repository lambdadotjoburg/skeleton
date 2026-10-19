#!/usr/bin/env node

// This script collects client's cmd args from
// app/frontend/package.json scripts relevant
// to the framework & delegates to webpack,

import path from "path";
import { spawn } from "child_process";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const webpackConfig = path.resolve(
    __dirname,
    "../src/webpack.config.js"
);

const args = process.argv.slice(2);

const command = args.shift();

if (command !== "serve" && command !== "build") {
    console.error(
        "Usage: skeleton-webpack <serve|build> [webpack options]"
    );
    process.exit(1);
}

const webpackArgs = [
    ...(command === "serve" ? ["serve"] : []),
    "--config",
    webpackConfig,
    ...args,
];

console.log("WEBPACK ARGS:", webpackArgs);

const child = spawn(
    "webpack",
    webpackArgs,
    {
        stdio: "inherit",
        shell: true,
    }
);

child.on(
    "exit", (code) => {
        process.exit(code ?? 1);
    }
);