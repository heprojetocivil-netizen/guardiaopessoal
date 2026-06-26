import streamlit as st
from groq import Groq
from datetime import datetime
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GUARDIÃO PESSOAL", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        background-color: #EFF6FF !important;
        color: #000000 !important;
        border: 1px solid #3B82F6 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #1E3A8A, #1D4ED8) !important;
        color: white !important; font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(30,58,138,0.25);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #172554, #1E3A8A) !important; transform: translateY(-1px); }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }
    p, span, label, div { color: #1A1A2E !important; font-family: 'DM Sans', sans-serif; }

    .card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #3B82F6; margin-bottom: 15px;
        color: #1A1A2E; box-shadow: 0 2px 12px rgba(30,58,138,0.08);
        white-space: pre-wrap;
    }
    .card-dark {
        background: linear-gradient(135deg, #0B1120 0%, #0F172A 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #1D4ED8; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-dark, .card-dark * { color: #BFDBFE !important; }

    .card-green {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #86EFAC; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-orange {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FDBA74; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-purple {
        background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #C4B5FD; margin-bottom: 15px;
        white-space: pre-wrap;
    }

    /* ── NÍVEL DE RISCO ── */
    .risco-box {
        border-radius: 18px; padding: 24px; text-align: center; margin: 14px 0;
        border: 2px solid;
    }
    .risco-baixo   { background: linear-gradient(135deg,#F0FDF4,#DCFCE7); border-color:#22C55E; }
    .risco-moderado{ background: linear-gradient(135deg,#FFFBEB,#FEF3C7); border-color:#F59E0B; }
    .risco-elevado { background: linear-gradient(135deg,#FEF2F2,#FEE2E2); border-color:#EF4444; }
    .risco-titulo  { font-family:'Playfair Display',serif; font-size:1.6em; font-weight:700; }

    /* ── EMERGÊNCIA ── */
    .btn-emergencia button {
        background: linear-gradient(135deg, #DC2626, #EF4444) !important;
        box-shadow: 0 4px 20px rgba(220,38,38,0.4) !important;
        font-size: 1.05em !important;
        animation: pulse-emerg 2s infinite;
    }
    @keyframes pulse-emerg {
        0%, 100% { box-shadow: 0 4px 20px rgba(220,38,38,0.4); }
        50% { box-shadow: 0 4px 30px rgba(220,38,38,0.7); }
    }

    .badge         { background: #1D4ED8; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-verde   { background: #22C55E; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-amarelo { background: #F59E0B; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-vermelho{ background: #EF4444; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }

    .stat-box { background: #EFF6FF; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #3B82F6; }
    .stat-numero { font-size: 2em; font-weight: 700; color: #1D4ED8 !important; font-family: 'Playfair Display', serif; }

    .hist-item { background: #EFF6FF; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid #3B82F6; }

    .checklist-item {
        background: #FFFFFF; border: 1px solid #BFDBFE; border-radius: 10px;
        padding: 10px 16px; margin-bottom: 6px;
    }

    .perfil-btn>button {
        background: linear-gradient(135deg, #1E3A8A, #1D4ED8) !important;
        color: white !important; font-weight: 700 !important;
        border-radius: 12px !important; height: 3em !important;
    }

    .disclaimer {
        background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 10px;
        padding: 12px 16px; font-size: 0.8em; color: #475569; margin-top: 14px; line-height: 1.6;
    }

    .divider { border: none; height: 1px; background: linear-gradient(to right, transparent, #3B82F6, transparent); margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_guardiao():
    return {"perfis": {}}

_cache = get_cache_guardiao()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_relatorios', 'relatorios_salvos',
    'cidade_padrao', 'tem_filhos', 'tem_idosos_em_casa',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_relatorio(tipo: str, local: str, conteudo: str):
    st.session_state.historico_relatorios.append({
        'data':     datetime.now().strftime('%d/%m %H:%M'),
        'tipo':     tipo,
        'local':    local,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':                "Login",
    'usuario':              "",
    'api_key':              "",
    'pagina':               "Home",
    'historico_relatorios': [],
    'relatorios_salvos':    [],
    'cidade_padrao':        "",
    'tem_filhos':           False,
    'tem_idosos_em_casa':   False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO ÉTICO COMPARTILHADO EM TODOS OS PROMPTS ---
PRINCIPIO_COMUNICACAO = """
PRINCÍPIO OBRIGATÓRIO DE COMUNICAÇÃO DE RISCO — siga isso em TODA a resposta:
- NUNCA afirme como fato absoluto que um lugar "é perigoso" ou que algo "vai acontecer"
- Use sempre linguagem de probabilidade e prevenção: "esta região apresenta maior registro histórico de determinados tipos de ocorrência",
  "isso não significa que um incidente vá acontecer, mas pode justificar cuidados adicionais"
- Você está fornecendo orientação preventiva geral baseada em padrões conhecidos de segurança urbana — não dados em tempo real
  nem estatísticas oficiais verificadas. Deixe isso implícito no tom, sem precisar repetir a cada frase
- Nunca estigmatize bairros, grupos de pessoas ou regiões inteiras
- O objetivo é AUMENTAR a sensação de preparo e cuidado, NUNCA gerar pânico ou medo excessivo
- Equilibre sempre alertas com reforço de que a esmagadora maioria dos trajetos e situações do dia a dia ocorre sem qualquer incidente
"""

# --- MOTOR DE IA ---
def guardiao_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um consultor especializado em segurança pessoal e prevenção de riscos urbanos.
Usuário: {st.session_state.usuario}.
{PRINCIPIO_COMUNICACAO}
{system_extra}
Seja prático, específico e útil. Escreva em português brasileiro, tom calmo e responsável — nunca alarmista."""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total  = len(st.session_state.historico_relatorios)
    salvos = len(st.session_state.relatorios_salvos)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#EFF6FF;border:1px solid #3B82F6;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} relatórios gerados · {salvos} salvos</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"guardiao_pessoal_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

def renderizar_nivel_risco(texto: str):
    """Detecta o nível de risco mencionado no texto e renderiza o card visual."""
    texto_lower = texto.lower()
    if "elevado" in texto_lower or "🔴" in texto:
        nivel, classe, emoji = "ELEVADO", "risco-elevado", "🔴"
    elif "moderado" in texto_lower or "🟡" in texto:
        nivel, classe, emoji = "MODERADO", "risco-moderado", "🟡"
    else:
        nivel, classe, emoji = "BAIXO", "risco-baixo", "🟢"

    st.markdown(f"""
    <div class="risco-box {classe}">
        <div style="font-size:2.5em;">{emoji}</div>
        <div class="risco-titulo">NÍVEL DE RISCO: {nivel}</div>
        <div style="font-size:0.85em;color:#555;margin-top:6px;">Estimativa preventiva baseada nas informações fornecidas</div>
    </div>
    """, unsafe_allow_html=True)

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Importante:</strong> este relatório é uma orientação preventiva geral gerada por IA, baseada em padrões conhecidos
de segurança urbana — não é um dado oficial de criminalidade nem uma garantia de que algo vai ou não acontecer.
Use como apoio para tomar precauções, não como verdade absoluta sobre qualquer região ou pessoa.
Em caso de emergência real, ligue para a Polícia (190) ou o serviço de emergência local.
</div>
"""

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🛡️ GUARDIÃO PESSOAL")
        st.markdown("**Seu consultor inteligente de segurança e prevenção de riscos**")

        st.markdown("""<div style="background:#EFF6FF;border:1px solid #3B82F6;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#1D4ED8;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # ── PERFIS SALVOS NO SERVIDOR ─────────────────────────
        perfis = perfis_salvos()
        if perfis:
            st.markdown("#### 🛡️ Guardião Pessoal — clique para acessar seus dados")
            st.caption("Seus relatórios estão no servidor. Um clique e você entra.")
            chave_rapida = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for nome_p in perfis:
                dados_p = carregar_perfil_cache(nome_p)
                total_p = len(dados_p.get('historico_relatorios', [])) if dados_p else 0
                cidade_p= dados_p.get('cidade_padrao', '') if dados_p else ''
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(
                    f"🛡️ {nome_p}  —  {total_p} relatórios  {('· ' + cidade_p) if cidade_p else ''}",
                    key=f"perfil_{nome_p}",
                    use_container_width=True
                ):
                    if not chave_rapida.strip():
                        st.warning("Cole sua chave API acima antes de entrar.")
                    else:
                        st.session_state.usuario = nome_p
                        st.session_state.api_key = chave_rapida
                        carregar_json_sessao(dados_p)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("**Ou entre com outro nome:**")

        nome  = st.text_input("Seu Nome:")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            st.markdown("""<div style="background:#EFF6FF;border:1px solid #3B82F6;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#1A1A2E;line-height:1.7;margin:10px 0;">
            📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — tudo volta como era.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None

        dados_login = None
        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                nome_login  = dados_login.get('usuario', '')
                st.success(f"✅ Dados de **{nome_login}** reconhecidos! Clique em Entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None

        if st.button("✨ ENTRAR E SE PROTEGER"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#1D4ED8;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    # ── BOTÃO DE EMERGÊNCIA — sempre visível no topo ──
    st.markdown('<div class="btn-emergencia">', unsafe_allow_html=True)
    if st.button("🚨 MODO EMERGÊNCIA — PRECISO DE AJUDA AGORA", key="btn_emerg_top", use_container_width=True):
        st.session_state.pagina = "Emergencia"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # NAVBAR
    cols = st.columns(8)
    paginas_nav = [
        ("🏠", "Home"), ("🚶", "Trajeto"), ("🏨", "Viagem"), ("🏠2", "Residencia"),
        ("👶", "Infantil"), ("👵", "Idosos"), ("📱", "Golpes"), ("📚", "Biblioteca"),
    ]
    nomes_nav = {
        "Home": "Painel Principal", "Trajeto": "Análise de Trajeto",
        "Viagem": "Segurança em Viagem", "Residencia": "Segurança Residencial",
        "Infantil": "Segurança Infantil", "Idosos": "Segurança para Idosos",
        "Golpes": "Guia de Golpes Comuns", "Biblioteca": "Biblioteca de Relatórios",
    }
    for i, (icone, pagina) in enumerate(paginas_nav):
        if cols[i].button(icone, key=f"nav_{pagina}", help=nomes_nav[pagina]):
            st.session_state.pagina = pagina
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ========================
    # HOME
    # ========================
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🛡️")
            st.markdown("<span class='badge'>Modo Proteção Ativo</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_relatorios) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### ⚙️ Seu perfil")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.session_state.cidade_padrao = st.text_input("Sua cidade:", value=st.session_state.cidade_padrao, placeholder="ex: São Paulo, SP")
        with col_b:
            st.session_state.tem_filhos = st.checkbox("👶 Tenho filhos", value=st.session_state.tem_filhos)
        with col_c:
            st.session_state.tem_idosos_em_casa = st.checkbox("👵 Tenho idosos em casa", value=st.session_state.tem_idosos_em_casa)

        st.markdown("<br>", unsafe_allow_html=True)

        tipos = {}
        for r in st.session_state.historico_relatorios:
            tipos[r['tipo']] = tipos.get(r['tipo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_relatorios)}</div><div>Relatórios gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.relatorios_salvos)}</div><div>Salvos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Trajeto',0)}</div><div>Trajetos analisados</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Residência',0)}</div><div>Análises residenciais</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>💡 <em>'Prevenção não é viver com medo. É viver com preparo.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "🚶 Trajeto":      "Analisa seu deslocamento — origem, destino, meio de transporte e horário — e gera relatório de risco",
            "🏨 Viagem":       "Segurança específica para quando você for viajar — região, golpes contra turistas, apps recomendados",
            "🏠 Residência":   "Avalia a segurança da sua casa, apartamento ou condomínio com sugestões práticas",
            "👶 Infantil":     "Orientações de segurança para quando os filhos saem sozinhos ou ficam em casa",
            "👵 Idosos":       "Cuidados de segurança específicos para idosos — em casa e em deslocamentos",
            "📱 Golpes":       "Explicação detalhada dos golpes mais comuns e como se proteger de cada um",
            "📚 Biblioteca":   "Todos os relatórios salvos, organizados para consulta",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_relatorios:
            st.markdown("### 🕐 Últimos Relatórios")
            for item in reversed(st.session_state.historico_relatorios[-4:]):
                st.markdown(
                    f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> "
                    f"<small style='color:#888'>{item['data']}</small><br>"
                    f"<small>{item['local'][:80]}</small></div>", unsafe_allow_html=True)

    # ========================
    # ANÁLISE DE TRAJETO
    # ========================
    elif st.session_state.pagina == "Trajeto":
        st.header("🚶 Análise de Trajeto")
        st.markdown("Informe seu deslocamento e receba um relatório preventivo completo.")

        col1, col2 = st.columns(2)
        with col1:
            origem = st.text_input("📍 De onde você sai:", value=st.session_state.cidade_padrao, placeholder="ex: Bairro Centro, São Paulo")
            destino = st.text_input("📍 Para onde vai:", placeholder="ex: Bairro Vila Madalena, São Paulo")
            transporte = st.selectbox("🚶 Meio de transporte:", ["A pé", "Bicicleta", "Moto", "Carro", "Transporte público (ônibus/metrô)", "Aplicativo (Uber/99)"])
        with col2:
            horario = st.selectbox("🕒 Horário da saída:", [
                "Manhã (6h-12h)", "Tarde (12h-18h)", "Início da noite (18h-21h)", "Noite (21h-00h)", "Madrugada (00h-6h)",
            ])
            companhia = st.radio("👤 Você vai:", ["Sozinho(a)", "Acompanhado(a)"], horizontal=True)
            modelo_veiculo = ""
            if transporte in ["Carro", "Moto"]:
                modelo_veiculo = st.text_input("🚗 Modelo do veículo (opcional):", placeholder="ex: Honda Civic, Honda CG 160...")

        if st.button("🛡️ GERAR RELATÓRIO DE SEGURANÇA"):
            if origem.strip() and destino.strip():
                with st.spinner("Analisando seu trajeto..."):
                    prompt = (
                        f"Crie um relatório preventivo de segurança para este trajeto.\n"
                        f"Origem: {origem}. Destino: {destino}. Transporte: {transporte}.\n"
                        f"Horário: {horario}. Companhia: {companhia}.\n"
                        f"{'Veículo: ' + modelo_veiculo if modelo_veiculo else ''}\n\n"
                        f"FORMATO OBRIGATÓRIO:\n\n"
                        f"📊 NÍVEL DE RISCO: [🟢 Baixo / 🟡 Moderado / 🔴 Elevado]\n"
                        f"[1-2 linhas explicando essa estimativa preventiva — baseada em horário, tipo de trajeto, companhia]\n\n"
                        f"⚠️ PRINCIPAIS PONTOS DE ATENÇÃO NESTA ROTA:\n"
                        f"[Liste 3-5 tipos de ocorrência mais comuns para esse tipo de trajeto/horário — furto de celular, abordagens, etc — "
                        f"sempre com linguagem preventiva, nunca afirmativa]\n\n"
                        + (f"🚗 SEGURANÇA DO VEÍCULO:\n"
                           f"[Cuidados específicos para {modelo_veiculo or transporte} nesse horário e trajeto — onde estacionar, o que evitar]\n\n" if transporte in ["Carro","Moto"] else "")
                        + f"📱 GOLPES COMUNS NESSE TIPO DE DESLOCAMENTO:\n"
                        f"[1-2 golpes mais relevantes para esse contexto específico, com explicação rápida de como funcionam]\n\n"
                        f"💡 RECOMENDAÇÕES PRÁTICAS PARA ESTE TRAJETO:\n"
                        f"[3-5 ações concretas — rota alternativa, app de localização, horário melhor, etc]\n\n"
                        f"🎒 CHECKLIST RÁPIDO ANTES DE SAIR:\n"
                        f"☑ [item 1]\n☑ [item 2]\n☑ [item 3]\n☑ [item 4]\n☑ [item 5]"
                    )
                    res = guardiao_ia(prompt)
                    salvar_relatorio("Trajeto", f"{origem} → {destino}", res)
                    st.session_state['trajeto_temp'] = res
                    renderizar_nivel_risco(res)
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
                    st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            else:
                st.warning("Informe origem e destino.")

        if st.session_state.get('trajeto_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar relatório (.txt)", data=st.session_state['trajeto_temp'],
                    file_name="relatorio_trajeto.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar relatório", use_container_width=True):
                    st.session_state.relatorios_salvos.append({
                        'tipo': 'Trajeto', 'local': f"{origem} → {destino}" if 'origem' in dir() else '',
                        'conteudo': st.session_state['trajeto_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # SEGURANÇA EM VIAGEM
    # ========================
    elif st.session_state.pagina == "Viagem":
        st.header("🏨 Segurança em Viagem")
        st.markdown("Cuidados específicos para o destino que você vai visitar.")

        col1, col2 = st.columns(2)
        with col1:
            destino_viagem = st.text_input("✈️ Destino da viagem:", placeholder="ex: Rio de Janeiro, Cancún, Lisboa...")
            tipo_viagem = st.selectbox("🎯 Tipo de viagem:", ["Turismo/lazer", "Negócios", "Visita a família", "Mochilão/econômica"])
            hospedagem = st.selectbox("🏨 Tipo de hospedagem:", ["Hotel", "Airbnb/casa alugada", "Hostel", "Casa de família/amigos"])
        with col2:
            perfil_viajante = st.selectbox("👤 Perfil:", ["Sozinho(a)", "Casal", "Família com crianças", "Grupo de amigos", "Mulher viajando sozinha"])
            bairro_destino = st.text_input("📍 Bairro/região específica (se souber):", placeholder="ex: Copacabana, Centro Histórico...")

        if st.button("🛡️ GERAR RELATÓRIO DE SEGURANÇA DA VIAGEM"):
            if destino_viagem.strip():
                with st.spinner("Analisando segurança do destino..."):
                    prompt = (
                        f"Crie um relatório preventivo de segurança para viagem.\n"
                        f"Destino: {destino_viagem}. Bairro/região: {bairro_destino or 'não especificado'}.\n"
                        f"Tipo de viagem: {tipo_viagem}. Hospedagem: {hospedagem}. Perfil: {perfil_viajante}.\n\n"
                        f"FORMATO OBRIGATÓRIO:\n\n"
                        f"📊 NÍVEL DE RISCO GERAL DO DESTINO: [🟢 Baixo / 🟡 Moderado / 🔴 Elevado]\n"
                        f"[1-2 linhas com a estimativa preventiva]\n\n"
                        f"🏙️ SOBRE A REGIÃO:\n"
                        f"[Visão geral preventiva sobre {destino_viagem}{' / ' + bairro_destino if bairro_destino else ''} — pontos fortes e cuidados gerais]\n\n"
                        f"📱 GOLPES COMUNS CONTRA TURISTAS NESSE TIPO DE DESTINO:\n"
                        f"[2-4 golpes típicos com explicação de como funcionam e como evitar]\n\n"
                        f"🚫 CUIDADOS ESPECÍFICOS PARA {perfil_viajante.upper()}:\n"
                        f"[Orientações direcionadas a esse perfil de viajante]\n\n"
                        f"🗺️ ORIENTAÇÕES GERAIS DE DESLOCAMENTO:\n"
                        f"[Como se locomover com mais segurança nessa região — apps recomendados, transporte a evitar de madrugada, etc]\n\n"
                        f"🏨 SEGURANÇA NA HOSPEDAGEM ({hospedagem}):\n"
                        f"[Cuidados específicos para esse tipo de hospedagem]\n\n"
                        f"📲 APPS RECOMENDADOS PARA ESSE DESTINO:\n"
                        f"[Apps de transporte, mapas, tradução, emergência — relevantes para esse lugar]\n\n"
                        f"🎒 CHECKLIST DE VIAGEM SEGURA:\n"
                        f"☑ [item 1]\n☑ [item 2]\n☑ [item 3]\n☑ [item 4]\n☑ [item 5]"
                    )
                    res = guardiao_ia(prompt)
                    salvar_relatorio("Viagem", destino_viagem, res)
                    st.session_state['viagem_temp'] = res
                    renderizar_nivel_risco(res)
                    st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)
                    st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            else:
                st.warning("Informe o destino da viagem.")

        if st.session_state.get('viagem_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar relatório (.txt)", data=st.session_state['viagem_temp'],
                    file_name="relatorio_viagem.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar relatório", key="sv_viagem", use_container_width=True):
                    st.session_state.relatorios_salvos.append({
                        'tipo': 'Viagem', 'local': destino_viagem if 'destino_viagem' in dir() else '',
                        'conteudo': st.session_state['viagem_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # SEGURANÇA RESIDENCIAL
    # ========================
    elif st.session_state.pagina == "Residencia":
        st.header("🏠 Segurança Residencial")
        st.markdown("Avaliação preventiva da sua casa, apartamento ou condomínio.")

        col1, col2 = st.columns(2)
        with col1:
            tipo_moradia = st.selectbox("🏠 Tipo de moradia:", ["Casa térrea", "Casa com mais de 1 andar", "Apartamento", "Apartamento em condomínio fechado", "Sítio/zona rural"])
            bairro_casa = st.text_input("📍 Bairro/cidade:", value=st.session_state.cidade_padrao, placeholder="ex: Bairro Jardins, São Paulo")
            tem_portao = st.radio("🚪 Tem portão/grade na entrada?", ["Sim", "Não"], horizontal=True)
        with col2:
            tem_cameras = st.radio("📷 Já tem câmeras instaladas?", ["Sim", "Não"], horizontal=True)
            tem_alarme = st.radio("🔔 Já tem alarme?", ["Sim", "Não"], horizontal=True)
            moradores = st.selectbox("👥 Quem mora na casa:", ["Sozinho(a)", "Casal sem filhos", "Família com crianças", "Família com idosos", "Compartilhada (república/colegas)"])

        pontos_fracos = st.text_area("⚠️ Pontos que você já considera vulneráveis (opcional):", height=80,
            placeholder="ex: muro baixo nos fundos, rua pouco iluminada, fico muito tempo viajando...")

        if st.button("🛡️ GERAR ANÁLISE DE SEGURANÇA RESIDENCIAL"):
            if bairro_casa.strip():
                with st.spinner("Analisando sua residência..."):
                    prompt = (
                        f"Crie uma análise preventiva de segurança residencial.\n"
                        f"Tipo de moradia: {tipo_moradia}. Bairro: {bairro_casa}.\n"
                        f"Portão: {tem_portao}. Câmeras: {tem_cameras}. Alarme: {tem_alarme}.\n"
                        f"Moradores: {moradores}. Pontos já identificados: {pontos_fracos or 'nenhum informado'}.\n\n"
                        f"FORMATO OBRIGATÓRIO:\n\n"
                        f"📊 NÍVEL DE VULNERABILIDADE ESTIMADO: [🟢 Baixo / 🟡 Moderado / 🔴 Elevado]\n"
                        f"[1-2 linhas explicando a estimativa com base no que foi informado]\n\n"
                        f"💡 ILUMINAÇÃO:\n"
                        f"[Recomendações específicas para {tipo_moradia}]\n\n"
                        f"📷 CÂMERAS E MONITORAMENTO:\n"
                        f"[Sugestões de pontos estratégicos — considerando que {tem_cameras.lower()} já tem]\n\n"
                        f"🔒 FECHADURAS E TRANCAS:\n"
                        f"[Recomendações de tipo de fechadura e pontos de reforço]\n\n"
                        f"🔔 ALARME E SENSORES:\n"
                        f"[Sugestões considerando que {tem_alarme.lower()} já tem]\n\n"
                        f"🚪 ROTINA DE CHEGADA E SAÍDA:\n"
                        f"[Hábitos seguros específicos para {moradores}]\n\n"
                        f"🎯 PONTOS VULNERÁVEIS A REVISAR:\n"
                        f"[Baseado no tipo de moradia e no que foi informado, incluindo: {pontos_fracos or 'pontos genéricos comuns a esse tipo de moradia'}]\n\n"
                        f"📋 PLANO DE AÇÃO — PRIORIDADES:\n"
                        f"1. [ação mais urgente]\n2. [ação 2]\n3. [ação 3]\n4. [ação 4]"
                    )
                    res = guardiao_ia(prompt)
                    salvar_relatorio("Residência", f"{tipo_moradia} — {bairro_casa}", res)
                    st.session_state['residencia_temp'] = res
                    renderizar_nivel_risco(res)
                    st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)
                    st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            else:
                st.warning("Informe o bairro/cidade.")

        if st.session_state.get('residencia_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar análise (.txt)", data=st.session_state['residencia_temp'],
                    file_name="seguranca_residencial.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar análise", key="sv_resid", use_container_width=True):
                    st.session_state.relatorios_salvos.append({
                        'tipo': 'Residência', 'local': bairro_casa if 'bairro_casa' in dir() else '',
                        'conteudo': st.session_state['residencia_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # SEGURANÇA INFANTIL
    # ========================
    elif st.session_state.pagina == "Infantil":
        st.header("👶 Segurança Infantil")
        st.markdown("Orientações preventivas para a segurança dos seus filhos.")

        situacao_infantil = st.text_area(
            "📝 Descreva a situação:",
            height=100,
            placeholder="ex: Meu filho de 10 anos vai sozinho para a escola, caminhando 4 quadras pela manhã...",
        )

        col1, col2 = st.columns(2)
        with col1:
            idade_crianca = st.selectbox("👶 Idade da criança/adolescente:", ["Até 6 anos", "7 a 9 anos", "10 a 12 anos", "13 a 15 anos", "16 a 17 anos"])
            tem_celular = st.radio("📱 Tem celular?", ["Sim", "Não"], horizontal=True)
        with col2:
            frequencia = st.selectbox("🔁 Frequência da situação:", ["Diária", "Algumas vezes por semana", "Ocasional", "Primeira vez"])

        if st.button("🛡️ GERAR ORIENTAÇÕES DE SEGURANÇA"):
            if situacao_infantil.strip():
                with st.spinner("Preparando orientações..."):
                    prompt = (
                        f"Crie orientações preventivas de segurança infantil para esta situação.\n"
                        f"Situação: {situacao_infantil}\n"
                        f"Idade: {idade_crianca}. Tem celular: {tem_celular}. Frequência: {frequencia}.\n\n"
                        f"FORMATO OBRIGATÓRIO:\n\n"
                        f"📊 NÍVEL DE ATENÇÃO RECOMENDADO: [🟢 Baixo / 🟡 Moderado / 🔴 Elevado]\n"
                        f"[1-2 linhas explicando — considerando idade e contexto, sem alarmismo]\n\n"
                        f"⚠️ PRINCIPAIS PONTOS DE ATENÇÃO NESSA SITUAÇÃO:\n"
                        f"[3-4 pontos relevantes para essa idade e contexto específico]\n\n"
                        f"💬 CONVERSA COM A CRIANÇA/ADOLESCENTE:\n"
                        f"[Como conversar sobre isso de forma apropriada para a idade, sem assustar]\n\n"
                        f"📱 USO DE TECNOLOGIA PARA SEGURANÇA:\n"
                        f"[Apps de localização, como configurar, o que é apropriado para essa idade — considerando que {tem_celular.lower()} tem celular]\n\n"
                        f"🎯 ORIENTAÇÕES PRÁTICAS PARA A CRIANÇA:\n"
                        f"[O que ensinar — sinais de alerta, o que fazer em situações específicas, palavra-código com a família, etc]\n\n"
                        f"👨‍👩‍👧 ORIENTAÇÕES PARA OS PAIS/RESPONSÁVEIS:\n"
                        f"[Rotina de checagem, combinados, plano B em caso de imprevisto]\n\n"
                        f"📋 CHECKLIST DE PREPARO:\n"
                        f"☑ [item 1]\n☑ [item 2]\n☑ [item 3]\n☑ [item 4]"
                    )
                    res = guardiao_ia(prompt, "Você está orientando pais/responsáveis sobre segurança infantil. Seja acolhedor, nunca alarmista, e sempre apropriado para a idade da criança mencionada.")
                    salvar_relatorio("Infantil", situacao_infantil[:60], res)
                    st.session_state['infantil_temp'] = res
                    renderizar_nivel_risco(res)
                    st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)
                    st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            else:
                st.warning("Descreva a situação.")

        if st.session_state.get('infantil_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar orientações (.txt)", data=st.session_state['infantil_temp'],
                    file_name="seguranca_infantil.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_infantil", use_container_width=True):
                    st.session_state.relatorios_salvos.append({
                        'tipo': 'Infantil', 'local': situacao_infantil[:60] if 'situacao_infantil' in dir() else '',
                        'conteudo': st.session_state['infantil_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # SEGURANÇA PARA IDOSOS
    # ========================
    elif st.session_state.pagina == "Idosos":
        st.header("👵 Segurança para Idosos")
        st.markdown("Cuidados preventivos específicos para a segurança de idosos — em casa e fora dela.")

        situacao_idoso = st.text_area(
            "📝 Descreva a situação:",
            height=100,
            placeholder="ex: Minha mãe de 75 anos mora sozinha e sai para o mercado a pé todos os dias...",
        )

        col1, col2 = st.columns(2)
        with col1:
            contexto_idoso = st.selectbox("📍 Contexto principal:", [
                "Mora sozinho(a)", "Mora com família mas fica sozinho(a) em parte do dia",
                "Sai com frequência para compromissos", "Recebe visitas/prestadores de serviço em casa",
                "Usa transporte público ou aplicativos", "Tem dificuldade de locomoção",
            ])
        with col2:
            usa_celular_idoso = st.radio("📱 Usa celular/smartphone?", ["Sim, com facilidade", "Sim, com dificuldade", "Não usa"], horizontal=True)

        if st.button("🛡️ GERAR ORIENTAÇÕES DE SEGURANÇA"):
            if situacao_idoso.strip():
                with st.spinner("Preparando orientações..."):
                    prompt = (
                        f"Crie orientações preventivas de segurança para idosos.\n"
                        f"Situação: {situacao_idoso}\n"
                        f"Contexto: {contexto_idoso}. Uso de celular: {usa_celular_idoso}.\n\n"
                        f"FORMATO OBRIGATÓRIO:\n\n"
                        f"📊 NÍVEL DE ATENÇÃO RECOMENDADO: [🟢 Baixo / 🟡 Moderado / 🔴 Elevado]\n"
                        f"[1-2 linhas explicando — respeitoso com a autonomia do idoso, sem infantilizar]\n\n"
                        f"⚠️ PRINCIPAIS PONTOS DE ATENÇÃO NESSA SITUAÇÃO:\n"
                        f"[3-4 pontos relevantes — incluindo golpes comuns contra idosos, como falsa central bancária, falso parente, etc, se aplicável]\n\n"
                        f"📱 TECNOLOGIA DE APOIO:\n"
                        f"[Apps de localização compartilhada, botão de emergência, como configurar considerando o nível de uso de celular: {usa_celular_idoso}]\n\n"
                        f"💬 COMO CONVERSAR SOBRE ISSO:\n"
                        f"[Como abordar o tema com o idoso de forma respeitosa, preservando autonomia e dignidade]\n\n"
                        f"🏠 AJUSTES NO AMBIENTE/ROTINA:\n"
                        f"[Sugestões práticas adaptadas ao contexto: {contexto_idoso}]\n\n"
                        f"🚨 GOLPES ESPECÍFICOS CONTRA IDOSOS A EXPLICAR PARA ELE(A):\n"
                        f"[2-3 golpes mais comuns direcionados a idosos, explicados de forma clara]\n\n"
                        f"📋 CHECKLIST DE PREPARO:\n"
                        f"☑ [item 1]\n☑ [item 2]\n☑ [item 3]\n☑ [item 4]"
                    )
                    res = guardiao_ia(prompt, "Você está orientando sobre segurança de idosos. Seja respeitoso com a autonomia e dignidade da pessoa idosa — nunca infantilize ou trate como incapaz.")
                    salvar_relatorio("Idosos", situacao_idoso[:60], res)
                    st.session_state['idosos_temp'] = res
                    renderizar_nivel_risco(res)
                    st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)
                    st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            else:
                st.warning("Descreva a situação.")

        if st.session_state.get('idosos_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar orientações (.txt)", data=st.session_state['idosos_temp'],
                    file_name="seguranca_idosos.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_idosos", use_container_width=True):
                    st.session_state.relatorios_salvos.append({
                        'tipo': 'Idosos', 'local': situacao_idoso[:60] if 'situacao_idoso' in dir() else '',
                        'conteudo': st.session_state['idosos_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # GUIA DE GOLPES COMUNS
    # ========================
    elif st.session_state.pagina == "Golpes":
        st.header("📱 Guia de Golpes Comuns")
        st.markdown("Entenda como funcionam os golpes mais comuns para reconhecê-los antes que aconteçam.")

        golpes_predefinidos = [
            "Golpe da maquininha", "Golpe do Pix", "Falso motoboy/entregador",
            "Falsa central bancária", "Golpe do WhatsApp clonado", "Golpe do falso sequestro",
            "Golpe do amor (romance scam)", "Golpe do boleto falso", "Golpe da falsa promoção/sorteio",
            "Golpe do suporte técnico falso", "Outro (descrever)",
        ]
        golpe_selecionado = st.selectbox("📋 Qual golpe você quer entender:", golpes_predefinidos)

        descricao_extra = ""
        if golpe_selecionado == "Outro (descrever)":
            descricao_extra = st.text_area("Descreva a situação suspeita:", height=80,
                placeholder="ex: Recebi uma mensagem dizendo que ganhei um prêmio e preciso pagar uma taxa...")

        if st.button("📱 EXPLICAR ESSE GOLPE"):
            with st.spinner("Preparando explicação..."):
                topico = descricao_extra if golpe_selecionado == "Outro (descrever)" and descricao_extra.strip() else golpe_selecionado
                prompt = (
                    f"Explique detalhadamente como funciona: {topico}\n\n"
                    f"FORMATO:\n\n"
                    f"📱 {topico.upper()}\n\n"
                    f"🎭 COMO FUNCIONA:\n"
                    f"[Explicação passo a passo de como os criminosos aplicam esse golpe]\n\n"
                    f"🚩 SINAIS DE ALERTA:\n"
                    f"[3-5 sinais que indicam que você pode estar sendo vítima desse golpe]\n\n"
                    f"🛡️ COMO SE PROTEGER:\n"
                    f"[Ações preventivas concretas]\n\n"
                    f"⚡ O QUE FAZER SE JÁ CAIU NESSE GOLPE:\n"
                    f"[Passos imediatos — bancos, boletim de ocorrência, bloqueios]\n\n"
                    f"📞 CONTATOS ÚTEIS:\n"
                    f"[Telefones/canais relevantes para esse tipo de golpe — banco, polícia, etc]"
                )
                res = guardiao_ia(prompt)
                salvar_relatorio("Golpes", topico, res)
                st.session_state['golpe_temp'] = res
                st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('golpe_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar explicação (.txt)", data=st.session_state['golpe_temp'],
                    file_name="guia_golpe.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_golpe", use_container_width=True):
                    st.session_state.relatorios_salvos.append({
                        'tipo': 'Golpes', 'local': golpe_selecionado if 'golpe_selecionado' in dir() else '',
                        'conteudo': st.session_state['golpe_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # MODO EMERGÊNCIA
    # ========================
    elif st.session_state.pagina == "Emergencia":
        st.header("🚨 Modo Emergência")
        st.markdown("Descreva o que está acontecendo agora. Você vai receber orientações práticas imediatas.")

        st.markdown("""<div style="background:#FEF2F2;border:2px solid #EF4444;border-radius:12px;padding:14px 18px;margin-bottom:16px;">
        🚨 <strong>Se você está em perigo imediato, ligue agora para 190 (Polícia) ou 192 (SAMU).</strong><br>
        Este app complementa, mas nunca substitui o atendimento de emergência oficial.
        </div>""", unsafe_allow_html=True)

        st.markdown("**⚡ Situações comuns — clique para descrever rapidamente:**")
        col_s1, col_s2, col_s3 = st.columns(3)
        sugestoes_emerg = ["Acho que estou sendo seguido(a).", "Acabei de sofrer um golpe.", "Estou em um local que não me sinto seguro(a)."]
        for col, sug in zip([col_s1, col_s2, col_s3], sugestoes_emerg):
            if col.button(f"\"{sug}\"", key=f"sug_emerg_{sug[:15]}"):
                st.session_state['emerg_situacao_input'] = sug

        situacao_emerg = st.text_area(
            "O que está acontecendo:",
            value=st.session_state.get('emerg_situacao_input', ''),
            height=100,
            placeholder="ex: Acho que estou sendo seguido por alguém na rua...",
        )

        if st.button("🚨 PRECISO DE ORIENTAÇÃO AGORA", use_container_width=True):
            if situacao_emerg.strip():
                with st.spinner("..."):
                    prompt = (
                        f"SITUAÇÃO DE EMERGÊNCIA RELATADA: {situacao_emerg}\n\n"
                        f"Dê orientações práticas e imediatas para essa situação específica.\n\n"
                        f"FORMATO:\n\n"
                        f"🚨 ORIENTAÇÃO IMEDIATA\n\n"
                        f"[1-2 frases curtas e firmes reconhecendo a situação — tom calmo mas direto, sem fazer a pessoa esperar]\n\n"
                        f"⚡ AÇÕES IMEDIATAS (agora):\n"
                        f"1. [ação mais urgente e específica para essa situação]\n"
                        f"2. [ação 2]\n"
                        f"3. [ação 3]\n\n"
                        f"📞 QUEM CONTATAR:\n"
                        f"[Números/contatos relevantes para essa situação específica — 190, banco, etc]\n\n"
                        f"📝 DEPOIS QUE A SITUAÇÃO PASSAR:\n"
                        f"[O que fazer depois — boletim de ocorrência, avisar alguém, etc]"
                    )
                    res = guardiao_ia(prompt, "MODO EMERGÊNCIA: seja extremamente direto, prático e calmo. Frases curtas. Sem rodeios. A pessoa precisa de ação, não de teoria.")
                    salvar_relatorio("Emergência", situacao_emerg[:60], res)
                    st.session_state['emergencia_resposta'] = res
            else:
                st.warning("Descreva a situação para receber orientação.")

        if st.session_state.get('emergencia_resposta'):
            st.markdown(f"<div class='card-dark'>{st.session_state['emergencia_resposta']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar orientação (.txt)", data=st.session_state['emergencia_resposta'],
                file_name="orientacao_emergencia.txt", mime="text/plain")

    # ========================
    # BIBLIOTECA
    # ========================
    elif st.session_state.pagina == "Biblioteca":
        st.header("📚 Biblioteca de Relatórios")
        st.markdown("Todos os seus relatórios e análises salvos.")

        if not st.session_state.relatorios_salvos:
            st.info("Biblioteca vazia. Gere relatórios nas outras abas e salve os importantes aqui!")
        else:
            tipos_bib = list(set(r['tipo'] for r in st.session_state.relatorios_salvos))
            filtro = st.selectbox("Filtrar por tipo:", ["Todos"] + tipos_bib)

            rels_filtrados = [
                r for r in st.session_state.relatorios_salvos
                if filtro == "Todos" or r['tipo'] == filtro
            ]

            st.markdown(f"**{len(rels_filtrados)} relatório(s) encontrado(s)**")
            st.markdown("<br>", unsafe_allow_html=True)

            for i, item in enumerate(reversed(rels_filtrados)):
                idx_real = len(st.session_state.relatorios_salvos) - 1 - i
                with st.expander(f"[{item['tipo']}] {item['local']} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name=f"{item['tipo'].lower().replace(' ','_')}.txt",
                            mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.relatorios_salvos.pop(idx_real)
                            st.rerun()

        if st.session_state.historico_relatorios:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 📊 Histórico Completo")
            historico_txt = "\n\n".join(
                f"[{r['data']}] {r['tipo']} — {r['local']}\n{r['conteudo']}\n{'─'*40}"
                for r in st.session_state.historico_relatorios
            )
            st.download_button("⬇️ Exportar todo o histórico (.txt)", data=historico_txt,
                file_name="historico_guardiao.txt", mime="text/plain")

            if st.button("🗑️ Limpar Todo o Histórico"):
                st.session_state.historico_relatorios = []
                st.rerun()

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Guardião Pessoal — Consultor de Segurança e Prevenção com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
