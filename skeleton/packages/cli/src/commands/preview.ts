import path from "node:path";
import fs from "node:fs/promises";

import { exec } from "./exec.js";
import { build } from "./build.js";

export async function preview(root: string): Promise<void> {

    // 1) skeleton build

    const dist = path.join(root, "dist");

    try {

        await fs.access(dist);

    } catch {

        await build(root);
    }

    // 2) npx serve dist

    await exec("npx", ["serve", "dist"], root);
}