"""Interface local do laboratório educativo. Execute: streamlit run app.py."""
from pathlib import Path

import numpy as np
import streamlit as st
import torch

from modelos import Gerador

RAIZ = Path(__file__).resolve().parent
st.set_page_config(page_title="Como uma IA aprende a criar?", page_icon="👕", layout="wide")
st.title("Como uma IA aprende a criar?")
st.write("Explore como uma GAN gera imagens de roupas: leia, observe, compare e experimente.")
st.caption("Projeto educativo · UTFPR · Fashion-MNIST")


@st.cache_resource
def carregar_modelo(caminho, modificacao):
    torch.set_num_threads(2)
    modelo = Gerador()
    modelo.load_state_dict(torch.load(caminho, map_location="cpu", weights_only=True))
    return modelo.eval()


base, evolucao, experiencia, explicacao = st.tabs([
    "1. Conheça os dados", "2. Observe a evolução", "3. Gere imagens", "4. Entenda o processo"
])
with base:
    st.header("Exemplos que ajudam a IA a aprender")
    st.write("O Fashion-MNIST reúne imagens de dez categorias de roupas, calçados e acessórios. Cada imagem tem apenas 28 × 28 pixels, em tons de cinza.")
    painel = RAIZ / "artefatos/amostras_classes_reais.png"
    if painel.exists():
        st.image(str(painel), caption="Exemplos reais da base: estas imagens não foram geradas pela GAN.")
    else:
        st.info("Painel de exemplos indisponível. Execute preparacao_dados.py.")
    st.write("Na preparação local, 50 mil imagens são usadas no treinamento. Outras 10 mil ficam reservadas para validação, e as 10 mil do teste oficial permanecem separadas.")
with evolucao:
    st.header("Do início às primeiras formas")
    origem = st.radio("Execução", ["Original de Allan", "Local"], horizontal=True)
    if origem == "Original de Allan":
        st.caption("Épocas 0, 5 e 15 da execução original. Não misturamos essas imagens com o treino local, que usa outra divisão dos dados e outro procedimento de visualização.")
        arquivos = [(n, RAIZ / f"artefatos/sprint2_epoca_{n}.png") for n in (0, 5, 15)]
        st.write("No início aparecem texturas sem forma; depois surgem contornos de roupas e calçados. Mesmo ao final, há detalhes borrados e imagens ambíguas. Isso não representa uma porcentagem de acerto.")
    else:
        caminhos = sorted((RAIZ / "artefatos/sprint2_local").glob("epoca_*.png"))
        escolhidos = caminhos if len(caminhos) < 3 else [caminhos[0], caminhos[len(caminhos)//2], caminhos[-1]]
        arquivos = [(int(p.stem.split('_')[-1]), p) for p in escolhidos]
        st.caption("Mesma execução local, ruído fixo e escala de cinza fixa. Só são exibidas épocas com imagens disponíveis.")
        if len(arquivos) < 3:
            st.info("Ainda não há três momentos salvos desta execução local.")
    for coluna, (epoca, caminho) in zip(st.columns(max(len(arquivos), 1)), arquivos):
        with coluna:
            if caminho.exists():
                st.image(str(caminho), caption=f"Época {epoca}")
            else:
                st.warning(f"Imagem da época {epoca} indisponível.")
with experiencia:
    st.header("Experimente o gerador")
    st.write("Uma semente define os números aleatórios usados como entrada. Repita a semente para repetir as imagens; mude-a para explorar outras saídas.")
    st.caption("O modelo local disponível pode produzir formas borradas. Ele não permite escolher a categoria da roupa.")
    semente = st.number_input("Semente", min_value=0, max_value=2147483647, value=123, step=1)
    caminho = RAIZ / "checkpoints/sprint2_local/gerador.pt"
    if not caminho.exists():
        st.warning("Modelo local ausente. Transfira gerador.pt para checkpoints/sprint2_local/ ou execute o treinamento conforme o README.")
    elif st.button("Gerar 16 imagens", type="primary"):
        try:
            modelo = carregar_modelo(str(caminho), caminho.stat().st_mtime_ns)
            rng = torch.Generator().manual_seed(int(semente))
            with torch.inference_mode():
                imagens = ((modelo(torch.randn(16, 100, 1, 1, generator=rng)) + 1) / 2).clamp(0, 1)
            st.session_state["imagens"] = imagens[:, 0].numpy()
            st.session_state["semente_gerada"] = int(semente)
        except (OSError, RuntimeError, ValueError, EOFError) as erro:
            st.error(f"Não foi possível carregar o modelo: {erro}")
    if "imagens" in st.session_state:
        st.caption(f"Imagens geradas por IA · semente {st.session_state['semente_gerada']}")
        for linha in np.array_split(st.session_state["imagens"], 4):
            for coluna, imagem in zip(st.columns(4), linha):
                coluna.image(imagem, clamp=True, width=140)
with explicacao:
    st.header("Duas redes aprendendo juntas")
    st.markdown("**Gerador:** transforma números aleatórios em uma imagem.\n\n**Discriminador:** aprende a distinguir as imagens da base das produzidas pelo gerador.\n\n**Treinamento:** as duas redes são ajustadas alternadamente. O erro calculado ajuda o gerador a mudar suas próximas saídas. Uma época é uma passagem por todas as imagens de treino.")
    st.graphviz_chart('digraph { rankdir=LR; Dados -> Discriminador; Ruido [label="Ruído"]; Ruido -> Gerador; Gerador -> Discriminador [label="imagem gerada"]; Discriminador -> Gerador [label="sinal de erro no treino"]; Gerador -> Imagem [label="após salvar e carregar"]; }')
    st.markdown("**Limitações:** resolução pequena, imagens às vezes repetitivas ou pouco reconhecíveis e ausência de escolha de categoria. As perdas do treinamento não são acurácia. Uma imagem convincente não comprova compreensão humana nem garante que o modelo não tenha memorizado padrões.")
    st.info("Para refletir durante a leitura: o que mudou entre as épocas? Quais imagens são difíceis de reconhecer? Onde uma imagem gerada pode causar confusão?")
