#%%
import pandas as pd
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from pandas.plotting import table

from matplotlib.backends.backend_pdf import PdfPages

dados_file = Path() / '..' / 'dados'
dir_figures = Path() / 'figures'

df = pd.read_excel(dados_file / 'avaliacao_fisica.xlsx')

def analytics(dataframe: pd.DataFrame, local: str, name_file: str) -> plt.Figure:
    df = dataframe
    #df['Data'] = pd.to_datetime(df['Data'])
    #df['Ano_Mes'] = df['Data'].dt.to_period('M')

    # Converter Ano_Mes em strings no formato desejado (por exemplo, "2022-01")
    #df['Ano_Mes'] = df['Ano_Mes'].dt.strftime('%Y-%m')

    colunas = df.columns[1:]

    # Realizar o "unpivot" das colunas
    df = df.melt(id_vars=['Data'], value_vars=colunas, var_name='Musculo', value_name='Valores')

    # Sistema de Grids

    # Cor Fundo de Fundo
    #Cor_Fundo = '#f5f5f5'

    # Criar o sistema de Grids
    Grid_Graficos = sns.FacetGrid( df, col='Musculo', hue='Musculo', col_wrap=4 )

    # Adicionar grafico linhas em cada gráfico
    Grid_Graficos = Grid_Graficos.map( plt.plot, 'Data', 'Valores')

    # Adiconar uma sombra + Ajuste do titulo
    #Grid_Graficos = Grid_Graficos.map( plt.fill_between,  'Data', 'Valores', alpha=0.2).set_titles('{col_name} Musculo')

    # Filtrar o titulo
    Grid_Graficos = Grid_Graficos.set_titles('{col_name}')

    # Adicionar um subtitulo
    Grid_Graficos = Grid_Graficos.fig.suptitle(
        'Acompanhamento temporal dos musculos \n Autor @bruno.cardoso',
        fontsize=18
    )

    # Ajustando
    plt.subplots_adjust( top=0.92 )
    plt.savefig(fname=f'{local}/{name_file}.png', dpi=300, format=None)




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


def transpor_Table(dataframe: pd.DataFrame, local: str, name_file: str) -> plt.Figure:
    """Realizar mudança na estrutura da tabela original extraída dos documentos .png"""
    
    data = dataframe

    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d')
    # Transpor o DataFrame, de colunas para linhas
    data = data.T

    # Definir a primeira linha como o cabeçalho
    new_header = data.iloc[0]
    data = data[1:]
    data.columns = new_header

    # Remover a linha de Ano-Mes
    data = data.drop(data.index[-1])

    # Criar a figura e o eixo
    fig, ax = plt.subplots(figsize=(10, 8)) # Ajuste de largura e altura
    ax.axis('off')  # Desativa os eixos

    # Transformar a tabela em uma figura de tabela
    tab = table(ax, data, loc='center', colWidths=[0.1] * len(data.columns))

    # Estilizar a figura de tabela
    tab.auto_set_font_size(False)
    tab.set_fontsize(8)
    tab.scale(1.5, 1.5)

    # Salvar a figuara em .pnh
    plt.savefig(fname=f'{local}/{name_file}.png', dpi='figure', format=None) # dpi['figure']: Para trabalhar como figura, para retorno original dpi=100
    plt.close()  # Fecha a figura para liberar recursos


if __name__ == "__main__":
    df = pd.read_excel(dados_file / 'avaliacao_fisica.xlsx')


    fig1 = analytics(dataframe=df,local=dir_figures, name_file='figGride')
    fig2 = weight_evolution_curve(dataframe=df, column_name='Peso', local=dir_figures, name_file='fig1')
    fig3 = transpor_Table(dataframe=df, local=dir_figures, name_file='fig2')
# %%