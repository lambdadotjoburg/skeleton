
import path from "path";
import loadJSONSafe from "./loadJSONSafe.js";

export default function createConfig(flags = {}) {

    // Frontend root supplied by the Skeleton CLI.
    const root = flags.root;

    if (!root) {
        throw new Error(
            "Missing frontend root directory in Webpack configuration."
        );
    }

    // Load the client's required frontend configuration.
    const configPath = path.resolve(
        root,
        flags.config ?? "../skeleton-config.json"
    );

    const rawConfig = loadJSONSafe(configPath);

    if (
        rawConfig === null ||
        typeof rawConfig !== "object" ||
        Array.isArray(rawConfig)
    ) {
        throw new Error(
            `Required Skeleton configuration not found or invalid: ${configPath}`
        );
    }

    // Load the project's required server configuration.
    const serversPath = path.resolve(
        root,
        flags.servers ?? "../skeleton-servers.json"
    );

    const rootConfig = loadJSONSafe(serversPath);

    if (
        rootConfig === null ||
        typeof rootConfig !== "object" ||
        Array.isArray(rootConfig)
    ) {
        throw new Error(
            `Required Skeleton servers configuration not found or invalid: ${serversPath}`
        );
    }

    // Defaults fill in optional settings only.
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
            // Direct frontend development may open a browser.
            // Skeleton's gateway startup controls gateway browser opening.
            open: true,
            historyApiFallback: false,
            host: "127.0.0.1",
            port: 3000,
            hot: true,
            overlay: true,
        },

        // Optional proxy for direct frontend development.
        // This is separate from Skeleton's Python gateway.
        proxy: {
            on: false,
            host: "127.0.0.1",
            port: 8081,
            changeOrigin: true,
            secure: false,
        },

        tsconfig: {
            configFile: "./tsconfig.json",
        },
    };

    // The project's server configuration owns the frontend
    // development server's host and port.
    const frontendServer = rootConfig?.servers?.frontend;

    if (
        !frontendServer ||
        typeof frontendServer.host !== "string" ||
        !Number.isInteger(frontendServer.port) ||
        frontendServer.port < 1 ||
        frontendServer.port > 65535
    ) {
        throw new Error(
            `Invalid or missing servers.frontend host/port in ${serversPath}`
        );
    }

    const devServer = {
        ...DEFAULT_CONFIG.devServer,
        ...rawConfig.devServer,

        // Infrastructure settings take precedence.
        host: frontendServer.host,
        port: frontendServer.port,
    };

    // Merge client configuration with optional defaults.
    const configData = {

        ...DEFAULT_CONFIG,
        ...rawConfig,

        entry: {
            ...DEFAULT_CONFIG.entry,
            ...rawConfig.entry,
        },

        lib: {
            root,
            ...DEFAULT_CONFIG.lib,
            ...rawConfig.lib,
        },

        devServer,

        proxy: {
            ...DEFAULT_CONFIG.proxy,
            ...rawConfig.proxy,
        },

        tsconfig: {
            ...DEFAULT_CONFIG.tsconfig,
            ...rawConfig.tsconfig,
        },
    };

    // Resolve paths relative to the frontend directory.
    configData.paths = {

        lib: {
            root,
            src: path.resolve(root, configData.lib.src),
            dist: path.resolve(root, configData.lib.dist),
            static: path.resolve(root, configData.lib.static),
        },

        entry: {
            main: path.resolve(
                root,
                configData.lib.src,
                configData.entry.main
            ),

            index: path.resolve(
                root,
                configData.lib.src,
                `${configData.entry.index}.html`
            ),
        },

        tsconfig: {
            configFile: path.resolve(
                root,
                configData.tsconfig.configFile
            ),
        },

        // Keep Webpack's cache inside the frontend project.
        cache: {
            dir: path.resolve(
                root,
                "node_modules/.cache/webpack"
            ),
        },
    };

    console.log(configData);

    return configData;
}
