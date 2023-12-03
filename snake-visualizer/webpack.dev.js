const {merge} = require('webpack-merge');
const webpackConfig = require('./webpack.config.js');

module.exports = merge(webpackConfig, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
        port: 3001,
        hot: true,
        open: true,
        client: {
            overlay: false,
        },
    }
});

