#%%

def classificar_composicao_corporal(musculo, valor: float):
    categorias = {
        'Peso': [(0, 60, "Abaixo do Peso"), (60, 80, "Peso Normal"), (80, 100, "Sobrepeso"), (100, float('inf'), "Obesidade")],
        'Altura': [(0, 1.60, "Baixa Estatura"), (1.60, 1.80, "Estatura Normal"), (1.80, float('inf'), "Alta Estatura")],
        'IMC': [(0, 18.5, "Abaixo do Peso"), (18.5, 24.9, "Peso Normal"), (25, 29.9, "Sobrepeso"), (30, float('inf'), "Obesidade")],
        '%_Gordura': [(0, 15, "Baixo % de Gordura"), (15, 25, "Médio % de Gordura"), (25, float('inf'), "Alto % de Gordura")],
        'Massa_Magra': [(0, 10, "Baixa Massa Magra"), (10, 20, "Média Massa Magra"), (20, float('inf'), "Alta Massa Magra")],
        'Massa_Gorda': [(0, 15, "Baixa Massa Gorda"), (15, 25, "Média Massa Gorda"), (25, float('inf'), "Alta Massa Gorda")],
        'DC_Peitoral': [],  # Preencha com categorias apropriadas
        'DC_Abdominal': [],
        'DC_Coxa': [],
        'Ombro': [],
        'Torax_Relaxado': [],
        'Térax_Inspirado': [],
        'Abdome': [],
        'Cintura': [],
        'Quadril': [],
        'RCQ': [],
        'Antebraco_Esq': [],
        'Antebrago_Dir': [],
        'Brago_Relax_': [],
        'Braco_Relax_Dir': [],
        'Brago_Contr_': [],
        'Brago_Contr_Dir': [],
        'Coxa_Esq': [],
        'Coxa_Dir': [],
        'Panturrilha_Esq': []
    }

    if musculo not in categorias:
        return f"Métrica {musculo} não encontrada."

    for categoria in categorias[musculo]:
        limite_inferior, limite_superior, classificacao = categoria
        if limite_inferior <= float(valor) < limite_superior:
            return classificacao

    return "Classificação não encontrada para a métrica especificada."

# Exemplo de uso
valores = 28.98
musculo_escolhido = 'IMC'

classificacao = classificar_composicao_corporal(musculo=musculo_escolhido, valor=valores)
print(f"Classificação para {musculo_escolhido}: {classificacao}")
type(valores)

# %%
