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

# CSS Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
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
    
    /* Cards Compactos e Bonitos */
    .journal-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: all 0.3s;
    }
    
    .journal-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
        transform: translateX(4px);
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
        font-size: 1.1rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0 0 0.75rem 0;
    }
    
    .badge {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 0.5rem;
    }
    
    .badge-yes { background: #c6f6d5; color: #22543d; }
    .badge-no { background: #fed7d7; color: #742a2a; }
    .badge-high { background: #fef5e7; color: #744210; border: 2px solid #f6ad55; }
    .badge-medium { background: #bee3f8; color: #2a4365; }
    .badge-low { background: #e2e8f0; color: #718096; }
    
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-top: 0.75rem;
    }
    
    .metric-box {
        background: #f7fafc;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #718096;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .metric-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: #e2e8f0;
        border-radius: 12px;
        text-align: center;
    }
    
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-info { background: #ebf8ff; border-left: 4px solid #4299e1; }
    .alert-success { background: #f0fff4; border-left: 4px solid #48bb78; }
    .alert-warning { background: #fffaf0; border-left: 4px solid #ed8936; }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
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
# SEÇÃO EDUCACIONAL EXPANDÍVEL
# ==============================================================================
st.markdown('<div class="section-title">▸ Entenda a Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique para entender os 3 Procedimentos e Estratégias", expanded=False):
    st.markdown("""
    ### 🔍 Como Funciona a Avaliação CAPES 2025-2028
    
    A CAPES avalia os programas através de **3 procedimentos complementares**:
    
    #### **📊 Procedimento 1: Métricas do Periódico (Qualis)**
    - **O que avalia:** Qualidade da REVISTA onde você publica
    - **Como mede:** Fator de Impacto, Quartil (Q1-Q4), Citações
    - **Base:** OpenAlex (substituiu o JCR/Scopus pagos)
    - **Referências:**
      - Exatas/Saúde: Excelente >3.0 | Bom >1.5 | Aceitável >0.5
      - Humanas: Excelente >1.5 | Bom >0.5 | Aceitável >0.2
    
    #### **📢 Procedimento 2: Impacto Social (Altimetria)**
    - **O que avalia:** Impacto do SEU ARTIGO na sociedade
    - **Como mede:** 
      - Downloads e visualizações
      - Menções em redes sociais (Twitter, LinkedIn)
      - Compartilhamentos (ResearchGate, Mendeley)
      - Citações em políticas públicas, blogs, notícias
    - **Dica crucial:** Artigos em Acesso Aberto têm MUITO mais alcance!
    
    #### **✦ Procedimento 3: Ciência Aberta e Qualitativo**
    - **O que avalia:** Relevância e transparência da pesquisa
    - **Como mede:** 
      - Análise por pares consultores da CAPES
      - Disponibilização de dados (dados abertos)
      - Publicação de preprints
      - Contribuição social
    - **Dica de ouro:** Depositar dados no Zenodo/OSF conta MUITOS pontos!
    
    ---
    
    ### 🎯 Os 3 Tipos de Estratégia
    
    #### **⚖️ 1. Equilibrado (Impacto + Ciência Aberta)**
    **QUANDO USAR:**
    - ✓ Mais seguro e recomendado pela CAPES
    - ✓ Boa pontuação em todos os procedimentos
    - ✓ Ideal se não tem preferência específica
    
    **CARACTERÍSTICAS:**
    - Busca bom Fator de Impacto (Proc. 1)
    - Prioriza Acesso Aberto quando possível (Proc. 2)
    - Incentiva Ciência Aberta (Proc. 3)
    
    ---
    
    #### **📢 2. Máximo Impacto Social (Altimetria)**
    **QUANDO USAR:**
    - ✓ Pesquisa com aplicação prática/social
    - ✓ Quer maximizar leituras e compartilhamentos
    - ✓ Áreas: Saúde Pública, Educação, Políticas Públicas
    
    **CARACTERÍSTICAS:**
    - Prioriza revistas Open Access
    - Aceita FI moderado
    - Exige divulgação ativa pós-publicação
    
    **AÇÃO OBRIGATÓRIA:**
    Após publicar, compartilhe ativamente nas redes!
    
    ---
    
    #### **📈 3. Máximo Tradicional (Fator de Impacto)**
    **QUANDO USAR:**
    - ✓ Busca prestígio acadêmico máximo
    - ✓ Áreas que valorizam muito FI (Exatas, Saúde)
    - ✓ Quer competir por posições em universidades de elite
    
    **CARACTERÍSTICAS:**
    - Foca em revistas de alto FI (Nature, Science, Lancet)
    - Aceita que sejam fechadas (paywall)
    
    **COMPENSAÇÃO NECESSÁRIA:**
    Deposite o preprint em repositório aberto (arXiv, SciELO) para garantir altimetria!
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
        resumo = st.text_area(
            "🔑 Palavras-chave (em inglês)",
            height=120,
            placeholder="Ex: machine learning healthcare prediction"
        )
        foco = st.selectbox(
            "🎯 Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"]
        )
    
    submitted = st.form_submit_button("🚀 Gerar Relatório Completo", use_container_width=True)

# ==============================================================================
# FUNÇÕES
# ==============================================================================
def formatar_numero_grande(num):
    """Formata números grandes de forma elegante"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)

@st.cache_data(ttl=3600)
def buscar_revistas(query, max_results=5):
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
        st.markdown('<div class="alert-box alert-warning">⚠️ <strong>Atenção:</strong> Insira palavras-chave em inglês.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("⟳ Buscando revistas e gerando análise..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=5)
            
            if revistas:
                st.markdown('<div class="alert-box alert-success">✓ <strong>Relatório gerado com sucesso!</strong></div>', unsafe_allow_html=True)
                
                # Tabela Visual Compacta
                st.markdown('<div class="section-title">✦ Revistas Sugeridas (Métricas Reais)</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="alert-box alert-info">
                <strong>Legenda Visual:</strong><br>
                • 🟢 <strong>Card Verde:</strong> Open Access + Alto Impacto (Melhor opção!)<br>
                • 🔵 <strong>Card Azul:</strong> Open Access (Boa para altimetria)<br>
                • 🔴 <strong>Card Vermelho:</strong> Fechado/Paywall (Alto FI tradicional)
                </div>
                """, unsafe_allow_html=True)
                
                melhores_oa = []
                html_cards = ""
                
                for i, rev in enumerate(revistas, 1):
                    nome = rev.get("display_name", "N/A")
                    is_oa = rev.get("is_oa", False)
                    stats = rev.get("summary_stats", {})
                    fi = stats.get("2yr_mean_citedness", 0) or 0
                    citacoes = rev.get("cited_by_count", 0) or 0
                    
                    if is_oa:
                        melhores_oa.append(nome)
                    
                    # Determinar classe
                    if is_oa and citacoes > 5000:
                        card_class = "oa-high"
                        alt_badge = '<span class="badge badge-high">🔥 Alto</span>'
                    elif is_oa:
                        card_class = "oa-medium"
                        alt_badge = '<span class="badge badge-medium">● Médio</span>'
                    else:
                        card_class = "closed"
                        alt_badge = '<span class="badge badge-low">○ Baixo</span>'
                    
                    # Badge acesso
                    acesso_badge = '<span class="badge badge-yes">✓ Aberto</span>' if is_oa else '<span class="badge badge-no">✕ Fechado</span>'
                    
                    # Badge FI
                    if fi > 5:
                        fi_badge = f'<span class="badge badge-high">⭐ {fi:.2f}</span>'
                        fi_color = "#dd6b20"
                    elif fi > 2:
                        fi_badge = f'<span class="badge badge-medium">{fi:.2f}</span>'
                        fi_color = "#4a5568"
                    else:
                        fi_badge = f'<span class="badge badge-low">{fi:.2f}</span>'
                        fi_color = "#4a5568"
                    
                    # Destaque
                    destaque = "🏆 " if i == 1 else ""
                    
                    # Formatar citações
                    citacoes_fmt = formatar_numero_grande(citacoes)
                    
                    html_cards += f'''
                    <div class="journal-card {card_class}">
                        <h3 class="journal-name">{destaque}{nome}</h3>
                        <div style="margin-bottom: 0.75rem;">{acesso_badge} {alt_badge}</div>
                        <div class="metrics-row">
                            <div class="metric-box">
                                <div class="metric-label">Fator de Impacto</div>
                                <div class="metric-value" style="color: {fi_color};">{fi:.2f}</div>
                            </div>
                            <div class="metric-box">
                                <div class="metric-label">Citações</div>
                                <div class="metric-value">{citacoes_fmt}</div>
                            </div>
                            <div class="metric-box">
                                <div class="metric-label">Ranking</div>
                                <div class="metric-value">#{i}</div>
                            </div>
                        </div>
                    </div>
                    '''
                
                st.markdown(html_cards, unsafe_allow_html=True)
                
                # Análise Estratégica
                st.markdown('<div class="section-title">▸ Análise Estratégica Personalizada</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="alert-box alert-info"><strong>Área CAPES:</strong> {area_capes} | <strong>Estratégia:</strong> {foco}</div>', unsafe_allow_html=True)
                
                if "Equilibrado" in foco:
                    st.markdown("""
                    <div class="alert-box alert-success">
                    <h4 style="margin-top: 0;">✓ Estratégia Equilibrada - A Mais Recomendada</h4>
                    <p>Você escolheu a estratégia mais segura e alinhada com a CAPES 2025-2028.</p>
                    <p><strong>O que isso significa:</strong></p>
                    <ul>
                        <li>Busca revistas com <strong>bom Fator de Impacto</strong> (Proc. 1)</li>
                        <li>Prioriza <strong>Acesso Aberto</strong> quando possível (Proc. 2)</li>
                        <li>Valoriza <strong>Ciência Aberta</strong> e transparência (Proc. 3)</li>
                    </ul>
                    <p><strong>Recomendação:</strong> Priorize as revistas com cards <strong>verdes</strong> (Open Access + Alto Impacto). Elas oferecem o melhor dos dois mundos!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif "Impacto Social" in foco:
                    if melhores_oa:
                        st.markdown(f"""
                        <div class="alert-box alert-success">
                        <h4 style="margin-top: 0;">📢 Estratégia de Máximo Impacto Social</h4>
                        <p>Você prioriza o <strong>Procedimento 2 (Altimetria)</strong>.</p>
                        <p><strong>Revistas Open Access encontradas:</strong></p>
                        <ul>
                        {"".join([f"<li>{r}</li>" for r in melhores_oa])}
                        </ul>
                        <p><strong>Ação OBRIGATÓRIA:</strong> Após publicar, compartilhe ativamente no LinkedIn, Twitter, ResearchGate e mailing lists da área.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="alert-box alert-warning">
                        <h4 style="margin-top: 0;">⚠ Atenção: Nenhuma Open Access</h4>
                        <p><strong>Solução OBRIGATÓRIA:</strong> Deposite o preprint em SciELO Preprints, arXiv ou bioRxiv para garantir altimetria.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                else:
                    st.markdown("""
                    <div class="alert-box alert-success">
                    <h4 style="margin-top: 0;">📈 Estratégia de Máximo Impacto Tradicional</h4>
                    <p>Você prioriza o <strong>Procedimento 1 (Fator de Impacto)</strong>.</p>
                    <p><strong>Recomendação:</strong> Priorize revistas com FI > 3.0 (Exatas/Saúde) ou > 1.0 (Humanas).</p>
                    <p><strong>Compensação necessária:</strong> Revistas de alto impacto geralmente são fechadas. Deposite o preprint em repositório aberto (arXiv, SciELO) para não perder pontos no Proc. 2.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Procedimentos Detalhados
                st.markdown('<div class="section-title">▸ Guia dos 3 Procedimentos CAPES</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;">📊 Procedimento 1</h4>
                    <p><strong>Métricas do Periódico</strong></p>
                    <p>A CAPES usa a OpenAlex como base oficial.</p>
                    <p><strong>Referências:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li><strong>Exatas/Saúde:</strong>
                            <ul style="padding-left: 1rem; margin: 0;">
                                <li>Excelente: FI > 3.0</li>
                                <li>Bom: FI 1.5-3.0</li>
                                <li>Aceitável: FI 0.5-1.5</li>
                            </ul>
                        </li>
                        <li><strong>Humanas:</strong>
                            <ul style="padding-left: 1rem; margin: 0;">
                                <li>Excelente: FI > 1.5</li>
                                <li>Bom: FI 0.5-1.5</li>
                                <li>Aceitável: FI 0.2-0.5</li>
                            </ul>
                        </li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if melhores_oa:
                        st.markdown("""
                        <div class="alert-box alert-success">
                        <h4 style="margin-top: 0;">📢 Procedimento 2</h4>
                        <p><strong>Impacto Social (Altimetria)</strong></p>
                        <p style="color: #22543d;"><strong>✓ Vantagem:</strong> Você tem revistas Open Access!</p>
                        <p><strong>O que isso significa:</strong></p>
                        <ul style="padding-left: 1rem; margin: 0;">
                            <li>Artigo gratuito para todos</li>
                            <li>Mais downloads</li>
                            <li>Mais compartilhamentos</li>
                            <li>Mais citações em políticas públicas</li>
                        </ul>
                        <p style="margin-top: 0.5rem;"><strong>Ação:</strong> Divulgue ativamente nas redes!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="alert-box alert-warning">
                        <h4 style="margin-top: 0;">📢 Procedimento 2</h4>
                        <p><strong>Impacto Social (Altimetria)</strong></p>
                        <p style="color: #742a2a;"><strong>⚠ Atenção:</strong> Revistas fechadas</p>
                        <p><strong>Problema:</strong> Poucas pessoas conseguirão ler</p>
                        <p><strong>Solução OBRIGATÓRIA:</strong></p>
                        <ol style="padding-left: 1rem; margin: 0;">
                            <li>Deposite preprint</li>
                            <li>Compartilhe o link</li>
                            <li>Use redes sociais</li>
                        </ol>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;">✦ Procedimento 3</h4>
                    <p><strong>Ciência Aberta</strong></p>
                    <p>A CAPES premia MUITO a transparência!</p>
                    <p><strong>Ações que contam pontos:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li>Dados no <a href="https://zenodo.org" target="_blank">Zenodo</a> ou <a href="https://osf.io" target="_blank">OSF</a></li>
                        <li>Citar DOI dos dados no artigo</li>
                        <li>Publicar preprints</li>
                        <li>Código aberto (GitHub)</li>
                    </ul>
                    <p style="margin-top: 0.5rem;"><strong>💡 Dica:</strong> Dados abertos = até 30% mais citações!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Checklist
                st.markdown('<div class="section-title">▸ Checklist de Ação</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="alert-box alert-success">
                <h4 style="margin-top: 0;">📋 Antes da Submissão</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>Vincular ORCID</strong> ao Lattes (obrigatório)</li>
                    <li><strong>Preparar dados</strong> para repositório</li>
                    <li><strong>Escolher repositório</strong> (Zenodo ou OSF)</li>
                </ul>
                
                <h4 style="margin: 1rem 0 0.5rem 0;">📤 Durante a Submissão</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>Depositar preprint</strong> (se permitido)</li>
                    <li><strong>Subir dados</strong> no Zenodo/OSF e obter DOI</li>
                    <li><strong>Incluir DOI dos dados</strong> no manuscrito</li>
                </ul>
                
                <h4 style="margin: 1rem 0 0.5rem 0;">📢 Após a Publicação (CRUCIAL!)</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>Atualizar preprint</strong> com link da versão publicada</li>
                    <li><strong>Divulgar</strong> no LinkedIn, Twitter, ResearchGate</li>
                    <li><strong>Enviar</strong> para mailing da área</li>
                    <li><strong>Compartilhar</strong> com assessoria de comunicação</li>
                    <li><strong>Monitorar altimetria</strong> em altmetric.com</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="alert-box alert-warning">
                <h4 style="margin-top: 0;">⚠️ Nenhuma revista encontrada</h4>
                <p><strong>Dicas:</strong></p>
                <ul>
                    <li>Use palavras-chave em inglês</li>
                    <li>Use termos mais genéricos (ex: "machine learning" em vez de "deep learning neural network")</li>
                    <li>Verifique a ortografia</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com bases de dados abertas (OpenAlex) e alinhada às Diretrizes da CAPES (2025-2028).<br>
        Esta ferramenta não possui vinculação oficial com a CAPES ou MEC.
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Iniciativa de promoção da Ciência Aberta e Transparência na Pós-Graduação Brasileira</em>
    </p>
</div>
""", unsafe_allow_html=True)
