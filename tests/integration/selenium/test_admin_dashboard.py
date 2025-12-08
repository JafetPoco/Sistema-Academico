from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    driver.get("http://localhost:5000/auth/login")
    driver.find_element(By.ID, "email").send_keys("admin@prueba.com")
    driver.find_element(By.ID, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar sesión')]").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("http://localhost:5000/dashboard/")
    )

def test_load_view(driver):
    login(driver)

    # Verificar título
    title = driver.title
    assert "Administrador" in title

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

    card_title_usuarios = driver.find_element(By.ID, "card-title-usuarios")
    card_title_anuncios = driver.find_element(By.ID, "card-title-anuncios")
    card_title_perfil = driver.find_element(By.ID, "card-title-perfil")
    card_title_cursos = driver.find_element(By.ID, "card-title-cursos")
    assert card_title_usuarios.text.strip() == "Usuarios"
    assert card_title_anuncios.text.strip() == "Anuncios"
    assert card_title_perfil.text.strip() == "Mi Perfil"
    assert card_title_cursos.text.strip() == "Cursos"

def test_dashboard_routes(driver):
    login(driver)

    btn_usuarios = driver.find_element(By.ID, "btn-usuarios")
    btn_anuncios = driver.find_element(By.ID, "btn-anuncios")
    btn_perfil = driver.find_element(By.ID, "btn-perfil")
    btn_cursos = driver.find_element(By.ID, "btn-cursos")
    assert btn_usuarios.is_displayed()
    assert btn_anuncios.is_displayed()
    assert btn_perfil.is_displayed()
    assert btn_cursos.is_displayed()

    assert btn_usuarios.get_attribute("href") == "http://localhost:5000/admin/users"
    assert btn_anuncios.get_attribute("href") == "http://localhost:5000/anuncios/admin"
    assert btn_perfil.get_attribute("href") == "http://localhost:5000/user/profile"
    assert btn_cursos.get_attribute("href") == "http://localhost:5000/admin/courses"
