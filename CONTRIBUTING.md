# Adding a theme

Thanks for sharing a theme. To add one:

1. [Fork this repository](https://github.com/maxtrax04/outpost-themes/fork).
2. Make a folder named after your GitHub username, in lowercase (`MyName` becomes `myname/`), and put
   your theme in a folder inside it: `myname/my-theme/`. Folder names use lowercase letters, numbers, and
   hyphens. Your theme is then called `myname/my-theme`.
3. In the theme folder, add:
   - `theme.css`, starting with a comment that names the theme:
     `/* My Theme: what it looks like */`. The name (up to 40 characters) is what the theme button shows.
   - `README.md`: what the theme looks like, anything special about it, and how to use it.
   - `screenshot.jpg` (or `.png`, under 1 MB): the dashboard at 1280 × 800 is a good size.
   - Any images and fonts the theme uses.
4. Add a row for your theme to the table in [README.md](README.md).
5. Open a pull request. The checks run on it automatically; a theme is reviewed before it's added.

How to make a theme, and every token and hook a theme can use, is in Outpost's
[theme guide](https://github.com/maxtrax04/outpost/blob/main/docs/themes.md).

## Rules

- **Original work only.** No names, logos, characters, artwork, or fonts from games, films, TV, or other
  brands, even renamed. A theme can be inspired by a style (a 1950s television, a newsroom, a field
  computer), but not copy a specific product's look.
- **Only theme files.** CSS, fonts (`.woff2`, `.woff`, `.ttf`, `.otf`), and images (`.png`, `.jpg`, `.jpeg`,
  `.gif`, `.webp`, `.avif`, `.svg`), plus your README and font license files. Outpost serves nothing else.
- **Nothing from other sites.** Outpost's security rules block fonts, images, and stylesheets from other
  sites, and `data:` URLs, so put every file in your theme's folder.
- **Fonts need a license that allows sharing them** (such as the SIL Open Font License), with the license
  file in your theme's folder.
- **Readable and calm.** Text stays readable over any decoration, and the theme respects
  [reduced effects](https://github.com/maxtrax04/outpost/blob/main/docs/themes.md#reduced-effects): turn off
  your own animations and busy effects when `:root[data-effects="reduced"]` is set.
- **Shared under the MIT License**, like the rest of this repository.

## Building on another theme

- On a theme built into Outpost (such as `atomic-broadcast` or `field-station`), reach it two folders up:
  `@import url("../../atomic-broadcast/theme.css");`. Images from it work the same way.
- On another of your own themes, reach it one folder up: `@import url("../my-theme/theme.css");`. When
  someone downloads your theme, Outpost brings that one along.

## Trying your theme

Mount your fork as Outpost's custom themes folder (`- ./outpost-themes:/config/themes:ro`), restart the
container, and pick your theme with the theme button, or open `http://localhost:8088/?theme=myname/my-theme`.
Edits to the CSS show up when you reload the page. To see how alerts look, run Outpost with
`OUTPOST_PROVIDER=mock` and `OUTPOST_MOCK_ALERTS=true`.

To run the same checks as the pull request: `python3 .github/scripts/check_themes.py`.
