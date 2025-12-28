from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    driver.get("http://localhost:5000/auth/login")
    driver.find_element(By.ID, "email").send_keys("professor@test.com")
    driver.find_element(By.ID, "password").send_keys("professor")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar sesión')]").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("http://localhost:5000/dashboard/")
    )

def test_load_view(driver):
    login(driver)

    # Verificar título
    title = driver.title
    assert "Profesor" in title

    card_calificar = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "card-calificar"))
    )
    card_cursos = driver.find_element(By.ID, "card-cursos")
    card_reportes = driver.find_element(By.ID, "card-reportes")

    assert card_calificar.is_displayed()
    assert card_cursos.is_displayed()
    assert card_reportes.is_displayed()

    card_title_calificar = driver.find_element(By.ID, "card-title-calificar")
    card_title_cursos = driver.find_element(By.ID, "card-title-cursos")
    card_title_reportes = driver.find_element(By.ID, "card-title-reportes")

    assert card_title_calificar.text.strip() == "Calificar Estudiantes"
    assert card_title_cursos.text.strip() == "Mis Cursos"
    assert card_title_reportes.text.strip() == "Reportes"

def test_dashboard_routes(driver):
    login(driver)

    btn_calificar = driver.find_element(By.ID, "btn-calificar")
    btn_cursos = driver.find_element(By.ID, "btn-cursos")
    btn_reportes = driver.find_element(By.ID, "btn-reportes")

    assert btn_calificar.is_displayed()
    assert btn_cursos.is_displayed()
    assert btn_reportes.is_displayed()

    assert btn_calificar.get_attribute("href") == "http://localhost:5000/calificar"
    assert btn_cursos.get_attribute("href") == "http://localhost:5000/cursos"
    assert btn_reportes.get_attribute("href") == "http://localhost:5000/reporte/formulario"

