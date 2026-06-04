import streamlit as st
import requests
import urllib.parse

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILO
# ==============================================================================
st.set_page_config(
    page_title="Assistente de Estratégia de Publicação CAPES", 
    page_icon="", 
    layout="wide"
)

st.markdown("""
<style>
    .main-header {font-size: 2.2rem; font-weight: bold; color: #1f3a93;}
    .footer {margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.8rem; color: #666; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🎓 Assistente de Estratégia de Publicação (Ciclo CAPES 2025-2028)</p>', unsafe_allow_html=True)
st.markdown("Ferramenta de apoio à decisão para pesquisadores, baseada em dados abertos e nas Diretrizes Comuns da CAPES.")

# ==============================================================================
# 1. ENTRADA DE DADOS
# ==============================================================================
with st.form("dados_pesquisa"):
    st.markdown("### 📝 Dados da Produção Intelectual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input(
            "Título do Artigo ou Tema Geral da Pesquisa",
            help="💡 DICA CAPES: O título ajuda a ferramenta a contextualizar a relevância temática. Isso é fundamental para o Procedimento 3 (Avaliação Qualitativa)."
        )
        
        area_capes = st.selectbox(
            "Grande Área de Avaliação CAPES",
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas e da Terra", 
             "Engenharias", "Ciências Sociais Aplicadas", "Ciências Biológicas", "Linguística, Letras e Artes"],
            help="💡 DICA CAPES: Cada área possui um Documento de Área específico que pondera de forma diferente os Procedimentos 1, 2 e 3."
        )

    with col2:
        resumo = st.text_area(
            "Resumo ou Palavras-chave (Preferencialmente em Inglês)",
            height=120,
            help="💡 DICA CAPES: A ferramenta busca em bases globais (OpenAlex). Usar termos em inglês (ex: 'machine learning', 'public health') retorna revistas com métricas mais precisas."
        )
        
        foco = st.selectbox(
            "Foco da Estratégia de Publicação",
            [
                "Equilibrado (Impacto Tradicional + Ciência Aberta)", 
                "Máximo Impacto Social (Foco em Altimetria / Proc. 2)", 
                "Máximo Tradicional (Foco em Fator de Impacto / Proc. 1)"
            ],
            help="💡 DICA CAPES: O Proc. 1 avalia a revista (JCR). O Proc. 2 avalia o artigo (Altimetria, downloads). O Proc. 3 avalia a narrativa e a Ciência Aberta."
        )
    
    submitted = st.form_submit_button("🔍 Buscar Revistas e Gerar Relatório Estratégico", type="primary")

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
    
    # Fallback
    fallback_url = f"https://api.openalex.org/sources?per-page={max_results}"
    try:
        response = requests.get(fallback_url, timeout=15)
        return response.json().get("results", [])
    except:
        return []

# ==============================================================================
# 3. MOTOR DE RELATÓRIO (Lógica Alinhada à CAPES 2025-2028)
# ==============================================================================
def gerar_relatorio_capes(titulo, area, foco, revistas):
    if not revistas:
        return "⚠️ **Nenhuma revista encontrada com esses termos.**\n\n*Dica:* Tente usar palavras-chave em inglês ou termos mais amplos da sua área."

    relatorio = f"### 📊 Relatório Estratégico de Publicação\n"
    relatorio += f"**Pesquisa:** *{titulo}*\n"
    relatorio += f"**Área CAPES:** {area} | **Estratégia:** {foco}\n\n"
    relatorio += "---\n\n"
    
    relatorio += "#### 🏆 1. Análise de Revistas Sugeridas (Métricas Reais)\n\n"
    relatorio += "| Revista | Acesso | Fator de Impacto (Proxy JCR) | Potencial de Altimetria |\n"
    relatorio += "| :--- | :---: | :---: | :--- |\n"
    
    melhores_opcoes_oa = []
    
    for rev in revistas:
        nome = rev.get("display_name", "Nome não disponível")
        is_oa = rev.get("is_oa", False)
        is_oa_str = "✅ Sim" if is_oa else "❌ Não"
        
        # Métrica 1: Proxy do JCR
        summary_stats = rev.get("summary_stats", {})
        fator_impacto = summary_stats.get("2yr_mean_citedness", 0)
        fi_formatado = f"{fator_impacto:.2f}" if fator_impacto else "N/A"
        
        # Métrica 2: Potencial de Altimetria (Lógica Estratégica)
        citacoes = rev.get("cited_by_count", 0)
        
        if is_oa and citacoes > 5000:
            potencial_alt = "🔥 Alto (OA + Alto Impacto)"
        elif is_oa:
            potencial_alt = "🟢 Médio (OA favorece compartilhamento)"
        else:
            potencial_alt = "🟡 Baixo (Paywall limita alcance social)"
            
        relatorio += f"| **{nome}** | {is_oa_str} | `{fi_formatado}` | {potencial_alt} |\n"
        
        if is_oa:
            melhores_opcoes_oa.append(nome)

    relatorio += "\n---\n\n"
    relatorio += "#### 🎯 2. Estratégia de Pontuação CAPES (Ciclo 2025-2028)\n\n"
    
    relatorio += f"**Análise para a área de {area}:**\n\n"
    relatorio += "📌 **Procedimento 1 (Métricas do Periódico):**\n"
    relatorio += "A CAPES utiliza a OpenAlex como base oficial. O 'Fator de Impacto' exibido acima é o dado que os consultores verão. Para áreas Exatas/Saúde, busque valores > 1.5. Para Humanas, > 0.5 já é considerado bom.\n\n"
    
    relatorio += " **Procedimento 2 (Impacto do Artigo / Altimetria):**\n"
    if melhores_opcoes_oa:
        relatorio += f"✅ **Vantagem:** As revistas marcadas com '🔥 Alto' ou ' Médio' possuem Acesso Aberto. Isso remove barreiras de paywall, permitindo que seu artigo seja baixado e compartilhado no LinkedIn/X. O Crossref e a Altmetric rastreiam esses eventos e a CAPES os valoriza neste procedimento.\n"
    else:
        relatorio += "⚠️ **Atenção:** As revistas sugeridas possuem paywall (🟡 Baixo). Para pontuar no Proc. 2, é **obrigatório** que você deposite a versão 'Preprint' ou 'Pós-print' em um repositório institucional ou no SciELO Preprints, e divulgue esse link aberto.\n\n"
        
    relatorio += "📌 **Procedimento 3 (Avaliação Qualitativa e Ciência Aberta):**\n"
    relatorio += "A CAPES premia a transparência. A simples ação de disponibilizar os dados brutos da pesquisa em repositórios abertos (como Zenodo ou OSF) e citá-los no artigo é um diferencial qualitativo enorme na avaliação por pares.\n\n"

    relatorio += "---\n\n"
    relatorio += "####  3. Checklist de Ação Imediata para o Pesquisador\n"
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
        with st.spinner("🔄 Consultando base OpenAlex e calculando métricas estratégicas..."):
            query_busca = " ".join(resumo.split()[:15]) 
            revistas_encontradas = buscar_revistas_openalex(query_busca, max_results=5)
            
            if revistas_encontradas:
                relatorio_final = gerar_relatorio_capes(titulo, area_capes, foco, revistas_encontradas)
                st.success("✅ Relatório gerado com sucesso!")
                st.markdown(relatorio_final)
                
                st.download_button(
                    label="📥 Baixar Relatório em Texto",
                    data=relatorio_final,
                    file_name=f"Estrategia_CAPES_{titulo[:20].replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            else:
                st.warning("⚠️ Nenhuma revista encontrada com esses termos. Tente usar termos em inglês ou mais genéricos.")

# ==============================================================================
# 5. RODAPÉ OBRIGATÓRIO
# ==============================================================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>AVISO LEGAL E DISCLAIMER:</strong></p>
    <p>Esta é uma ferramenta de iniciativa de apoio à pesquisa e à gestão acadêmica. Ela utiliza bases de dados abertas (OpenAlex) para fornecer estimativas e estratégias alinhadas às tendências das Diretrizes Comuns da CAPES (Ciclo 2025-2028).</p>
    <p><strong>Esta ferramenta não possui vinculação oficial, endosso ou responsabilidade junto à Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (CAPES) ou ao Ministério da Educação (MEC).</strong> As métricas de "Fator de Impacto" são proxies calculadas pela OpenAlex (2yr_mean_citedness), reconhecida internacionalmente como alternativa aberta ao JCR. A decisão final de submissão é de responsabilidade exclusiva do pesquisador e do coordenador do programa.</p>
    <p style="margin-top: 15px;"><em>Desenvolvimento e Arquitetura da Solução: <strong>Roberto Cesar</strong></em></p>
</div>
""", unsafe_allow_html=True)
