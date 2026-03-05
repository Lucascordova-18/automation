from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import re
import time

def retry_click(func):
    def interna(*args, **kwargs):
        for trys in range(3):
            try:
                return func(*args, **kwargs)
            except TimeoutException:
                print(f"Click falhou na tentativa {trys + 1}. Retentando...")
                time.sleep(1) 
    return interna


@retry_click
def busca_text (wait, tag, text):
    click_text = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//{tag}[contains(. , '{text}')]"))
    )
    click_text.click()
    return click_text

def validador_cpf_cnpj(documento):
    documento = re.sub(r'\D', '', documento)

    if len(documento) == 11:
        return "CPF"
    elif len(documento) == 14:
        return "CNPJ"
    else:
        raise ValueError("Documento inválido. Deve ser CPF (11 dígitos) ou CNPJ (14 dígitos).")

def login (wait, driver, email, senha):
    usuario = wait.until(
    EC.presence_of_element_located((By.ID, "input-email"))
    )
    usuario.send_keys(email)

    senha_login = driver.find_element(By.ID, "input-password")
    senha_login.send_keys(senha)

    busca_text(wait,"button" , "Entrar")


def selecionar_documento(numbers, wait):
    if len(numbers) == 14:
        busca_text(wait,"button", "CNPJ")
    
    elif len(numbers) == 11:
        busca_text(wait, "button", "CPF")
    else:
        print("Documento inválido!")


def values_pf(wait):
    dados = {}

    try:
        wait.until(EC.visibility_of_element_located((By.ID, "input-email")))

        name = wait.until(
            EC.presence_of_element_located((By.ID, "input-name"))
        ).get_attribute("value")

        cpf = wait.until(
            EC.presence_of_element_located((By.ID, "input-cpf"))
        ).get_attribute("value")

        phone = wait.until(
            EC.presence_of_element_located((By.ID, "input-phone1"))
        ).get_attribute("value")

        email = wait.until(
            EC.presence_of_element_located((By.ID, "input-email"))
        ).get_attribute("value")

        dados["Type"] = "PF"
        dados["Name"] = name
        dados["CPF"] = cpf
        dados["Phone"] = phone
        dados["Email"] = email

        return dados

    except TimeoutException:
        print("Erro ao coletar dados do cliente PF. Algum campo não foi encontrado.")
        return None

def values_pj(wait):
    dados = {}

    try:
        wait.until(EC.visibility_of_element_located((By.ID, "input-email")))

        name = wait.until(
            EC.presence_of_element_located((By.ID, "input-name"))
        ).get_attribute("value")

        cnpj = wait.until(
            EC.presence_of_element_located((By.ID, "input-cnpj"))
        ).get_attribute("value")

        phone = wait.until(
            EC.presence_of_element_located((By.ID, "input-phone1"))
        ).get_attribute("value")

        email = wait.until(
            EC.presence_of_element_located((By.ID, "input-email"))
        ).get_attribute("value")

        dados["Type"] = "PJ"
        dados["Name Corporative"] = name
        dados["CNPJ"] = cnpj
        dados["Phone"] = phone
        dados["Email"] = email

        return dados

    except TimeoutException:
        print("Erro ao coletar dados do cliente PJ. Algum campo não foi encontrado.")
        return None

def email_validator(email_sistema, email_antigo):
    if email_sistema.strip().lower() == email_antigo.strip().lower():
        print("Email validado. Pode atualizar.")
        return True
    else:
        print("Email informado não bate com o cadastro.")
        return False

def insert_new_email (wait, driver, new_email):
    campo_email = wait.until(
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    campo_email.clear()
    campo_email.send_keys(new_email)

    campo_email_csat = wait.until(
        EC.element_to_be_clickable((By.ID, "input-nps_email"))
    )
    campo_email_csat.clear()
    campo_email_csat.send_keys(new_email)
    
    driver.save_screenshot(r"screenshot.png")

    busca_text(wait,"button", "Salvar")