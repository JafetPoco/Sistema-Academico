import os

BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")


def test_homepage(driver):
    driver.get(BASE_URL)

    title = driver.title
    print(f"Título de la página: {title}")
    assert title.strip() != ""
