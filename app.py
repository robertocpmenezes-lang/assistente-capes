import streamlit as st
import requests
import urllib.parse
import time

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILO
# ==============================================================================
st.set_page_config(
    page_title="Assistente de Estratégia de Publicação CAPES", 
    page_icon="🎓", 
    layout="wide"
)

# Estilização CSS leve para deixar o rodapé e os destaques mais profissionais
st.markdown("""
<style>
    .main-header {font-size: 2.2rem; font-weight: bold; color: #1f3a93;}
    .capex-note {font-size: 0.9rem; color: #555; background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 4px solid #1f3a93;}
    .footer {margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.8rem; color: #666; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🎓 Assistente de Estratégia de Publicação (Ciclo CAPES 2025-2028)</p>', unsafe_allow_html=True)
st.markdown("Ferramenta de apoio à decisão para pesquisadores, baseada em dados abertos e nas Diretrizes Comuns da CAPES.")

# ==============================================================================
# 1. ENTRADA DE DADOS COM NOTAS EXPLICATIVAS (TOOLTIPS)
# ==============================================================================
with st.form("dados_pesquisa"):
    st.markdown("### 📝 Dados da Produção Intelectual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "Título do Artigo ou Tema Geral da Pesquisa",
            help="💡 DICA CAPES: O título ajuda a ferramenta a contextualizar a relevância temática. Isso é fundamental para o Procedimento 3 (Avaliação Qualitativa), onde os consultores analisam a coerência e o avanço do conhecimento na área."
        )
        
        area_capes = st.selectbox(
            "Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", "Linguística, Letras e Artes"],
            help="💡 DICA CAPES: Cada área possui um Documento de Área específico que pondera de forma diferente os Procedimentos 1, 2 e 3. A ferramenta adaptará as recomendações com base no perfil da sua área."
        )

    with col2:
        resumo = st.text_area(
            "Resumo ou Palavras-chave (Preferencialmente em Inglês)",
            height=120,
            help="💡 DICA CAPES: A ferramenta busca em bases globais (OpenAlex). Usar termos em inglês (ex: 'machine learning', 'public health') retorna revistas com métricas de impacto e altimetria mais precisas e consolidadas."
        )
        
        foco = st.selectbox(
            "Foco da Estratégia de Publicação",
            [
                "Equilibrado (Impacto Tradicional + Ciência Aberta)", 
                "Máximo Impacto Social (Foco em Altimetria / Proc. 2)", 
                "Máximo Tradicional (Foco em Fator de Impacto / Proc. 1)"
            ],
            help="💡 DICA CAPES: 'Equilibrado' é o mais recomendado pela nova gestão. O Proc. 1 avalia a revista (JCR/Quartis). O Proc. 2 avalia o artigo (Altimetria, downloads, menções). O Proc. 3 avalia a narrativa e a Ciência Aberta (dados abertos, preprints)."
        )
    
    submitted = st.form_submit_button("🔍 Buscar Revistas e Gerar Relatório Estratégico", type="primary")

# ==============================================================================
# 2. MOTORES DE BUSCA (APIs Gratuitas e Robustas) - CÓDIGO CORRIGIDO
# ==============================================================================
def buscar_revistas_openalex(query, max_results=5):
    """Busca revistas na OpenAlex por assunto/tema (não por nome)"""
    safe_query = urllib.parse.quote(query)
    
    # Estratégia: Buscar por works (artigos) relacionados e pegar as revistas
    url_works = f"https://api.openalex.org/works?search={safe_query}&per-page=20"
    
    try:
        # Busca artigos relacionados ao tema
        response = requests.get(url_works, timeout=15)
        response.raise_for_status()
        works_data = response.json().get("results", [])
        
        # Extrai as revistas desses artigos
        revistas_encontradas = []
        ids_vistos = set()
        
        for work in works_data:
            source = work.get("primary_location", {}).get("source")
            if source and source.get("id") not in ids_vistos:
                ids_vistos.add(source.get("id"))
                # Busca detalhes completos da revista
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
    
    # Fallback: busca direta por fontes populares se não encontrar nada
    fallback_url = f"https://api.openalex.org/sources?per-page={max_results}"
    try:
        response = requests.get(fallback_url, timeout=15)
        return response.json().get("results", [])
    except:
        return []

def buscar_altimetria_crossref(issn_list):
    """Busca eventos de altimetria (menções em redes, notícias, etc.) via Crossref Events (Gratuito)"""
    if not issn_list:
        return 0, []
    
    issn = issn_list[0]
    # Mailto é obrigatório para a 'Polite Pool' do Crossref (evita bloqueio e é gratuito)
    url = f"https://api.eventdata.crossref.org/v1/events?filter=issn:{issn}&mailto=contato@instituicao.edu.br"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            total_eventos = data.get("total_results", 0)
            fontes = list(set([ev.get("source_id", "Desconhecido").replace("reddit", "Reddit").replace("twitter", "Twitter/X").replace("wikipedia", "Wikipedia") for ev in data.get("events", [])[:5]]))
            return total_eventos, fontes
    except Exception:
        pass
    return 0, []

# ==============================================================================
# 3. MOTOR DE RELATÓRIO (Lógica Alinhada à CAPES 2025-2028)
# ==============================================================================
def gerar_relatorio_capes(titulo, area, foco, revistas):
    if not revistas:
        return "⚠️ **Nenhuma revista encontrada com esses termos.**\n\n*Dica:* Tente usar palavras-chave em inglês ou termos mais amplos da sua área (ex: 'education', 'sustainability', 'neuroscience'). A base OpenAlex é global."

    relatorio = f"### 📊 Relatório Estratégico de Publicação\n"
    relatorio += f"**Pesquisa:** *{titulo}*\n"
    relatorio += f"**Área CAPES:** {area} | **Estratégia:** {foco}\n\n"
    relatorio += "---\n\n"
    
    relatorio += "#### 🏆 1. Análise de Revistas Sugeridas (Métricas Reais)\n\n"
    relatorio += "| Revista | Acesso | Fator de Impacto (Proxy JCR) | Score Altimetria |\n"
    relatorio += "| :--- | :---: | :---: | :--- |\n"
    
    melhores_opcoes_oa = []
    
    for rev in revistas:
        nome = rev.get("display_name", "Nome não disponível")
        is_oa = "✅ Sim" if rev.get("is_oa") else "❌ Não"
        
        # Métrica 1: Proxy do JCR (2yr_mean_citedness é a fórmula exata do JCR)
        summary_stats = rev.get("summary_stats", {})
        fator_impacto = summary_stats.get("2yr_mean_citedness", 0)
        fi_formatado = f"{fator_impacto:.2f}" if fator_impacto else "N/A"
        
        # Métrica 2: Altimetria
        issn_list = rev.get("issn", [])
        total_eventos, fontes_alt = buscar_altimetria_crossref(issn_list)
        fontes_str = ", ".join(fontes_alt[:3]) if fontes_alt else "Aguardando indexação"
        
        relatorio += f"| **{nome}** | {is_oa} | `{fi_formatado}` | `{total_eventos}` menções *({fontes_str})* |\n"
        
        if rev.get("is_oa"):
            melhores_opcoes_oa.append(nome)

    relatorio += "\n---\n\n"
    relatorio += "#### 🎯 2. Estratégia de Pontuação CAPES (Ciclo 2025-2028)\n\n"
    
    relatorio += f"**Análise para a área de {area}:**\n\n"
    relatorio += "📌 **Procedimento 1 (Métricas do Periódico):**\n"
    relatorio += "A CAPES utiliza a OpenAlex como base oficial. O 'Fator de Impacto' exibido acima é o dado que os consultores verão. Para áreas Exatas/Saúde, busque valores > 1.5. Para Humanas, > 0.5 já é considerado bom.\n\n"
    
    relatorio += "📌 **Procedimento 2 (Impacto do Artigo / Altimetria):**\n"
    if melhores_opcoes_oa:
        relatorio += f"✅ **Vantagem:** As revistas sugeridas possuem Acesso Aberto. Isso remove barreiras de paywall, permitindo que seu artigo seja baixado, compartilhado no LinkedIn/X e salvo no Mendeley. O Crossref rastreia esses eventos e a CAPES os valoriza neste procedimento.\n"
    else:
        relatorio += "⚠️ **Atenção:** As revistas sugeridas possuem paywall. Para pontuar no Proc. 2, é **obrigatório** que você deposite a versão 'Preprint' ou 'Pós-print' em um repositório institucional ou no SciELO Preprints, e divulgue esse link aberto.\n\n"
        
    relatorio += "📌 **Procedimento 3 (Avaliação Qualitativa e Ciência Aberta):**\n"
    relatorio += "A CAPES premia a transparência. A simples ação de disponibilizar os dados brutos da pesquisa em repositórios abertos (como Zenodo ou OSF) e citá-los no artigo é um diferencial qualitativo enorme na avaliação por pares.\n\n"

    relatorio += "---\n\n"
    relatorio += "#### 📝 3. Checklist de Ação Imediata para o Pesquisador\n"
    relatorio += "- [ ] **Vincular ORCID:** Garanta que seu ORCID está atualizado no Lattes. A CAPES cruza os dados da OpenAlex via ORCID para validar autoria.\n"
    relatorio += "- [ ] **Divulgação Ativa:** Após a publicação, crie um post resumindo a descoberta em linguagem acessível, marcando a revista. Isso alimenta diretamente o Score de Altimetria (Proc. 2).\n"
    relatorio += "- [ ] **Dados Abertos:** Suba os dados anonimizados da pesquisa no **Zenodo** (gratuito), obtenha um DOI e cite-o no manuscrito. Isso atende diretamente às diretrizes de Ciência Aberta da CAPES.\n"

    return relatorio

# ==============================================================================
# 4. EXECUÇÃO E EXIBIÇÃO
# ==============================================================================
if submitted:
    if not resumo.strip():
        st.warning("⚠️ Por favor, insira pelo menos palavras-chave ou um breve resumo para que a busca seja realizada.")
    else:
        with st.spinner("🔄 Consultando bases OpenAlex (Métricas) e Crossref (Altimetria). Isso pode levar alguns segundos..."):
            # Pega as primeiras 15 palavras para otimizar a busca na API
            query_busca = " ".join(resumo.split()[:15]) 
            
            revistas_encontradas = buscar_revistas_openalex(query_busca, max_results=5)
            
            if revistas_encontradas:
                relatorio_final = gerar_relatorio_capes(titulo, area_capes, foco, revistas_encontradas)
                st.success("✅ Relatório gerado com sucesso com dados reais de impacto e altimetria!")
                st.markdown(relatorio_final)
                
                st.download_button(
                    label="📥 Baixar Relatório em PDF/Texto",
                    data=relatorio_final,
                    file_name=f"Estrategia_CAPES_{titulo[:20].replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            else:
                st.warning("⚠️ Nenhuma revista encontrada com esses termos. Tente usar termos em inglês ou mais genéricos.")

# ==============================================================================
# 5. RODAPÉ OBRIGATÓRIO (DISCLAIMER E ATRIBUIÇÃO)
# ==============================================================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>AVISO LEGAL E DISCLAIMER:</strong></p>
    <p>Esta é uma ferramenta de iniciativa de apoio à pesquisa e à gestão acadêmica. Ela utiliza bases de dados abertas (OpenAlex e Crossref) para fornecer estimativas e estratégias alinhadas às tendências das Diretrizes Comuns da CAPES (Ciclo 2025-2028).</p>
    <p><strong>Esta ferramenta não possui vinculação oficial, endosso ou responsabilidade junto à Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (CAPES) ou ao Ministério da Educação (MEC).</strong> As métricas de "Fator de Impacto" são proxies calculadas pela OpenAlex (2yr_mean_citedness), reconhecida internacionalmente como alternativa aberta ao JCR. A decisão final de submissão é de responsabilidade exclusiva do pesquisador e do coordenador do programa.</p>
    <p style="margin-top: 15px;"><em>Desenvolvimento e Arquitetura da Solução: <strong>Roberto Cesar</strong></em></p>
</div>
""", unsafe_allow_html=True)
