from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    driver.get("http://localhost:5000/auth/login")
    driver.find_element(By.ID, "email").send_keys("admin@prueba.com")
    driver.find_element(By.ID, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar sesión')]").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("http://localhost:5000/dashboard/")
    )
    
    btn_usuarios = driver.find_element(By.ID, "btn-usuarios")
    btn_usuarios.click()

def test_admin_carga_usuarios(driver):
    login(driver)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
    )

    filas = driver.find_elements(By.XPATH, "//table/tbody/tr[td]")

    assert len(filas) > 0, f"No se encontraron usuarios. Filas encontradas: {len(filas)}"

def test_cambiar_rol(driver):
    login(driver)

    fila = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    select_element = fila.find_element(By.CSS_SELECTOR, "select[name='role']")
    select = Select(select_element)

    select.select_by_value("2")

    boton = fila.find_element(By.CSS_SELECTOR, "button[id^='btn-update-']")
    boton_id = boton.get_attribute("id")
    boton.click()

    WebDriverWait(driver, 5).until(EC.url_contains("/admin/users"))

    driver.refresh()

    boton_actualizado = driver.find_element(By.ID, boton_id)
    fila_actualizada = boton_actualizado.find_element(By.XPATH, "./ancestor::tr")

    select_actualizado = Select(
        fila_actualizada.find_element(By.CSS_SELECTOR, "select[name='role']")
    )

    assert select_actualizado.first_selected_option.get_attribute("value") == "2"

def test_elementos_por_fila(driver):
    login(driver)

    filas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    assert filas, "No hay filas de usuario"

    for fila in filas:
        assert fila.find_elements(By.TAG_NAME, "td")[0]
        assert fila.find_element(By.CSS_SELECTOR, "select[name='role']")
        assert fila.find_element(By.CSS_SELECTOR, "button[id^='btn-update-']")

