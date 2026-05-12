# 🚀 Deploy Instructions

## Quick Deploy (3 steps)

### Step 1: Test Locally

```bash
# Verify installation
python scripts/verify_install.py

# Run tests
pytest tests/ -v

# Quick demo
python scripts/demo.py --task pick_place
```

### Step 2: Push to GitHub

```bash
# Make script executable
chmod +x scripts/git_setup.sh

# Run setup and push
bash scripts/git_setup.sh
```

This will:
- Initialize git repository
- Add remote: https://github.com/omargarraoui/mujoco-rl
- Commit all files
- Push to GitHub

### Step 3: Enable GitHub Pages

1. Go to: https://github.com/omargarraoui/mujoco-rl/settings/pages
2. Under **Source**, select: **GitHub Actions**
3. Click **Save**
4. Wait ~2 minutes for deployment
5. Visit: https://omargarraoui.github.io/mujoco-rl/

## What Gets Deployed

### GitHub Repository
- ✅ Complete source code
- ✅ Documentation
- ✅ Tests
- ✅ CI/CD workflows

### GitHub Pages
- ✅ Interactive demo page
- ✅ Mobile detection
- ✅ Feature showcase
- ✅ Quick start guide
- ✅ Architecture diagram

### GitHub Actions
- ✅ Automated testing on push
- ✅ Automatic Pages deployment
- ✅ Coverage reports

## Verification

After deployment, verify:

1. **Repository**: https://github.com/omargarraoui/mujoco-rl
   - [ ] All files visible
   - [ ] README displays correctly
   - [ ] CI badge shows passing

2. **Actions**: https://github.com/omargarraoui/mujoco-rl/actions
   - [ ] CI workflow passing
   - [ ] Deploy Pages workflow passing

3. **GitHub Pages**: https://omargarraoui.github.io/mujoco-rl/
   - [ ] Page loads correctly
   - [ ] Mobile warning works (test on phone)
   - [ ] All links work
   - [ ] Styling looks good

## Troubleshooting

### Push Fails

```bash
# If authentication fails, use personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/omargarraoui/mujoco-rl.git
git push -u origin main
```

### Pages Not Deploying

1. Check Actions tab for errors
2. Ensure repository is public
3. Verify Pages source is "GitHub Actions"
4. Wait 2-3 minutes and refresh

### CI Failing

1. Check Actions logs
2. Verify all dependencies in requirements.txt
3. Test locally first: `bash scripts/ci_test.sh`

## Manual Steps (if script fails)

```bash
# 1. Initialize git
git init

# 2. Add remote
git remote add origin https://github.com/omargarraoui/mujoco-rl.git

# 3. Add files
git add .

# 4. Commit
git commit -m "Initial commit: Complete embodied AI system"

# 5. Push
git branch -M main
git push -u origin main
```

## Post-Deployment

### Update README badges

The badges in README.md will automatically update once workflows run:
- CI badge: Shows test status
- Deploy Pages badge: Shows deployment status

### Share Your Work

Once deployed, share:
- 🌐 Live demo: https://omargarraoui.github.io/mujoco-rl/
- 📦 Repository: https://github.com/omargarraoui/mujoco-rl
- 📚 Documentation: In `docs/` folder

## Continuous Deployment

After initial setup, every push to `main` will:
1. Run CI tests automatically
2. Deploy to GitHub Pages automatically
3. Update live site within 2 minutes

No manual intervention needed! 🎉

## Next Steps

1. ✅ Test locally
2. ✅ Push to GitHub
3. ✅ Enable Pages
4. ✅ Verify deployment
5. 🎯 Start training models!
6. 📊 Share results
7. 🤝 Accept contributions

## Support

Need help?
- 📖 See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)
- 🐛 Open an issue
- 💬 Check GitHub Discussions
