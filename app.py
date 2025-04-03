import pandas as pd
import streamlit as st

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

# Caminho do seu CSV
CSV_PATH = '/Users/jp230/Documents/mudanca_sp_relacao/itens_pro1.csv'

# Carrega os dados no session_state, se ainda não existirem
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = pd.read_csv(CSV_PATH)

if 'checked_itens' not in st.session_state:
    st.session_state.checked_itens = set()

# 👉 Abas principais
aba1, aba2 = st.tabs(["✅ Checklist de Itens", "📝 Editar Itens"])

with aba1:
    st.title("📦 Checklist da Mudança")
    st.markdown("Marque os itens que **já foram armazenados com sucesso**.")

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
    st.title("📝 Editar Itens da Mudança")
    st.markdown("Edite abaixo os campos. As mudanças são salvas automaticamente.")

    edited_df = st.data_editor(
        st.session_state.df_raw,
        use_container_width=True,
        num_rows="dynamic",
        key="editor_df"
    )

    # Salva somente se houve alterações
    if not edited_df.equals(st.session_state.df_raw):
        st.session_state.df_raw = edited_df
        st.session_state.df_raw.to_csv(CSV_PATH, index=False)
        st.success("💾 Alterações salvas com sucesso!")