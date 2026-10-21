import { exec } from "./exec.js";

export async function serve(root: string): Promise<void> {

    const args = [

        "serve",

        "--env",
        "root=.",

        "--env",
        "config=../skeleton-config.json",

        "--env",
        "servers=../skeleton-servers.json",

        "--env",
        "mode=dev",
    ];

    await exec("skeleton-webpack", args, root);
}