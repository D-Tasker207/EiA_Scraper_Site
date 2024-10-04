const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { optimize } = require('webpack');

module.exports = (env, argv) => {
    const isProduction = argv.mode === 'production';
    return {
        entry: './client/src/index.js',
        output: {
            path: path.resolve(__dirname, 'static/dist'),
            filename: 'bundle.js',
            publicPath: '/static/dist/'
        },

        devServer: {
            static: path.join(__dirname, 'static/dist'),
            compress: true,
            port: 3000,
            historyApiFallback: true,
            proxy: {
                '/api': {
                    target: 'http://localhost:5000',
                    changeOrigin: true
                },
                '/socket.io': {
                    target: 'http://localhost:5000',
                    ws: true
                },
            },
        },

        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env', '@babel/preset-react']
                        },
                    },
                },
                {
                    test: /\.css$/,
                    use: ['style-loader', 'css-loader'],
                },
                {
                    test: /\.(png|svg|jpg|jpeg|gif)$/i,
                    use: {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'images',
                        },
                    },
                },
            ],
        },

        devtool: isProduction ? 'source-map' : 'eval-source-map',

        plugins: [
            new HtmlWebpackPlugin({
                template: './client/public/index.html'
            }),
        ],

        resolve: {
            extensions: ['.js', '.jsx']
        },

        optimization: {
            minimize: isProduction,
        },
    };
};