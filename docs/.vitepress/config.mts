import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'ja',
  title: 'Overclocked 日本語訳',
  description:
    'Cory Doctorow 著 Overclocked: Stories of the Future Present の日本語訳。CC BY-NC-SA 2.5 ライセンスの英語版をもとにした翻訳プロジェクトです。',

  base: '/overclocked-ja/',

  head: [
    ['meta', { name: 'author', content: 'Cory Doctorow (原著); 翻訳: 高須正和 / TAKASU Masakazu' }],
    ['script', { async: '', src: 'https://www.googletagmanager.com/gtag/js?id=G-E0N88X4QBG' }],
    [
      'script',
      {},
      "window.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('config', 'G-E0N88X4QBG');",
    ],
  ],

  themeConfig: {
    siteTitle: 'Overclocked 日本語訳',

    nav: [
      { text: 'ホーム', link: '/' },
      { text: 'クレジット', link: '/credits' },
      { text: 'ライセンス', link: '/license' },
      {
        text: '翻訳方針',
        link: 'https://github.com/Nico-Tech-Shenzhen/overclocked-ja/blob/main/TRANSLATION_GUIDE.md',
      },
    ],

    sidebar: [
      {
        text: '短編',
        items: [
          { text: 'Printcrime', link: '/ja/printcrime' },
          { text: 'When Sysadmins Ruled the Earth', link: '/ja/when-sysadmins-ruled-the-earth' },
          { text: "Anda's Game", link: '/ja/andas-game' },
          { text: 'I, Robot', link: '/ja/i-robot' },
          { text: 'I, Row-Boat', link: '/ja/i-row-boat' },
          { text: 'After the Siege', link: '/ja/after-the-siege' },
        ],
      },
      {
        text: '情報',
        items: [
          {
            text: '翻訳方針',
            link: 'https://github.com/Nico-Tech-Shenzhen/overclocked-ja/blob/main/TRANSLATION_GUIDE.md',
          },
          { text: 'コンテンツライセンス', link: '/license' },
          { text: 'クレジット', link: '/credits' },
        ],
      },
    ],

    footer: {
      message:
        '高須正和（@tks）による日本語訳です。原著は Cory Doctorow に帰属します。',
      copyright:
        '翻訳テキスト © 翻訳者 | 原著 © 2007 Cory Doctorow | CC BY-NC-SA 2.5',
    },

    editLink: {
      pattern: 'https://github.com/Nico-Tech-Shenzhen/overclocked-ja/edit/main/docs/:path',
      text: 'このページを編集',
    },
  },

  markdown: {
    lineNumbers: false,
  },
})
