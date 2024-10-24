# Critic

A simple API for analysing images for their dominant colours using k-means clustering.

## Analyse a Jpg

```bash
curl -X POST -d '{"n_colours": "7", "image_url": "https://i.ibb.co/L8rTYy4/image.jpg"}' -H  "Content-Type: application/json" "http://127.0.0.1:5000/analyse-color"
```

## Analyse a Png (with an alpha channel)

```bash
curl -X POST -d '{"n_colours": "7", "image_url": "https://i.ibb.co/TYs0KSY/image.png"}' -H  "Content-Type: application/json" "http://127.0.0.1:5000/analyse-color"
```

## Environment

Environment is provided by pyenv and virtual-env. The environment should automatically be switched to, but if python not available it's because pyenv virtual-env didn't autoswitch the Python environment.

To do it manually:

```bash
pyenv local python-playground
```

## Start the server

```bash
python src/app.py
```

## Run Tests

```bash
pytest tests/test_app.py  -s
```
