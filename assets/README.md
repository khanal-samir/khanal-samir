# Profile assets

The hero illustrations and animations were created for this profile. The animations play once and finish on a readable frame. Still versions are available in the README; GitHub cannot automatically switch GIFs off based on reduced-motion preferences.

Badges use locally embedded brand icons rather than remote badge services. Exact upstream URLs are recorded in `icon-sources.json`. Logos and trademarks belong to their respective owners; their inclusion indicates tools, not endorsement.

Icon sources:
- [Simple Icons](https://github.com/simple-icons/simple-icons): CC0 icons, subject to individual brand guidelines.
- [Devicon](https://github.com/devicons/devicon): MIT-licensed icon collection. [License](https://github.com/devicons/devicon/blob/master/LICENSE).
- [Lobe Icons](https://github.com/lobehub/lobe-icons): MIT-licensed OpenAI icon. [License](https://github.com/lobehub/lobe-icons/blob/master/LICENSE).
- Mastra, OpenCode, and Pi: brand marks from their official websites or repositories, linked in the source manifest. Respect their upstream terms and brand guidelines.

## Maintenance

From the repository root, with Python 3 and Pillow installed:

```sh
python3 scripts/generate-assets.py
python3 scripts/check-profile.py
```

The generator needs Fira Code at `/usr/share/fonts/truetype/firacode/`. It downloads icons only when regenerating; viewing the profile does not contact those upstream sources.

`python3 scripts/update-writing.py` refreshes the three latest public dev.to articles. A daily GitHub Action runs the same command after this branch is merged. Failed API requests leave the README unchanged and fail the workflow visibly. Hashnode remains a direct blog link; it is not scraped. Repository settings must allow Actions to write contents for automatic commits.

The README uses GitHub-native expandable sections and normal links. It does not claim to run JavaScript, custom CSS, or embedded apps.
