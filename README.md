# LexiSense — Advanced NLP Lab 5 (Python 3.15)

## Aim
Develop a word sense disambiguation system using lexical relations and a Simplified Lesk baseline.

## Requirements
- Windows, macOS, or Linux
- Python 3.15 (standard library only for offline mode)
- VS Code or a terminal
- No pip installation, PowerShell activation, compiler, Streamlit, or Pandas required

## Run in VS Code / PowerShell
1. Extract the ZIP and open the `wsd_lab5_python315` folder in VS Code.
2. Open Terminal > New Terminal.
3. Run `py -3.15 server.py` (or `python server.py` if Python 3.15 is your default).
4. Visit http://127.0.0.1:8501 in your browser.
5. Stop the server using Ctrl+C.

If port 8501 is busy, run `$env:PORT=8502; py -3.15 server.py` and visit http://127.0.0.1:8502.

## Features
- Modern responsive dashboard with accessible contrast
- Context-based Simplified Lesk WSD with overlap ranking and zero-overlap fallback flag
- Curated offline lexical inventory for bank, bat, plant, spring, light, crane, mouse
- Definitions, examples, synonyms, antonyms, hypernyms, hyponyms
- Sample sentence batch processing and downloadable CSV
- Optional full NLTK WordNet mode (requires compatible NLTK + downloaded corpus)

## Optional: full WordNet corpus
The default curated dataset is an educational **limited WordNet-style** inventory, not a complete WordNet dump. For real WordNet synsets, if a Python-3.15-compatible NLTK package is available:

```powershell
py -3.15 -m pip install nltk
py -3.15 -m nltk.downloader wordnet omw-1.4
```

Restart the server and select **Full NLTK WordNet (optional)** in the app. If unavailable, the app reports the issue instead of silently substituting offline data. The offline mode does not require these commands.

## Test
`py -3.15 -m unittest discover -s tests -v`

## Project files
- `server.py`: HTTP server and API routes
- `wsd_engine.py`: sense lookup and Simplified Lesk algorithm
- `senses.json`: curated offline educational lexical dataset
- `static/`: responsive frontend (HTML, CSS, JavaScript)
- `sample_sentences.csv`: input samples
- `REPORT.md`: analysis report
- `tests/test_wsd.py`: automated tests
- `requirements.txt`: dependency explanation

## Limitations
The offline inventory covers only seven words and a subset of their possible meanings. Scores measure token overlap, not calibrated probabilities. No gold-standard accuracy is claimed. The optional NLTK mode is contingent on third-party support for Python 3.15.
