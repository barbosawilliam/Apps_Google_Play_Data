# PROGRAMA QUE VAI BUSCAR A LISTA DE APPS EM ALTA ("lista_apps.txt") E VAI PROCURAR, A PARTIR DO URL DESTES,
# OS APPS SEMELHANTES QUE PERTENCEM À MESMA CATEGORIA

# DIFERENTE DOS DATAFRAMES RELATIVOS AOS TOP45 APPS, NÃO HÁ UMA COLUNA 'RANKING'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

def main():
    #Inicializando uma aba do Google Chrome
    link_google_play = 'https://play.google.com/store/apps'
    driver = Inicializa_Navegador(link_google_play)

    #Fazendo a leitura de todos os apps encontrados ao ler os Apps em Alta
    arquivo = open("lista_apps.txt", "r")
    conteudo = arquivo.readlines()
    arquivo.close()

    #Lendo os 135 apps encontrados e seus apps semelhantes
    lista_geral = [] # Lista que vai armazenar a leitura dos encontrados
    links_lidos = [] # Salvar os apps que já foram lidos
    for linha in conteudo:
        try:
            linha = linha.split(",")
            link = linha[0]
            print(f"Lendo o aplicativo: {link}")
            categoria = linha[1]

            #Extraindo informações do App inicial
            driver.get(link)
            sleep(2)
            leitura_app = Extrai_Dados(driver, categoria)

            #Adicionando a leitura do app na lista 'lista_geral'
            lista_geral.append(leitura_app)
            links_lidos.append(link)
            
            #Fechando a aba de informações
            xpath_close = '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[1]/button'
            driver.find_element(By.XPATH, xpath_close).click()

            #Buscando os apps semelhantes a esse
            lista_apps_semelhantes = []
            try:
                xpath_titulo = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[2]/section/header/div/div[1]/h2/span'
                titulo = driver.find_element(By.XPATH, xpath_titulo).text

                if (titulo == "Apps semelhantes"):

                    xpath_semelhantes = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[2]/section/header/div/div[2]/a'
                    link_semelhantes = driver.find_element(By.XPATH, xpath_semelhantes).get_attribute("href")
                    driver.get(link_semelhantes)

                    Libera_Apps (driver)
                    lista_apps_semelhantes = Encontra_Apps_Semelhantes(driver, categoria)

            except:
                pass

        except:
            pass
        #Preciso verificar se o app já foi adicionado na lista
        for app in lista_apps_semelhantes:
            link_semelhante = app[0]
            print(f"Lendo o app: {link_semelhante}")
            if (link_semelhante not in links_lidos):
                #fazer a leitura desse link, salvando na categoria 'app[1]'
                driver.get(link_semelhante)
                sleep(1)
                leitura_app = Extrai_Dados(driver, categoria)
                lista_geral.append(leitura_app)
                links_lidos.append(link_semelhante)
        
        
    print(f"Quantidade de apps lidos: {len(lista_geral)}")
    #Pegando as informações da 'lista_geral' e salvando em um DataFrame
    colunas = ["App", "Categoria", "Downloads", "Tipo", "Preco", "Nota", "Avaliacoes", "Contem_Anuncios", "Compras_no_App", "Versao", "Ultima_Atualizacao", "Android", "Classificacao_Conteudo", "Lancamento"]
    df = pd.DataFrame(lista_geral, columns=colunas)

    #Salvando o DataFrame em um arquivo .csv
    df.to_csv("dataframe_geral.csv", index=False)

def Encontra_Apps_Semelhantes (driver, categoria):
    xpath_apps = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/c-wiz/div/c-wiz/c-wiz/c-wiz/section/div/div/div/div/div/div'
    apps = driver.find_elements(By.XPATH, xpath_apps)
    print(f"Quantidade de apps encontrados: {len(apps)}")
    lista_apps = []
    for app in apps:
        link = app.find_element(By.XPATH, ".//div/div/a").get_attribute("href")
        print("Link encontrado: ", link)
        lista_apps.append([link, categoria])
    
    return lista_apps

def Inicializa_Navegador (link):
    print("Inicializando o navegador...")
    driver = webdriver.Chrome()
    driver.get(link)
    return driver

def Formata_Dimensao (leitura):
    multiplicador = 1
    numero = float(leitura[0].replace(',', '.'))
    if (leitura[1] == 'mil'):
        multiplicador *= 10**3
    elif (leitura[1] == 'mi'):
        multiplicador *= 10**6
    elif (leitura[1] == 'bi'):
        multiplicador *= 10**9
        
    return int(numero * multiplicador)

def Formata_Data(data):
    data = data.replace(".", "").split()
    dic_meses = {
        "jan":"01",
        "fev":"02",
        "mar":"03",
        "abr":"04",
        "mai":"05",
        "jun":"06",
        "jul":"07",
        "ago":"08",
        "set":"09",
        "out":"10",
        "nov":"11",
        "dez":"12"
    }
    dia = data[0]
    mes = dic_meses[data[2]]
    ano = data[-1]
    data_final = dia+'/'+mes+"/"+ano
    return data_final

def Libera_Apps (driver):
    altura = 100
    for i in range(10):
        driver.execute_script("window.scrollTo(0," + str(altura) + ")")
        altura += 300

    driver.execute_script("window.scrollTo(0,0)") #Voltando para o topo da página.

def Extrai_Dados(driver, categoria):
    xpath_nome = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/span'
    nome_app = driver.find_element(By.XPATH, xpath_nome).text

    xpath_cabecalho = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div'
    infos_introdutorias = driver.find_elements(By.XPATH, xpath_cabecalho)
    nota_app = 0
    num_avaliacoes = 0
    for info in infos_introdutorias:
        leitura = info.find_element(By.XPATH, ".//div[2]").text
        for valor in leitura.split():
            if (valor == "avaliações"):
                num_avaliacoes = Formata_Dimensao(leitura.split())
                nota_app = info.find_element(By.XPATH, ".//div[1]/div/div").text.split()[0]
                nota_app = float(nota_app.replace(",", "."))

    xpath_botao_instalar = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/c-wiz/div/div/div/div/button/span'
    conteudo_botao = driver.find_element(By.XPATH, xpath_botao_instalar).text
    tipo = 'Gratuito'
    preco = 0
    if (conteudo_botao != "Instalar"):
        tipo = "Pago"
        preco = float(conteudo_botao.split()[2][:-1].replace(",", "."))

    contem_anuncios = "Não"
    compras_no_app = "Não"

    try:
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div[2]')
        content1 = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div[2]/div/span[1]').text
        if (content1 == "Contém anúncios"):
            contem_anuncios = "Sim"
        elif (content1 == "Compras no app"):
            compras_no_app = "Sim"
        
        try:
            content2 = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div[2]/div/span[2]').text
            if (content2 == "Contém anúncios"):
                contem_anuncios = "Sim"
            elif (content2 == "Compras no app"):
                compras_no_app = "Sim"
        except:
            pass
    except:
        pass

    height = 300
    driver.execute_script("window.scrollTo(0," + str(height) + ")") # Descendo um pouco a página para clicar em "Sobre este app"

    mudou_de_pagina = False
    while (not mudou_de_pagina):
        try:
            xpath_botao_infos = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[2]/button'
            driver.find_element(By.XPATH, xpath_botao_infos).click() #Abrindo "Sobre este app"
            mudou_de_pagina = True
        except:
            height += 300
            driver.execute_script("window.scrollTo(0," + str(height) + ")") # Descendo mais um pouco a página
    sleep(1)

    informacoes = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[2]/div[3]/div')
        
    #Inicializando variáveis
    versao_app = ''
    ultima_atualizacao = ''
    android_min = ''
    num_downloads_min = ''
    classificacao_usuarios = ''
    data_lancamento = ''

    for info in informacoes:
        titulo_campo = info.find_element(By.XPATH, "./div[1]").text
        valor_campo = info.find_element(By.XPATH, "./div[2]").text
        match titulo_campo:
            case "Versão":
                versao_app = valor_campo
            case "Atualizado em":
                ultima_atualizacao = valor_campo
                ultima_atualizacao = Formata_Data(ultima_atualizacao)
            case "Requer Android":
                android_min = valor_campo.split()[0]
            case "Downloads":
                num_downloads_min = valor_campo.split()[0].replace("+", "")
                num_downloads_min = int(num_downloads_min.replace(".", ""))
            case "Classificação do conteúdo":
                classificacao_usuarios = valor_campo.replace("Saiba mais", "").strip()
            case "Lançado em":
                data_lancamento = valor_campo
                data_lancamento = Formata_Data(data_lancamento)

    lista_geral = [nome_app, categoria, num_downloads_min, tipo, preco, nota_app, num_avaliacoes, contem_anuncios, compras_no_app, versao_app, ultima_atualizacao, android_min, classificacao_usuarios, data_lancamento]
    return lista_geral    

main()