import streamlit as st
import requests
import urllib.parse

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================
st.set_page_config(
    page_title="Assistente CAPES 2025-2028", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Simplificado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
    }
    
    .sub-header {
        color: #4a5568;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .section-title {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-info { background: #ebf8ff; border-left: 4px solid #4299e1; }
    .alert-success { background: #f0fff4; border-left: 4px solid #48bb78; }
    .alert-warning { background: #fffaf0; border-left: 4px solid #ed8936; }
    
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: #e2e8f0;
        border-radius: 12px;
        text-align: center;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">✦ Assistente de Estratégia de Publicação</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ciclo de Avaliação CAPES 2025-2028</p>', unsafe_allow_html=True)

# ==============================================================================
# SEÇÃO EDUCACIONAL
# ==============================================================================
st.markdown('<div class="section-title">▸ Entenda a Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique para entender os 3 Procedimentos e Estratégias", expanded=False):
    st.markdown("""
    ### 🔍 Como Funciona a Avaliação CAPES 2025-2028
    
    **📊 Procedimento 1:** Métricas do Periódico (Fator de Impacto, Quartil)  
    ** Procedimento 2:** Impacto Social (Altimetria, downloads, menções)  
    **✦ Procedimento 3:** Ciência Aberta e Avaliação Qualitativa
    
    ### 🎯 Estratégias:
    - **⚖️ Equilibrado:** Mais seguro - bom em todos os procedimentos
    - **📢 Impacto Social:** Prioriza Open Access e divulgação
    - **📈 Tradicional:** Foca em alto Fator de Impacto
    """)

# ==============================================================================
# FORMULÁRIO
# ==============================================================================
st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box alert-info">
<strong> Dica:</strong> Preencha os campos abaixo. Quanto mais detalhado, mais precisas serão as recomendações!
</div>
""", unsafe_allow_html=True)

with st.form("dados_pesquisa", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema",
            help="💡 O título ajuda a contextualizar a relevância para o Procedimento 3 (Qualitativo)."
        )
        
        area_capes = st.selectbox(
            "📚 Grande Área CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"],
            help="💡 Cada área pondera diferentemente os 3 procedimentos."
        )

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (PREFERENCIALMENTE EM INGLÊS)",
            height=130,
            placeholder="Ex: machine learning healthcare prediction",
            help="💡 Use 3-8 palavras-chave em INGLÊS para buscar na base global OpenAlex."
        )
        
        foco = st.selectbox(
            " Estratégia de Publicação",
            ["️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             " Máximo Tradicional (Fator de Impacto)"],
            help="💡 Equilibrado é o mais seguro. Impacto Social prioriza Open Access. Tradicional foca em FI alto."
        )
    
    submitted = st.form_submit_button(" Gerar Relatório com Grade Comparativa", use_container_width=True)

# ==============================================================================
# FUNÇÕES
# ==============================================================================
def formatar_numero(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.0f}K"
    return str(num)

@st.cache_data(ttl=3600)
def buscar_revistas(query, max_results=6):
    safe_query = urllib.parse.quote(query)
    url = f"https://api.openalex.org/works?search={safe_query}&per-page=20"
    
    try:
        resp = requests.get(url, timeout=15)
        works = resp.json().get("results", [])
        
        revistas = []
        seen = set()
        
        for work in works:
            source = work.get("primary_location", {}).get("source")
            if source and source.get("id") not in seen:
                seen.add(source.get("id"))
                source_id = source.get("id").replace("https://openalex.org/", "")
                try:
                    r = requests.get(f"https://api.openalex.org/sources/{source_id}", timeout=10)
                    if r.status_code == 200:
                        revistas.append(r.json())
                        if len(revistas) >= max_results:
                            break
                except:
                    pass
        return revistas
    except:
        return []

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
if submitted:
    if not resumo.strip():
        st.warning("⚠️ Insira palavras-chave em inglês.")
    else:
        with st.spinner("⟳ Buscando revistas..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=6)
            
            if revistas:
                st.success("✓ Relatório gerado!")
                
                # Grade Comparativa
                st.markdown('<div class="section-title">✦ Grade Comparativa de Revistas</div>', unsafe_allow_html=True)
                
                st.info("""
                ** Como usar:** Compare lado a lado - Fator de Impacto, Citações e Potencial de Altimetria.
                -  Open Access + Alto Impacto (melhor)
                - 🔵 Open Access (boa para altimetria)
                - 🔴 Fechado (alto FI tradicional)
                """)
                
                # Criar grid com columns nativo
                melhores_oa = []
                cols = st.columns(2)  # 2 colunas
                
                for i, rev in enumerate(revistas):
                    nome = rev.get("display_name", "N/A")
                    is_oa = rev.get("is_oa", False)
                    stats = rev.get("summary_stats", {})
                    fi = stats.get("2yr_mean_citedness", 0) or 0
                    citacoes = rev.get("cited_by_count", 0) or 0
                    
                    if is_oa:
                        melhores_oa.append(nome)
                    
                    # Determinar emoji e cor
                    if is_oa and citacoes > 5000:
                        card_emoji = "🟢"
                        alt_text = "🔥 Alto"
                    elif is_oa:
                        card_emoji = "🔵"
                        alt_text = "● Médio"
                    else:
                        card_emoji = "🔴"
                        alt_text = "○ Baixo"
                    
                    acesso_text = "✓ Open Access" if is_oa else "✕ Fechado"
                    
                    # Destaque top 3
                    destaque = " " if i < 3 else ""
                    
                    # Selecionar coluna
                    col_idx = i % 2
                    
                    with cols[col_idx]:
                        st.markdown(f"### {destaque}{card_emoji} {nome}")
                        
                        # Badges
                        badge_col1, badge_col2 = st.columns(2)
                        with badge_col1:
                            if is_oa:
                                st.success(f"**{acesso_text}**", icon="✅")
                            else:
                                st.error(f"**{acesso_text}**", icon="❌")
                        
                        with badge_col2:
                            st.info(f"**Altimetria: {alt_text}**", icon="📊")
                        
                        # Métricas
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.metric("Fator de Impacto", f"{fi:.2f}")
                        with metric_col2:
                            st.metric("Citações", formatar_numero(citacoes))
                        with metric_col3:
                            st.metric("Ranking", f"#{i+1}")
                        
                        st.markdown("---")
                
                # Análise Estratégica
                st.markdown('<div class="section-title"> Análise Estratégica</div>', unsafe_allow_html=True)
                st.info(f"**Área:** {area_capes} | **Estratégia:** {foco}")
                
                if "Equilibrado" in foco:
                    st.success("""
                    **✓ Estratégia Equilibrada Recomendada**
                    
                    Priorize os cards 🟢 (Open Access + Alto Impacto). Eles oferecem o melhor equilíbrio entre FI (Proc. 1) e Altimetria (Proc. 2).
                    """)
                elif "Impacto Social" in foco:
                    if melhores_oa:
                        st.success(f"""
                        **📢 Foco em Impacto Social**
                        
                        **Revistas Open Access (priorize):**
                        {chr(10).join([f"- {r}" for r in melhores_oa])}
                        
                        **Ação:** Compartilhe ativamente nas redes após publicar!
                        """)
                    else:
                        st.warning("⚠️ Nenhuma Open Access. Deposite preprint em SciELO/arXiv!")
                else:
                    st.success("""
                    **📈 Foco Tradicional**
                    
                    Priorize FI > 3.0 (Exatas/Saúde) ou > 1.0 (Humanas).
                    
                    **Importante:** Deposite preprint se for fechada para compensar no Proc. 2!
                    """)
                
                # Procedimentos
                st.markdown('<div class="section-title">▸ Guia dos Procedimentos</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **📊 Proc. 1 - Métricas**
                    
                    CAPES usa OpenAlex.
                    
                    **Exatas/Saúde:**
                    - Excelente: FI > 3.0
                    - Bom: 1.5-3.0
                    - Aceitável: 0.5-1.5
                    
                    **Humanas:**
                    - Excelente: FI > 1.5
                    - Bom: 0.5-1.5
                    - Aceitável: 0.2-0.5
                    """)
                
                with col2:
                    if melhores_oa:
                        st.success("""
                        **📢 Proc. 2 - Altimetria
                        
                        ✓ Tem Open Access!
                        
                        **Benefícios:**
                        - Mais downloads
                        - Mais compartilhamentos
                        - Mais menções
                        
                        **Ação:** Divulgue!
                        """)
                    else:
                        st.warning("""
                        **📢 Proc. 2 - Altimetria
                        
                        ⚠ Fechadas
                        
                        **Solução:**
                        1. Deposite preprint
                        2. Compartilhe link
                        3. Use redes sociais
                        """)
                
                with col3:
                    st.info("""
                    **✦ Proc. 3 - Ciência Aberta
                    
                    CAPES premia transparência!
                    
                    **Ações:**
                    - Dados no Zenodo/OSF
                    - Citar DOI dos dados
                    - Preprints
                    - Código aberto
                    
                    💡 Dados abertos = 30% mais citações!
                    """)
                
                # Checklist
                st.markdown('<div class="section-title">▸ Checklist</div>', unsafe_allow_html=True)
                st.success("""
                ** Antes:** [ ] ORCID vinculado | [ ] Dados organizados  
                ** Durante:** [ ] Preprint | [ ] DOI no artigo  
                **📢 Após:** [ ] Divulgar | [ ] Monitorar altimetria
                """)
                
            else:
                st.warning("⚠️ Nenhuma revista encontrada. Tente termos em inglês mais genéricos.")

# Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0;"><strong> Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0;">
        OpenAlex + CAPES 2025-2028 | Sem vínculo oficial CAPES/MEC
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Promovendo Ciência Aberta</em>
    </p>
</div>
""", unsafe_allow_html=True)
