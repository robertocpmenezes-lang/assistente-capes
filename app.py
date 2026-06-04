import streamlit as st
import requests
import urllib.parse
import pandas as pd
import time

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
    
    /* Disclaimer específico */
    .disclaimer {
        background: #1a202c;
        border-left: 4px solid #e53e3e;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-size: 0.8rem;
        text-align: left;
    }
    
    .disclaimer a {
        color: #90cdf4;
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
# FORMULÁRIO COM EXPLICAÇÕES DETALHADAS
# ==============================================================================
st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box alert-info">
<strong>💡 Dica geral:</strong> Preencha os campos destacados abaixo com informações da sua pesquisa. 
Quanto mais detalhado, mais precisas serão as recomendações de revistas!
</div>
""", unsafe_allow_html=True)

# Inicializar variáveis no session_state para persistência
if 'dados_gerados' not in st.session_state:
    st.session_state.dados_gerados = None
if 'revistas_data' not in st.session_state:
    st.session_state.revistas_data = None
if 'relatorio_texto' not in st.session_state:
    st.session_state.relatorio_texto = None
if 'melhores_oa_list' not in st.session_state:
    st.session_state.melhores_oa_list = None
if 'dados_tabela' not in st.session_state:
    st.session_state.dados_tabela = None

with st.form("dados_pesquisa", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "📝 Título do Artigo ou Tema da Pesquisa",
            help="Seja específico e descritivo. Exemplo: 'Machine Learning para Diagnóstico Precoce de Diabetes Tipo 2'"
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
            help="Cada área possui critérios específicos de avaliação. Escolha a que melhor se encaixa."
        )

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (PREFERENCIALMENTE EM INGLÊS)",
            height=140,
            placeholder="Ex: machine learning diabetes prediction healthcare genomics",
            help="Termos em inglês retornam MUITO mais revistas e métricas precisas na base OpenAlex."
        )
        st.markdown("""
        <div class="input-note">
        <strong>📌 Como escolher as palavras-chave?</strong><br>
        • Use <strong>termos técnicos em inglês</strong> da sua área<br>
        • Combine: <strong>método + aplicação + área</strong><br>
        • Exemplos: "machine learning healthcare prediction" ou "CRISPR gene editing agriculture"
        </div>
        """, unsafe_allow_html=True)
        
        foco = st.selectbox(
            "🎯 Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"],
            help="Escolha a estratégia alinhada com seus objetivos de carreira e tipo de pesquisa."
        )
    
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
    """Busca periódicos na API OpenAlex com fallback e tratamento de erro"""
    safe_query = urllib.parse.quote(query)
    url = f"https://api.openalex.org/works?search={safe_query}&per-page=20"
    
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return []
            
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
                    time.sleep(0.2)  # Pequena pausa para não sobrecarregar a API
                except:
                    continue
        return revistas
    except requests.exceptions.Timeout:
        st.warning("Tempo limite excedido. Tentando novamente...")
        return []
    except Exception as e:
        st.error(f"Erro na conexão com a API: {str(e)}")
        return []

def gerar_dados_tabela(revistas, foco_str):
    """Gera os dados formatados para tabela e relatório"""
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
    
    return dados, melhores_oa

def gerar_relatorio_texto(titulo, area_capes, foco, dados, melhores_oa, revistas):
    """Gera o conteúdo do relatório para download"""
    
    relatorio = f"""
RELATÓRIO ESTRATÉGICO DE PUBLICAÇÃO CAPES 2025-2028
====================================================

Pesquisa: {titulo if titulo else "Não informado"}
Área CAPES: {area_capes}
Estratégia Escolhida: {foco}
Data de geração: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}

================================================================================
REVISTAS SUGERIDAS (Ordenadas por Relevância)
================================================================================

"""
    
    for row in dados:
        relatorio += f"""
{row['📊 Ranking']} - {row['Revista']}
   Acesso: {row['🚪 Acesso']}
   Fator de Impacto: {row['📈 FI']}
   Classificação: {row['Class']}
   Citações: {row['💬 Citações']}
   Altimetria: {row['📢 Altimetria']}

"""
    
    relatorio += f"""
================================================================================
RESUMO VISUAL
================================================================================

Open Access Encontradas: {len(melhores_oa)} de {len(revistas)}
Maior Fator de Impacto: {max([rev.get('summary_stats', {{}}).get('2yr_mean_citedness', 0) or 0 for rev in revistas]):.2f}

"""
    
    if melhores_oa:
        relatorio += "Revistas Open Access:\n"
        for rev in melhores_oa:
            relatorio += f"  - {rev}\n"
    
    relatorio += f"""
================================================================================
ANÁLISE ESTRATÉGICA
================================================================================

Estratégia: {foco}

"""
    
    if "Equilibrado" in foco:
        if melhores_oa:
            relatorio += f"✓ Equilibrado Recomendado\nPriorize: {', '.join(melhores_oa[:2])}\n"
        else:
            relatorio += "⚠️ Sem Open Access. Deposite preprint!\n"
    elif "Impacto" in foco:
        if melhores_oa:
            relatorio += f"📢 Impacto Social\nPriorize: {', '.join(melhores_oa)}\nAção: Compartilhe ativamente nas redes!\n"
        else:
            relatorio += "⚠️ Deposite preprint no SciELO/arXiv!\n"
    else:
        relatorio += "📈 Tradicional\nPriorize maior FI na tabela.\n"
    
    relatorio += f"""
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
        relatorio += "✓ Vantagem: Tem Open Access!\nAção: Divulgue ativamente nas redes!\n"
    else:
        relatorio += "⚠ Atenção: Revistas fechadas\nSolução: Deposite preprint!\n"
    
    relatorio += f"""
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
DISCLAIMER
================================================================================

⚠️ AVISO LEGAL:

Esta ferramenta foi desenvolvida para fins de apoio à pesquisa e NÃO possui 
vinculação oficial com a CAPES, MEC ou qualquer órgão governamental.

As métricas apresentadas são proxies calculadas pela OpenAlex, uma base de 
dados aberta internacionalmente reconhecida como alternativa ao JCR/Scopus. 
Os valores de Fator de Impacto e demais indicadores são estimativas baseadas 
no modelo da OpenAlex e podem não corresponder exatamente aos valores oficiais.

A classificação de periódicos segue as Diretrizes Comuns da CAPES para o 
Ciclo 2025-2028, porém a decisão final sobre a adequação de um periódico 
para submissão é de responsabilidade EXCLUSIVA do pesquisador e do 
coordenador do programa de pós-graduação.

Recomenda-se sempre consultar os documentos oficiais da CAPES e da área 
específica do conhecimento antes de tomar qualquer decisão de submissão.

================================================================================
Fim do relatório
================================================================================
"""
    
    return relatorio

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if submitted:
    if not resumo.strip():
        st.warning("⚠️ Insira palavras-chave em inglês para buscar periódicos.")
    else:
        with st.spinner("⟳ Buscando periódicos na base OpenAlex... Isso pode levar alguns segundos."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=6)
            
            if revistas:
                # Gerar dados
                dados, melhores_oa = gerar_dados_tabela(revistas, foco)
                relatorio_texto = gerar_relatorio_texto(titulo, area_capes, foco, dados, melhores_oa, revistas)
                
                # Salvar no session_state para persistência
                st.session_state.dados_gerados = True
                st.session_state.revistas_data = revistas
                st.session_state.relatorio_texto = relatorio_texto
                st.session_state.melhores_oa_list = melhores_oa
                st.session_state.dados_tabela = dados
                
                st.success("✓ Relatório gerado com sucesso!")
                
                # Tabela Comparativa
                st.markdown('<div class="section-title">✦ Tabela Comparativa</div>', unsafe_allow_html=True)
                
                st.info("""
                **Como ler:** Tabela ordenada por relevância | 🟢 OA+Alto = melhor | 🔵 OA = boa altimetria | 🔴 Fechado
                """)
                
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
                st.markdown('<div class="section-title">▸ Resumo Visual</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if melhores_oa:
                        st.success(f"**🟢 Open Access: {len(melhores_oa)}**\n\n{chr(10).join([f'- {r}' for r in melhores_oa[:3]])}")
                        if len(melhores_oa) > 3:
                            st.caption(f"+ {len(melhores_oa)-3} outras")
                    else:
                        st.warning("**🔴 Nenhuma Open Access encontrada**\n\nDeposite preprint!")
                
                with col2:
                    max_fi = max([rev.get("summary_stats", {}).get("2yr_mean_citedness", 0) or 0 for rev in revistas])
                    st.success(f"**🔥 Maior Fator de Impacto**\n\n{max_fi:.2f}")
                
                with col3:
                    st.info(f"**📊 Total de periódicos**\n\n{len(revistas)} encontrados\nÁrea: {area_capes.split()[0]}")
                
                # Análise
                st.markdown('<div class="section-title">▸ Análise Estratégica</div>', unsafe_allow_html=True)
                
                if "Equilibrado" in foco:
                    if melhores_oa:
                        st.success(f"**✓ Estratégia Equilibrada**\n\nRecomenda-se priorizar: {', '.join(melhores_oa[:2])}\n\nEstas revistas combinam bom Fator de Impacto com Acesso Aberto, maximizando sua pontuação nos Procedimentos 1 e 2.")
                    else:
                        st.warning("**⚠ Estratégia Equilibrada - Atenção**\n\nNenhuma revista Open Access foi encontrada. Para melhorar sua pontuação no Procedimento 2 (Impacto Social), deposite um preprint em repositório aberto antes da submissão.")
                    
                elif "Impacto" in foco:
                    if melhores_oa:
                        st.success(f"**📢 Estratégia de Impacto Social**\n\nRevistas prioritárias: {', '.join(melhores_oa)}\n\n**Ações necessárias:** Após a publicação, compartilhe ativamente o link em LinkedIn, Twitter/X e ResearchGate para maximizar a altimetria.")
                    else:
                        st.error("**⚠ Estratégia de Impacto Social - Ação Necessária**\n\nTodas as revistas sugeridas são fechadas (paywall). Você PRECISA depositar um preprint no SciELO/arXiv/bioRxiv para garantir visibilidade e pontuação no Procedimento 2.")
                    
                else:
                    st.success("**📈 Estratégia Tradicional**\n\nPriorize os periódicos com maior Fator de Impacto na tabela acima. Lembre-se que revistas fechadas (🔴) não contribuem para o Procedimento 2 (Altimetria).")
                
                # ==============================================================================
                # GUIA DETALHADO DOS 3 PROCEDIMENTOS CAPES
                # ==============================================================================
                st.markdown('<div class="section-title">▸ Guia Detalhado dos 3 Procedimentos CAPES</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="alert-box alert-info">
                    <h4 style="margin-top: 0;">📊 Procedimento 1</h4>
                    <p><strong>Métricas do Periódico</strong></p>
                    <p><strong>O que a CAPES avalia:</strong> A qualidade da revista onde você publica, usando a OpenAlex como base oficial.</p>
                    <p><strong>Referências Exatas e Saúde:</strong></p>
                    <ul>
                        <li>Excelente: FI > 3.0</li>
                        <li>Bom: FI entre 1.5 e 3.0</li>
                        <li>Aceitável: FI entre 0.5 e 1.5</li>
                    </ul>
                    <p><strong>Referências Humanas:</strong></p>
                    <ul>
                        <li>Excelente: FI > 1.5</li>
                        <li>Bom: FI entre 0.5 e 1.5</li>
                        <li>Aceitável: FI entre 0.2 e 0.5</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if melhores_oa:
                        st.markdown("""
                        <div class="alert-box alert-success">
                        <h4 style="margin-top: 0;">📢 Procedimento 2</h4>
                        <p><strong>Impacto Social (Altimetria)</strong></p>
                        <p style="color: #22543d;"><strong>✓ Vantagem:</strong> Você tem revistas Open Access disponíveis!</p>
                        <p><strong>O que a CAPES avalia:</strong> Impacto do artigo na sociedade (downloads, menções, compartilhamentos).</p>
                        <p><strong>Benefícios do Open Access:</strong></p>
                        <ul>
                            <li>Mais downloads e visualizações</li>
                            <li>Mais compartilhamentos em redes</li>
                            <li>Maior chance de citação</li>
                        </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="alert-box alert-warning">
                        <h4 style="margin-top: 0;">📢 Procedimento 2</h4>
                        <p><strong>Impacto Social (Altimetria)</strong></p>
                        <p style="color: #742a2a;"><strong>⚠ Atenção:</strong> Nenhuma revista Open Access encontrada.</p>
                        <p><strong>Solução obrigatória:</strong></p>
                        <ol>
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
                    <p><strong>Ações que contam muitos pontos:</strong></p>
                    <ul>
                        <li><strong>Disponibilizar dados brutos</strong> no Zenodo/OSF</li>
                        <li><strong>Citar o DOI dos dados</strong> no artigo</li>
                        <li><strong>Publicar preprints</strong></li>
                        <li><strong>Usar software livre</strong> (GitHub)</li>
                    </ul>
                    <p><strong>💡 Dica:</strong> Dados abertos = +30% citações!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ==============================================================================
                # CHECKLIST DETALHADO
                # ==============================================================================
                st.markdown('<div class="section-title">▸ Checklist de Ação Passo a Passo</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="alert-box alert-success">
                <h4 style="margin-top: 0;">📋 Antes da Submissão</h4>
                <ul>
                    <li><strong>Vincular ORCID ao Lattes</strong> - A CAPES cruza dados via ORCID</li>
                    <li><strong>Preparar dados para repositório</strong> - Organize dados brutos e metadados</li>
                    <li><strong>Escolher repositório</strong> - Zenodo (recomendado) ou OSF</li>
                </ul>
                
                <h4 style="margin: 1rem 0 0.5rem 0;">📤 Durante a Submissão</h4>
                <ul>
                    <li><strong>Depositar preprint</strong> (se a revista permitir)</li>
                    <li><strong>Subir dados no Zenodo/OSF</strong> - Obtenha o DOI</li>
                    <li><strong>Incluir no manuscrito</strong> - "Data available at: [DOI]"</li>
                </ul>
                
                <h4 style="margin: 1rem 0 0.5rem 0;">📢 Após a Publicação (CRUCIAL!)</h4>
                <ul>
                    <li><strong>Atualizar preprint</strong> com link da versão publicada</li>
                    <li><strong>Divulgar nas redes sociais</strong> (LinkedIn, Twitter, ResearchGate)</li>
                    <li><strong>Enviar para mailing</strong> da área e grupos de pesquisa</li>
                    <li><strong>Compartilhar com assessoria de comunicação</strong> da universidade</li>
                    <li><strong>Monitorar altimetria</strong> em altmetric.com</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # ==============================================================================
                # BOTÃO DE DOWNLOAD
                # ==============================================================================
                st.markdown('<div class="section-title">▸ Download do Relatório</div>', unsafe_allow_html=True)
                
                # Nome do arquivo seguro
                safe_title = titulo[:30].replace(' ', '_').replace('/', '_') if titulo else "relatorio"
                safe_title = safe_title or "relatorio"
                
                st.download_button(
                    label="📥 Baixar Relatório Completo (TXT)",
                    data=relatorio_texto,
                    file_name=f"Relatorio_CAPES_{safe_title}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.info("""
                **💡 O que está incluído no download:**
                - Lista completa das revistas sugeridas com todas as métricas
                - Análise estratégica personalizada para seu foco
                - Guia detalhado dos 3 procedimentos CAPES
                - Checklist de ação passo a passo
                - Lista de repositórios recomendados
                """)
                
            else:
                st.warning("⚠️ Nenhum periódico encontrado para os termos informados. Tente palavras-chave diferentes ou mais específicas em inglês.")
                
                st.markdown("""
                <div class="alert-box alert-info">
                <strong>💡 Sugestões para melhorar sua busca:</strong><br>
                • Use termos em inglês (ex: "cancer therapy" ao invés de "câncer tratamento")<br>
                • Seja mais específico (ex: "machine learning healthcare" ao invés de "machine learning")<br>
                • Evite palavras muito genéricas como "research", "study", "analysis"<br>
                • Tente combinações de método + aplicação + área
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# FOOTER COMPLETO COM DISCLAIMER
# ==============================================================================
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com bases de dados abertas (OpenAlex) e alinhada às Diretrizes Comuns da CAPES (Ciclo 2025-2028).
    </p>
    
    <div class="disclaimer">
        <strong>⚠️ DISCLAIMER / AVISO LEGAL</strong><br><br>
        Esta ferramenta é um recurso auxiliar e <strong>NÃO possui vinculação oficial com a CAPES, MEC ou qualquer órgão governamental</strong>.<br><br>
        As métricas de Fator de Impacto e demais indicadores são <strong>proxies calculadas pela OpenAlex</strong>, uma base de dados aberta 
        internacionalmente reconhecida como alternativa ao JCR/Scopus. Os valores apresentados podem não corresponder exatamente aos valores oficiais.<br><br>
        A classificação segue as Diretrizes Comuns da CAPES para o Ciclo 2025-2028, porém a <strong>decisão final sobre a adequação de um periódico 
        é de responsabilidade EXCLUSIVA do pesquisador e do coordenador do programa</strong> de pós-graduação.<br><br>
        Recomenda-se sempre consultar os <strong>documentos oficiais da CAPES</strong> e da <strong>área específica do conhecimento</strong> 
        antes de qualquer decisão de submissão.
    </div>
    
    <p style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.8;">
        <em>Iniciativa de promoção da Ciência Aberta e Transparência na Pós-Graduação Brasileira</em><br>
        Dados: OpenAlex | Interface: Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
