# README

## Environment

Environment is provided by pyenv and virtual-env. The environment should automatically be switched to, but if python not available it's because pyenv virtual-env didn't autoswitch the Python environment.

To do it manually:

```bash
pyenv local python-playground
```

# Jupyter

To open Jupyter notebooks:

```bash
jupyter notebook
```

# Start the server:

```bash
python src/app.py
```

# Analyse and image:

## Jpg

```
curl -X POST -d '{"n_colours": "7", "image_url": "https://i.ibb.co/L8rTYy4/image.jpg"}' -H  "Content-Type: application/json" "http://127.0.0.1:5000/analyse-color"
```

## Png with alpha

```
curl -X POST -d '{"n_colours": "7", "image_url": "https://i.ibb.co/TYs0KSY/image.png"}' -H  "Content-Type: application/json" "http://127.0.0.1:5000/analyse-color"
```

# Tests

```
pytest tests/test_app.py  -s
```
