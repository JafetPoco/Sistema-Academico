import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")


def login(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "email").send_keys("parent@test.com")
    driver.find_element(By.ID, "password").send_keys("parent")
    driver.find_element(By.ID, "btn-login").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

def test_load_view(driver):
    login(driver)

    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.welcome-title"))
    )
    assert "padre" in header.text.lower() or "madre" in header.text.lower()

    card_calificaciones = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "card-calificaciones"))
    )
    card_perfil = driver.find_element(By.ID, "card-perfil")

    assert card_calificaciones.is_displayed()
    assert card_perfil.is_displayed()

    card_title_calificaciones = driver.find_element(By.ID, "card-title-calificaciones")
    card_title_perfil = driver.find_element(By.ID, "card-title-perfil")

    assert card_title_calificaciones.text.strip() == "Ver Calificaciones"
    assert card_title_perfil.text.strip() == "Mi Perfil"

def test_dashboard_routes(driver):
    login(driver)

    btn_calificaciones = driver.find_element(By.ID, "btn-notas")
    btn_perfil = driver.find_element(By.ID, "btn-perfil")

    assert btn_calificaciones.is_displayed()
    assert btn_perfil.is_displayed()

    assert btn_calificaciones.get_attribute("href").endswith("/grades/parent")
    assert btn_perfil.get_attribute("href").endswith("/user/profile")

