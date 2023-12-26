"""modulo de gerar visoes necessárias para a análise de resultados físico."""
#%%
import pandas as pd
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from report_utils import classificar_composicao_corporal
from pandas.plotting import table

from matplotlib.backends.backend_pdf import PdfPages

dados_file = Path() / '..' / 'dados'
dir_figures = Path() / 'figures'

def read_data(name: str='raw_data') -> pd.DataFrame:
    df = pd.read_excel(dados_file / 'avaliacao_fisica.xlsx', sheet_name=name)
    return df

df = read_data()

def analytics(local: str = None, name_file: str = None):

    df = read_data(name='unpivot_for_valueInRow')

    return df


def weight_evolution_curve(dataframe: pd.DataFrame, column_name: str, local: str, name_file: str) -> plt.Figure:
    df = dataframe
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Classificar o DataFrame por data
    df = df.sort_values(by='Data')
    
    # Calcular o crescimento percentual
    initial_weight = df[column_name].iloc[0]
    df['Crescimento Percentual (%)'] = ((df[column_name] - initial_weight) / initial_weight) * 100

    fig = plt.figure() #figsize=(8, 5)
    plt.plot(df['Data'], df[column_name], marker='o', linestyle='-', label='Peso (kg)')
    plt.plot(df['Data'], df['Crescimento Percentual (%)'], marker='o', linestyle='-', label='Crescimento Percentual (%)')
    plt.title('Evolução do Peso com Crescimento Percentual')
    plt.xlabel('Data')
    plt.grid(True)
    plt.legend()

    # Adicionar rótulos absolutos acima da linha de peso
    for i, weight in enumerate(df[column_name]):
        plt.annotate(f'{weight:.2f} kg', (df['Data'].iloc[i], weight), textcoords="offset points", xytext=(0,10), ha='center')
    
    # Adicionar rótulos percentuais acima da linha de crescimento percentual
    for i, percent in enumerate(df['Crescimento Percentual (%)']):
        plt.annotate(f'{percent:.2f}%', (df['Data'].iloc[i], percent), textcoords="offset points", xytext=(0,10), ha='center')

    # Mostrar o gráfico
    plt.xticks(rotation=45)  # Rotação dos rótulos no eixo x para melhor visualização
    plt.tight_layout()
    plt.savefig(fname=f'{local}/{name_file}.png', dpi='figure', format=None)
    plt.close()  # Fecha a figura para liberar recursos




def Table(local: str=None, name_file: str=None) -> plt.Figure:
    """Realizar mudança na estrutura da tabela original extraída dos documentos .png"""
    
    data = read_data(name='data_for_date')

    # Criar a figura e o eixo
    fig, ax = plt.subplots(figsize=(10, 8)) # Ajuste de largura e altura
    ax.axis('off')  # Desativa os eixos

    # Transformar a tabela em uma figura de tabela
    tab = table(ax, data, loc='center', colWidths=[0.1] * len(data.columns))

    # Estilizar a figura de tabela
    tab.auto_set_font_size(False)
    tab.set_fontsize(8)
    tab.scale(1.5, 1.5)

    # Salvar a figuara em .png
    plt.savefig(fname=f'{local}/{name_file}.png', dpi='figure', format=None) # dpi['figure']: Para trabalhar como figura, para retorno original dpi=100
    plt.close()  # Fecha a figura para liberar recursos




def comparative_muscle_left_and_right(left_name: str=None, right_name: str=None, local: str=None, name_file: str=None) -> plt.Figure:
    
    df = read_data(name='unpivot_for_valueInRow')

    esquerdo = df[df['Musculo'] == left_name]
    direito = df[df['Musculo'] == right_name]

    # Combine o nome do músculo com o valor
    esquerdo['Musculo-Valor'] = esquerdo['Musculo'] + ' ' + esquerdo['Valores'].astype(str)
    direito['Musculo-Valor'] = direito['Musculo'] + ' ' + direito['Valores'].astype(str)

    # Classifique os DataFrames com base na nova coluna
    esquerdo = esquerdo.sort_values(by='Musculo-Valor')
    direito = direito.sort_values(by='Musculo-Valor')

    plt.figure(figsize=(10, 6))
    plt.plot(esquerdo['Ano_Mes'], esquerdo['Valores'], marker='o', label=left_name)
    plt.plot(direito['Ano_Mes'], direito['Valores'], marker='o', label=right_name)

    plt.xlabel('Ano_Mes')
    plt.ylabel('Valores')
    plt.title(f'Comparativo de {left_name} e {right_name}')
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()

    # Salvar a figura em .png
    plt.savefig(fname=f'{local}/{name_file}.png', dpi=300, format='png')
    plt.close()


def circleMassaMagraXGorda(local: str, name_file: str, massaMagra: float, massaGorda: float): 
    # Rótulos para as fatias
    rotulos = ['Massa Magra', 'Massa Gorda']

    # explosão da parte desejada
    explode = [0, 0.1]

    fig1, ax1 = plt.subplots(figsize=(6,6))

    # setando cores dos pedações
    cores = ["#3CB371", "#ADFF2F"]

    # Construção da visão gráfica
    ax1.pie([massaMagra, massaGorda], explode=explode, labels=rotulos, autopct='%1.1f',
            shadow=True, startangle=90, colors=cores)

    ax1.axis('equal')
    plt.savefig(fname=f'{local}/{name_file}.png', dpi=300, format='png')


###########################################
df = pd.read_excel(dados_file / 'avaliacao_fisica.xlsx', sheet_name="unpivot_for_valueInRow")
df = df[df['Ano_Mes'] == "2023-09"]

###########################################

var_peso = df[df['Musculo'] == "Peso"]["Valores"].values[0]

###########################################

var_altura = df[df['Musculo'] == "Altura"]["Valores"].values[0]

###########################################

indice_linha_IMC = df[df['Musculo'] == "IMC"].index[0]
var_IMC = df.loc[indice_linha_IMC, "Valores"]

var_IMC = float(var_IMC)  # Convertendo para float, se necessário
cls_imc = classificar_composicao_corporal("IMC", var_IMC)
text_IMC = f"{var_IMC} - {cls_imc}"

###########################################

var_peitoral = df[df["Musculo"] == "DC_Peitoral"]["Valores"].values[0]

var_abdominal = df[df["Musculo"] == "DC_Abdominal"]["Valores"].values[0]

var_coxa = df[df["Musculo"] == "DC_Coxa"]["Valores"].values[0]


###########################################

porcentage_gordura_ideal = 14.00
text_gorduraIdeal = f"% Gordura ideal: {porcentage_gordura_ideal}%"
###########################################

indice_porcentagemGordura = df[df["Musculo"] == "%_Gordura"].index[0]
var_porcentagem_gordura = df.loc[indice_porcentagemGordura, "Valores"]

var_porcentagem_gordura = var_porcentagem_gordura.replace("%","")
var_porcentagem_gordura = float(var_porcentagem_gordura)
cls_porcentagem_gordura = classificar_composicao_corporal(musculo="%_Gordura", valor=var_porcentagem_gordura)

###########################################

indice_massaMagra = df[df["Musculo"] == "Massa_Magra"].index[0]
var_massaMagra = df.loc[indice_massaMagra, "Valores"]

var_massaMagra = float(var_massaMagra)
cls_massaMagra = classificar_composicao_corporal(musculo="Massa_Magra", valor=var_massaMagra)

###########################################

indice_massaGorda = df[df["Musculo"] == "Massa_Gorda"].index[0]
var_massaGorda = df.loc[indice_massaGorda, "Valores"]

var_massaGorda = float(var_massaGorda)
cls_massaGorda = classificar_composicao_corporal(musculo="Massa_Gorda", valor=var_massaGorda)

if __name__ == "__main__":
    df = read_data()

    #fig1 = analytics(dataframe=df,local=dir_figures, name_file='figGride')
    fig2 = weight_evolution_curve(dataframe=df, column_name='Peso', local=dir_figures, name_file='fig_evolucaoPeso')
    fig3 = Table(local=dir_figures, name_file='fig_table')
    fig4 = comparative_muscle_left_and_right(left_name='Antebraco_Esq', right_name='Antebrago_Dir', local=dir_figures, name_file='fig_compAntebraco')
    fig5_circleMG = circleMassaMagraXGorda(local=dir_figures, name_file='fig_circleMassa_Magra_Gorda', massaMagra=var_massaMagra, massaGorda=var_massaGorda)
# %%
