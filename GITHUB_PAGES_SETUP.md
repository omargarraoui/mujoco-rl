# GitHub Pages Setup Guide

## Automatic Deployment

This repository is configured for automatic deployment to GitHub Pages using GitHub Actions.

## Setup Steps

### 1. Push to GitHub

```bash
# Make script executable
chmod +x scripts/git_setup.sh

# Run setup script
bash scripts/git_setup.sh
```

Or manually:

```bash
# Initialize git (if not already done)
git init

# Add remote
git remote add origin https://github.com/omargarraoui/mujoco-rl.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete embodied AI system"

# Push
git branch -M main
git push -u origin main
```

### 2. Enable GitHub Pages

1. Go to: https://github.com/omargarraoui/mujoco-rl
2. Click **Settings** (top right)
3. Click **Pages** (left sidebar)
4. Under **Source**, select: **GitHub Actions**
5. Click **Save**

### 3. Wait for Deployment

- GitHub Actions will automatically deploy the site
- Check progress: https://github.com/omargarraoui/mujoco-rl/actions
- Deployment takes ~2 minutes

### 4. Visit Your Site

Once deployed, visit:
**https://omargarraoui.github.io/mujoco-rl/**

## Features

### ✅ Automatic Deployment
- Deploys on every push to `main` branch
- No manual intervention needed
- Fast deployment (~2 minutes)

### ✅ Mobile Detection
- Automatically detects mobile devices
- Shows warning to use desktop
- Optimized for desktop viewing

### ✅ Interactive Demo
- Beautiful gradient design
- Feature showcase
- Code examples
- Architecture diagram
- Quick start guide

## Troubleshooting

### Pages Not Deploying

1. Check Actions tab for errors
2. Ensure Pages is enabled in Settings
3. Verify `docs/index.html` exists
4. Check workflow file: `.github/workflows/deploy-pages.yml`

### 404 Error

1. Wait 2-3 minutes after first push
2. Clear browser cache
3. Check repository is public
4. Verify Pages source is set to "GitHub Actions"

### Mobile Warning Not Showing

- The warning only shows on screens < 768px width
- Test on actual mobile device or use browser dev tools

## Manual Deployment

If automatic deployment fails, you can deploy manually:

1. Go to Actions tab
2. Click "Deploy to GitHub Pages"
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

## Customization

### Update Content

Edit `docs/index.html` and push:

```bash
# Edit the file
nano docs/index.html

# Commit and push
git add docs/index.html
git commit -m "Update GitHub Pages content"
git push
```

### Change Mobile Breakpoint

In `docs/index.html`, find:

```css
@media (max-width: 768px) {
    .mobile-warning {
        display: flex;
    }
}
```

Change `768px` to your preferred breakpoint.

### Disable Mobile Warning

In `docs/index.html`, remove or comment out:

```html
<!-- Mobile Warning -->
<div class="mobile-warning">
    ...
</div>
```

## Testing Locally

To test the page locally before pushing:

```bash
# Simple HTTP server
cd docs
python -m http.server 8000

# Visit: http://localhost:8000
```

## Repository Settings

Ensure these settings are correct:

1. **Repository Visibility**: Public (required for free GitHub Pages)
2. **Pages Source**: GitHub Actions
3. **Workflow Permissions**: Read and write permissions
   - Settings → Actions → General → Workflow permissions

## Links

- **Live Site**: https://omargarraoui.github.io/mujoco-rl/
- **Repository**: https://github.com/omargarraoui/mujoco-rl
- **Actions**: https://github.com/omargarraoui/mujoco-rl/actions
- **Settings**: https://github.com/omargarraoui/mujoco-rl/settings/pages

## Support

If you encounter issues:

1. Check [GitHub Pages documentation](https://docs.github.com/en/pages)
2. Review [GitHub Actions logs](https://github.com/omargarraoui/mujoco-rl/actions)
3. Open an issue on GitHub
