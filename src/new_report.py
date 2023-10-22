#%%
from fpdf import FPDF
import pandas as pd

from pathlib import Path
from datetime import datetime

dir_figures = Path() / 'figures'
dados_file = Path() / '..' / 'dados'

df = pd.read_excel(dados_file / 'avaliacao_fisica.xlsx')

# Tamanho da página A$ do PDF
WIDTH = 210
HEIGHT = 297

DATE =  datetime.now().strftime('%Y-%m-%d')



def create_title(day, pdf):
    # Unicode is not yet supported in the py3k version; use windows-1252 standard font
    pdf.set_font('Arial', '', 24)  
    pdf.ln(60)
    pdf.write(5, f"Bruno Analytics Report")
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'{day}')
    pdf.ln(5)


def create_first_page(pdf, date=DATE):
    pdf.add_page()

    image_path_letterHead = Path() / '..' / 'resources' / "letterhead_cropped.png" # Imagem temporária
    pdf.image(str(image_path_letterHead), 0, 0, WIDTH)
    create_title(day=date, pdf=pdf)

    image_path_back = Path() / '..' / 'resources' / "capa.png"
    pdf.image(str(image_path_back), 5, 90, WIDTH-20)


def create_second_page(pdf, data):
    pdf.add_page()
    pdf.set_fill_color(230,230,230) # setar a cor de fundo da célula RGB
    pdf.cell(w=40, h=10, txt='Dados Pessoais', fill=True) # Habilitar que o fundo deve ser Preenchido fill=True

    df = data.tail(1)[['Data','Peso', 'Altura','IMC','%_Gordura']]

    for index, row in df.iterrows():
        data_dict = {}
        data_dict['Nome'] = 'Bruno'
        data_dict['Peso'] = row['Peso']
        data_dict['Altura'] = row['Altura']
        data_dict['IMC'] = row['IMC']
        data_dict['%_Gordura'] = row['%_Gordura']
        data_dict['Últ. Av'] = pd.to_datetime(row['Data'], format='%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    for label, value in data_dict.items():
        pdf.ln(15)
        pdf.cell(40, 10, label + ': ', border=1)
        pdf.cell(60, 10, str(value), border=1)


def create_report(date=DATE, filename='report.pdf'):


    pdf = FPDF() # Objeto PDF, as propriedades podem ser ajustadas em PDF()

    '''First Page'''
    create_first_page(pdf=pdf)

    '''Second Page'''
    create_second_page(pdf=pdf, data=df)


    '''Third Page'''
    pdf.add_page()
    
    name = "Bruno"
    pdf.cell(40, 10, f'Avaliação Física de {name} em Perspectiva Gráfica: Insights e Conclusões')
    
    # Realizando ajuste de tamanho da imagem/localização
    pdf.image(f'{dir_figures}/fig1.png', x=5, y=30, w=WIDTH/2-5)

    # Simulando uma segunda imagem 
    pdf.image(f'{dir_figures}/fig1.png', x=WIDTH/2-5, y=30, w=WIDTH/2-5)


    '''Fourth Page'''
    pdf.add_page()

    pdf.cell(h=40, w=10, txt=f'Avaliação Física de {name} em Perspectiva Gráfica: Insights e Conclusões', )
    pdf.image(f'{dir_figures}/fig2.png', x=5, y=100, w=WIDTH-5)


    pdf.output(filename, 'F')


if __name__ == '__main__':
    create_report()

# %%

# Selecionar as colunas a serem mantidas (exceto a coluna 'Data')
colunas = df.columns[1:]

# Realizar o "unpivot" das colunas
df = df.melt(id_vars=['Data'], value_vars=colunas, var_name='Musculo', value_name='Valores')
