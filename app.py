from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from random import randint

# Constantes
INSTAGRAM_LOGIN_URL = 'https://instagram.com/'
INSTAGRAM_PROFILE_URL = 'https://www.instagram.com/curiosidadesobrepets/'
USERNAME = 'usuário'
PASSWORD = 'senha'

def initial_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1200,1000', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(
        driver,
        10,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )
    return driver, wait

def write_smoothly(text, element):
    for char in text:
        element.send_keys(char)
        sleep(randint(1, 10) / 30)

def login_to_instagram(driver, wait):
    driver.get(INSTAGRAM_LOGIN_URL)
    sleep(3)

    email_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
    write_smoothly(USERNAME, email_field)
    sleep(2)

    password_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
    write_smoothly(PASSWORD, password_field)
    sleep(2)

    enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Entrar"]')))
    enter_button.click()
    sleep(10)

def like_latest_post(driver, wait):
    driver.get(INSTAGRAM_PROFILE_URL)
    sleep(8)

    while True:
        try:
            # Localizar e clicar na última postagem
            last_post = wait.until(EC.visibility_of_any_elements_located((By.XPATH, '//div[@class="_aagw"]')))
            last_post[0].click()
            sleep(4)

            # Verificar se o botão de curtir está presente
            like_button = wait.until(EC.visibility_of_any_elements_located((By.XPATH, '//*[@aria-label="Curtir"]')))
            driver.execute_script("arguments[0].scrollIntoView();", like_button[0])
            sleep(1)
            like_button[0].click()
            print('Deu certo! A imagem acabou de ser curtida.')
        except TimeoutException:
            print('Imagem já havia sido curtida ou não foi possível localizar o botão!')
        except Exception as e:
            print(f'Ocorreu um erro inesperado: {e}')
        finally:
            sleep(86400)  # Espera 24 horas

# Função principal
def main():
    driver, wait = initial_driver()
    try:
        login_to_instagram(driver, wait)
        like_latest_post(driver, wait)
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

