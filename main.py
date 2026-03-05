from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import defs

indice = input("Input your CPF or CNPJ. Only numbers: ")
email_antigo = input("Input the old email: ")
new_email = input("Input the new email: ")

email = input("Input your email: ")
password = input("Input your password: ")

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("your_website_url_here")

wait = WebDriverWait(driver, 20)


defs.login(wait, driver, email, password)

defs.busca_text(wait, "label", "Administração")


defs.busca_text(wait,"label","Clientes do Site")

defs.selecionar_documento(indice, wait)

register = wait.until(
    EC.presence_of_element_located((By.ID, "input-search"))
)
register.send_keys(indice)
register.send_keys(Keys.ENTER)


btn_cadastro = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@title='Editar']"))
)
btn_cadastro.click()

wait.until(
    EC.visibility_of_element_located((By.ID, "input-email"))
)

defs.validador_cpf_cnpj(indice)


if len(indice) == 11:
    dados = defs.values_pf(wait)
else:
    dados = defs.values_pj(wait)

email_sistema = dados["Email"]


print("Dados encontraados")
for chave, valor in dados.items():
    print(f"{chave}: {valor}")

confirmar = input("Confirma alteração do email? (s/n): ").lower()

valido = defs.gmail_validator(email_sistema, email_antigo)

if valido and confirmar == "s":
    new_email(wait, driver)

else:
    print("Operação cancelada.")

input("Pressione ENTER para sair...")
driver.quit()
