# llm.store

Minimal GitHub Pages site for llm.store.

What I added

- index.html: site entry
- CNAME: custom domain llm.store
- assets/css/style.css, assets/js/main.js
- 404.html, .gitignore, LICENSE

Publish

Run these commands (replace yourusername):

```bash
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin git@github.com:yourusername/llm.store.git
git push -u origin main
```

After pushing, enable GitHub Pages for the `main` branch (root) if not automatic.

## Emoji plugin packages

🔍 Search · 📋 Capture · 🏎️ Motorsports · 📺 Television and briefings.

The [plugin release factory](docs/plugin-factory.md) builds reproducible public-upload draft ZIPs from versioned sources. Run `python3 scripts/build_plugins.py` or use **Build emoji plugin drafts** in Actions. Read each readiness receipt before submission; packages are not yet publicly listed.
