def test_homepage(driver):
    driver.get("http://localhost:5000")

    # Validar contenido
    title = driver.title
    print(f"Título de la página: {title}")
    assert title == "Inicio - EDUNET"

    # Cerrar
    driver.quit()
