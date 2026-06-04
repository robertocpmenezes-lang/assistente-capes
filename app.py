import streamlit as st
import requests
import urllib.parse
import pandas as pd

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Assistente CAPES 2025-2028", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Simplificado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #667eea;
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">✦ Assistente de Estratégia de Publicação</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ciclo de Avaliação CAPES 2025-2028</p>', unsafe_allow_html=True)

# ==============================================================================
# SEÇÃO EDUCACIONAL
# ==============================================================================
st.markdown('<div class="section-title">▸ Entenda a Nova Avaliação CAPES</div>', unsafe_allow_html=True)

with st.expander("📚 Clique aqui para entender os 3 Procedimentos de Avaliação", expanded=False):
    st.markdown("""
    ### Como Funciona a Avaliação CAPES 2025-2028
    
    A CAPES avalia através de **3 procedimentos complementares**:
    
    **📊 Procedimento 1: Métricas do Periódico (Qualis)**
    - Avalia a qualidade da REVISTA onde você publica
    - Usa Fator de Impacto, Quartil (Q1-Q4), Citações
    - Base: OpenAlex (substituiu o JCR pago)
    
    **📢 Procedimento 2: Impacto Social do Artigo (Altimetria)**
    - Avalia o impacto do SEU ARTIGO na sociedade
    - Mede: downloads, menções em redes sociais, compartilhamentos
    - Artigos em Acesso Aberto têm MUITO mais alcance
    
    **✦ Procedimento 3: Avaliação Qualitativa e Ciência Aberta**
    - Avalia relevância e transparência da pesquisa
    - Análise por pares consultores da CAPES
    - Disponibilizar dados de pesquisa conta muitos pontos
    
    ---
    
    ### Os 3 Tipos de Estratégia (Focos)
    
    **⚖️ 1. Equilibrado (Impacto + Ciência Aberta)**
    - Mais seguro e recomendado
    - Busca bom Fator de Impacto + Acesso Aberto
    - Boa pontuação em todos os procedimentos
    
    **📢 2. Máximo Impacto Social (Altimetria)**
    - Prioriza revistas Open Access
    - Foca em maximizar downloads e compartilhamentos
    - Ideal para pesquisas com aplicação prática
    
    **📈 3. Máximo Tradicional (Fator de Impacto)**
    - Foca em revistas de alto prestígio (Nature, Science)
    - Aceita que sejam fechadas (paywall)
    - Ideal para carreiras acadêmicas de elite
    """)

# ==============================================================================
# FORMULÁRIO
# ==============================================================================
with st.form("dados_pesquisa", clear_on_submit=False):
    st.markdown('<div class="section-title">▸ Dados da Produção Intelectual</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input("📝 Título do Artigo ou Tema da Pesquisa")
        area_capes = st.selectbox(
            "📚 Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", 
             "Linguística, Letras e Artes", "Ciências Agrárias"]
        )

    with col2:
        resumo = st.text_area(
            "🔑 Palavras-chave (preferencialmente em inglês)",
            height=130,
            placeholder="Ex: machine learning healthcare prediction"
        )
        foco = st.selectbox(
            "🎯 Foco da Estratégia de Publicação",
            ["⚖️ Equilibrado (Impacto + Ciência Aberta)", 
             "📢 Máximo Impacto Social (Altimetria)", 
             "📈 Máximo Tradicional (Fator de Impacto)"]
        )
    
    submitted = st.form_submit_button("🚀 Gerar Relatório Estratégico", use_container_width=True)

# ==============================================================================
# FUNÇÕES DE BUSCA
# ==============================================================================
@st.cache_data(ttl=3600)
def buscar_revistas_openalex(query, max_results=5):
    """Busca revistas na OpenAlex com cache"""
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
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if submitted:
    if not resumo.strip():
        st.warning("⚠️ Insira pelo menos 3-5 palavras-chave em inglês para realizar a busca.")
    else:
        with st.spinner("⟳ Consultando base OpenAlex e gerando análise..."):
            query_busca = " ".join(resumo.split()[:15]) 
            revistas_encontradas = buscar_revistas_openalex(query_busca, max_results=5)
            
            if revistas_encontradas:
                st.success("✓ Relatório gerado com sucesso!")
                
                # Tabela de Revistas (USANDO PANDAS - SEM HTML)
                st.markdown('<div class="section-title">✦ Revistas Sugeridas (Métricas Reais)</div>', unsafe_allow_html=True)
                
                st.info("""
                **Como ler esta tabela:**
                - **Acesso Aberto (✓):** Artigo gratuito → Melhor para Altimetria (Proc. 2)
                - **Fechado (✕):** Requer assinatura → Melhor para Fator de Impacto (Proc. 1)
                - **Fator de Impacto:** Quanto maior, melhor
                - **Potencial Altimetria:** 🔥 Alto = mais downloads esperados
                """)
                
                # Preparar dados para DataFrame
                dados_tabela = []
                melhores_oa = []
                
                for rev in revistas_encontradas:
                    nome = rev.get("display_name", "Nome não disponível")
                    is_oa = rev.get("is_oa", False)
                    
                    summary_stats = rev.get("summary_stats", {})
                    fator_impacto = summary_stats.get("2yr_mean_citedness", 0)
                    citacoes = rev.get("cited_by_count", 0)
                    
                    # Determinar potencial de altimetria
                    if is_oa and citacoes > 5000:
                        potencial = "🔥 Alto"
                    elif is_oa:
                        potencial = "● Médio"
                    else:
                        potencial = "○ Baixo"
                    
                    if is_oa:
                        melhores_oa.append(nome)
                        acesso_str = "✓ Aberto"
                    else:
                        acesso_str = "✕ Fechado"
                    
                    dados_tabela.append({
                        "Revista": nome,
                        "Acesso": acesso_str,
                        "Fator de Impacto": f"{fator_impacto:.2f}" if fator_impacto else "N/A",
                        "Potencial Altimetria": potencial
                    })
                
                # Exibir tabela com pandas (funciona perfeitamente!)
                df = pd.DataFrame(dados_tabela)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Análise Estratégica
                st.markdown('<div class="section-title">▸ Análise Estratégica</div>', unsafe_allow_html=True)
                st.info(f"**Área CAPES:** {area_capes} | **Estratégia:** {foco}")
                
                # Explicação baseada no foco
                if "Equilibrado" in foco:
                    st.success("""
                    **✓ Estratégia Equilibrada - A Mais Recomendada**
                    
                    Você escolheu a estratégia mais segura e alinhada com a CAPES 2025-2028.
                    
                    **O que isso significa:**
                    - Busca revistas com bom Fator de Impacto (Proc. 1)
                    - Prioriza Acesso Aberto quando possível (Proc. 2)
                    - Valoriza Ciência Aberta e transparência (Proc. 3)
                    
                    **Recomendação:** Priorize as revistas marcadas com "✓ Aberto" que tenham Fator de Impacto acima de 1.0.
                    """)
                    
                elif "Impacto Social" in foco:
                    st.success("""
                    **📢 Estratégia de Máximo Impacto Social**
                    
                    Você prioriza o Procedimento 2 (Altimetria) da CAPES.
                    
                    **O que isso significa:**
                    - Foco em Acesso Aberto para maximizar downloads
                    - Menor preocupação com Fator de Impacto tradicional
                    - Exige divulgação ativa após publicação
                    
                    **Recomendação:** Publique APENAS em revistas marcadas com "✓ Aberto". Após publicar, compartilhe ativamente no LinkedIn, Twitter e ResearchGate.
                    
                    **Atenção:** Se publicar em revista fechada, DEPOSITAR o preprint em repositório aberto é OBRIGATÓRIO.
                    """)
                    
                else:
                    st.success("""
                    **📈 Estratégia de Máximo Impacto Tradicional**
                    
                    Você prioriza o Procedimento 1 (Fator de Impacto) da CAPES.
                    
                    **O que isso significa:**
                    - Foco em revistas de alto prestígio e FI elevado
                    - Busca maximizar pontuação no Qualis tradicional
                    - Ideal para carreiras acadêmicas de elite
                    
                    **Recomendação:** Priorize revistas com FI acima de 3.0 (Exatas/Saúde) ou 1.0 (Humanas).
                    
                    **Compensação necessária:** Revistas de alto impacto geralmente são fechadas. Para não perder pontos no Proc. 2, você DEVE depositar o preprint em repositório aberto (arXiv, SciELO Preprints).
                    """)
                
                # Procedimento 1
                st.markdown('<div class="section-title">▸ Procedimento 1: Métricas do Periódico</div>', unsafe_allow_html=True)
                st.info("""
                **📊 O Que a CAPES Avalia**
                
                A CAPES utiliza a OpenAlex como base oficial (substituindo o JCR/Scopus pagos).
                
                **Referências por Área:**
                
                **Ciências Exatas e da Saúde:**
                - Excelente: FI > 3.0
                - Bom: FI entre 1.5 e 3.0
                - Aceitável: FI entre 0.5 e 1.5
                
                **Ciências Humanas e Sociais:**
                - Excelente: FI > 1.5
                - Bom: FI entre 0.5 e 1.5
                - Aceitável: FI entre 0.2 e 0.5
                
                **Dica:** Além do FI, a CAPES considera o Quartil (Q1, Q2, Q3, Q4). Q1 e Q2 têm maior pontuação.
                """)
                
                # Procedimento 2
                st.markdown('<div class="section-title">▸ Procedimento 2: Impacto Social (Altimetria)</div>', unsafe_allow_html=True)
                
                if melhores_oa:
                    st.success(f"""
                    **📢 Vantagem: Acesso Aberto Detectado**
                    
                    ✓ Excelente notícia! Algumas revistas sugeridas possuem Acesso Aberto:
                    
                    {chr(10).join([f"- {rev}" for rev in melhores_oa[:3]])}
                    
                    **O que isso significa para o Procedimento 2:**
                    - Seu artigo poderá ser baixado gratuitamente por qualquer pessoa
                    - Maior chance de ser compartilhado no Twitter, LinkedIn, ResearchGate
                    - Mais salvamentos no Mendeley, Zotero
                    - Possibilidade de ser citado em políticas públicas e notícias
                    
                    **Ação necessária:** Após a publicação, compartilhe ativamente o link do artigo em suas redes profissionais.
                    """)
                else:
                    st.warning("""
                    **⚠ Atenção: Revistas Fechadas**
                    
                    As revistas sugeridas possuem paywall (acesso restrito).
                    
                    **Problema para o Procedimento 2:**
                    - Poucas pessoas conseguirão ler seu artigo
                    - Menos downloads = menos compartilhamentos = menos altimetria
                    - Risco de baixa pontuação no Proc. 2
                    
                    **Solução OBRIGATÓRIA:**
                    1. **Deposite o preprint** em repositório aberto ANTES ou durante a submissão:
                       - SciELO Preprints (multidisciplinar)
                       - arXiv (Exatas, Computação)
                       - bioRxiv/medRxiv (Ciências da Vida)
                       - SSRN (Ciências Sociais)
                    2. **Compartilhe o link do preprint** nas redes sociais
                    3. **Após publicação**, atualize o preprint com o link da versão final
                    
                    **Resultado:** O Crossref rastreará as menções ao preprint aberto e você ganhará altimetria mesmo publicando em revista fechada!
                    """)
                
                # Procedimento 3
                st.markdown('<div class="section-title">▸ Procedimento 3: Ciência Aberta</div>', unsafe_allow_html=True)
                st.info("""
                **✦ O Diferencial Qualitativo**
                
                O Procedimento 3 é avaliado por pares consultores da CAPES e considera:
                
                **1. Relevância da Pesquisa:**
                - Contribuição para o avanço do conhecimento
                - Impacto social, econômico ou cultural
                - Inovação metodológica ou teórica
                
                **2. Ciência Aberta (OPEN SCIENCE):**
                
                A CAPES premia MUITO a transparência! Ações que contam pontos:
                
                ✓ **Disponibilizar dados brutos** em repositórios abertos:
                  - [Zenodo](https://zenodo.org) (gratuito, gera DOI)
                  - [OSF](https://osf.io) (gratuito)
                  - Repositórios institucionais
                
                ✓ **Citar o DOI dos dados** no artigo publicado
                  - Exemplo: "Dados disponíveis em: [DOI do Zenodo]"
                
                ✓ **Publicar preprints** (versões prévias)
                
                ✓ **Usar software livre** e abrir códigos (GitHub, GitLab)
                
                **💡 Dica de ouro:** Pesquisadores que disponibilizam dados abertos têm até 30% mais citações!
                """)
                
                # Checklist
                st.markdown('<div class="section-title">▸ Checklist de Ação</div>', unsafe_allow_html=True)
                st.success("""
                **📋 Antes da Submissão**
                - [ ] Vincular ORCID ao Lattes (obrigatório)
                - [ ] Preparar dados para repositório
                - [ ] Escolher repositório (Zenodo ou OSF)
                
                **📤 Durante a Submissão**
                - [ ] Depositar preprint (se permitido)
                - [ ] Subir dados no Zenodo/OSF e obter DOI
                - [ ] Incluir DOI dos dados no manuscrito
                
                **📢 Após a Publicação (CRUCIAL!)**
                - [ ] Atualizar preprint com link da versão publicada
                - [ ] Divulgar nas redes sociais (LinkedIn, Twitter, ResearchGate)
                - [ ] Enviar para mailing da área
                - [ ] Compartilhar com assessoria de comunicação da universidade
                - [ ] Monitorar altimetria em altmetric.com
                """)
                
                # Download
                resumo_texto = f"""
RELATÓRIO CAPES 2025-2028
=========================
Pesquisa: {titulo}
Área: {area_capes}
Estratégia: {foco}

REVISTAS SUGERIDAS:
"""
                for row in dados_tabela:
                    resumo_texto += f"\n- {row['Revista']} ({row['Acesso']}, FI: {row['Fator de Impacto']})"
                
                st.download_button(
                    label="📥 Baixar Resumo",
                    data=resumo_texto,
                    file_name=f"Relatorio_CAPES_{titulo[:30].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            else:
                st.warning("""
                ⚠️ Nenhuma revista encontrada.
                
                **Dicas:**
                - Use palavras-chave em inglês
                - Use termos mais genéricos
                - Exemplo: "machine learning" em vez de "deep learning neural network"
                """)

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem; background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%); border-radius: 12px; color: white;">
    <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p style="margin: 0 0 1rem 0; line-height: 1.6;">
        Desenvolvida com bases de dados abertas (OpenAlex) e alinhada às Diretrizes da CAPES (2025-2028).<br>
        Esta ferramenta não possui vinculação oficial com a CAPES ou MEC.
    </p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
        <em>Iniciativa de promoção da Ciência Aberta</em>
    </p>
</div>
""", unsafe_allow_html=True)
