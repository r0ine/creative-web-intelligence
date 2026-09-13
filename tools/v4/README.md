# v4 Tools

```bash
python tools/v4/source_intelligence.py sources
python tools/v4/source_intelligence.py policy iconscout
python tools/v4/source_intelligence.py icon-collections
python tools/v4/source_intelligence.py icon-search "settings" --prefix line-md
python tools/v4/source_intelligence.py icon-collection line-md
python tools/v4/source_intelligence.py font-catalog
python tools/v4/source_intelligence.py font-search --subsets latin-ext --variable --category sans-serif
python tools/v4/source_intelligence.py font roboto-flex
python tools/v4/validate_v4.py
```

The CLI intentionally refuses generic automation for sources marked restricted/manual. It does not contain API keys and does not bypass source controls.
