import path from "path";

import { merge } from "webpack-merge";

import createConfig from "./config.js";
// import { server } from "typescript";

export const toBool = (v) => v === true || v === "true";

export default async (env = {}) => {

    // log command line args for visual output!
    console.log("ENV:", env)

    // collect command line args/flags
    const flags = {

        root: path.resolve(env.root ?? "."),

        proxy: toBool(env.proxy) === true,
        mode: env.mode === "dev" ? "dev" : "prod",

        servers: env.servers,
        config: env.config,
    }

    // log parsed flags for visual output!
    // console.log("FLAGS:", flags)

    // collect config data/info
    const config = createConfig(flags);

    // log config data for visual output!
    // console.log("CONFIG", config)
    
    // activate features, depending on mode
    const envModule = await import(`./webpack.${flags.mode}.js`);
    const envConfig = envModule.default(config);

    // compose config data
    const commonModule = await import(`./webpack.common.js`);
    const commonConfig = await commonModule.default(config);
    let monoConfig = merge(commonConfig,envConfig);

    // activate features, depending on options (proxy)
    const useProxy = (flags.proxy !== undefined)
        ? flags.proxy : config.proxy.on;

    /**
     * Handle proxy settings
     */
    if (useProxy) {
        const proxyModule = await import(`./webpack.proxy.js`);
        const proxyConfig = proxyModule.default(config);
        monoConfig = merge(monoConfig, proxyConfig);
    }

    return monoConfig;
};