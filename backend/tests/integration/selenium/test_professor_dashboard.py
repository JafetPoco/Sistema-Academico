import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:4173")


def login(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "email").send_keys("professor@test.com")
    driver.find_element(By.ID, "password").send_keys("professor")
    driver.find_element(By.ID, "btn-login").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

def test_load_view(driver):
    login(driver)

    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.welcome-title"))
    )
    assert "profesor" in header.text.lower()

    card_calificar = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "calificar"))
    )
    card_cursos = driver.find_element(By.ID, "cursos")
    card_reportes = driver.find_element(By.ID, "reportes")

    assert card_calificar.is_displayed()
    assert card_cursos.is_displayed()
    assert card_reportes.is_displayed()

    card_title_calificar = card_calificar.find_element(By.TAG_NAME, "h5")
    card_title_cursos = card_cursos.find_element(By.TAG_NAME, "h5")
    card_title_reportes = card_reportes.find_element(By.TAG_NAME, "h5")

    assert "calificar" in card_title_calificar.text.lower()
    assert "cursos" in card_title_cursos.text.lower()
    assert "reportes" in card_title_reportes.text.lower()

def test_dashboard_routes(driver):
    login(driver)

    btn_calificar = driver.find_element(By.CSS_SELECTOR, "#calificar a")
    btn_cursos = driver.find_element(By.CSS_SELECTOR, "#cursos a")
    btn_reportes = driver.find_element(By.CSS_SELECTOR, "#reportes a")

    assert btn_calificar.is_displayed()
    assert btn_cursos.is_displayed()
    assert btn_reportes.is_displayed()

    assert btn_calificar.get_attribute("href").endswith("/calificaciones/form")
    assert btn_cursos.get_attribute("href").endswith("/courses/professor")
    assert btn_reportes.get_attribute("href").endswith("/reportes")

