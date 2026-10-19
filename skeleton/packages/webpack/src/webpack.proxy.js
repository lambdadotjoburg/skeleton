/**
 * mainly for quick dev to avoid CORS errors!
 * mainly applicable for frontend-first dev!
 */
export default (config) => (
    {
        devServer: {
            /**
             *  merge proxy server into config if command line arg provided, used like:
             * "start": "webpack serve --config webpack/webpack.config.js --env scaffold=true --env mode=dev --open",
             */
            proxy: [
                {
                    context: () => true,
                    target: `http://${config.proxy.host}:${config.proxy.port}`,
                    changeOrigin: config.proxy.changeOrigin,
                    secure: config.proxy.secure,
                }
            ]
        }
    }
);
