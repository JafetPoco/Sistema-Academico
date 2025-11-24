from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "http://localhost:5000/auth/login"

def do_login(driver, email, password):
    driver.get(LOGIN_URL)

    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "btn-login").click()

def test_login_page_load(driver):
    driver.get(LOGIN_URL)

    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )

    password_input = driver.find_element(By.ID, "password")
    btn_login = driver.find_element(By.ID, "btn-login")
    link_register = driver.find_element(By.ID, "btn-registrate")

    assert email_input is not None
    assert password_input is not None
    assert btn_login is not None
    assert link_register is not None

    assert email_input.is_displayed()
    assert password_input.is_displayed()
    assert btn_login.is_displayed()
    assert link_register.is_displayed()

    assert email_input.get_attribute("type") == "email"
    assert password_input.get_attribute("type") == "password"
    assert btn_login.text.strip().lower() == "iniciar sesión"

def test_login_wrong_password(driver):
    do_login(driver, "admin@prueba.com", "wrongpass")

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "mensage-error"))
    )

    assert "contraseña incorrecta" in error.text.lower()

def test_login_nonexistent_email(driver):
    do_login(driver, "userNotRegister@prueba.com", "somepass")
    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "mensage-error"))
    )
    assert "usuario no registrado" in error.text.lower()

def test_login_professor_acount(driver):
    do_login(driver, "professor@test.com", "professor")
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard/")
    )
    assert "/dashboard/" in driver.current_url

    role_element = driver.find_element(By.ID, "welcome-title")
    assert "Profesor" in role_element.text

def test_login_parent_acount(driver):
    do_login(driver, "parent@test.com", "parent")
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard/")
    )
    assert "/dashboard/" in driver.current_url
    role_element = driver.find_element(By.ID, "welcome-title")
    assert "Padre/Madre" in role_element.text


def test_login_admin_acount(driver):
    do_login(driver, "admin@prueba.com", "admin")
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard/")
    )
    assert "/dashboard/" in driver.current_url
    role_element = driver.find_element(By.ID, "welcome-title")
    assert "Administrador" in role_element.text

def test_login_no_activate_acount(driver):
    do_login(driver, "noActivate@test.com", "noActivate")
    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "mensage-error"))
    )
    assert "no se activo su cuenta" in error.text.lower()