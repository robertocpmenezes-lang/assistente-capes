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

# CSS com Background Premium e Grid Comparativo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Background Gradiente Suave e Profissional */
    .stApp {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Container Principal com Fundo Branco Suave */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem auto;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }
    
    /* Header com Gradiente */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        color: #4a5568;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Seções */
    .section-title {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        -webkit-background-clip: text;
        -webkit-text-fill-color: #2d3748;
        background-clip: text;
    }
    
    /* Grid Comparativo Premium */
    .comparison-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .journal-card-compact {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .journal-card-compact::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .journal-card-compact.oa-high::before {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    }
    
    .journal-card-compact.oa-medium::before {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
    }
    
    .journal-card-compact.closed::before {
        background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
    }
    
    .journal-card-compact:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .journal-rank {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .journal-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0 0 1rem 0;
        padding-right: 2.5rem;
        line-height: 1.3;
    }
    
    .badges-row {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .badge {
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .badge-yes { background: #c6f6d5; color: #22543d; }
    .badge-no { background: #fed7d7; color: #742a2a; }
    .badge-high { background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%); color: white; }
    .badge-medium { background: #90cdf4; color: #2a4365; }
    .badge-low { background: #e2e8f0; color: #718096; }
    
    .metrics-comparison {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-top: 1rem;
    }
    
    .metric-compare {
        background: #f7fafc;
        padding: 0.75rem 0.5rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .metric-compare-label {
        font-size: 0.7rem;
        color: #718096;
        font-weight: 600;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
    }
    
    .metric-compare-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    /* Formulário com Background */
    .form-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .input-help {
        font-size: 0.85rem;
        color: #4a5568;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background: rgba(255,255,255,0.7);
        border-radius: 6px;
        border-left: 3px solid #667eea;
    }
    
    /* Alertas */
    .alert-box {
        padding: 1.25rem;
        border-radius: 10px;
        margin: 1.5rem 0;
    }
    
    .alert-info { 
        background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%); 
        border-left: 4px solid #4299e1; 
    }
    .alert-success { 
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%); 
        border-left: 4px solid #48bb78; 
    }
    .alert-warning { 
        background: linear-gradient(135deg, #fffaf0 0%, #feebc8 100%); 
        border-left: 4px solid #ed8936; 
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding: 2.5rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: #e2e8f0;
        border-radius: 15px;
        text-align: center;
    }
    
    /* Botão */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.05rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">✦ Assistente de Estratégia de Publicação</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ciclo de Avaliação CAPES 2025-2028 | Baseado em Ciência Aberta</p>', unsafe_allow_html=True)

# ==============================================================================
# SEÇÃO EDUCACIONAL
# ==============================================================================
st.markdown('<div class="section-title">▸ Entenda a Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique para entender os 3 Procedimentos e Estratégias", expanded=False):
    st.markdown("""
    ### 🔍 Como Funciona a Avaliação CAPES 2025-2028
    
    **📊 Procedimento 1:** Métricas do Periódico (Fator de Impacto, Quartil)  
    **📢 Procedimento 2:** Impacto Social (Altimetria, downloads, menções)  
    **✦ Procedimento 3:** Ciência Aberta e Avaliação Qualitativa
    
    ### 🎯 Estratégias:
    - **⚖️ Equilibrado:** Mais seguro - bom em todos os procedimentos
    - **📢 Impacto Social:** Prioriza Open Access e divulgação
    - **📈 Tradicional:** Foca em alto Fator de Impacto
    """)

# ==============================================================================
# FORMULÁRIO COM EXPLICAÇÕES DETALHADAS
# ==============================================================================
st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box alert-info">
<strong>💡 Dica:</strong> Preencha os campos abaixo com informações da sua pesquisa. 
Quanto mais detalhado, mais precisas serão as recomendações de revistas!
</div>
""", unsafe_allow_html=True)

with st.form("dados_pesquisa", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema da Pesquisa",
            help="💡 **Por que isso importa?** O título ajuda a entender o contexto e a relevância da pesquisa para o Procedimento 3 (Avaliação Qualitativa). Seja específico!"
        )
        st.markdown('<div class="input-help"><strong>Exemplo:</strong> "Machine Learning para Diagnóstico Precoce de Diabetes Tipo 2"</div>', unsafe_allow_html=True)
        
        area_capes = st.selectbox(
            "📚 Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"],
            help="💡 **Importante:** Cada área tem critérios diferentes. Exatas/Saúde valorizam mais FI alto. Humanas valorizam mais o Proc. 3 (Qualitativo)."
        )
        st.markdown('<div class="input-help">Selecione a área que melhor representa sua pesquisa</div>', unsafe_allow_html=True)

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (PREFERENCIALMENTE EM INGLÊS)",
            height=140,
            placeholder="Ex: machine learning diabetes prediction healthcare genomics",
            help="💡 **CRUCIAL:** Use 3-8 palavras-chave em INGLÊS. A ferramenta busca na base global OpenAlex. Termos em inglês retornam MUITO mais revistas e métricas precisas!"
        )
        st.markdown("""
        <div class="input-help">
        <strong>Como escolher:</strong><br>
        • Use termos técnicos da sua área<br>
        • Combine: método + aplicação + área<br>
        • Ex: "machine learning healthcare prediction" ou "CRISPR gene editing agriculture"
        </div>
        """, unsafe_allow_html=True)
        
        foco = st.selectbox(
            "🎯 Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"],
            help="💡 **Qual escolher?**<br>• **Equilibrado:** Mais seguro, recomendado para maioria<br>• **Impacto Social:** Se quer máximo alcance/divulgação<br>• **Tradicional:** Se busca prestígio acadêmico máximo"
        )
        st.markdown('<div class="input-help">Escolha baseado no seu objetivo de carreira</div>', unsafe_allow_html=True)
    
    submitted = st.form_submit_button("🚀 Gerar Relatório Completo com Grade Comparativa", use_container_width=True)

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
        with st.spinner("⟳ Consultando OpenAlex e gerando análise comparativa..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=6)
            
            if revistas:
                st.markdown('<div class="alert-box alert-success">✓ <strong>Relatório gerado com sucesso! Compare as revistas na grade abaixo.</strong></div>', unsafe_allow_html=True)
                
                # Grade Comparativa Visual
                st.markdown('<div class="section-title">✦ Grade Comparativa de Revistas</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="alert-box alert-info">
                <strong>📊 Como usar esta grade comparativa:</strong><br>
                • Cada card representa uma revista sugerida<br>
                • 🟢 <strong>Card Verde:</strong> Open Access + Alto Impacto (melhor opção!)<br>
                • 🔵 <strong>Card Azul:</strong> Open Access (boa para altimetria)<br>
                • 🔴 <strong>Card Vermelho:</strong> Fechado/Paywall (alto FI tradicional)<br>
                • Compare lado a lado: FI, citações e potencial de altimetria
                </div>
                """, unsafe_allow_html=True)
                
                # Preparar dados
                melhores_oa = []
                html_grid = '<div class="comparison-grid">'
                
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
                    
                    # Badges
                    acesso_badge = '<span class="badge badge-yes">✓ Open Access</span>' if is_oa else '<span class="badge badge-no">✕ Fechado</span>'
                    
                    # Cor do FI
                    if fi > 5:
                        fi_color = "#dd6b20"
                        fi_class = "high"
                    elif fi > 2:
                        fi_color = "#4299e1"
                        fi_class = "medium"
                    else:
                        fi_color = "#4a5568"
                        fi_class = "low"
                    
                    # Destaque top
                    rank_badge = f'<div class="journal-rank">#{i}</div>' if i <= 3 else ''
                    
                    html_grid += f'''
                    <div class="journal-card-compact {card_class}">
                        {rank_badge}
                        <h3 class="journal-name">{nome}</h3>
                        <div class="badges-row">
                            {acesso_badge}
                            {alt_badge}
                        </div>
                        <div class="metrics-comparison">
                            <div class="metric-compare">
                                <div class="metric-compare-label">Fator de Impacto</div>
                                <div class="metric-compare-value" style="color: {fi_color};">{fi:.2f}</div>
                            </div>
                            <div class="metric-compare">
                                <div class="metric-compare-label">Citações</div>
                                <div class="metric-compare-value">{formatar_numero(citacoes)}</div>
                            </div>
                            <div class="metric-compare">
                                <div class="metric-compare-label">Ranking</div>
                                <div class="metric-compare-value">#{i}</div>
                            </div>
                        </div>
                    </div>
                    '''
                
                html_grid += '</div>'
                st.markdown(html_grid, unsafe_allow_html=True)
                
                # Análise Estratégica
                st.markdown('<div class="section-title">▸ Análise Estratégica</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="alert-box alert-info"><strong>Área:</strong> {area_capes} | <strong>Estratégia:</strong> {foco}</div>', unsafe_allow_html=True)
                
                if "Equilibrado" in foco:
                    st.markdown("""
                    <div class="alert-box alert-success">
                    <h4 style="margin-top: 0;">✓ Estratégia Equilibrada Recomendada</h4>
                    <p>Você escolheu a estratégia mais segura e alinhada com a CAPES 2025-2028.</p>
                    <p><strong>Recomendação:</strong> Na grade acima, priorize os cards <strong>verdes</strong> (Open Access + Alto Impacto). Eles oferecem o melhor equilíbrio entre Fator de Impacto (Proc. 1) e potencial de Altimetria (Proc. 2).</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif "Impacto Social" in foco:
                    if melhores_oa:
                        st.markdown(f"""
                        <div class="alert-box alert-success">
                        <h4 style="margin-top: 0;">📢 Foco em Impacto Social</h4>
                        <p><strong>Revistas Open Access encontradas (priorize estas):</strong></p>
                        <ul>
                        {"".join([f"<li><strong>{r}</strong></li>" for r in melhores_oa])}
                        </ul>
                        <p><strong>Ação pós-publicação:</strong> Compartilhe ativamente no LinkedIn, Twitter/X, ResearchGate e mailing lists da área. Isso alimenta diretamente o score de Altimetria!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="alert-box alert-warning">
                        <h4 style="margin-top: 0;">⚠ Atenção: Nenhuma Open Access</h4>
                        <p><strong>Solução OBRIGATÓRIA:</strong> Deposite o preprint em SciELO Preprints, arXiv ou bioRxiv ANTES ou durante a submissão. Isso garante altimetria mesmo com revista fechada!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                else:
                    st.markdown("""
                    <div class="alert-box alert-success">
                    <h4 style="margin-top: 0;">📈 Foco Tradicional</h4>
                    <p><strong>Recomendação:</strong> Priorize revistas com FI > 3.0 (Exatas/Saúde) ou > 1.0 (Humanas). Na grade, observe os cards com FI mais alto.</p>
                    <p><strong>Importante:</strong> Revistas de alto impacto geralmente são fechadas. Deposite o preprint em repositório aberto para compensar no Proc. 2!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Procedimentos
                st.markdown('<div class="section-title">▸ Guia dos Procedimentos CAPES</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;">📊 Proc. 1</h4>
                    <p><strong>Métricas do Periódico</strong></p>
                    <p>A CAPES usa OpenAlex como base oficial.</p>
                    <p><strong>Referências Exatas/Saúde:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li>Excelente: FI > 3.0</li>
                        <li>Bom: FI 1.5-3.0</li>
                        <li>Aceitável: FI 0.5-1.5</li>
                    </ul>
                    <p><strong>Referências Humanas:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li>Excelente: FI > 1.5</li>
                        <li>Bom: FI 0.5-1.5</li>
                        <li>Aceitável: FI 0.2-0.5</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if melhores_oa:
                        st.markdown("""
                        <div class="alert-box alert-success">
                        <h4 style="margin-top: 0;">📢 Proc. 2</h4>
                        <p><strong>Impacto Social</strong></p>
                        <p style="color: #22543d;"><strong>✓ Vantagem:</strong> Tem Open Access!</p>
                        <p><strong>Benefícios:</strong></p>
                        <ul style="padding-left: 1rem; margin: 0;">
                            <li>Artigo gratuito</li>
                            <li>Mais downloads</li>
                            <li>Mais compartilhamentos</li>
                            <li>Mais menções</li>
                        </ul>
                        <p style="margin-top: 0.5rem;"><strong>Ação:</strong> Divulgue ativamente!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="alert-box alert-warning">
                        <h4 style="margin-top: 0;">📢 Proc. 2</h4>
                        <p><strong>Impacto Social</strong></p>
                        <p style="color: #742a2a;"><strong>⚠ Fechadas</strong></p>
                        <p><strong>Solução:</strong></p>
                        <ol style="padding-left: 1rem; margin: 0;">
                            <li>Deposite preprint</li>
                            <li>Compartilhe link</li>
                            <li>Use redes sociais</li>
                        </ol>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;">✦ Proc. 3</h4>
                    <p><strong>Ciência Aberta</strong></p>
                    <p>A CAPES premia a transparência!</p>
                    <p><strong>Ações:</strong></p>
                    <ul style="padding-left: 1rem; margin: 0;">
                        <li>Dados no <a href="https://zenodo.org" target="_blank">Zenodo</a></li>
                        <li>Citar DOI dos dados</li>
                        <li>Preprints</li>
                        <li>Código aberto</li>
                    </ul>
                    <p style="margin-top: 0.5rem;"><strong>💡 Dica:</strong> Dados abertos = 30% mais citações!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Checklist
                st.markdown('<div class="section-title">▸ Checklist</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="alert-box alert-success">
                <strong>📋 Antes:</strong> [ ] ORCID vinculado | [ ] Dados organizados<br>
                <strong>📤 Durante:</strong> [ ] Preprint depositado | [ ] DOI no artigo<br>
                <strong>📢 Após:</strong> [ ] Divulgar | [ ] Monitorar altimetria
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="alert-box alert-warning">
                <h4 style="margin-top: 0;">⚠️ Nenhuma revista encontrada</h4>
                <p><strong>Dicas:</strong></p>
                <ul>
                    <li>Use palavras-chave em inglês</li>
                    <li>Use termos mais genéricos</li>
                    <li>Ex: "machine learning" em vez de "deep learning neural network"</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com OpenAlex e alinhada à CAPES 2025-2028.<br>
        Sem vínculo oficial com CAPES/MEC.
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Promovendo Ciência Aberta e Transparência</em>
    </p>
</div>
""", unsafe_allow_html=True)
