import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * RAG Tricks Quartz configuration.
 *
 * The deployment workflow copies this file into a pinned Quartz v4.5.2
 * checkout before building. Keep this file compatible with that pinned
 * engine revision; upgrade the engine and config together.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "RAG Tricks",
    pageTitleSuffix: " · RAG 工程知识库",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "zh-CN",
    baseUrl: "1998x-stack.github.io/rag-tricks",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Sans SC",
        body: "Noto Sans SC",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#fafafa",
          lightgray: "#e8e8e8",
          gray: "#b5b5b5",
          darkgray: "#4a4a4a",
          dark: "#202124",
          secondary: "#2563eb",
          tertiary: "#0f766e",
          highlight: "rgba(37, 99, 235, 0.12)",
          textHighlight: "#fef08a88",
        },
        darkMode: {
          light: "#15171a",
          lightgray: "#30343a",
          gray: "#656b73",
          darkgray: "#d4d7dc",
          dark: "#f3f4f6",
          secondary: "#7aa2ff",
          tertiary: "#5eead4",
          highlight: "rgba(122, 162, 255, 0.14)",
          textHighlight: "#a1620788",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
