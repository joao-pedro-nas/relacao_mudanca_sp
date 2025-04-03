import pandas as pd
import streamlit as st

# Dicionário de nomes bonitos
nomes_bonitos = {
    "BANQUETA": "Banqueta",
    "CAIXA CABIDEIRO": "Caixa para cabideiro",
    "CAIXA PARA LIVROS": "Caixa para livros",
    "PERSIANAS": "Persianas",
    "PIANO ARMARIO": "Piano-armário",
    "VENTILADOR": "Ventilador",
    "VARAL": "Varal",
    "ESTANTE": "Estante",
    "RACK TV": "Rack de TV",
    "SOFA": "Sofá",
    "CADEIRA ESTOFADA": "Cadeira estofada",
    "MESA JANTAR": "Mesa de jantar",
    "SAPATEIRA": "Sapateira",
    "ARMÁRIO COZINHA": "Armário de cozinha",
    "FOGAO": "Fogão",
    "GELADEIRA": "Geladeira",
    "CAMA CASAL": "Cama de casal",
    "COLCHÃO CASAL": "Colchão de casal",
    "CAIXA PARA FERRAMENTAS": "Caixa para ferramentas",
    "COLCHAO CASAL": "Colchão de casal",
    "ESTANTE DE ACO": "Estante de aço",
    "CESTO": "Cesto",
    "MICROONDAS": "Micro-ondas",
    "ESCADA PEQUENA": "Escada pequena",
    "TABUA DE PASSAR": "Tábua de passar"
}

CSV_PATH = 'itens_pro1.csv'

# Inicializa session_state
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = pd.read_csv(CSV_PATH)

if 'checked_itens' not in st.session_state:
    st.session_state.checked_itens = set()

# Abas principais
aba1, aba2, aba3 = st.tabs(["✅ Checklist", "🛠 Adicionar/Editar/Remover", "📊 Visualização Final"])

with aba1:
    st.title("📦 Checklist da Mudança")

    for i, row in st.session_state.df_raw.iterrows():
        nome_caps = row['objeto']
        if pd.isna(nome_caps) or not isinstance(nome_caps, str):
            nome_bonito = "⚠️ Nome inválido"
        else:
            nome_bonito = nomes_bonitos.get(nome_caps, nome_caps.title())

        key = f"check_{i}_{nome_caps}"

        checked = st.checkbox(
            f"{row['quantidade']}x {nome_bonito}",
            key=key,
            value=nome_caps in st.session_state.checked_itens
        )

        if checked:
            st.session_state.checked_itens.add(nome_caps)
        else:
            st.session_state.checked_itens.discard(nome_caps)

    st.markdown("---")
    st.success(f"{len(st.session_state.checked_itens)} de {len(st.session_state.df_raw)} itens marcados como armazenados.")

    if st.button("🔄 Limpar todos os checks"):
        st.session_state.checked_itens.clear()
        st.rerun()

with aba2:
    st.title("🛠 Adicionar, Editar ou Remover Itens")

    opcoes = ["Adicionar", "Editar", "Remover"]
    operacao = st.selectbox("O que você deseja fazer?", opcoes)

    todos_itens = list(st.session_state.df_raw['objeto'].dropna().unique())

    if operacao == "Adicionar":
        novo_nome = st.text_input("Digite o nome do novo item (em letras maiúsculas):", "")
        nova_qtd = st.number_input("Quantidade", min_value=1, value=1, step=1)
        nova_desc = st.text_input("Descrição (opcional):", "")
        valor_str = st.text_input("Valor (opcional) (somente números inteiros):")
        novo_valor = int(valor_str) if valor_str.strip().isdigit() else None

        if st.button("Salvar Novo Item"):
            novo_registro = pd.DataFrame([{
                'objeto': novo_nome,
                'quantidade': nova_qtd,
                'descricao': nova_desc,
                'valor': novo_valor
            }])
            st.session_state.df_raw = pd.concat([st.session_state.df_raw, novo_registro], ignore_index=True)
            st.session_state.df_raw.to_csv(CSV_PATH, index=False)
            st.success("Item adicionado com sucesso!")

    elif operacao == "Editar":
        item_selecionado = st.selectbox("Selecione o item que deseja editar", todos_itens)

        # Pega os valores atuais para preencher os campos automaticamente
        item_data = st.session_state.df_raw[st.session_state.df_raw['objeto'] == item_selecionado]
        quantidade_atual = int(item_data['quantidade'].values[0]) if not item_data.empty else 1
        descricao_atual = item_data['descricao'].values[0] if not item_data.empty else ""
        valor_atual = item_data['valor'].values[0] if not item_data.empty else None
        valor_str = str(int(valor_atual)) if pd.notna(valor_atual) else ""

        nova_qtd = st.number_input("Nova quantidade", min_value=1, value=quantidade_atual, step=1)
        
        nova_desc_input = st.text_input("Nova descrição (opcional):", descricao_atual or "")
        nova_desc = nova_desc_input.strip() or None
        
        novo_valor_str = st.text_input("Novo valor (opcional) (somente números inteiros):", valor_str)
        novo_valor = int(novo_valor_str) if novo_valor_str.strip().isdigit() else None

        if st.button("Salvar Alteração"):
            idx = st.session_state.df_raw[st.session_state.df_raw['objeto'] == item_selecionado].index
            if len(idx) > 0:
                st.session_state.df_raw.loc[idx, ['quantidade', 'descricao', 'valor']] = [nova_qtd, nova_desc, novo_valor]
                st.session_state.df_raw.to_csv(CSV_PATH, index=False)
                st.success("Item atualizado com sucesso!")

    elif operacao == "Remover":
        item_selecionado = st.selectbox("Selecione o item que deseja remover", todos_itens)

        if st.button("Remover Item"):
            st.session_state.df_raw = st.session_state.df_raw[st.session_state.df_raw['objeto'] != item_selecionado]
            st.session_state.df_raw.to_csv(CSV_PATH, index=False)
            st.success("Item removido com sucesso!")

with aba3:
    st.title("📊 Visualização Final")
    st.dataframe(st.session_state.df_raw, use_container_width=True)
