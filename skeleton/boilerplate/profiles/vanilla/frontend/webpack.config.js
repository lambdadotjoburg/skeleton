import fs from "node:fs";

import path from "node:path";

import HtmlWebpackPlugin from "html-webpack-plugin";

import TsconfigPathsPlugin from "tsconfig-paths-webpack-plugin";

import CopyWebpackPlugin from "copy-webpack-plugin";

export default (env = {}) => {

    console.log(env["custom-client-env-var"])

    const mode = {
        development: "development",
        production: "production",
        preview: "production",
    }[env.mode ?? "development"]?? "none";
        
    const root = path.resolve(env.root ?? process.cwd());

    const project = JSON.parse(
        fs.readFileSync(
            path.join(
                root, "config",
                "skeleton-project.json"
            ), "utf-8",
        ),
    );

    const frontend = path.resolve(
        root, project.frontend.dir,
    );

    console.log("Starting webpack server ...");

    return {

        mode: mode, 

        entry: path.resolve(
            frontend,
            project.frontend.lib.src,
            project.frontend.lib.main,
        ),

        output: {
            path: path.resolve(
                frontend,
                project.frontend.build.outdir,
            ),
            filename: "bundle.js",
            publicPath: "/",
            clean: true,
        },

        resolve: {
            extensions: [".ts", ".js"],

            plugins: [
                new TsconfigPathsPlugin(
                    {
                        configFile: path.resolve(
                            frontend,
                            project.frontend.config.tsconfig,
                        ),
                    }
                ),
            ],
        },

        module: {
            rules: [
                {
                    test: /\.ts$/,
                    exclude: [
                        /node_modules/,
                        path.resolve(
                            frontend,
                            project.frontend.build.outdir
                        ),
                    ],
                    use: {
                        loader: "ts-loader",
                        options: {
                            compilerOptions: {
                                noEmit: false,
                            }
                        }
                    }
                },

                // CSS modules
                {
                    test: /\.module\.css$/,
                    use: [
                        "style-loader",
                        {
                            loader: "css-loader",
                            options: {
                                modules: {
                                    localIdentName: "[local]__[hash:base64:5]",
                                },
                                esModule: false,
                            },
                        },
                    ],
                },

                // Ordinary CSS
                {
                    test: /\.css$/,
                    exclude: /\.module\.css$/,
                    use: [
                        "style-loader",
                        "css-loader",
                    ],
                },

                // Images
                {
                    test: /\.(png|jpg|jpeg|ico|gif)$/i,
                    type: "asset/resource",
                    generator: {
                        filename: "[path][name][ext]",
                    },
                },

                // Fonts
                {
                    test: /\.(woff2?|eot|ttf|otf)$/i,
                    type: "asset/resource",
                    generator: {
                        filename: "[path][name][ext]",
                    },
                },

                // SVG
                {
                    test: /\.svg$/i,
                    type: "asset/resource",
                    generator: {
                        filename: "[path][name][ext]",
                    },
                },
            ],
        },

        plugins: [
            
            new HtmlWebpackPlugin(
                {
                    template: path.resolve(
                        frontend,
                        project.frontend.lib.src,
                        `${project.frontend.lib.index}.html`,
                    ),
                }
            ),

            new CopyWebpackPlugin(
                {
                    patterns: [
                        {
                            from: path.resolve(
                                frontend,
                                project.frontend.lib.src,
                                project.frontend.lib.static,
                            ),

                            // conditionally, copy to dist
                            to: project.frontend.lib.static,
                            noErrorOnMissing: true,
                        },
                    ],
                }
            ),
        ],

        cache: {
            type: "filesystem",
        },

        devServer: {
        
            // devtool: "cheap-module-source-map",
            // devtool: "source-map", // prod

            hot: true,

            open: false,
            
            historyApiFallback: true,

            client: {

                overlay: {
                    errors: true,
                    warnings: true,
                    runtimeErrors: true
                },
            },

            static: {
                            
                directory: path.resolve(
                    frontend,
                    project.frontend.lib.src,
                    project.frontend.lib.static,
                ),
                
                publicPath: `/${project.frontend.lib.static}`,
            },

            host: env.host,
            port: Number(env.port),
        },
    };
};