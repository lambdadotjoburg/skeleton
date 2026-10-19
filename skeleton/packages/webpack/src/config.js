// import fs from "fs";
import path from "path";

// import { fileURLToPath } from "url";
import loadJSONSafe from "./loadJSONSafe.js";

export default function createConfig(flags = {}) {

    const root = flags.root;

    // read config.json!
    const rawConfig = loadJSONSafe(
        path.resolve(
            root,
            flags.config
                ?? "skeleton-config.json"
        )
    ) ?? {};

    // default configuration settings to be merged
    // in case client omits any of the required data!
    const DEFAULT_CONFIG = {

        entry: {
            main: "main",
            index: "index",
        },

        lib: {
            src: "src",
            dist: "dist",
            static: "static",
        },

        devServer: {
            /**
             * NOTE: open: true/false
             * default: open in frontend dev mode
             * DO NOT: open in root gateway reverse proxy mode
             */
            open: true, // safe
            historyApiFallback: false,
            host: "127.0.0.1",
            port: 3000,
            hot: true,
            overlay: true,
        },

        /**
         * proxy server for quick-dev => not used for reverse proxy!
         * python's uvicorn will act as reverse proxy for SPA-like behaviour
         */
        proxy: {
            on: false, // off by default!
            host: "127.0.0.1",
            port: 8081,
            changeOrigin: true,
            secure: false,
        },
        
        tsconfig: {
            configFile: "./tsconfig.json"
        }
    }

    // root's server+host wins over frontend!
    // inject rootConfig options into devServer!

    const rootConfig = loadJSONSafe(
        path.resolve(
            root,
            flags.servers
                ?? "skeleton-servers.json"
        )
    ) ?? {};

    const frontendServer = rootConfig?.servers?.frontend ?? {
            "host": "127.0.0.1", // default
            "port": 3000 // default
        };

    const devServer = {
        
        ...DEFAULT_CONFIG.devServer,
        ...rawConfig.devServer,

        // infrastructure overrides
        host: frontendServer.host,
        port: frontendServer.port,
    }

    // merge
    const configData = {

        ...DEFAULT_CONFIG,
        ...rawConfig,
        
        entry: {
            ...DEFAULT_CONFIG.entry,
            ...rawConfig.entry,
        },

        lib: {
            root: root,
            ...DEFAULT_CONFIG.lib,
            ...rawConfig.lib,
        },

        // scaffold!
        devServer: devServer,

        proxy: {
            ...DEFAULT_CONFIG.proxy,
            ...rawConfig.proxy,
        },
        tsconfig: {
            ...DEFAULT_CONFIG.tsconfig,
            ...rawConfig.tsconfig,
        }
    }

    // add a new paths entry to configData!
    configData.paths = {

        lib: {
            root: root,
            src: path.resolve(root, configData.lib.src),
            dist: path.resolve(root, configData.lib.dist),
            static: path.resolve(root, configData.lib.static),
        },

        entry: {
            main: path.resolve(configData.lib.src, `${configData.entry.main}`),
            index: path.resolve(configData.lib.src, `${configData.entry.index}.html`),
        },

        tsconfig: {
            configFile: path.resolve(root, `${configData.tsconfig.configFile}`),
        },
        
        cache: {
            // node_modules => restrict client to store in front-end!
            dir: path.resolve(root, "node_modules/.cache/webpack"),
        },
    }

    console.log(configData);

    return configData;
}