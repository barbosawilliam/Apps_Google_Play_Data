# PROGRAMA QUE VAI BUSCAR A LISTA DE APPS EM ALTA ("lista_apps.txt") E VAI PROCURAR, A PARTIR DO URL DESTES,
# OS APPS SEMELHANTES QUE PERTENCEM À MESMA CATEGORIA

# DIFERENTE DOS DATAFRAME RELATIVOS AOS TOP45 APPS, NÃO HÁ UMA COLUNA 'RANKING'

def main():
    arquivo = open("lista_apps.txt", "r")
    conteudo = arquivo.readlines()
    arquivo.close()
    for linha in conteudo:
        print(linha)
main()