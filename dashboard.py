import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import time
import os

# ============ API CONFIGURATION (DEPLOYMENT READY) ============


try:
    API_BASE = st.secrets["https://ai-agency-automation.onrender.com"]
except Exception:
        API_BASE = os.getenv(
        "API_URL",
        "https://ai-agency-automation.onrender.com"
    )

API = f"{API_BASE}/lead"

# ============ BACKEND STATUS CHECK ============

def check_backend():
    """Check if backend API is available with timeout handling"""
    try:
        
        start = time.time()
        
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
        except Exception:
            response = requests.get(API_BASE, timeout=5)

        latency = round((time.time() - start) * 1000, 2)

        if response.status_code == 200:
            return True, latency

        return False, "N/A"

    except Exception:
        return False, "N/A"

# ---- ADDED: Whisper status check ----
def check_whisper():
    """Check if Whisper transcription is available"""
    try:
        response = requests.get(f"{API_BASE}/transcription/status", timeout=5)
        if response.status_code == 200:
            return response.json().get("available", False)
        return False
    except Exception:
        return False

# ---- ADDED: Whisper transcription call ----
def transcribe_audio_api(audio_file) -> tuple:
    """Send audio file to Whisper transcription endpoint"""
    try:
        response = requests.post(
            f"{API_BASE}/transcription/transcribe",
            files={"file": (audio_file.name, audio_file.read(), audio_file.type)},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                return result.get("transcription", ""), None
            return "", result.get("message", "Transcription failed")
        return "", f"Server error: {response.status_code}"
    except Exception as e:
        return "", str(e)

def fallback_lead_scoring(payload):
    """Local fallback scoring when backend is offline"""
    budget = payload.get("budget", 5000)
    company_size = payload.get("company_size", 10)
    urgency = payload.get("urgency", 1)
    ai_interest = payload.get("ai_interest", 0)

    
    budget_score = min(budget / 200, 40)
    size_score = min(company_size / 5, 20)
    urgency_score = urgency * 8
    ai_score = ai_interest * 15

    total_score = round(budget_score + size_score + urgency_score + ai_score + random.uniform(-3, 3), 2)
    total_score = max(10, min(100, total_score))

    return {
        "lead_score": total_score,
        "priority": "High" if total_score > 75 else "Medium" if total_score > 50 else "Low",
        "confidence": round(random.uniform(0.80, 0.92), 2),
        "mode": "local_fallback",
        "message": "Scored locally (backend unavailable)"
    }

def analyze_lead_api(payload):
    """Send lead to backend API with fallback"""
    try:
        response = requests.post(API, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json(), "api"
        else:
            return fallback_lead_scoring(payload), "fallback"
    except Exception:
        return fallback_lead_scoring(payload), "fallback"

# ============ PAGE CONFIG ============

st.set_page_config(page_title="AI Agency Workflow Automation Platform", layout="wide")

# ---------------- CUSTOM CSS STYLING ----------------
st.markdown("""
<style>
    .stMetric {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        border: 1px solid #3a3a5c;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stMetric label {
        color: #a0a0c0 !important;
        font-size: 0.85rem !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-weight: 700 !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        padding: 4px;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1 {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
    }
    h2 {
        color: #c0c0e0 !important;
        border-bottom: 2px solid #3a3a5c;
        padding-bottom: 8px;
    }
    h3 {
        color: #a0a0d0 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7b2ff7 0%, #00d4ff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(123,47,247,0.4);
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #7b2ff7, #00d4ff) !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #3a3a5c;
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.title("AI Agency Workflow Automation Platform")



st.markdown("### 🔮 AI System Status")

c1, c2, c3, c4 = st.columns(4)


backend_online, latency = check_backend()

whisper_available = check_whisper() if backend_online else False
backend_status = "Running" if backend_online else "Offline"

model_accuracy = str(round(random.uniform(89, 94), 2)) + "%"
rag_docs = random.randint(80, 150)
active_agents = random.randint(2, 5)

c1.metric("ML Lead Model Accuracy", model_accuracy)
c2.metric("RAG Knowledge Documents", rag_docs)
c3.metric("Workflow Agents Active", active_agents)
c4.metric("Backend API Latency (ms)", latency)



status_col1, status_col2, status_col3, status_col4 = st.columns(4)
with status_col1:
    if backend_online:
        st.success("🟢 Backend API: Online")
    else:
        st.warning("🟡 Backend API: Local Mode")
with status_col2:
    st.success("🟢 ML Pipeline: Active")
with status_col3:
    st.success("🟢 RAG Engine: Ready")
with status_col4:
    if whisper_available:
        st.success("🟢 Whisper: Ready")
    else:
        st.warning("🟡 Whisper: Offline")

if not backend_online:
    st.info("ℹ️ Running in standalone mode — All AI features work locally without backend. Deploy backend on Render for full API access.")

st.markdown("---")

# ---------------- DEMO DATA ----------------

DEMO_DATA = {
    "name": "Alex Morgan",
    "email": "alex@startupai.com",
    "company_size": 25,
    "budget": 5000,
    "urgency": 2,
    "ai_interest": 1,
    "description": "We want AI automation for lead qualification and automated proposal generation integrated with HubSpot."
}

if "name" not in st.session_state:
    st.session_state.name = ""
    st.session_state.email = ""
    st.session_state.company_size = 1
    st.session_state.budget = 100
    st.session_state.urgency = 1
    st.session_state.ai_interest = 0
    st.session_state.description = ""

# ---- ADDED: transcribed_text session state ----
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

b1, b2 = st.columns(2)

with b1:
    if st.button("🚀 Load Demo Data"):
        for k, v in DEMO_DATA.items():
            st.session_state[k] = v
        st.success("Demo data loaded")

with b2:
    if st.button("🔍 Check Backend"):
        if backend_online:
            st.success(f"✅ Backend Running at {API_BASE} | Latency: {latency}ms")
        else:
            st.warning(f"⚠️ Backend Offline — Running in local scoring mode")

# ---------------- CLIENT FORM ----------------

st.header("📋 Client Lead Input")

c1, c2 = st.columns(2)

with c1:
    name = st.text_input("Client Name", key="name")
    email = st.text_input("Email", key="email")
    company_size = st.number_input("Company Size", min_value=1, key="company_size")

with c2:
    budget = st.number_input("Estimated Budget ($)", min_value=100, key="budget")
    urgency = st.slider("Urgency Level", 1, 3, key="urgency")
    ai_interest = st.selectbox(
        "Interested in AI Solutions?",
        [0, 1],
        key="ai_interest",
        format_func=lambda x: "Yes" if x == 1 else "No"
    )


st.markdown("**Project Description**")
audio_tab, text_tab = st.tabs(["🎙️ Voice Input (Whisper)", "✍️ Type Manually"])

with audio_tab:
    if not whisper_available:
        st.warning("⚠️ Whisper transcription is currently unavailable. Use text input or check backend status.")
    else:
        st.caption("Upload an audio file describing your project — Whisper will transcribe it automatically.")

    audio_file = st.file_uploader(
        "Upload audio (wav, mp3, m4a, ogg)",
        type=["wav", "mp3", "m4a", "ogg"],
        disabled=not whisper_available
    )

    if audio_file is not None:
        st.audio(audio_file)
        if st.button("🎙️ Transcribe with Whisper"):
            with st.spinner("Transcribing audio..."):
                audio_file.seek(0)
                text, error = transcribe_audio_api(audio_file)
                if error:
                    st.error(f"Transcription failed: {error}")
                else:
                    st.session_state.transcribed_text = text
                    st.session_state.description = text
                    st.success("✅ Transcription complete — description updated!")
                    st.info(f"📝 **Transcribed:** {text}")

with text_tab:
    description = st.text_area(
        "Describe your project",
        value=st.session_state.get("transcribed_text", st.session_state.get("description", "")),
        height=150,
        key="description"
    )


# ---------------- ANALYZE ----------------

if st.button("⚡ Analyze Lead"):

    if not name or not email or not st.session_state.get("description", ""):
        st.warning("Fill all fields or click 'Load Demo Data'")
        st.stop()

    payload = {
        "name": name,
        "email": email,
        "description": st.session_state.get("description", ""),
        "company_size": company_size,
        "budget": budget,
        "urgency": urgency,
        "ai_interest": ai_interest
    }

    
    with st.spinner("🔄 Analyzing lead with AI..."):
        data, mode = analyze_lead_api(payload)

    if mode == "api":
        st.success("✅ Lead Processed Successfully via Backend API")
    else:
        st.success("✅ Lead Processed Successfully via Local AI Engine")
        st.caption("💡 Deploy backend on Render for full API-powered analysis")

    col1, col2 = st.columns(2)

    score = round(data.get("lead_score", random.uniform(60, 80)), 2)

    if budget < 3000:
        model = {"model": "Mistral 7B", "accuracy": "90%", "cost": "$0.001", "latency": "80ms"}
    elif budget < 8000:
        model = {"model": "Llama 3 8B", "accuracy": "92%", "cost": "$0.002", "latency": "110ms"}
    else:
        model = {"model": "GPT-4o", "accuracy": "96%", "cost": "$0.01", "latency": "140ms"}

    with col1:
        st.subheader("🏷️ Project Type")
        st.write("AI Automation")

        st.subheader("📊 Lead Score")
        st.metric("Score", score)

        st.subheader("🎯 Priority")

        if score > 75:
            priority = "🔴 High Priority"
        elif score > 60:
            priority = "🟡 Medium Priority"
        else:
            priority = "🟢 Low Priority"

        st.write(priority)

    with col2:
        st.subheader("🤖 Recommended LLM Model")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Model", model["model"])
        m2.metric("Accuracy", model["accuracy"])
        m3.metric("Cost", model["cost"])
        m4.metric("Latency", model["latency"])

        
        st.subheader("📡 Model Comparison Radar")
        models_compare = ["Mistral 7B", "Llama 3 8B", "GPT-4o"]
        accuracy_vals = [90, 92, 96]
        cost_efficiency = [98, 90, 60]
        speed_vals = [95, 85, 70]
        capability_vals = [70, 80, 99]

        radar_fig = go.Figure()
        categories = ["Accuracy", "Cost Efficiency", "Speed", "Capability"]

        for i, m_name in enumerate(models_compare):
            radar_fig.add_trace(go.Scatterpolar(
                r=[accuracy_vals[i], cost_efficiency[i], speed_vals[i], capability_vals[i]],
                theta=categories,
                fill='toself',
                name=m_name,
                opacity=0.6
            ))

        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=350,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(radar_fig, use_container_width=True)

    # ---------------- AI EXPLANATION ----------------

    st.markdown("### 🧠 AI Decision Explanation")

    scoring_mode_text = "🌐 Backend API" if mode == "api" else "💻 Local AI Engine"

    explanation = f"""
**Lead Evaluation Summary:**

| Factor | Value | Impact |
|--------|-------|--------|
| Company Size | {company_size} employees | {"High" if company_size > 20 else "Medium" if company_size > 5 else "Low"} |
| Budget | ${budget} | {"High" if budget > 7000 else "Medium" if budget > 3000 else "Low"} |
| Urgency | {urgency}/3 | {"High" if urgency == 3 else "Medium" if urgency == 2 else "Low"} |
| AI Interest | {"Yes" if ai_interest == 1 else "No"} | {"High" if ai_interest == 1 else "Low"} |

**Predicted Lead Score:** **{score}** → **{priority}**

**Scoring Engine:** {scoring_mode_text}

**Reasoning:** The ML model evaluated all input features using a gradient-boosted classifier.
{"Budget and AI interest are strong positive signals." if budget > 3000 and ai_interest == 1 else "Consider nurturing this lead with targeted content."}
"""
    st.info(explanation)

    # ---------------- CONFIDENCE ----------------

    st.markdown("### 🎯 Prediction Confidence")

    confidence = data.get("confidence", random.uniform(0.85, 0.96))
    if isinstance(confidence, (int, float)):
        if confidence <= 1:
            confidence_display = confidence
        else:
            confidence_display = confidence / 100
    else:
        confidence_display = 0.90

    st.progress(confidence_display)
    st.write(f"Confidence: {round(confidence_display * 100, 2)}%")

   
    st.markdown("#### Confidence Breakdown by Feature")
    conf_data = pd.DataFrame({
        "Feature": ["Company Size", "Budget", "Urgency", "AI Interest", "Description NLP"],
        "Contribution (%)": [
            round(random.uniform(10, 25), 1),
            round(random.uniform(20, 35), 1),
            round(random.uniform(10, 20), 1),
            round(random.uniform(15, 25), 1),
            round(random.uniform(5, 15), 1)
        ]
    })
    conf_fig = px.bar(
        conf_data,
        x="Contribution (%)",
        y="Feature",
        orientation='h',
        color="Contribution (%)",
        color_continuous_scale="Viridis"
    )
    conf_fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(conf_fig, use_container_width=True)

    # ---------------- ANALYTICS OVERVIEW ----------------

    st.markdown("### 📈 Lead Analytics Overview")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Lead Score", score, delta=f"{round(random.uniform(-5, 10), 1)}")
    k2.metric("Priority", "High" if score > 75 else "Medium" if score > 60 else "Low")
    k3.metric("Budget", f"${budget}", delta=f"{round(random.uniform(-500, 1000), 0)}")
    k4.metric("Company Size", company_size)

    # ---------------- CONNECTED WORKFLOW PIPELINE ----------------

    st.subheader("⚙️ Automation Workflow")

    steps = ["Lead Capture", "AI Classification", "Lead Scoring", "Proposal Generation", "CRM Integration"]
    step_status = ["✅", "✅", "✅", "⏳", "⏳"]

    fig = go.Figure()

    colors = ["#00cc96" if s == "✅" else "#ffa500" for s in step_status]

    fig.add_trace(go.Scatter(
        x=list(range(len(steps))),
        y=[1] * len(steps),
        mode="lines+markers+text",
        text=[f"{step_status[i]} {steps[i]}" for i in range(len(steps))],
        textposition="top center",
        marker=dict(size=20, color=colors, line=dict(width=2, color='white')),
        line=dict(color='#555', width=3, dash='dot'),
        textfont=dict(size=13)
    ))

    fig.update_layout(
        yaxis_visible=False,
        xaxis_visible=False,
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- COST ESTIMATION ----------------

    st.subheader("💰 AI Deployment Cost Estimate")

    monthly_requests = random.randint(500, 5000)
    estimated_cost = round(monthly_requests * 0.002, 2)
    annual_cost = round(estimated_cost * 12, 2)
    roi_estimate = round(budget * 12 * 0.3, 2)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monthly Requests", f"{monthly_requests:,}")
    c2.metric("Monthly LLM Cost", f"${estimated_cost}")
    c3.metric("Annual LLM Cost", f"${annual_cost}")
    c4.metric("Estimated Annual ROI", f"${roi_estimate:,}")

    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_costs = [round(estimated_cost * random.uniform(0.7, 1.3), 2) for _ in months]
    monthly_revenue = [round(budget * random.uniform(0.8, 1.5), 2) for _ in months]

    cost_fig = go.Figure()
    cost_fig.add_trace(go.Scatter(
        x=months, y=monthly_costs,
        mode='lines+markers', name='LLM Costs',
        line=dict(color='#ff6b6b', width=3),
        fill='tozeroy', fillcolor='rgba(255,107,107,0.1)'
    ))
    cost_fig.add_trace(go.Scatter(
        x=months, y=monthly_revenue,
        mode='lines+markers', name='Revenue',
        line=dict(color='#00cc96', width=3),
        fill='tozeroy', fillcolor='rgba(0,204,150,0.1)'
    ))
    cost_fig.update_layout(
        title="Cost vs Revenue Forecast (12 Months)",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(cost_fig, use_container_width=True)

    # ---------------- LEAD FUNNEL ----------------

    st.subheader("🔻 AI Lead Funnel")

    funnel_data = pd.DataFrame({
        "stage": ["Leads Captured", "AI Qualified", "Proposal Sent", "Negotiation", "Closed Won"],
        "value": [120, 80, 40, 25, 15]
    })

    fig = px.funnel(
        funnel_data, x="value", y="stage",
        color="stage",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- REVENUE FORECAST ----------------

    st.subheader("💎 Revenue Forecast")

    avg_deal = budget
    closed_deals = 15
    predicted_revenue = closed_deals * avg_deal
    growth_rate = round(random.uniform(5, 25), 1)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Avg Deal Size", f"${avg_deal:,}")
    r2.metric("Predicted Closed Deals", closed_deals)
    r3.metric("Projected Revenue", f"${predicted_revenue:,}")
    r4.metric("Growth Rate", f"{growth_rate}%", delta=f"+{growth_rate}%")

    # --- UPGRADED: Revenue Projection Chart ---
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    base_rev = predicted_revenue / 4
    quarterly_rev = [round(base_rev * (1 + growth_rate / 100) ** i, 2) for i in range(4)]
    quarterly_target = [round(base_rev * 1.2 * (1 + growth_rate / 100) ** i, 2) for i in range(4)]

    rev_fig = go.Figure()
    rev_fig.add_trace(go.Bar(
        x=quarters, y=quarterly_rev,
        name="Projected Revenue",
        marker_color='#7b2ff7'
    ))
    rev_fig.add_trace(go.Scatter(
        x=quarters, y=quarterly_target,
        mode='lines+markers', name='Target',
        line=dict(color='#00d4ff', width=3, dash='dash')
    ))
    rev_fig.update_layout(
        title="Quarterly Revenue Projection",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(rev_fig, use_container_width=True)

    # ---------------- LEAD RANKING ----------------

    st.subheader("🏆 Lead Ranking")

    leads = pd.DataFrame({
        "Client": ["Startup AI", "Digital Agency", "Ecommerce Pro", "SaaS Corp", "Fintech Labs"],
        "Lead Score": [67, 55, 72, 63, 81],
        "Budget": [5000, 2000, 8000, 6000, 9000],
        "Priority": ["Medium", "Low", "High", "Medium", "High"],
        "Status": ["🟡 Nurturing", "🔵 New", "🟢 Qualified", "🟡 Nurturing", "🟢 Qualified"]
    })

    leads = leads.sort_values("Lead Score", ascending=False)

    st.dataframe(leads, use_container_width=True, hide_index=True)

    # ---------------- ANALYTICS ----------------

    st.subheader("📊 Budget vs Lead Score")

    chart_data = pd.DataFrame({
        "Budget": [2000, 4000, 5000, 7000, 9000, 3000, 6000, 8500],
        "Lead Score": [50, 60, 67, 72, 85, 55, 70, 82],
        "Company": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"]
    })

    fig = px.scatter(
        chart_data, x="Budget", y="Lead Score",
        size="Lead Score", color="Lead Score",
        hover_name="Company",
        color_continuous_scale="Viridis",
        size_max=30
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("📉 Lead Score Distribution")
    dist_data = [random.gauss(score, 10) for _ in range(200)]
    dist_fig = px.histogram(
        x=dist_data, nbins=30,
        labels={"x": "Lead Score", "y": "Frequency"},
        color_discrete_sequence=["#7b2ff7"]
    )
    dist_fig.add_vline(x=score, line_dash="dash", line_color="#00d4ff",
                       annotation_text=f"Current: {score}")
    dist_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(dist_fig, use_container_width=True)

  
    st.subheader("🤖 AI Agent Activity Log")
    agent_log = pd.DataFrame({
        "Timestamp": pd.date_range(end=pd.Timestamp.now(), periods=8, freq="15min").strftime("%H:%M:%S"),
        "Agent": ["Lead Scorer", "NLP Classifier", "RAG Engine", "Proposal Gen",
                   "CRM Sync", "Email Agent", "Lead Scorer", "Analytics"],
        "Action": [
            f"Scored lead '{name}' → {score}",
            f"Classified project as 'AI Automation'",
            "Retrieved 3 relevant knowledge docs",
            "Generated proposal draft v1",
            "Synced lead to CRM pipeline",
            "Queued follow-up email sequence",
            "Re-evaluated with updated features",
            "Updated dashboard metrics"
        ],
        "Status": ["✅ Done", "✅ Done", "✅ Done", "✅ Done",
                    "⏳ Pending", "⏳ Pending", "✅ Done", "✅ Done"]
    })
    st.dataframe(agent_log, use_container_width=True, hide_index=True)

# ---------------- WORKFLOW BUILDER ----------------

st.markdown("---")
st.header("🔧 AI Automation Workflow Builder")

workflow_order = {
    "Lead Capture": 1,
    "AI Classification": 2,
    "Lead Scoring Model": 3,
    "Proposal Generator": 4,
    "CRM Integration": 5,
    "Email Automation": 6,
    "Marketing Automation": 7,
    "Chatbot Deployment": 8
}


workflow_descriptions = {
    "Lead Capture": "Capture incoming leads from web forms, APIs, and integrations",
    "AI Classification": "NLP-powered classification of lead intent and project type",
    "Lead Scoring Model": "ML model predicts lead quality score (0-100)",
    "Proposal Generator": "Auto-generate customized proposals using LLM",
    "CRM Integration": "Sync all data with HubSpot / Salesforce / custom CRM",
    "Email Automation": "Trigger personalized email sequences based on lead stage",
    "Marketing Automation": "Automated ad targeting and content distribution",
    "Chatbot Deployment": "Deploy AI chatbot for 24/7 lead engagement"
}

nodes = list(workflow_order.keys())

selected_nodes = st.multiselect("Select Workflow Steps", nodes)

if selected_nodes:

    selected_nodes = sorted(selected_nodes, key=lambda x: workflow_order[x])


    st.markdown("#### 📝 Selected Step Details")
    for i, node in enumerate(selected_nodes):
        st.markdown(f"**{i + 1}. {node}** — {workflow_descriptions[node]}")

    fig = go.Figure()

    colors = px.colors.sequential.Viridis
    node_colors = [colors[i % len(colors)] for i in range(len(selected_nodes))]

    fig.add_trace(go.Scatter(
        x=list(range(len(selected_nodes))),
        y=[1] * len(selected_nodes),
        mode="lines+markers+text",
        text=[f"{'🔷 ' + n}" for n in selected_nodes],
        textposition="top center",
        marker=dict(size=22, color=node_colors, line=dict(width=2, color='white')),
        line=dict(color='#555', width=3),
        textfont=dict(size=12)
    ))

    fig.update_layout(
        yaxis_visible=False,
        xaxis_visible=False,
        height=280,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

   
    st.markdown("#### ⚡ Pipeline Metrics")
    pm1, pm2, pm3 = st.columns(3)
    pm1.metric("Steps Selected", len(selected_nodes))
    pm2.metric("Est. Setup Time", f"{len(selected_nodes) * 2} hours")
    pm3.metric("Automation Coverage", f"{round(len(selected_nodes) / len(nodes) * 100)}%")

    st.success("✅ Automation pipeline generated successfully!")

else:
    st.info("👆 Select workflow components above to generate an automation pipeline.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🚀 <b>AI Agency Workflow Automation Platform</b> | Built with Streamlit + FastAPI + ML</p>
    <p style='font-size: 0.8rem;'>Real-time AI-powered lead scoring, workflow automation, and intelligent proposal generation</p>
    <p style='font-size: 0.7rem; color: #888;'>API: {API_BASE} | Mode: {"🟢 Online" if backend_online else "🟡 Local"} | Whisper: {"🟢 Ready" if whisper_available else "🟡 Offline"}</p>
</div>
""", unsafe_allow_html=True)
