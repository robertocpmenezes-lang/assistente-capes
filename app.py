import streamlit as st
import requests
import urllib.parse

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================
st.set_page_config(
    page_title="Assistente CAPES 2025-2028", 
    page_icon="📊", 
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .journal-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
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
    .metric-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.25rem;
    }
    .badge-yes { background: #c6f6d5; color: #22543d; }
    .badge-no { background: #fed7d7; color: #742a2a; }
    .badge-high { background: #fef5e7; color: #744210; border: 2px solid #f6ad55; }
    .badge-medium { background: #bee3f8; color: #2a4365; }
    .badge-low { background: #e2e8f0; color: #4a5568; }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .metric-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .metric-label { font-size: 0.85rem; color: #718096; font-weight: 600; }
    .metric-value { font-size: 1.3rem; font-weight: 700; color: #2d3748; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Assistente de Estratégia de Publicação CAPES 2025-2028")

# ==============================================================================
# FORMULÁRIO
# ==============================================================================
with st.form("dados_pesquisa"):
    col1, col2 = st.columns(2)
    with col1:
        titulo = st.text_input("📝 Título/Tema")
        area = st.selectbox("📚 Área CAPES", 
            ["Ciências da Saúde", "Ciências Humanas", "Ciências Exatas", 
             "Engenharias", "Ciências Sociais", "Ciências Biológicas"])
    with col2:
        resumo = st.text_area("🔑 Palavras-chave (inglês)", height=100)
        foco = st.selectbox("🎯 Estratégia",
            ["⚖️ Equilibrado", "📢 Impacto Social", "📈 Tradicional"])
    
    submitted = st.form_submit_button("🚀 Gerar Relatório", use_container_width=True)

# ==============================================================================
# FUNÇÕES
# ==============================================================================
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
        st.warning("⚠️ Insira palavras-chave")
    else:
        with st.spinner("Buscando..."):
            query = " ".join(resumo.split()[:15])
            revistas = buscar_revistas(query, max_results=5)
            
            if revistas:
                st.success("✓ Relatório gerado!")
                
                st.markdown("### ✦ Revistas Sugeridas")
                st.info("""
                **Legenda:** 
                - 🟢 Card Verde = Open Access + Alto Impacto (Melhor!)
                - 🔵 Card Azul = Open Access 
                - 🔴 Card Vermelho = Fechado (Paywall)
                """)
                
                melhores_oa = []
                
                for i, rev in enumerate(revistas, 1):
                    nome = rev.get("display_name", "N/A")
                    is_oa = rev.get("is_oa", False)
                    stats = rev.get("summary_stats", {})
                    fi = stats.get("2yr_mean_citedness", 0) or 0
                    citacoes = rev.get("cited_by_count", 0) or 0
                    
                    if is_oa:
                        melhores_oa.append(nome)
                    
                    # Determinar classe do card
                    if is_oa and citacoes > 5000:
                        card_class = "oa-high"
                        alt_text = "🔥 Alto"
                        alt_class = "badge-high"
                    elif is_oa:
                        card_class = "oa-medium"
                        alt_text = "● Médio"
                        alt_class = "badge-medium"
                    else:
                        card_class = "closed"
                        alt_text = "○ Baixo"
                        alt_class = "badge-low"
                    
                    # Badge de acesso
                    acesso_badge = '<span class="metric-badge badge-yes">✓ Aberto</span>' if is_oa else '<span class="metric-badge badge-no">✕ Fechado</span>'
                    
                    # Badge de FI
                    if fi > 5:
                        fi_badge = f'<span class="metric-badge badge-high">⭐ {fi:.2f}</span>'
                        fi_color = "#dd6b20"
                    elif fi > 2:
                        fi_badge = f'<span class="metric-badge badge-medium">{fi:.2f}</span>'
                        fi_color = "#4a5568"
                    else:
                        fi_badge = f'<span class="metric-badge badge-low">{fi:.2f}</span>'
                        fi_color = "#4a5568"
                    
                    # Destaque top 1
                    destaque = "🏆 " if i == 1 else ""
                    
                    # HTML do card (SEM f-strings complexos!)
                    html_card = f'''
                    <div class="journal-card {card_class}">
                        <h3 style="margin: 0 0 1rem 0; color: #2d3748;">{destaque}{nome}</h3>
                        <div>{acesso_badge} <span class="metric-badge {alt_class}">{alt_text}</span></div>
                        <div class="metrics-grid">
                            <div class="metric-item">
                                <div class="metric-label">Fator de Impacto</div>
                                <div class="metric-value" style="color: {fi_color};">{fi:.2f}</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-label">Citações</div>
                                <div class="metric-value">{citacoes:,}</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-label">Ranking</div>
                                <div class="metric-value">#{i}</div>
                            </div>
                        </div>
                    </div>
                    '''
                    
                    st.markdown(html_card, unsafe_allow_html=True)
                
                # Análise
                st.markdown("### ▸ Análise Estratégica")
                st.info(f"**Área:** {area} | **Estratégia:** {foco}")
                
                if "Equilibrado" in foco:
                    st.success("""
                    **✓ Estratégia Recomendada**
                    
                    Priorize revistas com cards **verdes** (Open Access + Alto Impacto).
                    """)
                elif "Impacto" in foco:
                    if melhores_oa:
                        st.success(f"""
                        **📢 Foco em Impacto Social**
                        
                        Revistas Open Access encontradas:
                        {chr(10).join([f"- {r}" for r in melhores_oa])}
                        
                        **Ação:** Compartilhe ativamente nas redes!
                        """)
                    else:
                        st.warning("⚠️ Nenhuma OA encontrada. Deposite preprint!")
                else:
                    st.success("""
                    **📈 Foco Tradicional**
                    
                    Priorize FI > 3.0 (Exatas/Saúde) ou > 1.0 (Humanas).
                    
                    **Importante:** Deposite preprint se for fechada!
                    """)
                
                # Procedimentos
                st.markdown("### ▸ Procedimentos CAPES")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **📊 Proc. 1**
                    
                    Métricas do Periódico
                    
                    FI > 3.0: Excelente
                    FI > 1.5: Bom
                    FI > 0.5: Aceitável
                    """)
                
                with col2:
                    if melhores_oa:
                        st.success("""
                        **📢 Proc. 2
                        
                        Impacto Social
                        
                        ✓ Tem Open Access!
                        
                        **Ação:** Divulgue!
                        """)
                    else:
                        st.warning("""
                        **📢 Proc. 2
                        
                        Impacto Social
                        
                        ⚠ Fechadas
                        
                        **Solução:** Preprint!
                        """)
                
                with col3:
                    st.info("""
                    **✦ Proc. 3
                    
                    Ciência Aberta
                    
                    **Ações:**
                    - Dados no Zenodo
                    - Citar DOI
                    - Preprints
                    - Código aberto
                    """)
                
            else:
                st.warning("⚠️ Nenhuma revista encontrada. Tente termos em inglês.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem; background: #2d3748; color: white; border-radius: 12px;">
    <p><strong>✦ Ferramenta de Apoio à Pesquisa</strong></p>
    <p>OpenAlex + CAPES 2025-2028 | Sem vínculo oficial CAPES/MEC</p>
</div>
""", unsafe_allow_html=True)
