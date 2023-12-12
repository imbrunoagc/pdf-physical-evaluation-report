"""modulo de extract necessárias para consolidar os dados de entrada."""

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

def extract_data(input_folder: str = documentos_dir) -> pd.DataFrame:
    """
    função para extrair dados de arquivos png.

    type: input_folder: str
    """

    df = pd.DataFrame(columns=['Data', 'Peso', 'Altura', 'IMC', '%_Gordura', 'Massa_Magra',
        'Massa_Gorda', '%_Gordura_Bio_', 'Massa_Gorda_', 'DC_', 'DC_Peitoral',
        'DC_Abdominal', 'DC_Coxa', 'Risco_=_=', 'vo', 'Ombro', 'Torax_Relaxado',
        'Térax_Inspirado', 'Abdome', 'Cintura', 'Quadril', 'RCQ',
        'Antebraco_Esq', 'Antebrago_Dir', 'Brago_Relax_', 'Braco_Relax_Dir',
        'Brago_Contr_', 'Brago_Contr_Dir', 'Coxa_Esq', 'Coxa_Dir'])

    for file in input_folder.glob("*.jpg"): # Filtro dos arquivos .jpg
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

    return df


def transpor_table_for_date(data: pd.DataFrame) -> pd.DataFrame:
    """
    função para transformar a estrutura do dataframe extraido dos arquivos .png.
    Colunas por data, linhas músculos e valores respectivos por tempo.

    type: data: pd.DataFrame
    """

    data['Data'] = pd.to_datetime(data['Data'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d')
    # Transpor o DataFrame, de colunas para linhas
    data = data.T

    # Definir a primeira linha como o cabeçalho
    new_header = data.iloc[0]
    data = data[1:]
    data.columns = new_header

    data.reset_index(inplace=True)
    # Remover a linha de Ano-Mes
    #data = data.drop(data.index[-1])

    return data


def transpor_table_for_valuesRow(data: pd.DataFrame) -> pd.DataFrame:
    """
    função para transformar a estrutura do dataframe extraido dos arquivos .png.
    3 colunas: Data, Musculo e Valores.

    type: data: pd.DataFrame
    """
    colunas = data.columns[1:]

    # Realizar o "unpivot" das colunas
    data = data.melt(id_vars=['Data'], value_vars=colunas, var_name='Musculo', value_name='Valores')
    data['Data'] = pd.to_datetime(data['Data'])
    data['Ano_Mes'] = data['Data'].dt.to_period('M')

    # Converter Ano_Mes em strings no formato desejado (por exemplo, "2022-01")
    data['Ano_Mes'] = data['Ano_Mes'].dt.strftime('%Y-%m')


    return data


def union_all_data():
    df1 = extract_data()
    df2 = transpor_table_for_date(data=df1)
    df3 = transpor_table_for_valuesRow(data=df1)

    sheet = {
        "raw_data": df1,
        "data_for_date": df2,
        "unpivot_for_valueInRow": df3
    }

    return sheet

if __name__ == "__main__":

    sheets = union_all_data()
    
    file_output = dados_dir / 'avaliacao_fisica.xlsx'
    
    with pd.ExcelWriter(file_output) as writer:
        for sheet_name in sheets.keys():
            sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Dados salvos em {file_output}")