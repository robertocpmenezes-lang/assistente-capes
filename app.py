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

with st.expander("📚 Clique para entender os 3 Procedimentos", expanded=False):
    st.markdown("""
    **📊 Procedimento 1:** Métricas do Periódico (Fator de Impacto)  
    **📢 Procedimento 2:** Impacto Social (Altimetria)  
    **✦ Procedimento 3:** Ciência Aberta e Qualitativo
    
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
        titulo = st.text_input("📝 Título do Artigo ou Tema")
        area_capes = st.selectbox(
            "📚 Grande Área CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"]
        )

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (EM INGLÊS)",
            height=120,
            placeholder="Ex: machine learning healthcare prediction"
        )
        foco = st.selectbox(
            "🎯 Estratégia",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"]
        )
    
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
        with st.spinner("⟳ Buscando revistas..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=6)
            
            if revistas:
                st.success("✓ Relatório gerado!")
                
                # Preparar dados para tabela
                dados_tabela = []
                melhores_oa = []
                
                for i, rev in enumerate(revistas, 1):
                    nome = rev.get("display_name", "N/A")
                    is_oa = rev.get("is_oa", False)
                    stats = rev.get("summary_stats", {})
                    fi = stats.get("2yr_mean_citedness", 0) or 0
                    citacoes = rev.get("cited_by_count", 0) or 0
                    
                    if is_oa:
                        melhores_oa.append(nome)
                    
                    # Determinar cores e ícones
                    if is_oa and citacoes > 5000:
                        acesso_icon = "🟢"
                        acesso_text = "Open Access"
                        altimetria = "🔥 Alto"
                        altimetria_cor = "🟢"
                    elif is_oa:
                        acesso_icon = "🔵"
                        acesso_text = "Open Access"
                        altimetria = "● Médio"
                        altimetria_cor = "🔵"
                    else:
                        acesso_icon = "🔴"
                        acesso_text = "Fechado"
                        altimetria = "○ Baixo"
                        altimetria_cor = "⚪"
                    
                    # Classificar FI
                    if fi > 10:
                        fi_class = "🔥 Excelente"
                    elif fi > 5:
                        fi_class = "⭐ Muito Bom"
                    elif fi > 2:
                        fi_class = "✅ Bom"
                    else:
                        fi_class = "📌 Aceitável"
                    
                    dados_tabela.append({
                        "📊 Ranking": f"#{i}",
                        "Revista": nome,
                        "🚪 Acesso": f"{acesso_icon} {acesso_text}",
                        "📈 Fator de Impacto": f"{fi:.2f}",
                        "Classificação FI": fi_class,
                        "💬 Citações": formatar_numero(citacoes),
                        "📢 Altimetria": f"{altimetria_cor} {altimetria}"
                    })
                
                # Tabela Comparativa
                st.markdown('<div class="section-title">✦ Tabela Comparativa de Revistas (Ordenada)</div>', unsafe_allow_html=True)
                
                st.info("""
                **Como ler a tabela:**
                - 🟢 **Open Access + Alto Impacto** = Melhor opção (verde)
                - 🔵 **Open Access** = Boa para altimetria (azul)
                - 🔴 **Fechado** = Paywall, mas alto FI (vermelho)
                - A tabela está ordenada por relevância
                """)
                
                # Criar DataFrame e exibir
                df = pd.DataFrame(dados_tabela)
                
                # Configurar display da tabela
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "📊 Ranking": st.column_config.TextColumn("📊 Ranking"),
                        "Revista": st.column_config.TextColumn("Revista", width="medium"),
                        "🚪 Acesso": st.column_config.TextColumn("🚪 Acesso"),
                        "📈 Fator de Impacto": st.column_config.NumberColumn("📈 Fator de Impacto"),
                        "Classificação FI": st.column_config.TextColumn("Classificação"),
                        "💬 Citações": st.column_config.TextColumn("💬 Citações"),
                        "📢 Altimetria": st.column_config.TextColumn("📢 Altimetria")
                    }
                )
                
                # Resumo Visual
                st.markdown('<div class="section-title">▸ Resumo Visual</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_oa = len(melhores_oa)
                    if total_oa > 0:
                        st.success(f"""
                        **🟢 Open Access Encontradas**
                        
                        Total: **{total_oa}** de {len(revistas)}
                        
                        {chr(10).join([f"- {r}" for r in melhores_oa])}
                        
                        **Vantagem:** Melhor para Proc. 2 (Altimetria)
                        """)
                    else:
                        st.warning(f"""
                        **🔴 Nenhuma Open Access**
                        
                        Todas {len(revistas)} revistas são fechadas.
                        
                        **Solução:** Deposite preprint!
                        """)
                
                with col2:
                    max_fi = max([rev.get("summary_stats", {}).get("2yr_mean_citedness", 0) or 0 for rev in revistas])
                    if max_fi > 10:
                        st.success(f"""
                        **🔥 Alto Impacto Encontrado**
                        
                        Maior FI: **{max_fi:.2f}**
                        
                        Excelente para Proc. 1 (Métricas)
                        """)
                    elif max_fi > 5:
                        st.info(f"""
                        **⭐ Bom Impacto**
                        
                        Maior FI: **{max_fi:.2f}**
                        
                        Muito bom para a área
                        """)
                    else:
                        st.info(f"""
                        **📌 Impacto Moderado**
                        
                        Maior FI: **{max_fi:.2f}**
                        
                        Aceitável para Humanas
                        """)
                
                with col3:
                    st.info(f"""
                    **📊 Total de Revistas**
                    
                    Encontradas: **{len(revistas)}**
                    
                    Área: {area_capes}
                    
                    Estratégia: {foco}
                    """)
                
                # Análise Estratégica
                st.markdown('<div class="section-title">▸ Análise Estratégica</div>', unsafe_allow_html=True)
                st.info(f"**Área CAPES:** {area_capes} | **Estratégia:** {foco}")
                
                if "Equilibrado" in foco:
                    if melhores_oa:
                        st.success(f"""
                        **✓ Estratégia Equilibrada Recomendada**
                        
                        **Melhores opções (Open Access + Bom FI):**
                        {chr(10).join([f"- {r}" for r in melhores_oa[:3]])}
                        
                        Priorize estas revistas! Elas equilibram FI (Proc. 1) e Altimetria (Proc. 2).
                        """)
                    else:
                        st.warning("""
                        **⚠️ Atenção: Sem Open Access**
                        
                        Para estratégia equilibrada, escolha a revista com melhor FI na tabela e **deposite preprint** em repositório aberto!
                        """)
                    
                elif "Impacto Social" in foco:
                    if melhores_oa:
                        st.success(f"""
                        **📢 Foco em Impacto Social**
                        
                        **Priorize estas (Open Access):**
                        {chr(10).join([f"- {r}" for r in melhores_oa])}
                        
                        **Ação pós-publicação:**
                        - Compartilhar no LinkedIn, Twitter, ResearchGate
                        - Enviar para mailing da área
                        - Divulgar ativamente
                        """)
                    else:
                        st.error("""
                        **⚠️ CRÍTICO: Nenhuma Open Access**
                        
                        Para máximo impacto social, você PRECISA:
                        1. Depositar preprint no SciELO/arXiv/bioRxiv
                        2. Compartilhar amplamente o link
                        3. Usar redes sociais ativamente
                        """)
                    
                else:
                    st.success(f"""
                    **📈 Foco Tradicional**
                    
                    **Priorize pela tabela (maior FI primeiro):**
                    - Veja a coluna "Fator de Impacto"
                    - Priorize: FI > 3.0 (Exatas/Saúde) ou > 1.0 (Humanas)
                    
                    **Importante:** Mesmo sendo fechada, deposite preprint para não perder pontos no Proc. 2!
                    """)
                
                # Procedimentos
                st.markdown('<div class="section-title">▸ Guia dos Procedimentos</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **📊 Proc. 1 - Métricas
                    
                    CAPES usa OpenAlex.
                    
                    **Referências:**
                    
                    Exatas/Saúde:
                    - Excelente: > 3.0
                    - Bom: 1.5-3.0
                    - Aceitável: 0.5-1.5
                    
                    Humanas:
                    - Excelente: > 1.5
                    - Bom: 0.5-1.5
                    - Aceitável: 0.2-0.5
                    """)
                
                with col2:
                    if melhores_oa:
                        st.success("""
                        **📢 Proc. 2 - Altimetria
                        
                        ✓ Tem Open Access!
                        
                        **Vantagens:**
                        - Artigo gratuito
                        - Mais downloads
                        - Mais compartilhamentos
                        - Mais menções sociais
                        
                        **Ação:** Divulgue ativamente!
                        """)
                    else:
                        st.warning("""
                        **📢 Proc. 2 - Altimetria
                        
                        ⚠ Todas fechadas
                        
                        **Solução OBRIGATÓRIA:**
                        1. Deposite preprint
                        2. Compartilhe link
                        3. Use redes sociais
                        4. Envie para mailing
                        """)
                
                with col3:
                    st.info("""
                    **✦ Proc. 3 - Ciência Aberta
                    
                    CAPES premia transparência!
                    
                    **Ações que contam:**
                    - Dados no Zenodo/OSF
                    - Citar DOI dos dados
                    - Preprints
                    - Código aberto
                    
                    💡 Dados abertos = +30% citações!
                    """)
                
                # Checklist
                st.markdown('<div class="section-title">▸ Checklist</div>', unsafe_allow_html=True)
                st.success("""
                **📋 Antes:** [ ] ORCID vinculado | [ ] Dados organizados  
                **📤 Durante:** [ ] Preprint | [ ] DOI no artigo  
                **📢 Após:** [ ] Divulgar nas redes | [ ] Monitorar altimetria
                """)
                
            else:
                st.warning("⚠️ Nenhuma revista encontrada. Tente termos em inglês mais genéricos.")

# Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0;">
        OpenAlex + CAPES 2025-2028 | Sem vínculo oficial CAPES/MEC
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Promovendo Ciência Aberta</em>
    </p>
</div>
""", unsafe_allow_html=True)
