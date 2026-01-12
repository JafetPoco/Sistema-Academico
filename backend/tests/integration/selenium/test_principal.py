import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")

def test_principal_carga(driver):
    driver.get(f"{BASE_URL}/")

    # Verificar título
    title = driver.title
    assert title.strip() != ""

    # Verificar carga de botones
    btn_home = driver.find_element(By.ID, "btn-home")
    btn_anuncios = driver.find_element(By.ID, "btn-anuncios")
    btn_dashboard = driver.find_element(By.XPATH, "//a[text()='Dashboard']")
    btn_iniciar_sesion = driver.find_element(By.ID, "btn-iniciar-sesion")
    btn_mi_perfil = driver.find_elements(By.ID, "btn-mi-perfil")

    assert btn_home.is_displayed()
    assert btn_anuncios.is_displayed()
    assert btn_dashboard.is_displayed()
    assert btn_iniciar_sesion.is_displayed()
    assert len(btn_mi_perfil) == 0  # No debe estar visible si no está logeado

    # Verificar carga del logo
    img_principal = driver.find_element(By.XPATH, "//img[@alt='EDUNET']")
    assert img_principal.is_displayed()

def test_principal_correct_path_sin_logear(driver):
    driver.get(f"{BASE_URL}/")

    # Verificacion de botones
    btn_home = driver.find_element(By.ID, "btn-home")
    btn_anuncios = driver.find_element(By.ID, "btn-anuncios")
    btn_dashboard = driver.find_element(By.XPATH, "//a[text()='Dashboard']")
    btn_iniciar_sesion = driver.find_element(By.ID, "btn-iniciar-sesion")

    assert btn_home.get_attribute("href").rstrip("/") == BASE_URL.rstrip("/")
    assert btn_anuncios.get_attribute("href").rstrip("/") == f"{BASE_URL}/anuncios".rstrip("/")
    assert btn_dashboard.get_attribute("href").endswith("/login")
    assert btn_iniciar_sesion.get_attribute("href").endswith("/login")

def login(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "email").send_keys("admin@prueba.com")
    driver.find_element(By.ID, "password").send_keys("admin")
    driver.find_element(By.ID, "btn-login").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )

def test_principal_correct_path_logeado(driver):
    login(driver)

    # Navegar a la pantalla principal
    driver.get(f"{BASE_URL}/")

    #Verificar botones
    btn_mi_perfil = driver.find_element(By.ID, "btn-mi-perfil")
    btn_logout = driver.find_element(By.ID, "btn-logout")
    btn_home = driver.find_element(By.ID, "btn-home")
    btn_anuncios = driver.find_element(By.ID, "btn-anuncios")
    btn_dashboard = driver.find_element(By.XPATH, "//a[text()='Dashboard']")

    assert btn_mi_perfil.is_displayed()

    assert btn_home.get_attribute("href").rstrip("/") == BASE_URL.rstrip("/")
    assert btn_anuncios.get_attribute("href").rstrip("/") == f"{BASE_URL}/anuncios".rstrip("/")
    assert btn_dashboard.get_attribute("href").endswith("/dashboard")
    assert btn_mi_perfil.get_attribute("href").endswith("/profile") or btn_mi_perfil.get_attribute("href").endswith("/user/profile")
    # logout button triggers fetch + redirect, href may be javascript:void(0) so just ensure clickable
    assert btn_logout.is_enabled()
    
    #Cerrar sesión
    btn_logout.click()
    WebDriverWait(driver, 10).until(
        EC.url_contains(BASE_URL.rstrip("/"))
    )
    assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")
