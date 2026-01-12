import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")


def login(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "email").send_keys("admin@prueba.com")
    driver.find_element(By.ID, "password").send_keys("admin")
    driver.find_element(By.ID, "btn-login").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

def test_load_view(driver):
    login(driver)

    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.welcome-title"))
    )
    assert "administrador" in header.text.lower()

    card_usuarios = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "card-usuarios"))
    )
    card_anuncios = driver.find_element(By.ID, "card-anuncios")
    card_perfil = driver.find_element(By.ID, "card-perfil")
    card_cursos = driver.find_element(By.ID, "card-cursos")

    assert card_usuarios.is_displayed()
    assert card_anuncios.is_displayed()
    assert card_perfil.is_displayed()
    assert card_cursos.is_displayed()

    card_title_usuarios = card_usuarios.find_element(By.TAG_NAME, "h5")
    card_title_anuncios = card_anuncios.find_element(By.TAG_NAME, "h5")
    card_title_perfil = card_perfil.find_element(By.TAG_NAME, "h5")
    card_title_cursos = card_cursos.find_element(By.TAG_NAME, "h5")
    assert "usuarios" in card_title_usuarios.text.lower()
    assert "anuncios" in card_title_anuncios.text.lower()
    assert "perfil" in card_title_perfil.text.lower()
    assert "cursos" in card_title_cursos.text.lower()

def test_dashboard_routes(driver):
    login(driver)

    btn_usuarios = driver.find_element(By.CSS_SELECTOR, "#card-usuarios a")
    btn_anuncios = driver.find_element(By.CSS_SELECTOR, "#card-anuncios a")
    btn_perfil = driver.find_element(By.CSS_SELECTOR, "#card-perfil a")
    btn_cursos = driver.find_element(By.CSS_SELECTOR, "#card-cursos a")
    assert btn_usuarios.is_displayed()
    assert btn_anuncios.is_displayed()
    assert btn_perfil.is_displayed()
    assert btn_cursos.is_displayed()

    assert btn_usuarios.get_attribute("href").endswith("/admin/users")
    assert btn_anuncios.get_attribute("href").endswith("/anuncios")
    assert btn_perfil.get_attribute("href").endswith("/user/profile")
    assert btn_cursos.get_attribute("href").endswith("/admin/courses")
