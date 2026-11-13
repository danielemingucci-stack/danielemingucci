# Free Linkable Profile — specification 0.2

A professional profile that lives on the website of the person who writes it, readable by
people, by search engines and by other profiles. No platform in between.

It is not a new protocol: it puts together open standards that already exist.

## 1. A profile is a page and a file

Every profile has an address, for example `https://www.mysite.com/profile/`, where you find:

- `index.html` — the page for people and for search engines;
- `profile.json` — the same data, for machines.

The page declares the file with:

```html
<link rel="alternate" type="application/json" title="Free Linkable Profile" href="profile.json">
```

By convention `profile.json` sits in the same folder as the page. Whoever keeps it elsewhere
says so in the connection (see section 3, `json` field).

## 2. The data format

`profile.json` follows the [JSON Resume](https://jsonresume.org/schema) 1.0.0 schema
(`basics`, `work`, `education`, `skills`, `languages`, `publications`, `projects`,
`certificates`, `awards`, `volunteer`), with two additions:

- `patents`: a list of patents (`name`, `office`, `number`, `date`, `url`, `summary`);
- `flp`: the block that turns a résumé into a linkable profile.

```json
"flp": {
  "version": "0.2",
  "lang": "en",
  "url": "https://www.mysite.com/profile/",
  "feed": "https://www.mysite.com/feed.xml",
  "follow": "https://…/subscribe",
  "cover": "https://www.mysite.com/cover.jpg",
  "theme": { "accent": "#7E6034", "background": "#F2F1ED", "card": "#FFFFFF",
             "ink": "#121212", "muted": "#57564F", "font": "…", "titleFont": "…" },
  "connections": [
    { "name": "First Last", "url": "https://www.othersite.com/profile/" }
  ]
}
```

`flp.url` is the identity of the profile: it is the address others write in order to connect.
A profile has one identity only, even when it is shown on several sites (section 7) or
hosted on someone else's site (section 8).

## 3. Connections

A connection is an entry in `flp.connections` with `name` and `url` (the address of the other
person's profile). Optional: `json`, the address of their `profile.json` if it is not in the
page's folder.

**A connection is mutual when each of the two profiles lists the other's address.**
Nobody certifies it: each page checks for itself, by reading the other site's `profile.json`.
The comparison ignores `http/https`, `www.`, upper case and the trailing slash.

A one-way connection stays visible, marked as "awaiting confirmation". An address that does
not expose a readable profile remains a plain link.

In the page, connections carry `rel="contact"`, and one's own other profiles `rel="me"`.

## 4. Being readable by other profiles

For a page on another site to read `profile.json`, the server must answer with

```
Access-Control-Allow-Origin: *
```

GitHub Pages already does. On other hosts it is added in the header settings (a `_headers`
file on Netlify and Cloudflare Pages, `.htaccess` on Apache).

`profile.json` is public by definition: it holds only what you want to show.

## 5. Being found

Search is done by search engines. The page carries:

- schema.org `ProfilePage` + `Person` structured data (name, headline, organisations,
  education, languages, `sameAs`, `knows`);
- `h-card` microformats (`p-name`, `p-job-title`, `u-photo`, `u-url`, `u-email`);
- a `title` with first and last name, a `description`, a canonical address.

## 6. Following

`flp.feed` is the feed (Atom or RSS) of what the person publishes. `flp.follow` is a page
where one can subscribe to receive it by email. The "Follow" button leads to `follow`, or
failing that to `feed`.

## 7. Showcase: the same profile on several sites

A profile can also be shown on other sites, without copying its data. A showcase is a page
that, on every visit, reads the original's `profile.json` and draws it:

```html
<link rel="canonical" href="https://www.mysite.com/profile/">
<main data-flp-showcase="https://www.mysite.com/profile/"></main>
```

Rules:

- the showcase declares the original with `rel="canonical"` and shows it plainly in the page,
  so that search engines attribute the name to one address only;
- the showcase has no `profile.json` of its own and is not an identity: connections are
  always made to the original, and mutuality is computed with respect to the original;
- if the original cannot be reached, the showcase shows only the link.

## 8. Hosting: several profiles on the same site

Someone without a website can be hosted by someone who has one: a person, a company, an
association. Each hosted profile sits in its own folder, with its page and its
`profile.json`, and has that address as its identity:

```
/profiles/                 list of the people hosted
/profiles/anna-bianchi/    index.html + profile.json
/profiles/luca-verdi/      index.html + profile.json
```

The folder name uses only lower-case letters, digits and hyphens. The list is a schema.org
`CollectionPage`. An optional `ospiti.json` file in the folder gives its title, introductory
text, address and theme (`title`, `intro`, `url`, `lang`, `theme`).

The profile still belongs to the person: it is a file, and whoever is hosted can take it
elsewhere whenever they want (section 9). The host undertakes, if the person leaves, to keep
the moving notice at the old address.

## 9. Moving

When a profile changes address:

- **at the old address** a `profile.json` remains with `flp.movedTo`, the new address; the
  page becomes a notice that leads there and declares it as `canonical`;
- **in the new profile**, `flp.previous` lists the old addresses.

```json
"flp": { "url": "https://www.oldsite.com/profile/", "movedTo": "https://www.newsite.com/profile/" }
"flp": { "url": "https://www.newsite.com/profile/", "previous": ["https://www.oldsite.com/profile/"] }
```

**A move is valid only if confirmed on both sides**: the old address declares `movedTo` and
the new one lists the old one in `previous`. One of the two is not enough: nobody can take
over someone else's address by declaring it their own, and nobody can redirect a profile to
an address that does not acknowledge it.

Whoever reads a profile that has moved follows the new address (three hops at most):

- the page does it on every visit, and shows the right link straight away;
- the generator does it on every run, and **rewrites the address in its own
  `profile.json`**. From then on the connection no longer depends on the old site.

No message travels between people: each profile checks for itself, by reading public files.
A moving notice received by email or chat must never be acted on; regenerating the profile
is enough. The notice at the old address should stay up long enough for connected people to
regenerate their page at least once (one year is recommended).

## 10. What is not in 0.2

- Real-time notifications between sites (to be done with [Webmention](https://www.w3.org/TR/webmention/)).
- A feed that gathers the posts of one's connections.
- Private messages, recommendations, skill endorsements.

## 11. Security for implementers

Data read from other people's profiles is untrusted text: it must be inserted into the page
as text, never as HTML. Image addresses are accepted only if `https:`. Links are accepted
only if `http(s):` or `mailto:`.
