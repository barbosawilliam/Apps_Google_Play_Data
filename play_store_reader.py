from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

# Funções auxiliares
def Adiciona_Link_em_Lista (link_atual, lista_links, categoria):
    """
    Função void que vai adicionar 'link_atual' em 'lista_links' na devida 'categoria'.
    Se o 'link_atual' já estiver dentro da 'lista_links', então verifica se a 'categoria' já está na 'lista_links'

    Param: 
        link_atual: str com o link do app
        lista_links: lista que contém os links dos apps e as categorias a que pertencem
            (ex. [[link1, [categoria1, categoria2]], [link33, [categoria3]]])
        categoria: str com a categoria que está sendo buscada

    Return:
        void
    """
    ja_registrado = False
    for registro in lista_links:
        if (link_atual in registro):
            if (categoria not in registro[1]):
                registro[1].append(categoria)
            ja_registrado = True
    
    if (not ja_registrado):
        lista_links.append([link_atual, [categoria]])

def Inicializa_Chrome (link):
    driver = webdriver.Chrome() #Criando uma instância do Google Chrome e salvando na variável 'driver'
    driver.get(link) #Navegando para o URL de interesse
    return driver

def Libera_Categorias (driver):
    # Antes de buscar as categorias, vou descer a página para liberar todas (algumas começam ocultas) 
    xpath_mostrar_mais = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/div/div/span/span'
    achou_botao = False

    while (not achou_botao):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        try:
            botao_mostrar_mais = driver.find_element(By.XPATH, xpath_mostrar_mais)
            print(f"Todas as categorias estão visíveis.")
            botao_mostrar_mais.click()
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            achou_botao = True
        except:
            # print("Ainda não achei o botão.")
            pass
        
    driver.execute_script("window.scrollTo(0,0)") #Voltando para o topo da página.

def Registra_Apps (driver, categorias_apps):
    #Localizando todas as divisões que contêm as categorias de Apps
    xpath_element = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz'
    elements = driver.find_elements(By.XPATH, xpath_element)
    print("Elementos localizados.")

    lista_link_apps = [] #Lista onde serão guardados os links dos apps encontrados com as categorias a que pertencem
    for element in elements:
        try:
            categoria = element.find_element(By.XPATH, ".//c-wiz/section/header/div").text
            
            if (categoria in categorias_apps): # Se o elemento lido está dentro da lista de categorias dos apps, então pegar os apps dela
            #if (categoria == "Comunicação"): #APAGAR ***************************************************
                
                apps = element.find_elements(By.XPATH, './/c-wiz/section/div/div/div/div/div/div[1]/div') # Caminho para todos os apps de uma categoria
                print(f"Quantidade de apps na categoria '{categoria}': {len(apps)}")
                #print("Link dos apps dessa categoria:")
                for app in apps:
                    app_link = app.find_element(By.XPATH, ".//div/div/a").get_attribute("href")
                    Adiciona_Link_em_Lista(app_link, lista_link_apps, categoria)
                    #print(app_link)
                
        except:
            pass
            # print("Elemento sem categoria.")
            # print(element.text)


def main():
    categorias_apps = [
        'Comunicação',
        'Mapas e GPS',
        'Assista programas de TV e filmes',
        'Entretenimento',
        'Players e editores de vídeo',
        'Turismo e guia local',
        'Ferramentas e utilitários',
        'Novidades',
        'Navegadores para dispositivos móveis',
        'Arte e design',
        'Música e áudio',
        'Ferramentas de negócios',
        'Vá às compras',
        'Livros e referências',
        'Edição profissional de fotos',
        'Produtividade',
        'Apps premium',
        'Rede social',
        'Ferramentas de orçamento',
        'Programas de treino',
        'Solicite uma viagem'
    ]
    
    link_google_play = 'https://play.google.com/store/apps'
    driver = Inicializa_Chrome(link_google_play)

    Libera_Categorias(driver)
    lista_classificacao = Registra_Apps(driver, categorias_apps)

    print(f"Quantidade de Apps encontrados de forma primária: {len(lista_classificacao)}.")

main()