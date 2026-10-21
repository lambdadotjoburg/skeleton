// import webpack from "webpack";

import HtmlWebpackPlugin from "html-webpack-plugin";
import CopyWebpackPlugin from "copy-webpack-plugin";
import TsconfigPathsPlugin from "tsconfig-paths-webpack-plugin";

// import MiniCssExtractPlugin from "mini-css-extract-plugin";
// import { createTransformer } from "@skeleton/transformer";

export default (config) => (
    {
        context: config.paths.lib.src,
        /**
         * NOTE: LOAD BEFORE DECORATORS!
         * inject reflect-metadata ("adcanced")
         * https://cdnjs.com/libraries/reflect-metadata
         */
        entry: [
            `./${config.entry.main}`, // relative to context
            /**
             * if client needs reflect-metadata
             * it would have to be installed in
             * frontend package
             * This line can be included here
             * or at the top of main.ts entry!
             */
            // "reflect-metadata",
        ],
        resolve: {
            extensions: [".tsx", ".ts", ".jsx", ".js"],
            plugins: [
                new TsconfigPathsPlugin(
                    {
                        configFile: config.paths.tsconfig.configFile
                    },
                ),
            ],
        },
        module: {
            rules: [
                // {
                //     test: /\.(ts|js)x?$/, // allow .ts & .tsx
                //     use: {
                //         loader: "ts-loader",
                //         options: {
                            
                //             // transpileOnly: true, // FALSE!
                //             compilerOptions: {
                //                 noEmit: false,
                //             },

                //             // getCustomTransformers:
                //             // (_program, getProgram) => (
                //             //     {
                //             //         before: [
                //             //             createTransformer(
                //             //                 // program,
                //             //                 getProgram,
                //             //             ),
                //             //         ],
                //             //     }
                //             // )
                //         },
                //     },
                //     exclude: [
                //         /node_modules/,
                //         /dist/ // exclude dist folder!
                //     ],
                // },

                {
                    test: /\.(ts|js)x?$/,
                    use: [
                        ...(config.framework === "solid"
                            ? [
                                {
                                    loader: "babel-loader",
                                    options: {
                                        presets: ["babel-preset-solid"],
                                    },
                                },
                            ]
                            : []),
                        {
                            loader: "ts-loader",
                            options: {
                                // transpileOnly: true, // FALSE!
                                compilerOptions: {
                                    noEmit: false,
                                },
                            },
                        },
                    ],
                    exclude: [
                        /node_modules/,
                        /dist/,
                    ],
                },

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
                {
                    test: /\.css$/,
                    exclude: /\.module\.css$/,
                    use: [
                        // order matters
                        "style-loader", // inject css into DOM
                        // MiniCssExtractPlugin.loader,
                        "css-loader" // resolve imports inside CSS
                    ],
                },                
                {
                    test: /\.(png|jpg|jpeg|ico|gif)$/i,
                    type: "asset/resource",
                    generator: {
                        // preserve file names for .png, .jpg images!
                        filename: "[path][name][ext]",
                    },
                },
                {
                    test: /\.(woff2?|eot|ttf|otf)$/i,
                    type: "asset/resource",
                    generator: {
                        // preserve file names!
                        filename: "[path][name][ext]",
                    },
                },
                // requires "svg-inline-loader": "^0.8.2",
                // {
                //     test: /\.svg$/i,
                //     resourceQuery: /inline/,
                //     use: [
                //         "svg-inline-loader",
                //     ],
                // },
                {
                    test: /\.svg$/i,
                    type: "asset/resource",
                    generator: {
                        // preserve file names!
                        filename: "[path][name][ext]",
                    },
                },
            ],
        },
        output: {
            path: config.paths.lib.dist,
            filename: `${config.entry.main}.js`,
            publicPath: "/",
            clean: true,
        },
        plugins: [

            // // to preserve css folder structure
            // new MiniCssExtractPlugin(
            //     {
            //         filename: "[name].css",
            //     }
            // ),
            
            /** inject main.js script element into index.html */
            new HtmlWebpackPlugin(
                {
                    template: config.paths.entry.index,
                    filename: `${config.entry.index}.html`,
                    inject: "body",
                },
            ),

            /** copy static assets from src to dist */
            new CopyWebpackPlugin(
                {
                    patterns: [
                        {
                            from: config.paths.lib.static,
                            to: "static",// `${config.paths.lib.static}`, // relative to output.path
                            /**
                             * Alternatively, check whether static directory exists!
                             */
                            noErrorOnMissing: true,
                        },
                    ],
                }
            ),
            
            /** For custom jsx h function! */
            // new webpack.ProvidePlugin(
            //     {
            //         h: ["@core/jsx", "h"],
            //         Fragment: ["@core/jsx", "Fragment"],
            //     },
            // ),
        ],
        
        // cache: false,
        cache: {
            type: "filesystem",
            cacheDirectory: config.paths.cache.dir,
        },
    }
);