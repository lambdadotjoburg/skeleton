export default (config) => (
    {
        // top-level attributes!
        mode: "development",
        devtool: "cheap-module-source-map",

        devServer: {

            // whether to open browser!
            open: config.devServer.open,

            static: config.paths.lib.dist,
            
            // if 404 => return index.html
            // (prevents refresh issues!)
            // most times, it's better to see 404!
            historyApiFallback: config.devServer.historyApiFallback,
    
            host: config.devServer.host,
            port: config.devServer.port,
    
            hot: config.devServer.hot, // hot-reload on change!
    
            client: {
                // pretty errors
                overlay: config.devServer.overlay,
            },
        }
    }
)