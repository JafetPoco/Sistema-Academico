from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "http://localhost:5000/auth/login"

def do_login(driver, email, password):
    driver.get(LOGIN_URL)

    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "btn-login").click()

def test_login_correct(driver):
    do_login(driver, "admin@prueba.com", "admin")

    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard/")
    )

    assert "/dashboard/" in driver.current_url


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