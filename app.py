import streamlit as st
import requests
import urllib.parse

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILO PREMIUM
# ==============================================================================
st.set_page_config(
    page_title="Assistente CAPES 2025-2028 | Estratégia de Publicação", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Premium com design moderno e profissional
st.markdown("""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Fundo gradiente sutil */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal estilizado */
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
    
    /* Cards modernos */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    /* Tabela premium */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Seções com ícones */
    .section-title {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Badges personalizados */
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
    
    /* Footer profissional */
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: #e2e8f0;
        border-radius: 12px;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .footer strong {
        color: #90cdf4;
    }
    
    /* Botão premium */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Alertas estilizados */
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
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<p class="main-header">✦ Assistente de Estratégia de Publicação</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ciclo de Avaliação CAPES 2025-2028 | Baseado em Ciência Aberta e Dados Reais</p>', unsafe_allow_html=True)

# ==============================================================================
# 1. FORMULÁRIO PREMIUM
# ==============================================================================
with st.form("dados_pesquisa", clear_on_submit=False):
    st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema da Pesquisa",
            help="💡 O título contextualiza a relevância temática para o Procedimento 3 (Avaliação Qualitativa)."
        )
        
        area_capes = st.selectbox(
            "📚 Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"],
            help="💡 Cada área pondera diferentemente os Procedimentos 1, 2 e 3."
        )

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (preferencialmente em inglês)",
            height=130,
            placeholder="Ex: machine learning healthcare prediction genomics",
            help="💡 Use termos em inglês para buscar em bases globais (OpenAlex)."
        )
        
        foco = st.selectbox(
            "🎯 Foco da Estratégia",
            [
                "⚖️ Equilibrado (Impacto + Ciência Aberta)", 
                "📢 Máximo Impacto Social (Altimetria / Proc. 2)", 
                "📈 Máximo Tradicional (Fator de Impacto / Proc. 1)"
            ],
            help="💡 Proc. 1 = Revista | Proc. 2 = Artigo | Proc. 3 = Ciência Aberta"
        )
    
    submitted = st.form_submit_button("🚀 Gerar Relatório Estratégico Completo", use_container_width=True)

# ==============================================================================
# 2. MOTOR DE BUSCA (OpenAlex API)
# ==============================================================================
def buscar_revistas_openalex(query, max_results=5):
    """Busca revistas na OpenAlex por assunto/tema"""
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
        
        if revistas_encontradas:
            return revistas_encontradas
            
    except Exception as e:
        print(f"Erro na busca: {e}")
    
    fallback_url = f"https://api.openalex.org/sources?per-page={max_results}"
    try:
        response = requests.get(fallback_url, timeout=15)
        return response.json().get("results", [])
    except:
        return []

# ==============================================================================
# 3. MOTOR DE RELATÓRIO PREMIUM
# ==============================================================================
def gerar_relatorio_capes(titulo, area, foco, revistas):
    if not revistas:
        return """
        <div class="alert-info">
            <strong>⚠️ Nenhuma revista encontrada</strong><br>
            Tente usar palavras-chave em inglês ou termos mais amplos da sua área 
            (ex: 'education', 'sustainability', 'neuroscience').
        </div>
        """

    html = '<div class="section-title">✦ Revistas Sugeridas (Métricas Reais)</div>'
    html += '<table style="width:100%; border-collapse: collapse; margin: 1rem 0;">'
    html += '''<thead>
        <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <th style="padding: 1rem; text-align: left; border-radius: 8px 0 0 0;">Revista</th>
            <th style="padding: 1rem; text-align: center;">Acesso</th>
            <th style="padding: 1rem; text-align: center;">Fator de Impacto</th>
            <th style="padding: 1rem; text-align: center; border-radius: 0 8px 0 0;">Potencial Altimetria</th>
        </tr>
    </thead>
    <tbody>'''
    
    melhores_opcoes_oa = []
    
    for rev in revistas:
        nome = rev.get("display_name", "Nome não disponível")
        is_oa = rev.get("is_oa", False)
        
        # Badge de Acesso
        if is_oa:
            acesso_badge = '<span class="badge-oa-yes">✓ Aberto</span>'
            melhores_opcoes_oa.append(nome)
        else:
            acesso_badge = '<span class="badge-oa-no">✕ Fechado</span>'
        
        # Fator de Impacto
        summary_stats = rev.get("summary_stats", {})
        fator_impacto = summary_stats.get("2yr_mean_citedness", 0)
        fi_formatado = f"{fator_impacto:.2f}" if fator_impacto else "N/A"
        
        # Potencial de Altimetria
        citacoes = rev.get("cited_by_count", 0)
        
        if is_oa and citacoes > 5000:
            potencial_badge = '<span class="badge-high">🔥 Alto</span>'
        elif is_oa:
            potencial_badge = '<span class="badge-medium">● Médio</span>'
        else:
            potencial_badge = '<span class="badge-low">○ Baixo</span>'
        
        html += f'''<tr style="background: white; border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 1rem; font-weight: 600; color: #2d3748;">{nome}</td>
            <td style="padding: 1rem; text-align: center;">{acesso_badge}</td>
            <td style="padding: 1rem; text-align: center; font-family: monospace; color: #667eea; font-weight: 600;">{fi_formatado}</td>
            <td style="padding: 1rem; text-align: center;">{potencial_badge}</td>
        </tr>'''
    
    html += '</tbody></table>'
    
    # Seção de Estratégia
    html += '<div class="section-title">▸ Estratégia CAPES 2025-2028</div>'
    html += f'<div class="alert-info"><strong>Área:</strong> {area} | <strong>Estratégia:</strong> {foco}</div>'
    
    html += '''
    <div class="metric-card">
        <h4 style="margin-top: 0; color: #667eea;">📊 Procedimento 1: Métricas do Periódico</h4>
        <p>A CAPES utiliza a OpenAlex como base oficial. O Fator de Impacto exibido é o dado que os consultores verão.</p>
        <ul>
            <li><strong>Ciências Exatas/Saúde:</strong> Busque valores > 1.5</li>
            <li><strong>Ciências Humanas:</strong> Valores > 0.5 já são considerados bons</li>
        </ul>
    </div>
    
    <div class="metric-card" style="border-left-color: #48bb78;">
        <h4 style="margin-top: 0; color: #48bb78;">📢 Procedimento 2: Impacto Social (Altimetria)</h4>
    '''
    
    if melhores_opcoes_oa:
        html += f'<p><strong style="color: #22543d;">✓ Vantagem:</strong> Revistas com Acesso Aberto permitem que seu artigo seja baixado, compartilhado e citado sem barreiras. Isso gera pontuação extra no Procedimento 2.</p>'
    else:
        html += '<p><strong style="color: #742a2a;">⚠ Atenção:</strong> Revistas fechadas exigem depósito em repositórios (SciELO Preprints, arXiv) para garantir visibilidade e altimetria.</p>'
    
    html += '''
    </div>
    
    <div class="metric-card" style="border-left-color: #ed8936;">
        <h4 style="margin-top: 0; color: #ed8936;">✦ Procedimento 3: Ciência Aberta e Qualitativo</h4>
        <p>Disponibilizar dados brutos em repositórios abertos (Zenodo, OSF) e citá-los no artigo é um diferencial qualitativo enorme na avaliação por pares.</p>
    </div>
    
    <div class="section-title">▸ Checklist de Ação</div>
    <div class="alert-success">
        <ul style="margin: 0; padding-left: 1.5rem;">
            <li><strong>Vincular ORCID</strong> ao Lattes (obrigatório para rastreamento)</li>
            <li><strong>Divulgar ativamente</strong> após publicação (LinkedIn, Twitter/X, ResearchGate)</li>
            <li><strong>Depositar dados</strong> no Zenodo ou OSF e citar o DOI no artigo</li>
            <li><strong>Compartilhar preprint</strong> em repositório institucional se a revista for fechada</li>
        </ul>
    </div>
    '''
    
    return html

# ==============================================================================
# 4. EXECUÇÃO
# ==============================================================================
if submitted:
    if not resumo.strip():
        st.markdown('<div class="alert-info">⚠️ <strong>Atenção:</strong> Insira pelo menos palavras-chave para realizar a busca.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("⟳ Consultando bases OpenAlex e gerando análise estratégica..."):
            query_busca = " ".join(resumo.split()[:15]) 
            revistas_encontradas = buscar_revistas_openalex(query_busca, max_results=5)
            
            if revistas_encontradas:
                st.markdown('<div class="alert-success">✓ <strong>Relatório gerado com sucesso!</strong></div>', unsafe_allow_html=True)
                relatorio_html = gerar_relatorio_capes(titulo, area_capes, foco, revistas_encontradas)
                st.markdown(relatorio_html, unsafe_allow_html=True)
                
                # Botão de download estilizado
                st.download_button(
                    label="📥 Baixar Relatório em PDF",
                    data=relatorio_html,
                    file_name=f"Relatorio_CAPES_{titulo[:30].replace(' ', '_')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            else:
                st.markdown('<div class="alert-info">⚠️ Nenhuma revista encontrada. Tente termos em inglês mais genéricos.</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. FOOTER PREMIUM
# ==============================================================================
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com bases de dados abertas (OpenAlex) e alinhada às Diretrizes Comuns da CAPES (Ciclo 2025-2028).<br>
        Esta ferramenta não possui vinculação oficial com a CAPES ou MEC.
    </p>
    <p style="margin: 0; padding-top: 1rem; border-top: 1px solid #4a5568;">
        <strong>Desenvolvimento e Arquitetura:</strong> Roberto Cesar<br>
        <em style="font-size: 0.85rem; color: #a0aec0;">Promovendo Ciência Aberta e Transparência na Pós-Graduação Brasileira</em>
    </p>
</div>
""", unsafe_allow_html=True)
