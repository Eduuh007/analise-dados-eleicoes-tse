import os
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

def carregar_dados(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1', dtype=str)
    except UnicodeDecodeError:
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8', dtype=str)
    return df

def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

def filtrar_por_municipio(df):
    municipio = input("Digite o nome do município para filtrar (ex: São Paulo) ou ENTER para analisar todo Brasil: ").strip()
    if municipio:
        municipio_norm = remover_acentos(municipio).upper()
        mask = df['nm_municipio'].apply(lambda x: municipio_norm in remover_acentos(x).upper())
        df_filtrado = df[mask]
        if df_filtrado.empty:
            print(f"Nenhum dado encontrado para o município: {municipio}")
            return None
        return df_filtrado
    return df

def resumo_votacao(df):
    df['qt_votos'] = pd.to_numeric(df['qt_votos'].str.replace('.', '', regex=False).str.replace(',', '', regex=False), errors='coerce').fillna(0).astype(int)
    votos_por_candidato = df.groupby('nm_votavel')['qt_votos'].sum().sort_values(ascending=False)
    print("\nResumo dos 10 candidatos com mais votos:")
    print(votos_por_candidato.head(10))
    return votos_por_candidato

def plotar_grafico(votos_por_candidato, municipio=None):
    top_n = 10
    votos_top = votos_por_candidato.head(top_n)[::-1]  # pega top 10 e inverte para gráfico horizontal

    plt.figure(figsize=(10, 7))
    ax = votos_top.plot(kind='barh', color='skyblue')

    titulo = 'Top 10 Votação para Prefeito'
    if municipio:
        titulo += f' em {municipio}'
    titulo += ' - Eleições 2024'

    plt.title(titulo)
    plt.xlabel('Número de Votos')
    plt.ylabel('Candidato')

    plt.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()

    nome_arquivo = 'votacao_prefeito_top10.png' if not municipio else f'votacao_prefeito_top10_{municipio.replace(" ", "_").lower()}.png'
    plt.savefig(nome_arquivo)
    print(f"\nGráfico salvo como {nome_arquivo}")
    plt.show()

def main():
    print("=== Análise de votação das Eleições 2024 ===")
    pasta = os.getcwd()
    nome_arquivo = "votacao_secao-brasil_2024_prefeito.csv"
    caminho_arquivo = os.path.join(pasta, nome_arquivo)

    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return

    df = carregar_dados(caminho_arquivo)
    df_filtrado = filtrar_por_municipio(df)
    if df_filtrado is None or df_filtrado.empty:
        print("Nenhum dado para análise após filtro.")
        return

    votos_por_candidato = resumo_votacao(df_filtrado)
    if votos_por_candidato.empty:
        print("Nenhum voto registrado para análise.")
        return

    municipio = input("Digite o nome do município para título do gráfico (ou ENTER para nenhum): ").strip()
    if municipio == '':
        municipio = None

    plotar_grafico(votos_por_candidato, municipio)

if __name__ == "__main__":
    main()












