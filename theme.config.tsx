import React from "react";
import { DocsThemeConfig } from "nextra-theme-docs";

const config: DocsThemeConfig = {
  logo: <span>LangChain in Action</span>,
  project: {
    link: "https://github.com/deepakkamboj/langchain-in-action",
  },
  chat: {
    link: "https://discord.com",
  },
  docsRepositoryBase: "https://github.com/deepakkamboj/langchain-in-action",
  footer: {
    text: "Nextra Docs Template",
  },
};

export default config;
