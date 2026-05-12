# 🚀 START HERE

## Benvenuto nel progetto Embodied AI in MuJoCo!

Questo file ti guida passo-passo per testare e deployare il progetto.

---

## 📦 Cosa Hai

Un sistema completo di embodied AI con:
- ✅ 3 task di manipolazione (pick-place, drawer, tool use)
- ✅ Training (Behavior Cloning + RL)
- ✅ Evaluation riproducibile
- ✅ CI/CD automatico
- ✅ GitHub Pages con demo interattiva
- ✅ ~2,200 linee di codice
- ✅ Documentazione completa

---

## 🎯 Cosa Fare Ora

### Opzione 1: Test Rapido (5 minuti) ⚡

```bash
# 1. Verifica che tutto funzioni
python scripts/verify_install.py

# 2. Run tests
pytest tests/ -v

# 3. Demo
python scripts/demo.py --task pick_place
```

✅ **Successo**: Tutti i test passano e hai un video `demo_pick_place.mp4`

### Opzione 2: Deploy su GitHub (10 minuti) 🚀

```bash
# 1. Push su GitHub
bash scripts/git_setup.sh

# 2. Abilita GitHub Pages
# Vai su: https://github.com/omargarraoui/mujoco-rl/settings/pages
# Seleziona: Source → GitHub Actions → Save

# 3. Aspetta 2 minuti e visita:
# https://omargarraoui.github.io/mujoco-rl/
```

✅ **Successo**: Sito live con demo interattiva!

### Opzione 3: Training Completo (30+ minuti) 🧠

```bash
# Train policy
python train/train_bc.py --task pick_place --epochs 50

# Evaluate
python eval.py \
  --task pick_place \
  --checkpoint checkpoints/bc_pick_place_final.pt \
  --episodes 50 \
  --render
```

✅ **Successo**: Policy trainata e valutata con metriche JSON!

---

## 📚 Guide Disponibili

Scegli in base a cosa vuoi fare:

### Per Iniziare
- **[QUICKSTART.md](QUICKSTART.md)** - Tutorial 5 minuti
- **[TEST_GUIDE.md](TEST_GUIDE.md)** - Come testare tutto
- **[HOW_TO_TEST_AND_DEPLOY.md](HOW_TO_TEST_AND_DEPLOY.md)** - Guida completa test + deploy

### Per Deployare
- **[DEPLOY_INSTRUCTIONS.md](DEPLOY_INSTRUCTIONS.md)** - Deploy su GitHub
- **[GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)** - Setup GitHub Pages

### Per Usare
- **[INSTALLATION.md](INSTALLATION.md)** - Installazione dettagliata
- **[docs/USAGE.md](docs/USAGE.md)** - Come usare il sistema
- **[docs/API.md](docs/API.md)** - API reference

### Per Capire
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Architettura sistema
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Struttura file
- **[SUMMARY.md](SUMMARY.md)** - Riepilogo completo

### Per Risolvere Problemi
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Soluzioni problemi comuni
- **[CHECKLIST.md](CHECKLIST.md)** - Checklist completamento

### Per Contribuire
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Come contribuire
- **[ROADMAP.md](ROADMAP.md)** - Piani futuri
- **[CHANGELOG.md](CHANGELOG.md)** - Storia versioni

---

## 🎬 Quick Commands

```bash
# Test
make test                    # Run unit tests
make test-ci                 # Run full CI suite
python scripts/verify_install.py  # Verify installation

# Demo
make demo                    # Run demo
python scripts/demo.py --task pick_place

# Training
make train-bc                # Train with BC
make train-rl                # Train with RL

# Evaluation
make eval                    # Evaluate policy

# Deploy
bash scripts/git_setup.sh    # Push to GitHub
bash scripts/setup.sh        # Initial setup

# Monitoring
make tensorboard             # Launch tensorboard

# Cleanup
make clean                   # Clean build artifacts
```

---

## 🔍 Verifica Veloce

Esegui questi comandi per verificare che tutto funzioni:

```bash
# 1. Python e dipendenze
python --version              # Deve essere >= 3.8
pip list | grep mujoco        # Deve mostrare mujoco

# 2. Import moduli
python -c "from envs import PickPlaceEnv; print('✓ Envs OK')"
python -c "from policies import MLPPolicy; print('✓ Policies OK')"

# 3. Test rapido
pytest tests/test_envs.py -v

# 4. Demo
python scripts/demo.py --task pick_place
```

Se tutti passano: **✅ Tutto OK!**

---

## 🌐 Link Utili

- **Repository**: https://github.com/omargarraoui/mujoco-rl
- **GitHub Pages**: https://omargarraoui.github.io/mujoco-rl/
- **Actions**: https://github.com/omargarraoui/mujoco-rl/actions
- **Issues**: https://github.com/omargarraoui/mujoco-rl/issues

---

## ❓ FAQ

**Q: Da dove inizio?**
A: Esegui `python scripts/verify_install.py` per verificare l'installazione.

**Q: Come testo tutto?**
A: Esegui `bash scripts/ci_test.sh` per test completi.

**Q: Come deploya su GitHub?**
A: Esegui `bash scripts/git_setup.sh` e segui le istruzioni.

**Q: Come funziona GitHub Pages?**
A: Leggi [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md).

**Q: Dove trovo la documentazione?**
A: Nella cartella `docs/` o su GitHub Pages.

**Q: Come aggiungo un nuovo task?**
A: Leggi [CONTRIBUTING.md](CONTRIBUTING.md).

**Q: I test falliscono, cosa faccio?**
A: Leggi [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

---

## 🎯 Prossimi Passi Consigliati

1. ✅ **Test locale** (5 min)
   ```bash
   python scripts/verify_install.py
   pytest tests/ -v
   ```

2. ✅ **Deploy GitHub** (10 min)
   ```bash
   bash scripts/git_setup.sh
   # Poi abilita Pages su GitHub
   ```

3. ✅ **Training** (30+ min)
   ```bash
   python train/train_bc.py --task pick_place --epochs 50
   ```

4. ✅ **Evaluation** (5 min)
   ```bash
   python eval.py --task pick_place --checkpoint <path> --episodes 50 --render
   ```

5. ✅ **Condividi** 🎉
   - Demo: https://omargarraoui.github.io/mujoco-rl/
   - Repo: https://github.com/omargarraoui/mujoco-rl

---

## 💡 Suggerimenti

- 📖 Leggi [QUICKSTART.md](QUICKSTART.md) per tutorial rapido
- 🐛 Usa [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) per problemi
- 🤝 Leggi [CONTRIBUTING.md](CONTRIBUTING.md) per contribuire
- 🚀 Usa `make help` per vedere tutti i comandi

---

## 🎉 Pronto!

Hai tutto quello che ti serve per:
- ✅ Testare il sistema
- ✅ Deployare su GitHub
- ✅ Trainare policy
- ✅ Valutare risultati
- ✅ Condividere il lavoro

**Buon lavoro! 🤖**

---

*Per domande o problemi, apri un issue su GitHub o consulta la documentazione.*
