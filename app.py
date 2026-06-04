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
    
    /* Destaque dos campos do formulário */
    .form-field {
        background: white !important;
        border: 2px solid #667eea !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Tabela unificada */
    .tabela-container {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
    }
    
    .tabela-completa {
        width: 100%;
        border-collapse: collapse;
    }
    
    .tabela-completa thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .tabela-completa tbody td {
        padding: 0.85rem 1rem;
        border-bottom: 1px solid #e2e8f0;
        vertical-align: middle;
    }
    
    .tabela-completa tbody tr:hover {
        background: #f7fafc;
    }
    
    .tabela-completa tbody tr:nth-child(even) {
        background: #fafbfc;
    }
    
    .tabela-completa tbody tr:nth-child(even):hover {
        background: #f0f4f8;
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

with st.expander(" Clique para entender os 3 Procedimentos e Estratégias", expanded=False):
    st.markdown("""
    ### 🔍 Como Funciona a Avaliação CAPES 2025-2028
    
    A CAPES avalia os programas de pós-graduação através de **3 procedimentos complementares**:
    
    #### ** Procedimento 1: Métricas do Periódico (Qualis)**
    - **O que avalia:** A qualidade da REVISTA onde você publica
    - **Como mede:** Fator de Impacto, Quartil (Q1-Q4), Citações
    - **Base de dados:** OpenAlex (substituiu o JCR/Scopus pagos)
    - **Referências:**
      - Exatas/Saúde: Excelente >3.0 | Bom >1.5 | Aceitável >0.5
      - Humanas: Excelente >1.5 | Bom >0.5 | Aceitável >0.2
    
    #### ** Procedimento 2: Impacto Social (Altimetria)**
    - **O que avalia:** O impacto do SEU ARTIGO na sociedade
    - **Como mede:** Downloads, menções em redes sociais, compartilhamentos, citações em políticas públicas
    - **Dica crucial:** Artigos em Acesso Aberto têm MUITO mais alcance!
    
    #### **✦ Procedimento 3: Ciência Aberta e Qualitativo**
    - **O que avalia:** Relevância e transparência da pesquisa
    - **Como mede:** Análise por pares, disponibilização de dados, preprints
    - **Dica de ouro:** Depositar dados no Zenodo/OSF conta MUITOS pontos!
    
    ---
    
    ### 🎯 Os 3 Tipos de Estratégia
    
    **️ 1. Equilibrado:** Mais seguro e recomendado. Boa pontuação em todos os procedimentos.
    
    **📢 2. Impacto Social:** Prioriza Open Access e divulgação. Ideal para pesquisas com aplicação prática.
    
    **📈 3. Tradicional:** Foca em alto Fator de Impacto. Ideal para prestígio acadêmico máximo.
    """)

# ==============================================================================
# FORMULÁRIO COM NOTAS EXPLICATIVAS E DESTAQUE
# ==============================================================================
st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box alert-info">
<strong>💡 Dica geral:</strong> Preencha os campos destacados abaixo com informações da sua pesquisa. 
Quanto mais detalhado, mais precisas serão as recomendações de revistas!
</div>
""", unsafe_allow_html=True)

with st.form("dados_pesquisa", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        # Campo destacado com borda
        st.markdown('<div class="form-field">', unsafe_allow_html=True)
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema da Pesquisa",
            help=" O título ajuda a ferramenta a contextualizar a relevância temática da sua pesquisa. Isso é fundamental para o Procedimento 3 (Avaliação Qualitativa), onde os consultores da CAPES analisam a coerência e o avanço do conhecimento na área."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="input-note">
        <strong>📌 Por que isso importa?</strong> O título define o contexto temático. 
        Seja específico! Exemplo: "Machine Learning para Diagnóstico Precoce de Diabetes Tipo 2" é melhor que apenas "Machine Learning".
        </div>
        """, unsafe_allow_html=True)
        
        # Campo destacado com borda
        st.markdown('<div class="form-field">', unsafe_allow_html=True)
        area_capes = st.selectbox(
            "📚 Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"],
            help="💡 Cada área possui um Documento de Área específico que pondera de forma diferente os Procedimentos 1, 2 e 3. Exatas/Saúde valorizam mais o FI alto. Humanas valorizam mais o Proc. 3 (Qualitativo)."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="input-note">
        <strong>📌 Como isso afeta a avaliação?</strong> 
        • <strong>Exatas/Saúde:</strong> FI > 3.0 é excelente<br>
        • <strong>Humanas:</strong> FI > 1.5 já é excelente<br>
        A ferramenta adaptará as recomendações conforme sua área.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Campo destacado com borda
        st.markdown('<div class="form-field">', unsafe_allow_html=True)
        resumo = st.text_area(
            "🔑 Palavras-chave (PREFERENCIALMENTE EM INGLÊS)",
            height=140,
            placeholder="Ex: machine learning diabetes prediction healthcare genomics",
            help="💡 CRUCIAL: Use 3-8 palavras-chave em INGLÊS. A ferramenta busca na base global OpenAlex. Termos em inglês retornam MUITO mais revistas e métricas precisas. A OpenAlex é a base oficial que a CAPES usa no novo Qualis."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="input-note">
        <strong>📌 Como escolher as palavras-chave?</strong><br>
        • Use <strong>termos técnicos em inglês</strong> da sua área<br>
        • Combine: <strong>método + aplicação + área</strong><br>
        • Exemplos:<br>
          - "machine learning healthcare prediction"<br>
          - "CRISPR gene editing agriculture"<br>
          - "renewable energy sustainability"<br>
        • <strong>Não use:</strong> frases longas em português
        </div>
        """, unsafe_allow_html=True)
        
        # Campo destacado com borda
        st.markdown('<div class="form-field">', unsafe_allow_html=True)
        foco = st.selectbox(
            "🎯 Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"],
            help="💡 A escolha do foco depende dos seus objetivos de carreira e do seu programa. O Equilibrado é o mais seguro e recomendado pela CAPES. O Impacto Social prioriza Open Access. O Tradicional foca em prestígio acadêmico."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="input-note">
        <strong>📌 Qual estratégia escolher?</strong><br>
        • <strong>️ Equilibrado:</strong> Mais seguro. Bom em todos os procedimentos. Recomendado para maioria.<br>
        • <strong>📢 Impacto Social:</strong> Se sua pesquisa tem aplicação prática e você quer máximo alcance/divulgação.<br>
        • <strong>📈 Tradicional:</strong> Se busca prestígio acadêmico máximo e quer competir por posições em universidades de elite.
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
        st.markdown('<div class="alert-box alert-warning">⚠️ <strong>Atenção:</strong> Insira pelo menos 3-5 palavras-chave em inglês para realizar a busca.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("⟳ Consultando OpenAlex e gerando análise..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=6)
            
            if revistas:
                st.markdown('<div class="alert-box alert-success">✓ <strong>Relatório gerado com sucesso!</strong></div>', unsafe_allow_html=True)
                
                # Tabela Comparativa Unificada
                st.markdown('<div class="section-title"> Tabela Comparativa de Revistas</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="alert-box alert-info">
                <strong>📊 Como ler:</strong> Tabela ordenada por relevância | 🟢 OA+Alto = melhor | 🔵 OA = boa altimetria | 🔴 Fechado = deposite preprint
                </div>
                """, unsafe_allow_html=True)
                
                # Preparar dados
                melhores_oa = []
                linhas_tabela = []
                
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
                        icone_acesso = ""
                        texto_acesso = "OA"
                        altimetria = "🟢"
                    elif is_oa:
                        icone_acesso = "🔵"
                        texto_acesso = "OA"
                        altimetria = ""
                    else:
                        icone_acesso = "🔴"
                        texto_acesso = "Fech"
                        altimetria = "⚪"
                    
                    if fi > 10:
                        fi_class = "🔥"
                    elif fi > 5:
                        fi_class = "⭐"
                    elif fi > 2:
                        fi_class = "✅"
                    else:
                        fi_class = "📌"
                    
                    destaque = "🏆" if i <= 3 else ""
                    
                    linhas_tabela.append({
                        "ranking": f"{destaque}#{i}",
                        "revista": nome,
                        "acesso": f"{icone_acesso} {texto_acesso}",
                        "fi": f"{fi:.2f}",
                        "class": fi_class,
                        "citacoes": formatar_numero(citacoes),
                        "altimetria": altimetria
                    })
                
                # Tabela HTML unificada (cabeçalho + dados juntos)
                html_tabela = '''
                <div class="tabela-container">
                <table class="tabela-completa">
                    <thead>
                        <tr>
                            <th style="width: 10%;">Ranking</th>
                            <th style="width: 30%;">Revista</th>
                            <th style="width: 12%;">Acesso</th>
                            <th style="width: 10%;">FI</th>
                            <th style="width: 8%;">Class</th>
                            <th style="width: 15%;">Citações</th>
                            <th style="width: 15%;">Altimetria</th>
                        </tr>
                    </thead>
                    <tbody>
                '''
                
                for row in linhas_tabela:
                    html_tabela += f'''
                        <tr>
                            <td><strong>{row["ranking"]}</strong></td>
                            <td><strong>{row["revista"]}</strong></td>
                            <td style="text-align: center;">{row["acesso"]}</td>
                            <td style="text-align: center;"><strong>{row["fi"]}</strong></td>
                            <td style="text-align: center; font-size: 1.2rem;">{row["class"]}</td>
                            <td style="text-align: center;">{row["citacoes"]}</td>
                            <td style="text-align: center; font-size: 1.3rem;">{row["altimetria"]}</td>
                        </tr>
                    '''
                
                html_tabela += '''
                    </tbody>
                </table>
                </div>
                '''
                
                st.markdown(html_tabela, unsafe_allow_html=True)
                
                # Legenda
                st.markdown("""
                <div style="font-size: 0.85rem; color: #4a5568; margin-top: 0.5rem; padding: 0.75rem; background: white; border-radius: 8px;">
                <strong>Legenda:</strong> 🟢=OA+Alto Impacto | 🔵=OA | 🔴=Fechado | 🔥=Excelente | ⭐=Muito Bom | ✅=Bom | 📌=Aceitável | 🏆=Top 3<br>
                <strong>Altimetria:</strong> 🟢=Alto | =Médio | ⚪=Baixo
                </div>
                """, unsafe_allow_html=True)
                
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
                        
                        **Solução:** Deposite preprint em repositório aberto!
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
                        ** Impacto Moderado**
                        
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
                
                # Análise Estratégica Detalhada
                st.markdown('<div class="section-title">▸ Análise Estratégica Personalizada</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="alert-box alert-info"><strong>Área CAPES:</strong> {area_capes} | <strong>Estratégia Escolhida:</strong> {foco}</div>', unsafe_allow_html=True)
                
                if "Equilibrado" in foco:
                    st.markdown("""
                    <div class="alert-box alert-success">
                    <h4 style="margin-top: 0;">✓ Estratégia Equilibrada - A Mais Recomendada</h4>
                    <p>Você escolheu a estratégia mais segura e alinhada com as diretrizes da CAPES 2025-2028.</p>
                    <p><strong>O que isso significa na prática:</strong></p>
                    <ul>
                        <li>Você busca revistas com <strong>bom Fator de Impacto</strong> (Proc. 1)</li>
                        <li>Prioriza <strong>Acesso Aberto</strong> quando possível (Proc. 2)</li>
                        <li>Valoriza <strong>Ciência Aberta</strong> e transparência (Proc. 3)</li>
                    </ul>
                    <p><strong>Recomendação:</strong> Na tabela acima, priorize as revistas marcadas com <strong>🟢 OA</strong> que tenham Fator de Impacto acima de 1.0. Elas oferecem o melhor equilíbrio entre os 3 procedimentos.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif "Impacto Social" in foco:
                    if melhores_oa:
                        st.markdown(f"""
                        <div class="alert-box alert-success">
                        <h4 style="margin-top: 0;">📢 Estratégia de Máximo Impacto Social</h4>
                        <p>Você prioriza o <strong>Procedimento 2 (Altimetria)</strong> da CAPES.</p>
                        <p><strong>Revistas Open Access encontradas (priorize estas):</strong></p>
                        <ul>
                        {"".join([f"<li><strong>{r}</strong></li>" for r in melhores_oa])}
                        </ul>
                        <p><strong>Ação OBRIGATÓRIA pós-publicação:</strong></p>
                        <ul>
                            <li>Compartilhe ativamente no LinkedIn, Twitter/X, ResearchGate</li>
                            <li>Envie para mailing lists da área</li>
                            <li>Escreva posts explicando a pesquisa em linguagem acessível</li>
                        </ul>
                        <p><strong>Por que isso importa?</strong> Cada compartilhamento, download e menção alimenta o score de Altimetria que a CAPES rastreia via Crossref e Dimensions!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="alert-box alert-warning">
                        <h4 style="margin-top: 0;">⚠ Atenção: Nenhuma Open Access Encontrada</h4>
                        <p>Para estratégia de máximo impacto social, você PRECISA de acesso aberto.</p>
                        <p><strong>Solução OBRIGATÓRIA:</strong></p>
                        <ol>
                            <li><strong>Deposite o preprint</strong> em repositório aberto ANTES ou durante a submissão:
                                <ul>
                                    <li>SciELO Preprints (multidisciplinar)</li>
                                    <li>arXiv (Exatas, Computação)</li>
                                    <li>bioRxiv/medRxiv (Ciências da Vida)</li>
                                    <li>SSRN (Ciências Sociais)</li>
                                </ul>
                            </li>
                            <li><strong>Compartilhe o link do preprint</strong> nas redes sociais</li>
                            <li><strong>Após publicação</strong>, atualize o preprint com o link da versão final</li>
                        </ol>
                        <p><strong>Resultado:</strong> O Crossref rastreará as menções ao preprint aberto e você ganhará altimetria mesmo publicando em revista fechada!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                else:
                    st.markdown("""
                    <div class="alert-box alert-success">
                    <h4 style="margin-top: 0;"> Estratégia de Máximo Impacto Tradicional</h4>
                    <p>Você prioriza o <strong>Procedimento 1 (Fator de Impacto)</strong> da CAPES.</p>
                    <p><strong>O que isso significa:</strong></p>
                    <ul>
                        <li>Foco em revistas de <strong>alto prestígio</strong> e FI elevado</li>
                        <li>Busca maximizar pontuação no Qualis/CAPES tradicional</li>
                        <li>Ideal para carreiras acadêmicas de elite</li>
                    </ul>
                    <p><strong>Recomendação:</strong> Na tabela acima, priorize revistas com FI acima de 3.0 (Exatas/Saúde) ou 1.0 (Humanas).</p>
                    <p><strong>Compensação necessária:</strong> Revistas de alto impacto geralmente são fechadas (🔴). Para não perder pontos no Proc. 2 (Altimetria), você DEVE:</p>
                    <ol>
                        <li>Depositar o <strong>preprint</strong> no arXiv, bioRxiv ou SciELO Preprints</li>
                        <li>Compartilhar o link do preprint nas redes sociais</li>
                        <li>Divulgar ativamente mesmo com paywall</li>
                    </ol>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Procedimentos Detalhados
                st.markdown('<div class="section-title">▸ Guia Detalhado dos 3 Procedimentos CAPES</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;"> Procedimento 1</h4>
                    <p><strong>Métricas do Periódico</strong></p>
                    <p><strong>O que a CAPES avalia:</strong> A qualidade da revista onde você publica, usando a OpenAlex como base oficial (substituindo o JCR/Scopus pagos).</p>
                    <p><strong>Referências por Área:</strong></p>
                    <p><strong>Exatas e Saúde:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li>Excelente: FI > 3.0</li>
                        <li>Bom: FI entre 1.5 e 3.0</li>
                        <li>Aceitável: FI entre 0.5 e 1.5</li>
                    </ul>
                    <p style="margin-top: 0.5rem;"><strong>Humanas:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li>Excelente: FI > 1.5</li>
                        <li>Bom: FI entre 0.5 e 1.5</li>
                        <li>Aceitável: FI entre 0.2 e 0.5</li>
                    </ul>
                    <p style="margin-top: 0.5rem;"><strong>Dica:</strong> Além do FI, a CAPES considera o Quartil (Q1, Q2, Q3, Q4). Q1 e Q2 têm maior pontuação.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if melhores_oa:
                        st.markdown("""
                        <div class="alert-box alert-success">
                        <h4 style="margin-top: 0;">📢 Procedimento 2</h4>
                        <p><strong>Impacto Social (Altimetria)</strong></p>
                        <p style="color: #22543d;"><strong>✓ Vantagem:</strong> Você tem revistas Open Access na tabela!</p>
                        <p><strong>O que a CAPES avalia:</strong> O impacto do SEU ARTIGO na sociedade, medido por downloads, menções em redes sociais, compartilhamentos e citações em políticas públicas.</p>
                        <p><strong>Benefícios do Open Access:</strong></p>
                        <ul style="padding-left: 1rem; margin: 0;">
                            <li>Artigo gratuito para todos</li>
                            <li>Mais downloads e visualizações</li>
                            <li>Mais compartilhamentos no Twitter, LinkedIn</li>
                            <li>Mais salvamentos no Mendeley, Zotero</li>
                            <li>Possibilidade de ser citado em políticas públicas</li>
                        </ul>
                        <p style="margin-top: 0.5rem;"><strong>Ação necessária:</strong> Após a publicação, compartilhe ativamente o link do artigo em suas redes profissionais. Isso alimenta diretamente o score de Altimetria!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="alert-box alert-warning">
                        <h4 style="margin-top: 0;"> Procedimento 2</h4>
                        <p><strong>Impacto Social (Altimetria)</strong></p>
                        <p style="color: #742a2a;"><strong> Atenção:</strong> Todas as revistas sugeridas possuem paywall (acesso restrito).</p>
                        <p><strong>Problema:</strong></p>
                        <ul style="padding-left: 1rem; margin: 0;">
                            <li>Poucas pessoas conseguirão ler seu artigo</li>
                            <li>Menos downloads = menos compartilhamentos = menos altimetria</li>
                            <li>Risco de baixa pontuação no Proc. 2</li>
                        </ul>
                        <p style="margin-top: 0.5rem;"><strong>Solução OBRIGATÓRIA:</strong></p>
                        <ol style="padding-left: 1rem; margin: 0;">
                            <li>Deposite o preprint em repositório aberto</li>
                            <li>Compartilhe o link do preprint</li>
                            <li>Use redes sociais ativamente</li>
                        </ol>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;">✦ Procedimento 3</h4>
                    <p><strong>Ciência Aberta e Qualitativo</strong></p>
                    <p><strong>O que a CAPES avalia:</strong> A relevância e transparência da pesquisa, analisada por pares consultores.</p>
                    <p><strong>Ações que contam MUITOS pontos:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li><strong>Disponibilizar dados brutos</strong> em repositórios abertos:
                            <ul>
                                <li><a href="https://zenodo.org" target="_blank">Zenodo</a> (gratuito, gera DOI)</li>
                                <li><a href="https://osf.io" target="_blank">OSF</a> (gratuito)</li>
                            </ul>
                        </li>
                        <li><strong>Citar o DOI dos dados</strong> no artigo publicado</li>
                        <li><strong>Publicar preprints</strong> (versões prévias)</li>
                        <li><strong>Usar software livre</strong> e abrir códigos (GitHub)</li>
                    </ul>
                    <p style="margin-top: 0.5rem;"><strong>💡 Dica de ouro:</strong> Pesquisadores que disponibilizam dados abertos têm até <strong>30% mais citações</strong> em média!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Checklist Detalhado
                st.markdown('<div class="section-title">▸ Checklist de Ação Passo a Passo</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="alert-box alert-success">
                <h4 style="margin-top: 0;">📋 Antes da Submissão</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>Vincular ORCID ao Lattes</strong> - A CAPES cruza dados via ORCID para validar autoria e impacto. É obrigatório!</li>
                    <li><strong>Preparar dados para repositório</strong> - Organize dados brutos, códigos e metadados. Anonimize dados sensíveis se houver.</li>
                    <li><strong>Escolher repositório</strong> - Zenodo (recomendado para iniciantes) ou OSF.</li>
                </ul>
                
                <h4 style="margin: 1rem 0 0.5rem 0;">📤 Durante a Submissão</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>Depositar preprint</strong> (se a revista permitir) - SciELO Preprints, arXiv, bioRxiv conforme sua área.</li>
                    <li><strong>Subir dados no Zenodo/OSF</strong> - Obtenha o DOI dos dados.</li>
                    <li><strong>Incluir no manuscrito</strong> - Cite o DOI dos dados: "Data available at: [DOI]"</li>
                </ul>
                
                <h4 style="margin: 1rem 0 0.5rem 0;">📢 Após a Publicação (CRUCIAL!)</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>Atualizar preprint</strong> com link da versão publicada</li>
                    <li><strong>Divulgar nas redes sociais</strong>:
                        <ul>
                            <li>LinkedIn: Post profissional explicando a relevância</li>
                            <li>Twitter/X: Thread resumindo os principais achados</li>
                            <li>ResearchGate: Upload da versão autor (se permitido)</li>
                        </ul>
                    </li>
                    <li><strong>Enviar para mailing</strong> da área e grupos de pesquisa</li>
                    <li><strong>Compartilhar com assessoria de comunicação</strong> da universidade</li>
                    <li><strong>Monitorar altimetria</strong> em <a href="https://www.altmetric.com" target="_blank">altmetric.com</a></li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="alert-box alert-warning">
                <h4 style="margin-top: 0;">⚠️ Nenhuma revista encontrada</h4>
                <p><strong>Dicas para melhorar a busca:</strong></p>
                <ul>
                    <li>Use <strong>palavras-chave em inglês</strong> (a OpenAlex é uma base global)</li>
                    <li>Use <strong>termos mais genéricos</strong> (ex: "machine learning" em vez de "deep learning neural network transformer")</li>
                    <li>Use <strong>3-8 palavras-chave</strong> separadas por espaço</li>
                    <li>Verifique a <strong>ortografia</strong> dos termos</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com bases de dados abertas (OpenAlex) e alinhada às Diretrizes Comuns da CAPES (Ciclo 2025-2028).<br>
        Esta ferramenta não possui vinculação oficial com a CAPES ou MEC.
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Iniciativa de promoção da Ciência Aberta e Transparência na Pós-Graduação Brasileira</em>
    </p>
</div>
""", unsafe_allow_html=True)
