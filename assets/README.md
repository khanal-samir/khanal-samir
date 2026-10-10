# Profile assets

The hero illustrations and animations were created for this profile. A glowing trace follows a Nepal-inspired mountain ridge, with a coordinated moving underline. The name stays readable throughout the smooth loop. Light and dark variants are included, along with still images selected through `<picture>` sources when the browser requests reduced motion.

Badges use locally embedded brand icons rather than remote badge services. Exact upstream URLs are recorded in `icon-sources.json`. Logos and trademarks belong to their respective owners; their inclusion indicates tools, not endorsement.

Icon sources:
- [Simple Icons](https://github.com/simple-icons/simple-icons): CC0 icons, subject to individual brand guidelines.
- [Devicon](https://github.com/devicons/devicon): MIT-licensed icon collection. [License](https://github.com/devicons/devicon/blob/master/LICENSE).
- [Lobe Icons](https://github.com/lobehub/lobe-icons): MIT-licensed OpenAI icon. [License](https://github.com/lobehub/lobe-icons/blob/master/LICENSE).
- [Lucide](https://github.com/lucide-icons/lucide): ISC-licensed globe and mail icons. See `LICENSE-lucide.txt`.
- Mastra, OpenCode, and Pi: brand marks from their official websites or repositories, linked in the source manifest. Respect their upstream terms and brand guidelines.

## Maintenance

From the repository root, with Python 3 and Pillow installed:

```sh
python3 scripts/generate-assets.py
python3 scripts/check-profile.py
```

The generator needs Fira Code at `/usr/share/fonts/truetype/firacode/` and DejaVu Sans at `/usr/share/fonts/truetype/dejavu/`. It downloads icons only when regenerating; viewing the profile does not contact those upstream sources.

The README keeps the original introduction, stack categories, social badges, and collaboration note, adding the requested AI tools and Jest. No feed updater, external badge service, JavaScript, or custom CSS is required.
