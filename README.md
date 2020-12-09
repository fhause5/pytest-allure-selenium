### Pytest-allure-selenium

# Run selenium

```
docker run --rm -p 4444:4444 selenium/standalone-chrome:latest

```

# Run tests:

```
pytest -v -s --alluredir=/reports operations/test_login.py
```

# Run tests in docker:

```
docker run -v /home/devops/WORKDIR/pytest-allure-selenium/reports:/reports pytesting:1
```
