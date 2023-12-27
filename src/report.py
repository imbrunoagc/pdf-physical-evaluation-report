#%%
from fpdf import FPDF
import pandas as pd

from pathlib import Path
from datetime import datetime

from report_data import var_peso, var_altura, var_abdominal, var_coxa, text_IMC, var_peitoral, var_porcentagem_gordura, porcentage_gordura_ideal, var_massaMagra, var_massaGorda
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

    # Adicionar imagem como fundo
    image_path_background = Path() / '..' / 'documentos' / 'modelo_branco.png'
    pdf.image(str(image_path_background), x=2.5, y=0, w=WIDTH-5, h=HEIGHT-5)

    pdf.set_font('Arial', 'B', 12)

    pdf.ln(3)

    pdf.cell(w=50, h=5, txt=f'{var_peso}', align="C", ln=1)
    pdf.ln(3)
    pdf.cell(w=50, h=5, txt=f'{var_altura}', align="C")


    pdf.set_xy(78, 17.5)
    pdf.cell(w=50, h=5, txt=f'{text_IMC}', align='C', ln=1)    


    pdf.set_xy(10, 77.5)
    pdf.cell(w=50, h=5, txt=f'{var_peitoral}', align='C', ln=1)    
    pdf.ln(2)
    
    pdf.cell(w=50, h=5, txt=f'{var_abdominal}', align='C', ln=1)
    
    pdf.ln(3)
    pdf.cell(w=50, h=5, txt=f'{var_coxa}', align='C', ln=1)
    

    pdf.set_xy(16.5, 118.3)
    pdf.cell(w=50, h=5, txt=f'{porcentage_gordura_ideal}', align='C', ln=1)    
    
    pdf.ln(3)
    pdf.cell(w=65, h=5, txt=f'{var_porcentagem_gordura}', align='C', ln=1)    
    
    pdf.ln(3)
    pdf.cell(w=65, h=5, txt=f'{var_massaMagra}', align='C', ln=1)    
    
    pdf.ln(3)
    pdf.cell(w=65, h=5, txt=f'{var_massaGorda}', align='C', ln=1)    

    pdf.ln(15)
    pdf.image(f'{dir_figures}/fig_circleMassa_Magra_Gorda.png', x=8, y=150, w=WIDTH/4-3)


def create_report(date=DATE, filename='../report.pdf'):


    pdf = FPDF() # Objeto PDF, as propriedades podem ser ajustadas em PDF()

    '''First Page'''
    create_first_page(pdf=pdf)

    '''Second Page'''
    create_second_page(pdf=pdf, data=df)

    name = "Bruno"
    '''Third Page'''
    '''pdf.add_page()
    
    
    pdf.cell(40, 10, f'Avaliação Física de {name} em Perspectiva Gráfica: Insights e Conclusões')
    
    # Realizando ajuste de tamanho da imagem/localização
    pdf.image(f'{dir_figures}/fig_evolucaoPeso.png', x=5, y=22.5, w=WIDTH/2-5)

    # Simulando uma segunda imagem 
    pdf.image(f'{dir_figures}/fig_evolucaoPeso.png', x=WIDTH/2-5, y=22.5, w=WIDTH/2-5)
    '''

    '''Fourth Page'''
    pdf.add_page()

    pdf.cell(h=30, w=10, txt=f'Avaliação Física de {name} em Perspectiva Gráfica: Insights e Conclusões', )
    pdf.image(f'{dir_figures}/fig_table.png', x=5, y=30, w=WIDTH-5)
    

    pdf.output(filename, 'F')


if __name__ == '__main__':
    create_report()

# %%
