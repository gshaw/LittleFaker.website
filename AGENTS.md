<!-- cspell:ignore DMARC ictool xcprivacy aedsim xcstrings vous -->

# Agent Notes

Background for AI agents working in this repo.

## What this is

The site for Little Faker, a menu bar app for macOS that copies placeholder text and fake
data, at [littlefaker.gshaw.ca](https://littlefaker.gshaw.ca). A Hugo site served by a
Cloudflare Worker (`littlefaker-website`) that has no script, only the built files. The
app lives in a separate repo, `LittleFaker`. Until 1.2 its pages were at
gshaw.ca/littlefaker/, which redirects here.

**The repo and the site are both public.** Anything committed here is published.

Keep it minimal. Don't add a theme, Hugo modules, pages or build steps unless asked. Every
template is in `layouts/`. Pico is the only styling, plus the screenshot's lines in `head.html`.

## Commands

```sh
mise run dev       # https://lf.dev.gshaw.ca, hugo on :4060 with live reload
mise run check     # build + spell + markdownlint + internal links
mise run deploy    # guard, check, push, wait for the build, verify
mise run verify    # curl the live site
mise run deploy-status  # is main live?
mise run shots     # crop the screenshot and og.jpg again from the App Store shots
```

**The dev URL is `https://lf.dev.gshaw.ca`**, on the Mac and the phone over the tailnet.
Caddy on lagoon forwards it to :4060, so give Gerry that URL to try a branch, never a
`ts.net` address or a port. One server owns it: `devhost serve lf`, run from your
checkout, stops whatever holds :4060 and runs the dev task there as a launchd job that
outlives your session (a background command stops at 2 hours). `devhost stop lf` ends it.
How it works: Workshop's `Tooling/one-dev-url.md`.

**Read the counts, not just the exit code.** lychee prints `N OK` and cspell
prints `Files checked: N`. A green run over zero files checked nothing.

## Deploys

Workers Builds builds every push. `main` runs `hugo` and `wrangler deploy` to
production; any other branch runs `wrangler preview`, which gives it a Preview URL
(`https://<branch>-littlefaker-website.gerry-shaw.workers.dev`) and a comment on its PR.
`wrangler.jsonc` serves `public/` with no script. The build runs
`hugo --cleanDestinationDir --panicOnWarning`, and the two build triggers each set
`HUGO_VERSION`, so a Hugo bump means changing `.mise.toml` and both triggers together.

**Deploy with `mise run deploy`**, never a bare `git push` to `main`.
`scripts/deploy-guard.sh` refuses unless the branch is `main`, the tree is clean and
`origin/main` isn't ahead. Then it runs `check`, pushes, waits for the "Workers Builds:
littlefaker-website" check run on the commit (`scripts/build-status.sh --wait`) and runs
`verify`. A merged PR also deploys. The rule and the list of sites are in
[Workshop's deploy note](https://github.com/gshaw/Workshop/blob/main/Tooling/deploy.md).

GitHub Actions runs `mise run -c check` on pushes and PRs. It doesn't block Cloudflare.

The domain is gshaw.ca's zone, which also carries Gerry's iCloud mail. Never touch its MX,
SPF, DKIM, DMARC or `apple-domain` records.

## Layout

- `hugo.toml` holds the site name, description, icon, Open Graph image, copyright start
  year and author. The layout reads them; don't hard-code them in HTML.
- `layouts/baseof.html` is the page shell. `layouts/_partials/head.html` has the meta and
  Open Graph tags and the screenshot's style; a page can override the description
  with `description:` and the preview image with `ogimage:` in front matter.
- `content/`: `_index.md` (the home page), `support.md`, `privacy.md`, `404.md`, each
  also as `<page>.de.md`, `.fr.md`, `.ja.md` and `.zh-hans.md`.
- The home page shows one screenshot, Contact, as `<figure class="shot">`, in the page's
  language. On a phone, CSS crops off the mostly empty left side.
- `static/` is published as it is: the icon (rendered from the app's `AppIcon.icon` with
  Icon Composer's `ictool`), the QR code, `og.jpg`, `pico.min.css` (Pico 1.5, copied in)
  and `screenshots/`.
- `scripts/shots.py` crops `static/screenshots/` and the `og` images from each language's
  App Store screenshots in the LittleFaker repo, with wallpaper added past the right edge so the
  rounded corners don't clip the menu bar.
- `public/` is build output and `tmp/` is scratch; both are gitignored.

## Languages

The site is in the app's five languages, with Hugo's multilingual mode: English at `/`,
then `/de/`, `/fr/`, `/ja/` and `/zh-hans/`, each in `hugo.toml`'s `[languages]` with
its description and `og.<lang>.jpg`. A page's translation is `<page>.<lang>.md`, the
template's words are in `i18n/<lang>.toml`, and the footer links each page's other
languages. No redirect by browser language. `mise run check` fails when a page or an
i18n key is missing in a language (`scripts/languages.sh`, and Hugo's
`--printI18nWarnings`). cspell checks English only.

The words are the app's: `Localizable.xcstrings` and `Docs/app-store/<locale>/` in the
LittleFaker repo, following its `Docs/translation.md` (du in German, vous in French, a
non-breaking space before French `:`, `!` and `?`, 拷贝 and 你 in Chinese). The privacy
page says in each language that it is a translation and the English one counts.

Hugo doesn't run template code inside Markdown files: a loop over data goes in a
shortcode in `layouts/_shortcodes/`. A link with spaces needs angle brackets:
`[text](<mailto:x?subject=A B>)`.

## Writing

Write as Gerry: first person, plain words, short sentences. Feature bullets are fragments
with no full stop, as on landnav.app and aedsim.com. The text follows the App Store copy in the LittleFaker repo (`Docs/app-store/en-US/`).
Keep the facts the same: languages, the eight countries, the phone ranges kept for
fiction, macOS 15 or later, three tips with nothing locked. The privacy page says the app
collects nothing and has no network access of its own; check that against the app's
entitlements and `PrivacyInfo.xcprivacy` when either changes.

## Suppressions

Suppress a check inline, with a reason, in the file that provoked it:
`<!-- cspell:ignore word -->` or `<!-- markdownlint-disable-next-line MD0xx -->`. Move a
word to `cspell.config.yaml` only once a second file needs it.

## Branches, issues and PRs

- Branch names are flat and short: `<issue>-<slug>`, no `claude/` prefix.
- Issue and PR bodies aren't hard-wrapped.
- Squash-merge only.
