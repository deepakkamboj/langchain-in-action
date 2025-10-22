const withNextra = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
});

module.exports = withNextra({
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  // Set basePath for GitHub Pages (repository name)
  basePath: process.env.NODE_ENV === "production" ? "/langchain-in-action" : "",
  assetPrefix:
    process.env.NODE_ENV === "production" ? "/langchain-in-action/" : "",
});
