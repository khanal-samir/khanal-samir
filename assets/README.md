# Profile assets

The banner is a self-contained dark SVG: a large name beside embedded TypeScript, React, and Node.js brand marks, with a rotating React mark and moving connection lines. The dark background stays the same in every GitHub theme. The name does not animate away. An animation-free SVG is selected through `<picture>` when the browser requests reduced motion; the animated SVG also respects that preference internally.

Badges use compact 18px SVG icons in 38px-high frames, with reduced padding. Labels retain the larger 18px type for readability. All graphics remain vector-sharp when scaled.

Badges use locally embedded brand icons rather than remote badge services. Exact upstream URLs are recorded in `icon-sources.json`. Logos and trademarks belong to their respective owners; their inclusion indicates tools, not endorsement.

Icon sources:
- [Simple Icons](https://github.com/simple-icons/simple-icons): CC0 icons, subject to individual brand guidelines.
- [Devicon](https://github.com/devicons/devicon): MIT-licensed icon collection. [License](https://github.com/devicons/devicon/blob/master/LICENSE).
- [Lobe Icons](https://github.com/lobehub/lobe-icons): MIT-licensed OpenAI icon. [License](https://github.com/lobehub/lobe-icons/blob/master/LICENSE).
- [Lucide](https://github.com/lucide-icons/lucide): ISC-licensed globe and mail icons. See `LICENSE-lucide.txt`.
- Mastra, OpenCode, and Pi: brand marks from their official websites or repositories, linked in the source manifest. Respect their upstream terms and brand guidelines.

## Maintenance

From the repository root, with Python 3 installed (no additional packages needed):

```sh
python3 scripts/generate-assets.py
python3 scripts/check-profile.py
```

The generator downloads icons only when regenerating; viewing the profile does not contact those upstream sources. SVG text uses local system fonts, with no external font requests. Animation uses CSS inside the SVG image, not JavaScript or CSS injected into the README.

The README keeps the original introduction, stack categories, social badges, and collaboration note, adding the requested AI tools and Jest. No feed updater, external badge service, JavaScript, or custom CSS is required.
