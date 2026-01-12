import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")


def go_to_users(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "email").send_keys("admin@prueba.com")
    driver.find_element(By.ID, "password").send_keys("admin")
    driver.find_element(By.ID, "btn-login").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

    driver.get(f"{BASE_URL}/admin/users")

def test_admin_carga_usuarios(driver):
    go_to_users(driver)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
    )

    filas = driver.find_elements(By.XPATH, "//table/tbody/tr[td]")

    assert len(filas) > 0, f"No se encontraron usuarios. Filas encontradas: {len(filas)}"

def test_cambiar_rol(driver):
    go_to_users(driver)

    fila = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    first_user_id = fila.find_elements(By.TAG_NAME, "td")[0].text.strip()
    select_element = fila.find_element(By.TAG_NAME, "select")
    select = Select(select_element)

    select.select_by_value("2")

    boton = fila.find_element(By.TAG_NAME, "button")
    boton.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))

    # Rebuscar la fila del mismo usuario para confirmar el rol
    fila_actualizada = driver.find_element(
        By.XPATH, f"//table/tbody/tr[td[1][normalize-space()='{first_user_id}']]"
    )
    select_actualizado = Select(
        fila_actualizada.find_element(By.TAG_NAME, "select")
    )

    assert select_actualizado.first_selected_option.get_attribute("value") == "2"

def test_elementos_por_fila(driver):
    go_to_users(driver)

    filas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    assert filas, "No hay filas de usuario"

    for fila in filas:
        assert fila.find_elements(By.TAG_NAME, "td")[0]
        assert fila.find_element(By.TAG_NAME, "select")
        assert fila.find_element(By.TAG_NAME, "button")

