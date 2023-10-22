import cv2
import pytesseract
import re
import pandas as pd

from pathlib import Path


script_dir = Path('src')
documentos_dir = script_dir / '..' / 'documentos'
dados_dir = script_dir / '..' / 'dados'

# Defina o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\BRZN\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Função para verificar se a linha contém valores numéricos
def linha_contem_valores_numericos(linha):
    # Use uma expressão regular para verificar se há números na linha
    return re.search(r'\d+(\.\d+)?\b', linha) is not None

df = pd.DataFrame(columns=['Data', 'Peso', 'Altura', 'IMC', '%_Gordura', 'Massa_Magra',
    'Massa_Gorda', '%_Gordura_Bio_', 'Massa_Gorda_', 'DC_', 'DC_Peitoral',
    'DC_Abdominal', 'DC_Coxa', 'Risco_=_=', 'vo', 'Ombro', 'Torax_Relaxado',
    'Térax_Inspirado', 'Abdome', 'Cintura', 'Quadril', 'RCQ',
    'Antebraco_Esq', 'Antebrago_Dir', 'Brago_Relax_', 'Braco_Relax_Dir',
    'Brago_Contr_', 'Brago_Contr_Dir', 'Coxa_Esq', 'Coxa_Dir'])

for file in documentos_dir.glob("*.jpg"): # Filtro dos arquivos .jpg
    imagem = cv2.imread(str(file))  # Use str(file) para obter o caminho como uma string
    page = file

    texto = pytesseract.image_to_string(imagem).split('\n')

    # Desempacotamento de lista
    date, rest = texto[2], texto[3:]

    # Divida a lista de datas
    date = date.split(' ')

    print(page)
    print(date)

    # Lista de strings que devem ser removidas
    strings_a_remover = ["vo2 S o 3", "DC - Bicipital - = 5", "DC -... - S 2", "Massa Gorda... = - 5", "Panturrilha_Dir_oi", "Panturrilha_Dir_fin_ni", "Panturrilha_Dir)", "Panturrilha_Dir", "%_Gordura_Bio_", "Massa_Gorda_", "DC_", "Risco_=_=", "vo"]

    # Renomeação     
    rename_musculo = {' ': '_', '.':'',  '-':'', '__':'_', 'Panturrilha_Dir_oi': 'Panturrilha_Dir', 'Panturrilha_Dir_fin_ni': 'Panturrilha_Dir'}
    rename_valores = {'...': '', '. ': '', ' ': '/', '  ': '', '//': '/', '/':' '}
    
    # Filtrar a lista original para manter apenas as linhas que NÃO contêm valores numéricos
    avaliacao = [linha for linha in rest if linha_contem_valores_numericos(linha) and linha != '' and linha != 'None' if all(string not in linha for string in strings_a_remover)]

    data = []

    data.append(date)

    for row in avaliacao:
        musculo = re.search(r'.*?(?=\d)', row).group(0).strip() 
        
        for key, value in rename_musculo.items():
            musculo = musculo.replace(key, value)

        valores = row[len(musculo):]
        for key, value in rename_valores.items():
            valores = valores.replace(key, value)

        valores = re.sub(r'[a-zA-Z]', '', valores).strip()

        match = f'{musculo} {valores}'.replace('  ',';').replace(' ', ';')

        data.append(match.split(';'))

    df_temp = pd.DataFrame(data)

    # Transpor o DataFrame para que as datas, ordens e valores estejam nas colunas
    df_temp = df_temp.T

    # Definir as duas primeiras linhas como o cabeçalho
    df_temp.columns = df_temp.iloc[0]
    df_temp = df_temp[1:]

    # Reiniciar os índices do DataFrame
    df_temp = df_temp.reset_index(drop=True)

    # Concatenar com o DataFrame principal
    df = pd.concat([df, df_temp])

# Remover as colunas indesejas ( Contém erros de leitura ou não esperamos trabalhar com essas)
df.drop(columns=strings_a_remover[-7:], inplace=True)

# Remover Linhas None
df.dropna(inplace=True)

# remover linhas duplicadas, a 4º Avaliação fisica estava nas duas páginas
df.drop_duplicates(inplace=True)

# Converter a coluna "Data" para o tipo de dados datetime
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

# Ordenar o DataFrame com base na coluna "Data"
df = df.sort_values(by=['Data'], ascending=True)

pasta_documentos = Path('..') / 'documentos'
df.to_excel(dados_dir / 'avaliacao_fisica.xlsx', index=False)