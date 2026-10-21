import { exec } from "./exec.js";

export async function build(root: string): Promise<void> {

    const args = [

        "build",

        "--env",
        "root=.",

        "--env",
        "config=../skeleton-config.json",

        "--env",
        "servers=../skeleton-servers.json",

        "--env",
        "mode=prod",
    ];

    await exec("skeleton-webpack", args, root);
}