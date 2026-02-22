# Contributing to payaza-python

Thanks for your interest in contributing! Here's how to get started.

## Setting up locally

```bash
git clone https://github.com/0xAfterSnow/payaza-python
cd payaza-python
pip install -e ".[dev]"
```

## Running tests

```bash
pytest --cov=payaza
```

## Making changes

1. Fork the repo and create a branch: `git checkout -b feat/my-feature`
2. Make your changes and add tests
3. Ensure all tests pass: `pytest`
4. Open a pull request with a clear description of what you changed and why

## Adding a new resource

1. Create `payaza/resources/my_resource.py` extending `Resource`
2. Register it in `payaza/resources/__init__.py`
3. Add it to the `Payaza` client in `payaza/client.py`
4. Write tests in `tests/test_my_resource.py`
5. Add usage examples in `examples/`

## Reporting bugs

Open an issue at https://github.com/0xAfterSnow/payaza-python/issues with:
- Python version
- SDK version
- Minimal code to reproduce
- Expected vs actual behaviour

## Code style

- Follow PEP 8
- Use type hints everywhere
- Write docstrings for all public methods