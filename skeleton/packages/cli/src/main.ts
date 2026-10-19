import { serve } from "./commands/serve.js";
import { build } from "./commands/build.js";
import { clean } from "./commands/clean.js";
import { purge } from "./commands/purge.js";
import { preview } from "./commands/preview.js";

export async function main(
    argv: string[]
): Promise<void> {

    const command = argv[0];

    const root = process.cwd();

    switch (command) {

        case "serve":
            await serve(root);
            break;

        case "build":
            await build(root);
            break;

        case "preview":
            await preview(root);
            break;

        case "clean":
            await clean(root);
            break;

        case "purge":
            await purge(root);
            break;

        default:
            console.log("SKELETON CLI");
            console.log(`Unknown command: ${command}`);
            break;
    }
}