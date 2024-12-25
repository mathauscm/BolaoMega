from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_megasena_results():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        url = 'https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx'
        driver.get(url)

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.numbers.megasena"))
        )

        numeros_sorteados = driver.find_elements(By.CSS_SELECTOR, 'ul.numbers.megasena li')
        numeros = [numero.text for numero in numeros_sorteados]

        try:
            concurso_e_data = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h2 > span.ng-binding"))
            ).text
        except Exception as e:
            concurso_e_data = None

    except Exception as e:
        numeros = []
        concurso_e_data = None
    finally:
        driver.quit()

    return numeros, concurso_e_data


if __name__ == '__main__':
    numeros, concurso_e_data = get_megasena_results()
    print("Números Sorteados:", numeros)
    print("Concurso e data:", concurso_e_data)
