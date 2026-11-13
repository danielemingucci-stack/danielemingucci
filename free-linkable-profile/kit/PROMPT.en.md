# Installation prompt

Copy all the text below and paste it to your AI assistant (Claude, ChatGPT, Gemini…), together with the kit folder and whatever you have to describe yourself: a résumé, the PDF of your LinkedIn profile, or just a couple of lines written by you.

---

I want to publish a professional profile on my own website using the **Free Linkable Profile** kit, which I am attaching. The kit contains:

- `profile.json`: my data, in the JSON Resume format plus an `flp` block;
- `build.py`: generates `index.html` from `profile.json` (Python 3, no libraries); it can also build a showcase, host several profiles and handle a change of address (see `README.md`);
- `flp.css` and `flp.js`: styling and mutual recognition between profiles;
- `README.md` and `SPEC.md`: instructions and the rules of the format (in Italian; `SPEC.en.md` is the English specification).

Do these things, in this order:

1. **Ask me for the missing data**, one section at a time: name, one-line headline, city, contact email, two or three sentences of introduction, experience (role, company, start, end), education, skills, languages, and whatever I have among publications, patents, projects, certifications, awards, volunteering. If I attached a résumé or a PDF, take the data from there and only ask me to confirm. **Do not make anything up**: whatever I don't know or don't tell you stays empty.
2. **Ask me for the address** where the profile will live on my site (for example `https://www.mysite.com/profile/`) and put it in `flp.url`. Also ask me, if I have them, for the address of a photo of me, of a cover image, of the feed of my articles (`flp.feed`) and of the page to subscribe to my newsletter (`flp.follow`).
3. **Adapt colours and fonts** in `flp.theme` to those of my site: ask me for them, or read them from the site if I point you to it. Set `"lang": "en"` in `flp` so the labels are in English.
4. **Ask me for my connections**: people I know who also have a profile of this kind. For each one I need a name and the address of their profile, to go in `flp.connections`.
5. **Fill in `profile.json`**, check that it is valid JSON, then run `python3 build.py` and show me the result.
6. **Tell me how to upload it** to my site: the four files `index.html`, `profile.json`, `flp.css`, `flp.js` go in the same folder, at the address chosen in step 2. Ask me what my site is built on (WordPress, GitHub Pages, Netlify, FTP hosting…) and give me the exact steps for that case.
7. **Check one last thing**: for other profiles to recognise mine, `profile.json` must be readable from other sites (header `Access-Control-Allow-Origin: *`). Tell me whether my hosting already does this, or how to turn it on.

If I don't have a site of my own, tell me before starting and suggest the possible routes: being hosted by someone who already has this kit (hosting mode), or a free host such as GitHub Pages. If I want to show the same profile on a second site as well, use showcase mode. If I am changing address, follow the moving procedure.

Rules: the profile is mine and stays on my site. Do not add external services, tracking or scripts beyond those in the kit. When I ask you to update the profile in the future, edit only `profile.json` and regenerate `index.html`.
