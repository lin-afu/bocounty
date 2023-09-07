const path = require("path");

module.exports = {
  entry: "./jsx/enter_point.jsx",
  mode: "development",
  watch: true,
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "src/js"),
  },
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [["@babel/preset-react", { targets: "defaults" }]],
          },
        },
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
};
