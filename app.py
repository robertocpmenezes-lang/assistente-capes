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
    initial_sidebar_state="expanded"
)

# CSS Premium
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
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-header {
        color: #4a5568;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .section-title {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .badge-oa-yes {
        background: #c6f6d5;
        color: #22543d;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-oa-no {
        background: #fed7d7;
        color: #742a2a;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-high {
        background: #feebc8;
        color: #744210;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-medium {
        background: #bee3f8;
        color: #2a4365;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-low {
        background: #e2e8f0;
        color: #4a5568;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: #e2e8f0;
        border-radius: 12px;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .alert-info {
        background: #ebf8ff;
        border-left: 4px solid #4299e1;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-success {
        background: #f0fff4;
        border-left: 4px solid #48bb78;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .expander-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin: 1rem 0;
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
# SEÇÃO EDUCACIONAL - ENTENDA A AVALIAÇÃO CAPES
# ==============================================================================
st.markdown('<div class="section-title">▸ Entenda a Nova Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique aqui para entender os 3 Procedimentos de Avaliação", expanded=False):
    st.markdown("""
    ### 🔍 Como Funciona a Avaliação CAPES 2025-2028
    
    A CAPES avalia os programas de pós-graduação através de **3 procedimentos complementares**:
    
    #### **📊 Procedimento 1: Métricas do Periódico (Qualis)**
    - **O que avalia:** A qualidade da REVISTA onde você publica
    - **Como mede:** Fator de Impacto, Quartil (Q1-Q4), Citações
    - **Base de dados:** OpenAlex (substituiu o JCR pago)
    - **Importância:** Tradicional e ainda muito relevante
    - **Dica:** Revistas Q1 e Q2 têm maior pontuação
    
    #### **📢 Procedimento 2: Impacto Social do Artigo (Altimetria)**
    - **O que avalia:** O impacto do SEU ARTIGO na sociedade
    - **Como mede:** 
      - Downloads e visualizações
      - Menções em redes sociais (Twitter, LinkedIn)
      - Compartilhamentos no ResearchGate, Mendeley
      - Citações em políticas públicas, blogs, notícias
    - **Base de dados:** Crossref Event Data, Altmetric, Dimensions
    - **Importância:** NOVO e cada vez mais valorizado
    - **Dica:** Artigos em Acesso Aberto têm MUITO mais alcance
    
    #### **✦ Procedimento 3: Avaliação Qualitativa e Ciência Aberta**
    - **O que avalia:** A relevância e transparência da pesquisa
    - **Como mede:** 
      - Análise por pares consultores da CAPES
      - Disponibilização de dados de pesquisa (dados abertos)
      - Publicação de preprints
      - Contribuição para a sociedade
    - **Importância:** Diferencial competitivo enorme
    - **Dica:** Depositar dados no Zenodo/OSF conta muitos pontos
    
    ---
    
    ### 🎯 Os 3 Tipos de Estratégia (Focos)
    
    A escolha do foco depende dos seus objetivos de carreira e do seu programa:
    
    #### **⚖️ 1. Equilibrado (Impacto + Ciência Aberta)**
    **QUANDO USAR:**
    - ✓ Você quer boa pontuação em todos os procedimentos
    - ✓ Não tem preferência específica
    - ✓ É a estratégia mais segura e recomendada pela CAPES
    
    **CARACTERÍSTICAS:**
    - Busca revistas com bom Fator de Impacto (Proc. 1)
    - Prioriza Acesso Aberto quando possível (Proc. 2)
    - Incentiva Ciência Aberta e dados abertos (Proc. 3)
    
    **EXEMPLO PRÁTICO:**
    Publicar em revistas como "Frontiers in Immunology" (FI 4.80 + Open Access)
    
    ---
    
    #### **📢 2. Máximo Impacto Social (Altimetria)**
    **QUANDO USAR:**
    - ✓ Sua pesquisa tem aplicação prática e interesse social
    - ✓ Você quer que seu trabalho seja lido e compartilhado
    - ✓ Seu programa precisa melhorar no Procedimento 2
    - ✓ Você atua em áreas como Saúde Pública, Educação, Políticas Públicas
    
    **CARACTERÍSTICAS:**
    - Prioriza revistas Open Access (Acesso Aberto)
    - Aceita Fator de Impacto moderado
    - Foca em maximizar downloads e compartilhamentos
    - Exige divulgação ativa nas redes
    
    **EXEMPLO PRÁTICO:**
    Publicar em "PLOS ONE" ou "BMJ Open" (Open Access, alto alcance social)
    
    **AÇÃO NECESSÁRIA:**
    Após publicar, você DEVE:
    - Compartilhar no LinkedIn, Twitter, ResearchGate
    - Escrever posts explicando a pesquisa em linguagem acessível
    - Enviar para mailing de interessados na área
    
    ---
    
    #### **📈 3. Máximo Tradicional (Fator de Impacto)**
    **QUANDO USAR:**
    - ✓ Você busca prestígio acadêmico máximo
    - ✓ Sua área valoriza muito o Fator de Impacto (Exatas, Saúde)
    - ✓ Você quer competir por posições em universidades de elite
    - ✓ Seu programa precisa subir no ranking tradicional
    
    **CARACTERÍSTICAS:**
    - Foca em revistas de alto Fator de Impacto (Nature, Science, Lancet)
    - Aceita que sejam fechadas (paywall)
    - Menor preocupação com altimetria imediata
    
    **EXEMPLO PRÁTICO:**
    Publicar em "Nature Reviews Drug Discovery" (FI 12.72, mas fechada)
    
    **COMPENSAÇÃO NECESSÁRIA:**
    Como a revista é fechada, você DEVE:
    - Depositar o preprint no arXiv, bioRxiv ou SciELO Preprints
    - Compartilhar o link do preprint nas redes
    - Isso garante altimetria mesmo com paywall
    
    ---
    
    ### 🎓 Qual Estratégia Escolher?
    
    | Se você... | Escolha... |
    |------------|------------|
    | Está em início de carreira e quer construir currículo | **Equilibrado** |
    | Quer impacto social e político da sua pesquisa | **Máximo Impacto Social** |
    | Busca posições em universidades de elite | **Máximo Tradicional** |
    | Não sabe qual escolher | **Equilibrado** (é o mais seguro) |
    
    **IMPORTANTE:** Consulte seu coordenador de programa para saber qual estratégia 
    é mais valorizada na sua área específica!
    """)

# ==============================================================================
# FORMULÁRIO
# ==============================================================================
with st.form("dados_pesquisa", clear_on_submit=False):
    st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema da Pesquisa",
            help="Digite o título completo ou o tema geral. Isso ajuda a contextualizar a relevância da pesquisa para o Procedimento 3 (Avaliação Qualitativa)."
        )
        area_capes = st.selectbox(
            "📚 Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"],
            help="Cada área tem um Documento de Área específico que pondera de forma diferente os 3 procedimentos. Humanas, por exemplo, valoriza mais o Proc. 3 do que Exatas."
        )

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (preferencialmente em inglês)",
            height=130,
            placeholder="Ex: machine learning healthcare prediction genomics",
            help="Use 3-5 palavras-chave em inglês. A ferramenta busca na base global OpenAlex. Termos em inglês retornam muito mais revistas e métricas precisas."
        )
        foco = st.selectbox(
            "🎯 Foco da Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria / Proc. 2)", 
             "📈 Máximo Tradicional (Fator de Impacto / Proc. 1)"],
            help="Escolha baseado no seu objetivo: Equilibrado é o mais seguro. Impacto Social é para quem quer alcance. Tradicional é para prestígio acadêmico máximo."
        )
    
    submitted = st.form_submit_button("🚀 Gerar Relatório Estratégico Completo", use_container_width=True)

# ==============================================================================
# FUNÇÕES DE BUSCA
# ==============================================================================
@st.cache_data(ttl=3600)
def buscar_revistas_openalex(query, max_results=5):
    """Busca revistas na OpenAlex com cache para performance"""
    safe_query = urllib.parse.quote(query)
    url_works = f"https://api.openalex.org/works?search={safe_query}&per-page=20"
    
    try:
        response = requests.get(url_works, timeout=15)
        response.raise_for_status()
        works_data = response.json().get("results", [])
        
        revistas_encontradas = []
        ids_vistos = set()
        
        for work in works_data:
            source = work.get("primary_location", {}).get("source")
            if source and source.get("id") not in ids_vistos:
                ids_vistos.add(source.get("id"))
                source_id = source.get("id").replace("https://openalex.org/", "")
                url_source = f"https://api.openalex.org/sources/{source_id}"
                try:
                    resp = requests.get(url_source, timeout=10)
                    if resp.status_code == 200:
                        revista_detalhes = resp.json()
                        revistas_encontradas.append(revista_detalhes)
                        if len(revistas_encontradas) >= max_results:
                            break
                except:
                    continue
        
        return revistas_encontradas if revistas_encontradas else []
            
    except Exception as e:
        st.error(f"Erro na conexão com OpenAlex: {str(e)}")
        return []

# ==============================================================================
# GERADOR DE RELATÓRIO DETALHADO
# ==============================================================================
def gerar_relatorio_detalhado(titulo, area, foco, revistas):
    """Gera relatório com explicações detalhadas"""
    
    if not revistas:
        st.markdown('<div class="alert-info">⚠️ <strong>Nenhuma revista encontrada.</strong><br>Tente usar palavras-chave em inglês mais genéricas ou amplas.</div>', unsafe_allow_html=True)
        return
    
    # Tabela de Revistas
    st.markdown('<div class="section-title">✦ Revistas Sugeridas (Métricas Reais da OpenAlex)</div>', unsafe_allow_html=True)
    
    st.info("""
    **Como ler esta tabela:**
    - **Acesso Aberto (✓):** Artigo gratuito para todos → Melhor para Altimetria (Proc. 2)
    - **Fechado (✕):** Requer assinatura → Melhor para Fator de Impacto tradicional (Proc. 1)
    - **Fator de Impacto:** Quanto maior, melhor. Exatas/Saúde: >1.5 é bom | Humanas: >0.5 é bom
    - **Potencial Altimetria:** 🔥 Alto = mais downloads e compartilhamentos esperados
    """)
    
    # Preparar dados da tabela
    dados_tabela = []
    melhores_oa = []
    
    for rev in revistas:
        nome = rev.get("display_name", "Nome não disponível")
        is_oa = rev.get("is_oa", False)
        
        summary_stats = rev.get("summary_stats", {})
        fator_impacto = summary_stats.get("2yr_mean_citedness", 0)
        citacoes = rev.get("cited_by_count", 0)
        
        # Determinar potencial de altimetria
        if is_oa and citacoes > 5000:
            potencial = "🔥 Alto"
            badge_potencial = '<span class="badge-high">🔥 Alto</span>'
        elif is_oa:
            potencial = "● Médio"
            badge_potencial = '<span class="badge-medium">● Médio</span>'
        else:
            potencial = "○ Baixo"
            badge_potencial = '<span class="badge-low">○ Baixo</span>'
        
        if is_oa:
            melhores_oa.append(nome)
            badge_acesso = '<span class="badge-oa-yes">✓ Aberto</span>'
        else:
            badge_acesso = '<span class="badge-oa-no">✕ Fechado</span>'
        
        dados_tabela.append({
            "Revista": nome,
            "Acesso": badge_acesso,
            "Fator de Impacto": f"{fator_impacto:.2f}" if fator_impacto else "N/A",
            "Potencial Altimetria": badge_potencial
        })
    
    # Exibir tabela
    tabela_html = '''
    <table style="width:100%; border-collapse: collapse; margin: 1rem 0;">
        <thead>
            <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <th style="padding: 1rem; text-align: left; border-radius: 8px 0 0 0;">Revista</th>
                <th style="padding: 1rem; text-align: center;">Acesso</th>
                <th style="padding: 1rem; text-align: center;">Fator de Impacto</th>
                <th style="padding: 1rem; text-align: center; border-radius: 0 8px 0 0;">Potencial Altimetria</th>
            </tr>
        </thead>
        <tbody>
    '''
    
    for row in dados_tabela:
        tabela_html += f'''
            <tr style="background: white; border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 1rem; font-weight: 600; color: #2d3748;">{row['Revista']}</td>
                <td style="padding: 1rem; text-align: center;">{row['Acesso']}</td>
                <td style="padding: 1rem; text-align: center; font-family: monospace; color: #667eea; font-weight: 600;">{row['Fator de Impacto']}</td>
                <td style="padding: 1rem; text-align: center;">{row['Potencial Altimetria']}</td>
            </tr>
        '''
    
    tabela_html += '</tbody></table>'
    st.markdown(tabela_html, unsafe_allow_html=True)
    
    # Análise Estratégica Personalizada
    st.markdown('<div class="section-title">▸ Análise Estratégica Personalizada</div>', unsafe_allow_html=True)
    
    st.info(f"**Área CAPES:** {area} | **Estratégia Escolhida:** {foco}")
    
    # Explicação baseada no foco escolhido
    if "Equilibrado" in foco:
        st.markdown("""
        <div class="alert-success">
            <h4 style="margin-top: 0;">✓ Estratégia Equilibrada - A Mais Recomendada</h4>
            <p>Você escolheu a estratégia mais segura e alinhada com as diretrizes da CAPES 2025-2028.</p>
            <p><strong>O que isso significa:</strong></p>
            <ul>
                <li>Você busca revistas com <strong>bom Fator de Impacto</strong> (Proc. 1)</li>
                <li>Prioriza <strong>Acesso Aberto</strong> quando possível (Proc. 2)</li>
                <li>Valoriza <strong>Ciência Aberta</strong> e transparência (Proc. 3)</li>
            </ul>
            <p><strong>Recomendação:</strong> Das revistas listadas, priorize as marcadas com ✓ Aberto e que tenham Fator de Impacto acima de 1.0.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif "Impacto Social" in foco:
        st.markdown("""
        <div class="alert-success">
            <h4 style="margin-top: 0;">📢 Estratégia de Máximo Impacto Social</h4>
            <p>Você prioriza o <strong>Procedimento 2 (Altimetria)</strong> da CAPES.</p>
            <p><strong>O que isso significa:</strong></p>
            <ul>
                <li>Foco em <strong>Acesso Aberto</strong> para maximizar downloads e compartilhamentos</li>
                <li>Menor preocupação com Fator de Impacto tradicional</li>
                <li>Exige <strong>divulgação ativa</strong> após publicação</li>
            </ul>
            <p><strong>Recomendação:</strong> Publique APENAS em revistas marcadas com ✓ Aberto. Após publicar, compartilhe ativamente no LinkedIn, Twitter, ResearchGate e mailing lists da área.</p>
            <p><strong>Atenção:</strong> Se publicar em revista fechada, DEPOSITAR o preprint em repositório aberto (SciELO Preprints, arXiv) é OBRIGATÓRIO para ter altimetria.</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div class="alert-success">
            <h4 style="margin-top: 0;">📈 Estratégia de Máximo Impacto Tradicional</h4>
            <p>Você prioriza o <strong>Procedimento 1 (Fator de Impacto)</strong> da CAPES.</p>
            <p><strong>O que isso significa:</strong></p>
            <ul>
                <li>Foco em revistas de <strong>alto prestígio</strong> e Fator de Impacto elevado</li>
                <li>Busca maximizar pontuação no Qualis/CAPES tradicional</li>
                <li>Ideal para carreiras acadêmicas de elite</li>
            </ul>
            <p><strong>Recomendação:</strong> Priorize revistas com Fator de Impacto acima de 3.0 (Exatas/Saúde) ou 1.0 (Humanas).</p>
            <p><strong>Compensação necessária:</strong> Revistas de alto impacto geralmente são fechadas (✕). Para não perder pontos no Proc. 2 (Altimetria), você DEVE:</p>
            <ol>
                <li>Depositar o <strong>preprint</strong> no arXiv, bioRxiv ou SciELO Preprints</li>
                <li>Compartilhar o link do preprint nas redes sociais</li>
                <li>Divulgar ativamente mesmo com paywall</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Procedimento 1
    st.markdown('<div class="section-title">▸ Procedimento 1: Métricas do Periódico</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="metric-card">
        <h4 style="margin-top: 0; color: #667eea;">📊 O Que a CAPES Avalia</h4>
        <p><strong>A CAPES utiliza a OpenAlex como base oficial</strong> (substituindo o JCR/Scopus pagos). O Fator de Impacto exibido na tabela acima é o dado que os consultores da CAPES verão.</p>
        
        <h5>Referências por Área:</h5>
        <ul>
            <li><strong>Ciências Exatas e da Saúde:</strong> 
                <ul>
                    <li>Excelente: FI > 3.0</li>
                    <li>Bom: FI entre 1.5 e 3.0</li>
                    <li>Aceitável: FI entre 0.5 e 1.5</li>
                </ul>
            </li>
            <li><strong>Ciências Humanas e Sociais:</strong> 
                <ul>
                    <li>Excelente: FI > 1.5</li>
                    <li>Bom: FI entre 0.5 e 1.5</li>
                    <li>Aceitável: FI entre 0.2 e 0.5</li>
                </ul>
            </li>
        </ul>
        
        <p><strong>Dica importante:</strong> Além do Fator de Impacto, a CAPES também considera o Quartil (Q1, Q2, Q3, Q4) da revista. Q1 e Q2 têm maior pontuação.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Procedimento 2
    st.markdown('<div class="section-title">▸ Procedimento 2: Impacto Social (Altimetria)</div>', unsafe_allow_html=True)
    
    if melhores_oa:
        st.markdown(f'''
        <div class="metric-card" style="border-left-color: #48bb78;">
            <h4 style="margin-top: 0; color: #48bb78;">📢 Vantagem: Acesso Aberto Detectado</h4>
            <p style="color: #22543d;"><strong>✓ Excelente notícia!</strong> Algumas revistas sugeridas possuem Acesso Aberto:</p>
            <ul>
                {"".join([f"<li>{rev}</li>" for rev in melhores_oa[:3]])}
            </ul>
            <p><strong>O que isso significa para o Procedimento 2:</strong></p>
            <ul>
                <li>Seu artigo poderá ser <strong>baixado gratuitamente</strong> por qualquer pessoa</li>
                <li>Maior chance de ser <strong>compartilhado</strong> no Twitter, LinkedIn, ResearchGate</li>
                <li>Mais <strong>salvamentos</strong> no Mendeley, Zotero e outros gerenciadores</li>
                <li>Possibilidade de ser citado em <strong>políticas públicas, blogs e notícias</strong></li>
            </ul>
            <p><strong>Ação necessária:</strong> Após a publicação, compartilhe ativamente o link do artigo em suas redes profissionais. Isso alimenta diretamente o score de Altimetria que a CAPES rastreia via Crossref e Dimensions.</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="metric-card" style="border-left-color: #fc8181;">
            <h4 style="margin-top: 0; color: #c53030;">⚠ Atenção: Revistas Fechadas</h4>
            <p style="color: #742a2a;"><strong>As revistas sugeridas possuem paywall (acesso restrito).</strong></p>
            
            <p><strong>Problema para o Procedimento 2:</strong></p>
            <ul>
                <li>Poucas pessoas conseguirão ler seu artigo (apenas quem tem assinatura)</li>
                <li>Menos downloads = menos compartilhamentos = menos altimetria</li>
                <li>Risco de baixa pontuação no Proc. 2 da CAPES</li>
            </ul>
            
            <p><strong>Solução OBRIGATÓRIA:</strong></p>
            <ol>
                <li><strong>Deposite o preprint</strong> em repositório aberto ANTES ou durante a submissão:
                    <ul>
                        <li>SciELO Preprints (multidisciplinar)</li>
                        <li>arXiv (Exatas, Computação)</li>
                        <li>bioRxiv/medRxiv (Ciências da Vida e Saúde)</li>
                        <li>SSRN (Ciências Sociais)</li>
                        <li>Repositório institucional da sua universidade</li>
                    </ul>
                </li>
                <li><strong>Compartilhe o link do preprint</strong> nas redes sociais</li>
                <li><strong>Após publicação</strong>, atualize o preprint com o link da versão final (mesmo que fechada)</li>
            </ol>
            
            <p><strong>Resultado:</strong> O Crossref rastreará as menções ao preprint aberto e você ganhará altimetria mesmo publicando em revista fechada!</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Procedimento 3
    st.markdown('<div class="section-title">▸ Procedimento 3: Ciência Aberta e Avaliação Qualitativa</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="metric-card" style="border-left-color: #ed8936;">
        <h4 style="margin-top: 0; color: #ed8936;">✦ O Diferencial Qualitativo</h4>
        <p><strong>O Procedimento 3 é avaliado por pares consultores da CAPES</strong> e considera:</p>
        
        <h5>1. Relevância da Pesquisa:</h5>
        <ul>
            <li>Contribuição para o avanço do conhecimento na área</li>
            <li>Impacto social, econômico ou cultural</li>
            <li>Inovação metodológica ou teórica</li>
        </ul>
        
        <h5>2. Ciência Aberta (OPEN SCIENCE):</h5>
        <p><strong>A CAPES premia MUITO a transparência!</strong> Ações que contam pontos:</p>
        <ul>
            <li><strong>✓ Disponibilizar dados brutos</strong> da pesquisa em repositórios abertos:
                <ul>
                    <li><a href="https://zenodo.org" target="_blank">Zenodo</a> (gratuito, multidisciplinar, gera DOI)</li>
                    <li><a href="https://osf.io" target="_blank">OSF (Open Science Framework)</a> (gratuito, gerencia todo o projeto)</li>
                    <li>Repositórios institucionais da universidade</li>
                </ul>
            </li>
            <li><strong>✓ Citar o DOI dos dados</strong> no artigo publicado
                <ul><li>Exemplo: "Os dados que suportam este estudo estão disponíveis em: [DOI do Zenodo]"</li></ul>
            </li>
            <li><strong>✓ Publicar preprints</strong> (versões prévias do artigo)
                <ul><li>Demonstra transparência e acelera a disseminação do conhecimento</li></ul>
            </li>
            <li><strong>✓ Usar software livre</strong> e abrir códigos de programação
                <ul><li>GitHub, GitLab, CodeOcean</li></ul>
            </li>
        </ul>
        
        <div class="alert-info">
            <strong>💡 Dica de ouro:</strong> Pesquisadores que disponibilizam dados abertos têm até <strong>30% mais citações</strong> em média, segundo estudos. Ou seja: Ciência Aberta beneficia você (mais citações) e a CAPES (mais transparência). Ganha-ganha!
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Checklist Detalhado
    st.markdown('<div class="section-title">▸ Checklist de Ação Passo a Passo</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="alert-success">
        <h4 style="margin-top: 0;">📋 Antes da Submissão</h4>
        <ul style="margin: 0; padding-left: 1.5rem;">
            <li><strong>[ ] Vincular ORCID ao Lattes</strong>
                <ul><li>Acesse lattes.cnpq.br e vincule seu ORCID (obrigatório para rastreamento CAPES)</li></ul>
            </li>
            <li><strong>[ ] Preparar dados para repositório</strong>
                <ul><li>Organize dados brutos, códigos e metadados</li><li>Anonimize dados sensíveis (se houver)</li></ul>
            </li>
            <li><strong>[ ] Escolher repositório de dados</strong>
                <ul><li>Zenodo (recomendado para iniciantes) ou OSF</li></ul>
            </li>
        </ul>
        
        <h4 style="margin: 1rem 0 0.5rem 0;">📤 Durante a Submissão</h4>
        <ul style="margin: 0; padding-left: 1.5rem;">
            <li><strong>[ ] Depositar preprint</strong> (se a revista permitir)
                <ul><li>SciELO Preprints, arXiv, bioRxiv conforme sua área</li></ul>
            </li>
            <li><strong>[ ] Subir dados no Zenodo/OSF</strong>
                <ul><li>Obtenha o DOI dos dados</li></ul>
            </li>
            <li><strong>[ ] Incluir no manuscrito</strong>
                <ul><li>Cite o DOI dos dados: "Data available at: [DOI]"</li><li>Cite o preprint se houver</li></ul>
            </li>
        </ul>
        
        <h4 style="margin: 1rem 0 0.5rem 0;">📢 Após a Publicação (CRUCIAL!)</h4>
        <ul style="margin: 0; padding-left: 1.5rem;">
            <li><strong>[ ] Atualizar preprint</strong> com link da versão publicada</li>
            <li><strong>[ ] Divulgar nas redes sociais</strong>
                <ul>
                    <li>LinkedIn: Post profissional explicando a relevância</li>
                    <li>Twitter/X: Thread resumindo os principais achados</li>
                    <li>ResearchGate: Upload da versão autor (se permitido)</li>
                </ul>
            </li>
            <li><strong>[ ] Enviar para mailing</strong> da área e grupos de pesquisa</li>
            <li><strong>[ ] Compartilhar com a assessoria de comunicação</strong> da universidade
                <ul><li>Eles podem fazer matéria no site institucional</li></ul>
            </li>
            <li><strong>[ ] Monitorar altimetria</strong>
                <ul><li>Acesse <a href="https://www.altmetric.com" target="_blank">altmetric.com</a> e busque pelo DOI do artigo</li></ul>
            </li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if submitted:
    if not resumo.strip():
        st.markdown('<div class="alert-info">⚠️ <strong>Atenção:</strong> Insira pelo menos 3-5 palavras-chave em inglês para realizar a busca. Exemplo: "machine learning healthcare prediction"</div>', unsafe_allow_html=True)
    else:
        with st.spinner("⟳ Consultando base OpenAlex e gerando análise estratégica detalhada..."):
            query_busca = " ".join(resumo.split()[:15]) 
            revistas_encontradas = buscar_revistas_openalex(query_busca, max_results=5)
            
            if revistas_encontradas:
                st.markdown('<div class="alert-success">✓ <strong>Relatório gerado com sucesso!</strong></div>', unsafe_allow_html=True)
                gerar_relatorio_detalhado(titulo, area_capes, foco, revistas_encontradas)
                
                # Botão de download
                resumo_texto = f"""
RELATÓRIO ESTRATÉGICO CAPES 2025-2028
=====================================

Pesquisa: {titulo}
Área: {area_capes}
Estratégia: {foco}

REVISTAS SUGERIDAS:
"""
                for rev in revistas_encontradas:
                    nome = rev.get("display_name", "N/A")
                    is_oa = "Aberto" if rev.get("is_oa") else "Fechado"
                    fi = rev.get("summary_stats", {}).get("2yr_mean_citedness", 0)
                    resumo_texto += f"\n- {nome} ({is_oa}, FI: {fi:.2f})"
                
                st.download_button(
                    label="📥 Baixar Resumo do Relatório",
                    data=resumo_texto,
                    file_name=f"Relatorio_CAPES_{titulo[:30].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.markdown('<div class="alert-info">⚠️ <strong>Nenhuma revista encontrada</strong> com esses termos.<br><br><strong>Dicas:</strong><ul><li>Use palavras-chave em inglês</li><li>Use termos mais genéricos (ex: "machine learning" em vez de "deep learning neural network")</li><li>Verifique a ortografia</li></ul></div>', unsafe_allow_html=True)

# ==============================================================================
# FOOTER ANÔNIMO
# ==============================================================================
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com bases de dados abertas (OpenAlex) e alinhada às Diretrizes Comuns da CAPES (Ciclo 2025-2028).<br>
        Esta ferramenta não possui vinculação oficial com a CAPES ou MEC.
    </p>
    <p style="margin: 0; padding-top: 1rem; border-top: 1px solid #4a5568; font-size: 0.85rem; color: #a0aec0;">
        <em>Iniciativa de promoção da Ciência Aberta e Transparência na Pós-Graduação Brasileira</em>
    </p>
</div>
""", unsafe_allow_html=True)
