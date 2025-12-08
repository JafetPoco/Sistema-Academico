from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    driver.get("http://localhost:5000/auth/login")
    driver.find_element(By.ID, "email").send_keys("parent@test.com")
    driver.find_element(By.ID, "password").send_keys("parent")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar sesión')]").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("http://localhost:5000/dashboard/")
    )

def test_load_view(driver):
    login(driver)

    # Verificar título
    title = driver.title
    assert "Padre" in title

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

    assert btn_calificaciones.get_attribute("href") == "http://localhost:5000/parent_query_grades"
    assert btn_perfil.get_attribute("href") == "http://localhost:5000/user/profile"

