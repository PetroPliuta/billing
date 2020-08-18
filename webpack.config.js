"use strict";
const path = require("path");

module.exports = {
  entry: "./frontend/index.js",
  mode: "development",
  output: {
    path: path.join(__dirname, "/static"),
    filename: "webpack.bundle.js",
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/,
        use: [
          "style-loader",
          {
            loader: "css-loader",
            options: {
              modules: true,
            },
          },
        ],
      },
    ],
  },
};
