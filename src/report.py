#%%
from fpdf import FPDF
import pandas as pd

from pathlib import Path
from datetime import datetime

dir_figures = Path() / 'figures'
dados_file = Path() / '..' / 'dados'

df = pd.read_excel(dados_file / 'avaliacao_fisica.xlsx', sheet_name='raw_data')


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

    image_path_letterHead = Path() / '..' / 'resources' / "cabecalho.png" # Imagem temporária
    pdf.image(str(image_path_letterHead), 0, 0, WIDTH)
    create_title(day=date, pdf=pdf)

    image_path_back = Path() / '..' / 'resources' / "capa-evolucao-fisica.jpg"
    pdf.image(str(image_path_back), 5, 90, WIDTH-10)


def create_second_page(pdf, data):
    # Criar uma nova página
    pdf.add_page()
    
    # Configurar a cor de preenchimento RGB para a barra
    pdf.set_fill_color(65, 138, 179)
    
    # Desenhar a barra na parte superior da página (tamanho da folha A4)
    pdf.rect(0, 0, 210, 20, 'F')  # Retângulo que inicia no canto superior esquerdo
    
    # Configurar a fonte para o título
    pdf.set_font('Arial', 'B', 22)
    pdf.set_text_color(255, 255, 255)  # Configurar a cor do texto para branco
    pdf.cell(w=90, h=8, txt='Dados Pessoais', align='C', ln=True)
    
    nome = 'Bruno'
    idade = 22
    
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)  # Configurar a cor do texto de volta para preto

    # Célula "Nome" à esquerda
    pdf.cell(w=30, h=30, txt=f'Nome: {nome}', align='L', ln=False)
    # Célula "Idade" à direita
    pdf.cell(w=0, h=30, txt=f'Idade: {idade}', align='C', ln=False)  # ln=False para evitar quebra de linha



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
    pdf.image(f'{dir_figures}/fig_evolucaoPeso.png', x=5, y=30, w=WIDTH/2-5)

    # Simulando uma segunda imagem 
    pdf.image(f'{dir_figures}/fig_evolucaoPeso.png', x=WIDTH/2-5, y=30, w=WIDTH/2-5)


    '''Fourth Page'''
    pdf.add_page()

    pdf.cell(h=40, w=10, txt=f'Avaliação Física de {name} em Perspectiva Gráfica: Insights e Conclusões', )
    pdf.image(f'{dir_figures}/fig_table.png', x=5, y=100, w=WIDTH-5)


    pdf.output(filename, 'F')


if __name__ == '__main__':
    create_report()

#Pegar o Nome da última posição do dataframe
# nome = data['Nome'].iloc[-1]
# %%
