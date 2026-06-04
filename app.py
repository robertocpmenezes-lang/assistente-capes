import streamlit as st
import requests
import urllib.parse
import pandas as pd

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================
st.set_page_config(
    page_title="Assistente CAPES 2025-2028", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
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
    
    .input-note {
        font-size: 0.85rem;
        color: #4a5568;
        margin-top: 0.5rem;
        padding: 0.5rem 0.75rem;
        background: rgba(255,255,255,0.8);
        border-radius: 6px;
        border-left: 3px solid #667eea;
    }
    
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
st.markdown('<p class="sub-header">Ciclo de Avaliação CAPES 2025-2028 | Ciência Aberta e Dados Reais</p>', unsafe_allow_html=True)

# ==============================================================================
# SEÇÃO EDUCACIONAL
# ==============================================================================
st.markdown('<div class="section-title">▸ Entenda a Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique para entender os 3 Procedimentos e Estratégias", expanded=False):
    st.markdown("""
    ### 🔍 Como Funciona a Avaliação CAPES 2025-2028
    
    A CAPES avalia os programas de pós-graduação através de **3 procedimentos complementares**:
    
    #### **📊 Procedimento 1: Métricas do Periódico (Qualis)**
    - **O que avalia:** A qualidade da REVISTA onde você publica
    - **Como mede:** Fator de Impacto, Quartil (Q1-Q4), Citações
    - **Base de dados:** OpenAlex (substituiu o JCR/Scopus pagos)
    - **Referências:**
      - Exatas/Saúde: Excelente >3.0 | Bom >1.5 | Aceitável >0.5
      - Humanas: Excelente >1.5 | Bom >0.5 | Aceitável >0.2
    
    #### **📢 Procedimento 2: Impacto Social (Altimetria)**
    - **O que avalia:** O impacto do SEU ARTIGO na sociedade
    - **Como mede:** Downloads, menções em redes sociais, compartilhamentos, citações em políticas públicas
    - **Dica crucial:** Artigos em Acesso Aberto têm MUITO mais alcance!
    
    #### **✦ Procedimento 3: Ciência Aberta e Qualitativo**
    - **O que avalia:** Relevância e transparência da pesquisa
    - **Como mede:** Análise por pares, disponibilização de dados, preprints
    - **Dica de ouro:** Depositar dados no Zenodo/OSF conta MUITOS pontos!
    
    ---
    
    ### 🎯 Os 3 Tipos de Estratégia
    
    **⚖️ 1. Equilibrado:** Mais seguro e recomendado. Boa pontuação em todos os procedimentos.
    
    **📢 2. Impacto Social:** Prioriza Open Access e divulgação. Ideal para pesquisas com aplicação prática.
    
    **📈 3. Tradicional:** Foca em alto Fator de Impacto. Ideal para prestígio acadêmico máximo.
    """)

# ==============================================================================
# FORMULÁRIO
# ==============================================================================
st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box alert-info">
<strong>💡 Dica geral:</strong> Preencha os campos abaixo com informações da sua pesquisa. 
Quanto mais detalhado, mais precisas serão as recomendações de revistas!
</div>
""", unsafe_allow_html=True)

with st.form("dados_pesquisa", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema da Pesquisa",
            help="💡 O título ajuda a ferramenta a contextualizar a relevância temática da sua pesquisa."
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Por que isso importa?</strong> O título define o contexto temático. 
        Seja específico! Exemplo: "Machine Learning para Diagnóstico Precoce de Diabetes Tipo 2".
        </div>
        """, unsafe_allow_html=True)
        
        area_capes = st.selectbox(
            "📚 Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"]
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Como isso afeta?</strong> 
        • <strong>Exatas/Saúde:</strong> FI > 3.0 é excelente<br>
        • <strong>Humanas:</strong> FI > 1.5 já é excelente
        </div>
        """, unsafe_allow_html=True)

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (EM INGLÊS)",
            height=120,
            placeholder="Ex: machine learning diabetes prediction healthcare",
            help="💡 Use 3-8 palavras-chave em INGLÊS para buscar na base global OpenAlex."
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Como escolher?</strong> Use termos técnicos em inglês.<br>
        Ex: "machine learning healthcare prediction"
        </div>
        """, unsafe_allow_html=True)
        
        foco = st.selectbox(
            "🎯 Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"]
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Qual escolher?</strong><br>
        • <strong>⚖️ Equilibrado:</strong> Mais seguro<br>
        • <strong>📢 Impacto Social:</strong> Máximo alcance<br>
        • <strong>📈 Tradicional:</strong> Prestígio máximo
        </div>
        """, unsafe_allow_html=True)
    
    submitted = st.form_submit_button("🚀 Gerar Relatório Completo", use_container_width=True)

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
        with st.spinner("⟳ Buscando..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=6)
            
            if revistas:
                st.success("✓ Relatório gerado!")
                
                # Tabela Comparativa
                st.markdown('<div class="section-title">✦ Tabela Comparativa</div>', unsafe_allow_html=True)
                
                st.info("""
                **Como ler:** Tabela ordenada por relevância | 🟢 OA+Alto = melhor | 🔵 OA = boa altimetria | 🔴 Fechado
                """)
                
                # Preparar dados
                dados = []
                melhores_oa = []
                
                for i, rev in enumerate(revistas, 1):
                    nome = rev.get("display_name", "N/A")
                    is_oa = rev.get("is_oa", False)
                    stats = rev.get("summary_stats", {})
                    fi = stats.get("2yr_mean_citedness", 0) or 0
                    citacoes = rev.get("cited_by_count", 0) or 0
                    
                    if is_oa:
                        melhores_oa.append(nome)
                    
                    # Ícones
                    if is_oa and citacoes > 5000:
                        acesso_icon = "🟢"
                        altimetria_icon = "🟢"
                    elif is_oa:
                        acesso_icon = "🔵"
                        altimetria_icon = "🔵"
                    else:
                        acesso_icon = "🔴"
                        altimetria_icon = "⚪"
                    
                    if fi > 10:
                        fi_class = "🔥"
                    elif fi > 5:
                        fi_class = "⭐"
                    elif fi > 2:
                        fi_class = "✅"
                    else:
                        fi_class = "📌"
                    
                    destaque = "🏆" if i <= 3 else ""
                    
                    dados.append({
                        "📊 Ranking": f"{destaque}#{i}",
                        "Revista": nome,
                        "🚪 Acesso": f"{acesso_icon}",
                        "📈 FI": round(fi, 2),
                        "Class": fi_class,
                        "💬 Citações": formatar_numero(citacoes),
                        "📢 Altimetria": altimetria_icon
                    })
                
                # DataFrame
                df = pd.DataFrame(dados)
                
                # Configurar colunas
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Legenda
                st.markdown("""
                <div style="font-size: 0.85rem; color: #4a5568; padding: 0.75rem; background: white; border-radius: 8px; margin-top: 0.5rem;">
                <strong>Legenda:</strong> 🟢=OA+Alto | 🔵=OA | 🔴=Fechado | 🔥=Excelente | ⭐=Muito Bom | ✅=Bom | 📌=Aceitável | 🏆=Top 3<br>
                <strong>Altimetria:</strong> 🟢=Alto | 🔵=Médio | ⚪=Baixo
                </div>
                """, unsafe_allow_html=True)
                
                # Resumo Visual
                st.markdown('<div class="section-title">▸ Resumo Visual</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if melhores_oa:
                        st.success(f"**🟢 Open Access: {len(melhores_oa)}**\n\n{chr(10).join([f'- {r}' for r in melhores_oa])}")
                    else:
                        st.warning(f"**🔴 Nenhuma Open Access**\n\nDeposite preprint!")
                
                with col2:
                    max_fi = max([rev.get("summary_stats", {}).get("2yr_mean_citedness", 0) or 0 for rev in revistas])
                    st.success(f"**🔥 Maior FI: {max_fi:.2f}**")
                
                with col3:
                    st.info(f"**📊 Total: {len(revistas)}**\n\nÁrea: {area_capes}")
                
                # Análise
                st.markdown('<div class="section-title">▸ Análise</div>', unsafe_allow_html=True)
                
                if "Equilibrado" in foco:
                    if melhores_oa:
                        st.success(f"**✓ Equilibrado**\n\nPriorize: {', '.join(melhores_oa[:2])}")
                    else:
                        st.warning("⚠️ Sem Open Access. Deposite preprint!")
                    
                elif "Impacto" in foco:
                    if melhores_oa:
                        st.success(f"**📢 Impacto Social**\n\nPriorize: {', '.join(melhores_oa)}\n\n**Ação:** Compartilhe!")
                    else:
                        st.error("⚠️ Deposite preprint no SciELO/arXiv!")
                    
                else:
                    st.success("**📈 Tradicional**\n\nPriorize maior FI na tabela.")
                
                # Procedimentos
                st.markdown('<div class="section-title">▸ Procedimentos</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **📊 Proc. 1 - Métricas**
                    
                    **Exatas/Saúde:**
                    - Excelente: > 3.0
                    - Bom: 1.5-3.0
                    
                    **Humanas:**
                    - Excelente: > 1.5
                    - Bom: 0.5-1.5
                    """)
                
                with col2:
                    if melhores_oa:
                        st.success("""
                        **📢 Proc. 2 - Altimetria
                        
                        ✓ Tem Open Access!
                        
                        **Ação:** Divulgue!
                        """)
                    else:
                        st.warning("""
                        **📢 Proc. 2 - Altimetria
                        
                        ⚠ Fechadas
                        
                        **Solução:** Preprint!
                        """)
                
                with col3:
                    st.info("""
                    **✦ Proc. 3 - Ciência Aberta
                    
                    **Ações:**
                    - Dados no Zenodo
                    - Citar DOI
                    - Preprints
                    
                    💡 +30% citações!
                    """)
                
                # Checklist
                st.markdown('<div class="section-title">▸ Checklist</div>', unsafe_allow_html=True)
                st.success("""
                **📋 Antes:** [ ] ORCID | [ ] Dados  
                **📤 Durante:** [ ] Preprint | [ ] DOI  
                **📢 Após:** [ ] Divulgar | [ ] Monitorar
                """)
                
            else:
                st.warning("⚠️ Nenhuma revista. Tente termos em inglês.")

# Footer
st.markdown("""
<div class="footer">
    <p><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p>OpenAlex + CAPES 2025-2028 | Sem vínculo oficial</p>
</div>
""", unsafe_allow_html=True)
