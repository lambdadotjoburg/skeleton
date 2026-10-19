#!/usr/bin/env node

// run with:
// npx skeleton init
// or if installed globall:
// npm install skeleton
// run with:
// skeleton init

// installs node_modules/skeleton
// not in node_modules/@skeleton/

import { main } from "../dist/index.js";

await main(process.argv.slice(2));