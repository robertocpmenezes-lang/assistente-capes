import streamlit as st
import requests
import urllib.parse

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Assistente CAPES 2025-2028", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Premium com Tabela Visual
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
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
    
    /* Cards de Revista - Visual Premium */
    .journal-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .journal-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
    }
    
    .journal-card.oa-high {
        border-left-color: #48bb78;
        background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
    }
    
    .journal-card.oa-medium {
        border-left-color: #4299e1;
        background: linear-gradient(135deg, #ebf8ff 0%, #ffffff 100%);
    }
    
    .journal-card.closed {
        border-left-color: #fc8181;
        background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
    }
    
    .journal-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .metric-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.25rem;
    }
    
    .badge-oa-yes {
        background: #c6f6d5;
        color: #22543d;
    }
    
    .badge-oa-no {
        background: #fed7d7;
        color: #742a2a;
    }
    
    .badge-fi-high {
        background: #fef5e7;
        color: #744210;
        border: 2px solid #f6ad55;
    }
    
    .badge-fi-medium {
        background: #bee3f8;
        color: #2a4365;
    }
    
    .badge-fi-low {
        background: #e2e8f0;
        color: #4a5568;
    }
    
    .badge-alt-high {
        background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
        color: white;
        font-weight: 700;
    }
    
    .badge-alt-medium {
        background: #90cdf4;
        color: #2a4365;
    }
    
    .badge-alt-low {
        background: #e2e8f0;
        color: #718096;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .metric-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #718096;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .footer {
        margin-top: 4rem;
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
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
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
st.markdown('<div class="section-title">▸ Entenda a Nova Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique aqui para entender os 3 Procedimentos", expanded=False):
    st.markdown("""
    ### Como Funciona a Avaliação CAPES 2025-2028
    
    **📊 Procedimento 1:** Métricas do Periódico (Fator de Impacto)  
    **📢 Procedimento 2:** Impacto Social (Altimetria)  
    **✦ Procedimento 3:** Ciência Aberta e Qualitativo
    
    ### Estratégias:
    - **⚖️ Equilibrado:** Mais seguro e recomendado
    - **📢 Impacto Social:** Prioriza Acesso Aberto
    - **📈 Tradicional:** Foca em alto Fator de Impacto
    """)

# ==============================================================================
# FORMULÁRIO
# ==============================================================================
with st.form("dados_pesquisa", clear_on_submit=False):
    st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)
    
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
        resumo = st.text_area("🔑 Palavras-chave (em inglês)", height=130, placeholder="Ex: machine learning healthcare")
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
@st.cache_data(ttl=3600)
def buscar_revistas_openalex(query, max_results=5):
    safe_query = urllib.parse.quote(query)
    url_works = f"https://api.openalex.org/works?search={safe_query}&per-page=20"
    
    try:
        response = requests.get(url_works, timeout=15)
        response.raise_for_status()
        works_data = response.json().get("results", [])
        
        revistas = []
        ids_vistos = set()
        
        for work in works_data:
            source = work.get("primary_location", {}).get("source")
            if source and source.get("id") not in ids_vistos:
                ids_vistos.add(source.get("id"))
                source_id = source.get("id").replace("https://openalex.org/", "")
                try:
                    resp = requests.get(f"https://api.openalex.org/sources/{source_id}", timeout=10)
                    if resp.status_code == 200:
                        revistas.append(resp.json())
                        if len(revistas) >= max_results:
                            break
                except:
                    continue
        return revistas
    except:
        return []

def criar_card_revista(nome, is_oa, fi, citacoes, rank):
    """Cria um card visual premium para cada revista"""
    
    # Determinar classe do card
    if is_oa and citacoes > 5000:
        card_class = "oa-high"
        alt_badge = '<span class="metric-badge badge-alt-high">🔥 Alto</span>'
    elif is_oa:
        card_class = "oa-medium"
        alt_badge = '<span class="metric-badge badge-alt-medium">● Médio</span>'
    else:
        card_class = "closed"
        alt_badge = '<span class="metric-badge badge-alt-low">○ Baixo</span>'
    
    # Badge de acesso
    if is_oa:
        acesso_badge = '<span class="metric-badge badge-oa-yes">✓ Acesso Aberto</span>'
    else:
        acesso_badge = '<span class="metric-badge badge-oa-no">✕ Fechado</span>'
    
    # Badge de FI
    if fi and fi > 5:
        fi_badge = f'<span class="metric-badge badge-fi-high">⭐ {fi:.2f}</span>'
        fi_class = "high"
    elif fi and fi > 2:
        fi_badge = f'<span class="metric-badge badge-fi-medium">{fi:.2f}</span>'
        fi_class = "medium"
    else:
        fi_badge = f'<span class="metric-badge badge-fi-low">{fi:.2f if fi else "N/A"}</span>'
        fi_class = "low"
    
    # Destaque para top 1
    destaque = "🏆 " if rank == 1 else ""
    
    html = f'''
    <div class="journal-card {card_class}">
        <div class="journal-name">{destaque}{nome}</div>
        <div style="margin: 1rem 0;">
            {acesso_badge}
            {alt_badge}
        </div>
        <div class="metrics-grid">
            <div class="metric-item">
                <div class="metric-label">Fator de Impacto</div>
                <div class="metric-value" style="color: {"#dd6b20" if fi_class == "high" else "#4a5568"};">{fi:.2f if fi else "N/A"}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Citações Totais</div>
                <div class="metric-value">{citacoes:,}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Classificação</div>
                <div class="metric-value">#{rank}</div>
            </div>
        </div>
    </div>
    '''
    return html

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
if submitted:
    if not resumo.strip():
        st.warning("⚠️ Insira palavras-chave em inglês.")
    else:
        with st.spinner("⟳ Buscando revistas e gerando análise..."):
            query_busca = " ".join(resumo.split()[:15]) 
            revistas = buscar_revistas_openalex(query_busca, max_results=5)
            
            if revistas:
                st.success("✓ Relatório gerado com sucesso!")
                
                # Cabeçalho da Tabela Visual
                st.markdown('<div class="section-title">✦ Revistas Sugeridas (Métricas Reais)</div>', unsafe_allow_html=True)
                
                st.info("""
                **Legenda Visual:**
                - 🟢 **Card Verde:** Acesso Aberto + Alto Impacto (Melhor opção!)
                - 🔵 **Card Azul:** Acesso Aberto (Boa para altimetria)
                - 🔴 **Card Vermelho:** Fechado (Requer assinatura, mas alto FI)
                - ⭐ **Fator de Impacto:** Laranja = Excelente (>5), Azul = Bom (>2)
                """)
                
                # Criar cards visuais
                html_cards = ""
                melhores_oa = []
                
                for i, rev in enumerate(revistas, 1):
                    nome = rev.get("display_name", "Nome não disponível")
                    is_oa = rev.get("is_oa", False)
                    summary_stats = rev.get("summary_stats", {})
                    fi = summary_stats.get("2yr_mean_citedness", 0)
                    citacoes = rev.get("cited_by_count", 0)
                    
                    if is_oa:
                        melhores_oa.append(nome)
                    
                    html_cards += criar_card_revista(nome, is_oa, fi, citacoes, i)
                
                st.markdown(html_cards, unsafe_allow_html=True)
                
                # Análise Estratégica
                st.markdown('<div class="section-title">▸ Análise Estratégica</div>', unsafe_allow_html=True)
                st.info(f"**Área:** {area_capes} | **Estratégia:** {foco}")
                
                if "Equilibrado" in foco:
                    st.success("""
                    **✓ Estratégia Equilibrada Recomendada**
                    
                    **Recomendação:** Priorize as revistas com cards **verdes** (Acesso Aberto + Alto Impacto). 
                    Elas oferecem o melhor dos dois mundos: bom Fator de Impacto (Proc. 1) e máximo potencial 
                    de Altimetria (Proc. 2).
                    """)
                elif "Impacto Social" in foco:
                    if melhores_oa:
                        st.success(f"""
                        **📢 Foco em Impacto Social**
                        
                        **Revistas Recomendadas (Acesso Aberto):**
                        {chr(10).join([f"- {rev}" for rev in melhores_oa])}
                        
                        **Ação:** Após publicar, compartilhe ativamente nas redes sociais!
                        """)
                    else:
                        st.warning("""
                        **⚠ Atenção:** Nenhuma revista Open Access encontrada.
                        
                        **Solução:** Deposite o preprint em SciELO Preprints ou arXiv para garantir altimetria.
                        """)
                else:
                    st.success("""
                    **📈 Foco Tradicional**
                    
                    **Recomendação:** Priorize revistas com Fator de Impacto > 3.0 (Exatas/Saúde) ou > 1.0 (Humanas).
                    
                    **Importante:** Se a revista for fechada, deposite o preprint em repositório aberto!
                    """)
                
                # Procedimentos CAPES
                st.markdown('<div class="section-title">▸ Guia dos Procedimentos CAPES</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **📊 Procedimento 1**
                    
                    **Métricas do Periódico**
                    
                    - FI > 3.0: Excelente (Exatas/Saúde)
                    - FI > 1.5: Bom
                    - FI > 0.5: Aceitável (Humanas)
                    
                    A CAPES usa OpenAlex como base oficial.
                    """)
                
                with col2:
                    if melhores_oa:
                        st.success("""
                        **📢 Procedimento 2
                        
                        **Impacto Social (Altimetria)**
                        
                        ✓ Você tem revistas Open Access!
                        
                        **Vantagens:**
                        - Mais downloads
                        - Mais compartilhamentos
                        - Mais citações
                        
                        **Ação:** Divulgue ativamente!
                        """)
                    else:
                        st.warning("""
                        **📢 Procedimento 2
                        
                        **Impacto Social (Altimetria)**
                        
                        ⚠ Revistas fechadas
                        
                        **Solução:**
                        - Deposite preprint
                        - Compartilhe o link
                        - Use redes sociais
                        """)
                
                with col3:
                    st.info("""
                    **✦ Procedimento 3**
                    
                    **Ciência Aberta**
                    
                    **Ações que contam pontos:**
                    - Dados no Zenodo/OSF
                    - Citar DOI dos dados
                    - Publicar preprints
                    - Código aberto (GitHub)
                    
                    **Dica:** Dados abertos = 30% mais citações!
                    """)
                
                # Checklist
                st.markdown('<div class="section-title">▸ Checklist</div>', unsafe_allow_html=True)
                st.success("""
                **Antes:** [ ] ORCID vinculado | [ ] Dados organizados  
                **Durante:** [ ] Preprint depositado | [ ] DOI dos dados no artigo  
                **Após:** [ ] Divulgar nas redes | [ ] Monitorar altimetria
                """)
                
            else:
                st.warning("⚠️ Nenhuma revista encontrada. Tente termos mais genéricos em inglês.")

# Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0;">
        Desenvolvida com OpenAlex e alinhada à CAPES 2025-2028.<br>
        Sem vínculo oficial com CAPES/MEC.
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Promovendo Ciência Aberta</em>
    </p>
</div>
""", unsafe_allow_html=True)
