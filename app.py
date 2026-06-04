import streamlit as st
import requests
import urllib.parse
import pandas as pd
from datetime import datetime

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #4a5568;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .section-title {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 700;
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
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
    
    /* Destaque dos campos de input */
    div[data-testid="stTextInput"] > div > input,
    div[data-testid="stTextArea"] > div > textarea,
    div[data-testid="stSelectbox"] > div > div {
        border: 2px solid #667eea !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15) !important;
        border-radius: 8px !important;
    }
    
    div[data-testid="stTextInput"] > div > input:focus,
    div[data-testid="stTextArea"] > div > textarea:focus,
    div[data-testid="stSelectbox"] > div > div:focus-within {
        border: 2px solid #764ba2 !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        background-color: #f7fafc !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Assistente de Estratégia de Publicação</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ciclo de Avaliação CAPES 2025-2028 | Ciência Aberta e Dados Reais</p>', unsafe_allow_html=True)

# ==============================================================================
# SEÇÃO EDUCACIONAL
# ==============================================================================
st.markdown('<div class="section-title">Entenda a Avaliação CAPES</div>', unsafe_allow_html=True)

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
# FORMULÁRIO COM EXPLICAÇÕES DETALHADAS
# ==============================================================================
st.markdown('<div class="section-title">Dados da Produção Intelectual</div>', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box alert-info">
<strong>💡 Dica geral:</strong> Preencha os campos destacados abaixo com informações da sua pesquisa. 
Quanto mais detalhado, mais precisas serão as recomendações de revistas!
</div>
""", unsafe_allow_html=True)

with st.form("dados_pesquisa", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema da Pesquisa",
            help="""
            💡 **Por que isso importa para a CAPES?**
            
            O título ajuda a ferramenta a contextualizar a relevância temática da sua pesquisa. 
            Isso é fundamental para o **Procedimento 3 (Avaliação Qualitativa)**, onde os consultores 
            da CAPES analisam a coerência e o avanço do conhecimento na área.
            
            **Como preencher:**
            • Seja específico e descritivo
            • Inclua método, aplicação e área
            • Evite títulos genéricos
            
            **Exemplo bom:** "Machine Learning para Diagnóstico Precoce de Diabetes Tipo 2 em Populações Vulneráveis"
            
            **Exemplo ruim:** "Machine Learning"
            """
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Por que isso importa?</strong> O título define o contexto temático. 
        Seja específico! Exemplo: "Machine Learning para Diagnóstico Precoce de Diabetes Tipo 2" é melhor que apenas "Machine Learning".
        </div>
        """, unsafe_allow_html=True)
        
        area_capes = st.selectbox(
            "📚 Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"],
            help="""
            💡 **Como cada área avalia?**
            
            Cada área possui um **Documento de Área** específico que pondera de forma diferente 
            os Procedimentos 1, 2 e 3.
            
            **Exatas/Saúde:**
            • Valorizam mais o Fator de Impacto (Proc. 1)
            • FI > 3.0 é considerado excelente
            • Quartil Q1 e Q2 têm maior peso
            
            **Humanas/Sociais:**
            • Valorizam mais o Proc. 3 (Qualitativo)
            • FI > 1.5 já é considerado excelente
            • Impacto social e cultural têm peso maior
            
            **A ferramenta adaptará as recomendações conforme sua área.**
            """
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Como isso afeta a avaliação?</strong> 
        • <strong>Exatas/Saúde:</strong> FI > 3.0 é excelente<br>
        • <strong>Humanas:</strong> FI > 1.5 já é excelente<br>
        A ferramenta adaptará as recomendações conforme sua área.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (PREFERENCIALMENTE EM INGLÊS)",
            height=140,
            placeholder="Ex: machine learning diabetes prediction healthcare genomics",
            help="""
            💡 **CRUCIAL: Por que em inglês?**
            
            A ferramenta busca na base global **OpenAlex** (base oficial que a CAPES usa no novo Qualis).
            Termos em inglês retornam MUITO mais revistas e métricas precisas.
            
            **Como escolher as palavras-chave:**
            • Use 3-8 termos técnicos em inglês da sua área
            • Combine: método + aplicação + área
            • Use termos específicos, não genéricos
            
            **Exemplos bons:**
            • "machine learning healthcare prediction"
            • "CRISPR gene editing agriculture"
            • "renewable energy sustainability"
            
            **Não use:**
            • Frases longas em português
            • Termos muito genéricos como "research", "study"
            """
        )
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
        
        foco = st.selectbox(
            "🎯 Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"],
            help="""
            💡 **Qual estratégia escolher?**
            
            A escolha do foco depende dos seus **objetivos de carreira** e do seu **programa**:
            
            **⚖️ Equilibrado (RECOMENDADO):**
            • Mais seguro e alinhado com a CAPES
            • Boa pontuação em todos os procedimentos
            • Ideal se não tem preferência específica
            • Busca bom FI + Acesso Aberto quando possível
            
            **📢 Impacto Social:**
            • Prioriza Open Access e divulgação
            • Ideal para pesquisas com aplicação prática
            • Áreas: Saúde Pública, Educação, Políticas Públicas
            • Exige divulgação ativa pós-publicação
            
            **📈 Tradicional:**
            • Foca em alto Fator de Impacto
            • Ideal para prestígio acadêmico máximo
            • Competir por posições em universidades de elite
            • Aceita revistas fechadas (paywall)
            """
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Qual estratégia escolher?</strong><br>
        • <strong>⚖️ Equilibrado:</strong> Mais seguro. Bom em todos os procedimentos. Recomendado para maioria.<br>
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
        st.warning("⚠️ Insira palavras-chave em inglês.")
    else:
        with st.spinner("⟳ Buscando..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=6)
            
            if revistas:
                st.success("✓ Relatório gerado!")
                
                # Tabela Comparativa
                st.markdown('<div class="section-title">Tabela Comparativa</div>', unsafe_allow_html=True)
                
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
                    
                    # Ícones e textos
                    if is_oa and citacoes > 5000:
                        acesso_icon = "🟢"
                        acesso_texto = "OA+Alto"
                        altimetria_icon = "🟢"
                        altimetria_texto = "Alto"
                    elif is_oa:
                        acesso_icon = "🔵"
                        acesso_texto = "OA"
                        altimetria_icon = "🔵"
                        altimetria_texto = "Médio"
                    else:
                        acesso_icon = "🔴"
                        acesso_texto = "Fechado"
                        altimetria_icon = "⚪"
                        altimetria_texto = "Baixo"
                    
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
                        "🚪 Acesso": f"{acesso_icon} {acesso_texto}",
                        "📈 FI": round(fi, 2),
                        "Class": fi_class,
                        "💬 Citações": formatar_numero(citacoes),
                        "📢 Altimetria": f"{altimetria_icon} {altimetria_texto}"
                    })
                
                # DataFrame
                df = pd.DataFrame(dados)
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Legenda
                st.markdown("""
                <div style="font-size: 0.85rem; color: #4a5568; padding: 0.75rem; background: white; border-radius: 8px; margin-top: 0.5rem;">
                <strong>Legenda:</strong> 🟢=OA+Alto Impacto | 🔵=OA | 🔴=Fechado | 🔥=Excelente | ⭐=Muito Bom | ✅=Bom | 📌=Aceitável | 🏆=Top 3<br>
                <strong>Altimetria:</strong> 🟢=Alto | 🔵=Médio | ⚪=Baixo
                </div>
                """, unsafe_allow_html=True)
                
                # Resumo Visual
                st.markdown('<div class="section-title">Resumo Visual</div>', unsafe_allow_html=True)
                
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
                st.markdown('<div class="section-title">Análise</div>', unsafe_allow_html=True)
                
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
                
                # ==============================================================================
                # GUIA DETALHADO DOS 3 PROCEDIMENTOS CAPES
                # ==============================================================================
                st.markdown('<div class="section-title">Guia Detalhado dos 3 Procedimentos CAPES</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;">📊 Procedimento 1</h4>
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
                        <h4 style="margin-top: 0;">📢 Procedimento 2</h4>
                        <p><strong>Impacto Social (Altimetria)</strong></p>
                        <p style="color: #742a2a;"><strong>⚠ Atenção:</strong> Todas as revistas sugeridas possuem paywall (acesso restrito).</p>
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
                
                # ==============================================================================
                # CHECKLIST DETALHADO
                # ==============================================================================
                st.markdown('<div class="section-title">Checklist de Ação Passo a Passo</div>', unsafe_allow_html=True)
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
                
                # ==============================================================================
                # BOTÃO DE DOWNLOAD
                # ==============================================================================
                st.markdown('<div class="section-title">Download do Relatório</div>', unsafe_allow_html=True)
                
                # Preparar conteúdo do relatório
                max_fi_valor = max([rev.get("summary_stats", {}).get("2yr_mean_citedness", 0) or 0 for rev in revistas])
                
                relatorio_texto = f"""
RELATÓRIO ESTRATÉGICO DE PUBLICAÇÃO CAPES 2025-2028
====================================================

Pesquisa: {titulo}
Área CAPES: {area_capes}
Estratégia Escolhida: {foco}

================================================================================
REVISTAS SUGERIDAS (Ordenadas por Relevância)
================================================================================

"""
                
                for idx, row in enumerate(dados, 1):
                    relatorio_texto += f"""
{row['📊 Ranking']} - {row['Revista']}
   Acesso: {row['🚪 Acesso']}
   Fator de Impacto: {row['📈 FI']}
   Classificação: {row['Class']}
   Citações: {row['💬 Citações']}
   Altimetria: {row['📢 Altimetria']}

"""
                
                relatorio_texto += f"""
================================================================================
RESUMO VISUAL
================================================================================

Open Access Encontradas: {len(melhores_oa)} de {len(revistas)}
Maior Fator de Impacto: {max_fi_valor:.2f}

"""
                
                if melhores_oa:
                    relatorio_texto += "Revistas Open Access:\n"
                    for rev in melhores_oa:
                        relatorio_texto += f"  - {rev}\n"
                
                relatorio_texto += f"""
================================================================================
ANÁLISE ESTRATÉGICA
================================================================================

Estratégia: {foco}

"""
                
                if "Equilibrado" in foco:
                    if melhores_oa:
                        relatorio_texto += f"✓ Equilibrado Recomendado\nPriorize: {', '.join(melhores_oa[:2])}\n"
                    else:
                        relatorio_texto += "⚠️ Sem Open Access. Deposite preprint!\n"
                elif "Impacto" in foco:
                    if melhores_oa:
                        relatorio_texto += f"📢 Impacto Social\nPriorize: {', '.join(melhores_oa)}\nAção: Compartilhe ativamente nas redes!\n"
                    else:
                        relatorio_texto += "⚠️ Deposite preprint no SciELO/arXiv!\n"
                else:
                    relatorio_texto += "📈 Tradicional\nPriorize maior FI na tabela.\n"
                
                relatorio_texto += """
================================================================================
GUIA DOS PROCEDIMENTOS CAPES
================================================================================

📊 PROCEDIMENTO 1 - Métricas do Periódico
O que avalia: Qualidade da revista (FI, Quartil, Citações)
Base: OpenAlex (oficial CAPES)

Referências Exatas/Saúde:
  - Excelente: FI > 3.0
  - Bom: FI 1.5-3.0
  - Aceitável: FI 0.5-1.5

Referências Humanas:
  - Excelente: FI > 1.5
  - Bom: FI 0.5-1.5
  - Aceitável: FI 0.2-0.5

📢 PROCEDIMENTO 2 - Impacto Social (Altimetria)
O que avalia: Impacto do artigo na sociedade
Mede: Downloads, menções, compartilhamentos

"""
                
                if melhores_oa:
                    relatorio_texto += "✓ Vantagem: Tem Open Access!\n"
                    relatorio_texto += "Ação: Divulgue ativamente nas redes!\n"
                else:
                    relatorio_texto += "⚠ Atenção: Revistas fechadas\n"
                    relatorio_texto += "Solução: Deposite preprint!\n"
                
                relatorio_texto += """
✦ PROCEDIMENTO 3 - Ciência Aberta
O que avalia: Relevância e transparência
Ações importantes:
  - Dados no Zenodo/OSF (gera DOI)
  - Citar DOI dos dados no artigo
  - Publicar preprints
  - Código aberto (GitHub)

💡 Dica: Dados abertos = +30% citações!

================================================================================
CHECKLIST DE AÇÃO
================================================================================

📋 ANTES DA SUBMISSÃO:
  [ ] Vincular ORCID ao Lattes
  [ ] Preparar dados para repositório
  [ ] Escolher repositório (Zenodo ou OSF)

📤 DURANTE A SUBMISSÃO:
  [ ] Depositar preprint (se permitido)
  [ ] Subir dados no Zenodo/OSF e obter DOI
  [ ] Incluir DOI dos dados no manuscrito

📢 APÓS A PUBLICAÇÃO:
  [ ] Atualizar preprint com link da versão publicada
  [ ] Divulgar no LinkedIn, Twitter/X, ResearchGate
  [ ] Enviar para mailing da área
  [ ] Compartilhar com assessoria de comunicação
  [ ] Monitorar altimetria em altmetric.com

================================================================================
REPOSITÓRIOS RECOMENDADOS
================================================================================

• Zenodo (https://zenodo.org) - Gratuito, multidisciplinar, gera DOI
• OSF (https://osf.io) - Gratuito, gerencia todo o projeto
• SciELO Preprints - Multidisciplinar
• arXiv - Exatas, Computação, Matemática
• bioRxiv/medRxiv - Ciências da Vida e Saúde
• SSRN - Ciências Sociais

================================================================================
INFORMAÇÕES IMPORTANTES
================================================================================

Esta ferramenta utiliza bases de dados abertas (OpenAlex) e está alinhada 
às Diretrizes Comuns da CAPES (Ciclo 2025-2028).

Esta ferramenta NÃO possui vinculação oficial com a CAPES ou MEC.
As métricas são proxies calculadas pela OpenAlex, reconhecida internacionalmente 
como alternativa aberta ao JCR.

A decisão final de submissão é de responsabilidade exclusiva do pesquisador 
e do coordenador do programa.

================================================================================
"""
                
                relatorio_texto += f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
                relatorio_texto += "=" * 80 + "\n"
                
                st.download_button(
                    label="📥 Baixar Relatório Completo (TXT)",
                    data=relatorio_texto,
                    file_name=f"Relatorio_CAPES_{titulo[:30].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.info("""
                **💡 O que está incluído no download:**
                - Lista completa das revistas sugeridas com todas as métricas
                - Análise estratégica personalizada
                - Guia detalhado dos 3 procedimentos CAPES
                - Checklist de ação passo a passo
                - Lista de repositórios recomendados
                - Informações importantes sobre a ferramenta
                """)
                
            else:
                st.warning("⚠️ Nenhuma revista. Tente termos em inglês.")

# ==============================================================================
# FOOTER COMPLETO - APENAS UMA VEZ
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%); color: #e2e8f0; border-radius: 12px; text-align: center;">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com bases de dados abertas (OpenAlex) e alinhada às Diretrizes Comuns da CAPES (Ciclo 2025-2028).<br>
        Esta ferramenta não possui vinculação oficial com a CAPES ou MEC.
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Iniciativa de promoção da Ciência Aberta e Transparência na Pós-Graduação Brasileira</em>
    </p>
</div>
""", unsafe_allow_html=True)
