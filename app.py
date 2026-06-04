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
    layout="wide"
)

# CSS Simplificado
st.markdown("""
<style>
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
        padding: 0.5rem;
        background: rgba(255,255,255,0.8);
        border-radius: 6px;
        border-left: 3px solid #667eea;
    }
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: white;
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
st.markdown('<p class="sub-header">Ciclo CAPES 2025-2028</p>', unsafe_allow_html=True)

# ==============================================================================
# SEÇÃO EDUCACIONAL
# ==============================================================================
st.markdown('<div class="section-title">▸ Entenda a Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique para entender os 3 Procedimentos", expanded=False):
    st.markdown("""
    **📊 Proc. 1:** Métricas do Periódico (Fator de Impacto)  
    **📢 Proc. 2:** Impacto Social (Altimetria)  
    **✦ Proc. 3:** Ciência Aberta e Qualitativo
    
    ### Estratégias:
    - **⚖️ Equilibrado:** Mais seguro
    - **📢 Impacto Social:** Prioriza Open Access
    - **📈 Tradicional:** Foca em alto FI
    """)

# ==============================================================================
# FORMULÁRIO
# ==============================================================================
st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)

with st.form("dados_pesquisa", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema",
            help="💡 O título ajuda a contextualizar a relevância para o Procedimento 3 (Qualitativo)."
        )
        st.markdown('<div class="input-note"><strong>📌 Exemplo:</strong> "Machine Learning para Diagnóstico de Diabetes" é melhor que apenas "Machine Learning"</div>', unsafe_allow_html=True)
        
        area_capes = st.selectbox(
            "📚 Grande Área CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"],
            help="💡 Cada área pondera diferentemente os 3 procedimentos."
        )
        st.markdown('<div class="input-note"><strong>📌 Importante:</strong> Exatas/Saúde valorizam FI > 3.0. Humanas valorizam FI > 1.5</div>', unsafe_allow_html=True)

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (EM INGLÊS)",
            height=120,
            placeholder="Ex: machine learning healthcare prediction",
            help="💡 Use 3-8 palavras-chave em INGLÊS para buscar na base global OpenAlex."
        )
        st.markdown('<div class="input-note"><strong>📌 Como escolher:</strong> Combine método + aplicação. Ex: "machine learning diabetes prediction"</div>', unsafe_allow_html=True)
        
        foco = st.selectbox(
            "🎯 Estratégia",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"],
            help="💡 Equilibrado é o mais seguro. Impacto Social prioriza Open Access."
        )
        st.markdown('<div class="input-note"><strong>📌 Dica:</strong> Equilibrado = mais seguro | Impacto Social = máximo alcance | Tradicional = prestígio</div>', unsafe_allow_html=True)
    
    submitted = st.form_submit_button("🚀 Gerar Relatório", use_container_width=True)

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
                    
                    # Determinar ícones e cores
                    if is_oa and citacoes > 5000:
                        acesso_emoji = "🟢"
                        acesso_text = "Open Access"
                        altimetria = "🔥 Alto"
                    elif is_oa:
                        acesso_emoji = "🔵"
                        acesso_text = "Open Access"
                        altimetria = "● Médio"
                    else:
                        acesso_emoji = "🔴"
                        acesso_text = "Fechado"
                        altimetria = "○ Baixo"
                    
                    if fi > 10:
                        fi_class = "🔥 Excelente"
                    elif fi > 5:
                        fi_class = "⭐ Muito Bom"
                    elif fi > 2:
                        fi_class = "✅ Bom"
                    else:
                        fi_class = "📌 Aceitável"
                    
                    dados.append({
                        "📊 Ranking": f"#{i}",
                        "Revista": nome,
                        "🚪 Acesso": f"{acesso_emoji} {acesso_text}",
                        "📈 FI": round(fi, 2),
                        "Classificação": fi_class,
                        "💬 Citações": formatar_numero(citacoes),
                        "📢 Altimetria": altimetria
                    })
                
                # Tabela Comparativa
                st.markdown('<div class="section-title">✦ Tabela Comparativa</div>', unsafe_allow_html=True)
                
                st.info("""
                **Como ler:**
                - 🟢 Open Access + Alto Impacto = Melhor opção
                - 🔵 Open Access = Boa para altimetria
                - 🔴 Fechado = Paywall (deposite preprint)
                - Tabela ordenada por relevância
                """)
                
                # DataFrame com formatação
                df = pd.DataFrame(dados)
                
                # Função para colorir altimetria
                def colorir_altimetria(val):
                    if "🔥" in val:
                        return 'background-color: #c6f6d5; color: #22543d'
                    elif "●" in val:
                        return 'background-color: #bee3f8; color: #2a4365'
                    else:
                        return 'background-color: #e2e8f0; color: #718096'
                
                # Aplicar formatação
                df_styled = df.style.applymap(colorir_altimetria, subset=['📢 Altimetria'])
                
                st.dataframe(
                    df_styled,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Resumo Visual
                st.markdown('<div class="section-title">▸ Resumo Visual</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if melhores_oa:
                        st.success(f"""
                        **🟢 Open Access: {len(melhores_oa)}**
                        
                        {chr(10).join([f"- {r}" for r in melhores_oa])}
                        
                        Melhor para Proc. 2
                        """)
                    else:
                        st.warning(f"""
                        **🔴 Nenhuma Open Access**
                        
                        Todas fechadas.
                        
                        Deposite preprint!
                        """)
                
                with col2:
                    max_fi = max([rev.get("summary_stats", {}).get("2yr_mean_citedness", 0) or 0 for rev in revistas])
                    st.success(f"**🔥 Maior FI: {max_fi:.2f}**\n\nExcelente para Proc. 1")
                
                with col3:
                    st.info(f"**📊 Total: {len(revistas)}**\n\nÁrea: {area_capes}")
                
                # Análise
                st.markdown('<div class="section-title">▸ Análise</div>', unsafe_allow_html=True)
                
                if "Equilibrado" in foco:
                    if melhores_oa:
                        st.success(f"""
                        **✓ Equilibrado Recomendado**
                        
                        Priorize: {', '.join(melhores_oa[:2])}
                        
                        Equilibram FI e Altimetria!
                        """)
                    else:
                        st.warning("⚠️ Sem Open Access. Deposite preprint!")
                    
                elif "Impacto" in foco:
                    if melhores_oa:
                        st.success(f"""
                        **📢 Impacto Social**
                        
                        Priorize: {', '.join(melhores_oa)}
                        
                        **Ação:** Compartilhe nas redes!
                        """)
                    else:
                        st.error("⚠️ CRÍTICO: Deposite preprint no SciELO/arXiv!")
                    
                else:
                    st.success("""
                    **📈 Tradicional**
                    
                    Priorize maior FI na tabela.
                    
                    **Importante:** Deposite preprint!
                    """)
                
                # Procedimentos
                st.markdown('<div class="section-title">▸ Procedimentos</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **📊 Proc. 1 - Métricas**
                    
                    **Exatas/Saúde:**
                    - Excelente: > 3.0
                    - Bom: 1.5-3.0
                    - Aceitável: 0.5-1.5
                    
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
                    - Código aberto
                    
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
