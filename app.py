import streamlit as st
import io
import os
import pandas as pd
import altair as alt
from PIL import Image
from nlp_detector import FakeNewsDetector
from deepfake_detector import DeepfakeDetector
from report_generator import generate_json_report, generate_html_report

# Page Configuration with wide layout
st.set_page_config(
    page_title="AI Integrity Shield Pro | Deepfake & Media Forensics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Elegant Soft Pastel / Warm Slate & Soft Cyan Light Theme (NOT Stark White)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0F172A !important; /* Deep space dark background */
        color: #ffffff !important;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Soft Pastel Blue-Lavender Hero Header */
    .pastel-header {
        position: relative;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #020617 100%);
        border: 1.5px solid #cbd5e1;
        border-radius: 24px;
        padding: 2.3rem 2.7rem;
        margin-bottom: 2rem;
        box-shadow: 0 12px 30px -8px rgba(99, 102, 241, 0.15), 
                    0 2px 4px rgba(0, 0, 0, 0.04);
        overflow: hidden;
    }
    
    .pastel-header::before {
        content: '';
        position: absolute;
        top: -60%;
        right: -10%;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(129, 140, 248, 0.25) 0%, rgba(192, 132, 252, 0.15) 50%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    /* Live Pulsing Dot */
    .pulse-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #0d9488;
        box-shadow: 0 0 10px rgba(13, 148, 136, 0.6);
        margin-right: 8px;
        animation: pulseAnimation 2s infinite;
    }
    
    @keyframes pulseAnimation {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(13, 148, 136, 0.7); }
        70% { transform: scale(1.2); box-shadow: 0 0 0 10px rgba(13, 148, 136, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(13, 148, 136, 0); }
    }

    /* High Contrast Modern Status Badges */
    .badge-authentic-pastel {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.25) 100%);
        color: #34d399;
        border: 1.5px solid #10b981;
        padding: 0.6rem 1.4rem;
        border-radius: 9999px;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 1.05rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        letter-spacing: -0.01em;
    }
    
    .badge-fake-pastel {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.25) 100%);
        color: #f87171;
        border: 1.5px solid #ef4444;
        padding: 0.6rem 1.4rem;
        border-radius: 9999px;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 1.05rem;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
        letter-spacing: -0.01em;
    }

    /* Soft Warm Slate Card Display */
    .token-display-box {
        background: rgba(31,41,55,0.6);
        border: 1.5px solid #cbd5e1;
        border-radius: 16px;
        padding: 1.6rem;
        font-size: 1.05rem;
        line-height: 2.2;
        color: #e2e8f0;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    /* Modern Glassmorphism Severity Indicators */
    .factor-item-critical {
        border-left: 5px solid #ef4444;
        padding: 0.95rem 1.25rem;
        background: rgba(239, 68, 68, 0.12);
        border-radius: 0 14px 14px 0;
        margin-bottom: 0.9rem;
        border-top: 1.5px solid rgba(239, 68, 68, 0.3);
        border-right: 1.5px solid rgba(239, 68, 68, 0.3);
        border-bottom: 1.5px solid rgba(239, 68, 68, 0.3);
    }
    
    .factor-item-warning {
        border-left: 5px solid #f59e0b;
        padding: 0.95rem 1.25rem;
        background: rgba(245, 158, 11, 0.12);
        border-radius: 0 14px 14px 0;
        margin-bottom: 0.9rem;
        border-top: 1.5px solid rgba(245, 158, 11, 0.3);
        border-right: 1.5px solid rgba(245, 158, 11, 0.3);
        border-bottom: 1.5px solid rgba(245, 158, 11, 0.3);
    }

    .factor-item-normal {
        border-left: 5px solid #10b981;
        padding: 0.95rem 1.25rem;
        background: rgba(16, 185, 129, 0.12);
        border-radius: 0 14px 14px 0;
        margin-bottom: 0.9rem;
        border-top: 1.5px solid rgba(16, 185, 129, 0.3);
        border-right: 1.5px solid rgba(16, 185, 129, 0.3);
        border-bottom: 1.5px solid rgba(16, 185, 129, 0.3);
    }

    /* Violet-Cyan Gradient Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #3B82F6 0%, #10B981 50%, #EF4444 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.6rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.28) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4) !important;
    }

    /* Dark Input Fields */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #e2e8f0 !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
    }
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }

    /* Dark Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        background-color: rgba(30, 41, 59, 0.8);
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.25) !important;
        color: #c4b5fd !important;
        border: 1.5px solid rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to render modern horizontal bar charts for dimension scores with soft palette
def render_dimension_chart(dimension_dict: dict, title: str = "Dimension Integrity Audit"):
    df_chart = pd.DataFrame({
        "Metric": list(dimension_dict.keys()),
        "Score": list(dimension_dict.values())
    })
    
    chart = alt.Chart(df_chart).mark_bar(cornerRadius=8, size=22).encode(
        x=alt.X('Score:Q', scale=alt.Scale(domain=[0, 100]), title='Integrity Score (%)'),
        y=alt.Y('Metric:N', sort='-x', title=None),
        color=alt.Color(
            'Score:Q',
            scale=alt.Scale(domain=[40, 70, 100], range=['#e11d48', '#d97706', '#0d9488']),
            legend=None
        ),
        tooltip=['Metric:N', 'Score:Q']
    ).properties(height=240, title=title).configure_axis(
        labelColor='#94a3b8',
        titleColor='#e2e8f0',
        gridColor='rgba(148, 163, 184, 0.15)'
    ).configure_title(
        color='#f8fafc'
    ).configure_view(strokeWidth=0)
    
    st.altair_chart(chart, use_container_width=True)

# Session State Persistence
if "nlp_engine" not in st.session_state:
    st.session_state.nlp_engine = FakeNewsDetector()
if "df_engine" not in st.session_state:
    st.session_state.df_engine = DeepfakeDetector()

nlp_engine = st.session_state.nlp_engine
df_engine = st.session_state.df_engine

# Top Hero Section in Soft Pastel Light Colors
st.markdown("""
<div class="pastel-header">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
        <div style="z-index: 1;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span class="pulse-dot"></span>
                <span style="background: rgba(99, 102, 241, 0.3); color: #c4b5fd; border: 1.5px solid rgba(139, 92, 246, 0.5); font-size: 0.75rem; font-weight: 800; padding: 4px 12px; border-radius: 9999px; letter-spacing: 0.08em; text-transform: uppercase;">
                    Deep Forensics & Media Intelligence
                </span>
                <span style="color: #a78bfa; font-size: 0.85rem; font-weight: 700;">★ Edition 4.5</span>
            </div>
            <h1 style="color: #ffffff; margin: 0; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em; text-shadow: 0 0 30px rgba(99,102,241,0.5);">
                🛡️ AI Integrity Shield
            </h1>
            <p style="color: #cbd5e1; margin-top: 0.6rem; font-size: 1.08rem; max-width: 820px; line-height: 1.6;">
                Intelligent digital verification platform for automated misinformation analysis, image splicing detection, 2D Fourier spectral diagnostics, and camera provenance auditing.
            </p>
        </div>
        <div style="display: flex; gap: 14px; z-index: 1;">
            <div style="background: rgba(99, 102, 241, 0.15); padding: 1rem 1.5rem; border-radius: 16px; border: 1.5px solid rgba(99, 102, 241, 0.4); text-align: center; box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2); backdrop-filter: blur(10px);">
                <div style="font-size: 0.72rem; text-transform: uppercase; color: #a5b4fc; font-weight: 800; letter-spacing: 0.06em;">Language Intelligence</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff; margin-top: 2px;">TF-IDF + Calibrated LR</div>
            </div>
            <div style="background: rgba(14, 165, 233, 0.15); padding: 1rem 1.5rem; border-radius: 16px; border: 1.5px solid rgba(14, 165, 233, 0.4); text-align: center; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.2); backdrop-filter: blur(10px);">
                <div style="font-size: 0.72rem; text-transform: uppercase; color: #7dd3fc; font-weight: 800; letter-spacing: 0.06em;">Vision Diagnostics</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff; margin-top: 2px;">Thermal ELA + 2D FFT</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.subheader("Intelligence Workspace")
    module_choice = st.radio(
        "Select Verification Track:",
        (
            "📰 Fake News NLP Module",
            "🔍 Deepfake & Image Forensics",
            "🌐 Multi-Modal Unified Audit",
            "⚡ Custom Model Retraining Suite"
        ),
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📊 Active Pipeline Specs")
    st.markdown(f"""
    - **Language Model**: Sublinear TF-IDF + Logistic Regression
    - **Corpus Breadth**: {len(nlp_engine.training_samples)} Reference Case Studies
    - **Vision Algorithms**: Thermal ELA, Fourier Radial Ratio, YCbCr Chroma Std
    - **Palette Styling**: Soft Pastel Slate & Lavender
    """)
    st.caption("AI Media Safety & Digital Forensics v4.5")

# ==========================================
# MODULE 1: FAKE NEWS DETECTION
# ==========================================
if module_choice == "📰 Fake News NLP Module":
    st.subheader("📰 Algorithmic Misinformation & Fake News Detection")
    st.write("Semantically audit digital text, press releases, or social claims to evaluate journalistic credibility and detect inflammatory framing patterns.")

    col1, col2 = st.columns([1.15, 0.85], gap="large")

    with col1:
        st.markdown("**⚡ Instant Case Presets:**")
        preset_options = [
            "— Select a preset or type your own —",
            "Preset 1: Official Medical Journal Publication (Peer-reviewed)",
            "Preset 2: Central Monetary Authority Monetary Policy",
            "Preset 3: Viral Miracle Cancer Cure Conspiracy Claim",
            "Preset 4: 5G Network Mind-Control Water Microchip Hoax"
        ]
        chosen_preset = st.selectbox("Load Sample Article:", preset_options, label_visibility="collapsed")

        preset_text_map = {
            "Preset 1: Official Medical Journal Publication (Peer-reviewed)": (
                "Official health authorities and university researchers reported a steady decline in seasonal viral infections "
                "following nationwide preventative vaccination programs. The findings were documented in a peer-reviewed clinical journal."
            ),
            "Preset 2: Central Monetary Authority Monetary Policy": (
                "The central bank announced an adjustment in benchmark interest rates to combat inflation, according to official "
                "economic statistics released by the federal monetary board during their quarterly briefing."
            ),
            "Preset 3: Viral Miracle Cancer Cure Conspiracy Claim": (
                "SHOCKING SECRET: Miracle kitchen fruit cures terminal cancer in 24 hours! Big Pharma wants this deleted immediately! "
                "Exposed proof will blow your mind before it gets banned everywhere!"
            ),
            "Preset 4: 5G Network Mind-Control Water Microchip Hoax": (
                "URGENT: Government insider leaks secret mind-control chips hidden in local drinking tap water and 5G cell towers! "
                "Proof is 100% verified by rogue whistleblowers. Share this viral truth now!"
            )
        }

        default_text = preset_text_map.get(chosen_preset, "")
        
        user_text = st.text_area(
            "Target Text Snippet / Headline:",
            value=default_text,
            height=180,
            placeholder="Paste news headline or article excerpt here..."
        )

        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            analyze_button = st.button("🚀 Run Forensic NLP Analysis", type="primary", use_container_width=True)
        with col_b2:
            if st.button("🧹 Clear Input", use_container_width=True):
                st.rerun()

    with col2:
        st.markdown("### 📊 Verification Verdict")
        if analyze_button:
            if not user_text.strip():
                st.warning("⚠️ Please provide an article snippet or select a preset.")
            else:
                with st.spinner("Decomposing semantic n-grams and stylistic markers..."):
                    result = nlp_engine.analyze_text(user_text)

                if "error" in result:
                    st.error(result["error"])
                else:
                    is_fake = result["verdict"] == "Fake"
                    badge_class = "badge-fake-pastel" if is_fake else "badge-authentic-pastel"
                    badge_icon = "🚨" if is_fake else "🛡️"

                    st.markdown(f"""
                    <div style="margin-bottom: 1.2rem;">
                        <span class="{badge_class}">{badge_icon} {result['prediction']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    m1, m2 = st.columns(2)
                    m1.metric(
                        label="Confidence Score",
                        value=f"{result['confidence']}%",
                        delta=result["risk_level"],
                        delta_color="inverse" if is_fake else "normal"
                    )
                    m2.metric(
                        label="Corpus Alignment",
                        value=f"{result['prob_real']}% Credible",
                        delta=f"{result['prob_fake']}% Misinfo Risk",
                        delta_color="normal" if not is_fake else "inverse"
                    )

                    # Dynamic Progress Bar
                    st.markdown("**Credibility Spectrum:**")
                    st.progress(result["prob_real"] / 100.0)

                    # Dimensional Chart
                    st.markdown("---")
                    render_dimension_chart(result["dimension_scores"], "Linguistic Quality Dimensions")

                    # Highlighted Annotated View
                    st.markdown("---")
                    st.markdown("**Interactive Token Annotation:**")
                    st.markdown(f"<div class='token-display-box'>{result['highlighted_html']}</div>", unsafe_allow_html=True)
                    st.caption("🔴 Red = Clickbait Trigger | 🟢 Green = Institutional Credibility Anchor | 🟠 Orange = Excessive Capitalization")

                    # Explanations
                    st.markdown("---")
                    st.markdown("**Forensic Linguistic Observations:**")
                    for note in result["explanation"]:
                        st.markdown(f"- {note}")

                    # Export Section
                    st.markdown("---")
                    st.markdown("**Export Digital Forensic Certificate:**")
                    rc1, rc2 = st.columns(2)
                    with rc1:
                        j_str = generate_json_report("Fake News NLP Verification", result)
                        st.download_button(
                            label="📥 Download JSON Report",
                            data=j_str,
                            file_name="fake_news_audit.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    with rc2:
                        h_str = generate_html_report("Fake News Verification", result, "Text NLP Analysis")
                        st.download_button(
                            label="📄 Download HTML Certificate",
                            data=h_str,
                            file_name="fake_news_audit.html",
                            mime="text/html",
                            use_container_width=True
                        )
        else:
            st.info("Paste news text or select a preset on the left, then click **Run Forensic NLP Analysis** to execute the pipeline.")

# ==========================================
# MODULE 2: DEEPFAKE DETECTION
# ==========================================
elif module_choice == "🔍 Deepfake & Image Forensics":
    st.subheader("🔍 Deepfake & Image Manipulation Forensics")
    st.write("Multi-factor forensic examination combining localized Error Level Analysis (ELA), 2D Fourier power spectra, and physical camera provenance signatures.")

    col_df1, col_df2 = st.columns([1.1, 0.9], gap="large")

    with col_df1:
        st.markdown("**Target Media Input:**")
        uploaded_file = st.file_uploader(
            "Upload Image (JPG, JPEG, PNG, WEBP):",
            type=["jpg", "jpeg", "png", "webp"]
        )

        sample_choice = st.selectbox(
            "Or load pre-configured forensic reference samples:",
            (
                "— Choose a pre-configured sample —",
                "Sample A: Authentic Nature Photograph (Hardware EXIF + Natural Noise)",
                "Sample B: Spliced Composite Image (Localized ELA Anomaly + Photoshop Signature)",
                "Sample C: Synthetic AI Pattern (High-Frequency Fourier Lattice Peaks)"
            )
        )

        test_image_bytes = None
        test_image_name = "upload.jpg"

        if uploaded_file is not None:
            test_image_bytes = uploaded_file.read()
            test_image_name = uploaded_file.name
        elif "Authentic" in sample_choice:
            sample_path = "samples/authentic_sample.jpg"
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    test_image_bytes = f.read()
                test_image_name = "authentic_sample.jpg"
        elif "Spliced" in sample_choice:
            sample_path = "samples/manipulated_sample.jpg"
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    test_image_bytes = f.read()
                test_image_name = "manipulated_sample.jpg"
        elif "Synthetic" in sample_choice:
            sample_path = "samples/synthetic_sample.jpg"
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    test_image_bytes = f.read()
                test_image_name = "synthetic_sample.jpg"

        if test_image_bytes:
            preview_img = Image.open(io.BytesIO(test_image_bytes))
            st.image(preview_img, caption=f"Active Forensic Target: {test_image_name} ({preview_img.size[0]}x{preview_img.size[1]})", use_container_width=True)
            run_df_button = st.button("🔬 Execute Forensic Vision Audit", type="primary", use_container_width=True)
        else:
            run_df_button = False
            st.info("👆 Upload an image or select a sample from the dropdown to start.")

    with col_df2:
        st.markdown("### 🔬 Authenticity Verdict")
        if test_image_bytes and run_df_button:
            with st.spinner("Extracting localized compression variance, Fourier power spectrum, and EXIF tags..."):
                df_result = df_engine.analyze_image(test_image_bytes, test_image_name)

            if "error" in df_result:
                st.error(df_result["error"])
            else:
                is_manipulated = "Manipulated" in df_result["verdict"] or "Deepfake" in df_result["verdict"]
                badge_class = "badge-fake-pastel" if is_manipulated else "badge-authentic-pastel"
                badge_icon = "🚨" if is_manipulated else "🛡️"

                st.markdown(f"""
                <div style="margin-bottom: 1.2rem;">
                    <span class="{badge_class}">{badge_icon} {df_result['verdict']}</span>
                </div>
                """, unsafe_allow_html=True)

                m1, m2 = st.columns(2)
                m1.metric(
                    label="Authenticity Score",
                    value=f"{df_result['authenticity_score']}/100",
                    delta=df_result["risk_classification"],
                    delta_color="normal" if not is_manipulated else "inverse"
                )
                m2.metric(
                    label="Tampering Probability",
                    value=f"{df_result['manipulation_probability']}%",
                    delta=df_result["status_badge"],
                    delta_color="inverse" if is_manipulated else "normal"
                )

                st.markdown("**Tampering Risk Bar:**")
                st.progress(df_result["manipulation_probability"] / 100.0)

                # Dimensional Chart
                st.markdown("---")
                render_dimension_chart(df_result["forensic_dimensions"], "Forensic Dimension Integrity")

                # Indicators Breakdown
                st.markdown("---")
                st.markdown("#### 🧪 Multi-Factor Forensic Indicators Breakdown")
                
                for ind in df_result["indicators"]:
                    sev = ind["severity"]
                    c_class = "factor-item-critical" if sev == "critical" else ("factor-item-warning" if sev == "warning" else "factor-item-normal")
                    c_badge = "🔴 Critical Anomaly" if sev == "critical" else ("🟡 Variance Alert" if sev == "warning" else "🔵 Natural Sensor Profile")
                    st.markdown(f"""
                    <div class="{c_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <strong style="color: #ffffff; font-size: 0.95rem;">{ind['factor']}</strong>
                            <span style="font-size: 0.8rem; font-weight: 700; color: #cbd5e1;">{c_badge}</span>
                        </div>
                        <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.4;">{ind['details']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Visual Forensics Tabs: ELA Thermal vs Grayscale vs FFT Spectrum
                st.markdown("---")
                st.markdown("#### 🖼️ Visual Diagnostic Maps")
                tab_ela_th, tab_ela_bw, tab_fft = st.tabs(["Thermal ELA Heatmap", "Differential ELA", "2D Fourier Spectrum (FFT)"])

                with tab_ela_th:
                    st.image(
                        df_result["ela_heatmap"],
                        caption=f"Thermal ELA Map (Peak Delta: {df_result['ela_p95']}). Hot zones (Red) indicate divergent compression histories.",
                        use_container_width=True
                    )
                with tab_ela_bw:
                    st.image(
                        df_result["ela_image"],
                        caption=f"Grayscale Difference ELA Map (Mean Delta: {df_result['ela_score']}).",
                        use_container_width=True
                    )
                with tab_fft:
                    st.image(
                        df_result["fft_image"],
                        caption=f"2D Fourier Power Spectrum (Radial Energy Ratio: {df_result['fft_score']}). Spikes outside center indicate GAN/diffusion periodicity.",
                        use_container_width=True
                    )

                with st.expander("📄 Hardware EXIF & Digital Metadata Details"):
                    meta = df_result["metadata_summary"]
                    st.write(f"- **Recorded EXIF Tags:** {meta['exif_count']}")
                    st.write(f"- **Camera Hardware Sensor:** {meta['camera_make'] or 'No camera hardware signature detected'}")
                    st.write(f"- **Editing Software Stamp:** {meta['software_tag'] or 'Standard/Stripped'}")
                    if meta["raw_tags"]:
                        st.json(meta["raw_tags"])
                    else:
                        st.info("No raw physical camera tags recorded.")

                # Export Section
                st.markdown("---")
                st.markdown("**Export Digital Forensic Certificate:**")
                clean_export = {k: v for k, v in df_result.items() if k not in ("ela_image", "ela_heatmap", "fft_image")}
                rc1, rc2 = st.columns(2)
                with rc1:
                    j_str = generate_json_report("Deepfake Media Forensics", clean_export)
                    st.download_button(
                        label="📥 Download JSON Report",
                        data=j_str,
                        file_name="deepfake_forensics_audit.json",
                        mime="application/json",
                        use_container_width=True
                    )
                with rc2:
                    h_str = generate_html_report("Deepfake Media Forensics", clean_export, "Visual Media Forensics")
                    st.download_button(
                        label="📄 Download HTML Certificate",
                        data=h_str,
                        file_name="deepfake_forensics_audit.html",
                        mime="text/html",
                        use_container_width=True
                    )
        else:
            st.info("Upload or choose a reference image on the left, then click **Execute Forensic Vision Audit**.")

# ==========================================
# MODULE 3: MULTI-MODAL UNIFIED AUDIT
# ==========================================
elif module_choice == "🌐 Multi-Modal Unified Audit":
    st.subheader("🌐 Multi-Modal Digital Media Cross-Verification")
    st.write("Perform simultaneous semantic and visual forensic audits on an article's narrative claims and its accompanying lead image.")

    mm_col1, mm_col2 = st.columns([1, 1], gap="large")

    with mm_col1:
        st.markdown("**1. Article Narrative Content:**")
        mm_text = st.text_area(
            "Article Headline & Body:",
            height=160,
            value="Official health authorities and university researchers reported a steady decline in seasonal viral infections following nationwide preventative vaccination programs."
        )

        st.markdown("**2. Associated Lead Visual Media:**")
        mm_file = st.file_uploader("Upload Image:", type=["jpg", "jpeg", "png", "webp"], key="mm_uploader")
        
        mm_img_bytes = None
        if mm_file is not None:
            mm_img_bytes = mm_file.read()
        else:
            with open("samples/authentic_sample.jpg", "rb") as f:
                mm_img_bytes = f.read()

        st.image(Image.open(io.BytesIO(mm_img_bytes)), caption="Lead Visual Media Attached", use_container_width=True)
        run_mm_btn = st.button("⚖️ Run Complete Multi-Modal Audit", type="primary", use_container_width=True)

    with mm_col2:
        st.markdown("### 📋 Multi-Modal Unified Verdict")
        if run_mm_btn:
            with st.spinner("Synthesizing linguistic semantics with computer vision forensics..."):
                t_res = nlp_engine.analyze_text(mm_text)
                i_res = df_engine.analyze_image(mm_img_bytes, "lead_multimodal.jpg")

            text_cred = t_res["prob_real"]
            img_auth = i_res["authenticity_score"]
            overall_integrity = round((text_cred * 0.5) + (img_auth * 0.5), 1)

            if overall_integrity >= 60.0:
                overall_verdict = "Verified Authentic Content"
                badge_class = "badge-authentic-pastel"
                badge_icon = "🛡️"
            elif overall_integrity >= 40.0:
                overall_verdict = "Suspicious / Mixed Indicators"
                badge_class = "badge-fake-pastel"
                badge_icon = "⚠️"
            else:
                overall_verdict = "High Risk: Fabricated Media"
                badge_class = "badge-fake-pastel"
                badge_icon = "🚨"

            st.markdown(f"""
            <div style="margin-bottom: 1.2rem;">
                <span class="{badge_class}">{badge_icon} {overall_verdict}</span>
            </div>
            """, unsafe_allow_html=True)

            m1, m2 = st.columns(2)
            m1.metric("Unified Integrity Score", f"{overall_integrity}/100", delta="Balanced Rating")
            m2.metric("Cross-Modal Alignment", f"{round(100.0 - abs(text_cred - img_auth), 1)}%", delta="Semantic Consistency")

            st.markdown("**Cross-Modal Correlation Radar:**")
            render_dimension_chart({
                "Text Credibility": text_cred,
                "Image Authenticity": img_auth,
                "Compression Integrity": i_res["forensic_dimensions"]["Compression Grid Consistency"],
                "Linguistic Objectivity": t_res["dimension_scores"]["Emotional Neutrality"],
                "Source Provenance": i_res["forensic_dimensions"]["Metadata Provenance"]
            }, "Multi-Modal Integrity Breakdown")

            st.markdown("---")
            st.markdown("**Synthesized Risk Evaluation:**")
            if t_res["verdict"] == "Fake" and "Manipulated" in i_res["verdict"]:
                st.error("🚨 Critical Cross-Modal Alert: Both narrative text and accompanying visual media exhibit artificial manipulation patterns. Strong indicator of coordinated disinformation.")
            elif t_res["verdict"] == "Fake":
                st.warning("⚠️ Semantic Discrepancy: Linguistic markers indicate misinformation, despite the image appearing photographically consistent.")
            elif "Manipulated" in i_res["verdict"]:
                st.warning("⚠️ Visual Manipulation Discrepancy: Text language reads as standard reporting, but the attached image contains synthetic/splicing anomalies.")
            else:
                st.success("✅ Multi-Modal Verification Passed: High consistency across semantic language patterns and digital media compression signatures.")

            # Export
            st.markdown("---")
            unified_dict = {
                "overall_verdict": overall_verdict,
                "overall_integrity_score": overall_integrity,
                "text_evaluation": {k: v for k, v in t_res.items() if k != "highlighted_html"},
                "image_evaluation": {k: v for k, v in i_res.items() if k not in ("ela_image", "ela_heatmap", "fft_image")}
            }
            u_json = generate_json_report("Unified Multi-Modal Audit", unified_dict)
            st.download_button(
                label="📥 Download Unified Multi-Modal Certificate (JSON)",
                data=u_json,
                file_name="multimodal_audit_certificate.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("Click **Run Complete Multi-Modal Audit** to evaluate narrative and imagery coherence.")

# ==========================================
# MODULE 4: MODEL RETRAINING SUITE
# ==========================================
elif module_choice == "⚡ Custom Model Retraining Suite":
    st.subheader("⚡ Live Model Retraining & Fine-Tuning Suite")
    st.write("Train or fine-tune the TF-IDF and Logistic Regression classifier with custom news corpora via CSV upload.")

    st.markdown("#### Active Classifier Diagnostics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Training Corpus", f"{len(nlp_engine.training_samples)} Samples")
    c2.metric("Feature Extractor", "TF-IDF (1-2 N-grams)")
    c3.metric("Regularization Penalty", "L2 (C=1.2)")

    st.markdown("---")
    st.markdown("#### Upload Custom Dataset (CSV)")
    csv_file = st.file_uploader("Upload CSV File:", type=["csv"])

    if csv_file is not None:
        try:
            df = pd.read_csv(csv_file)
            st.dataframe(df.head(5), use_container_width=True)

            col_names = df.columns.tolist()
            sc1, sc2 = st.columns(2)
            with sc1:
                text_col = st.selectbox("Select Article Text/Headline Column:", col_names)
            with sc2:
                label_col = st.selectbox("Select Ground Truth Label Column (0/1 or fake/real):", col_names)

            if st.button("🚀 Retrain Model on Uploaded Corpus", type="primary"):
                with st.spinner("Re-fitting TF-IDF vectorizer and optimizing Logistic Regression weights..."):
                    success, msg = nlp_engine.retrain(df, text_col, label_col)
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")
        except Exception as e:
            st.error(f"Failed to parse CSV: {str(e)}")

    st.markdown("---")
    st.markdown("#### Download CSV Training Template")
    sample_df = pd.DataFrame({
        "article_text": [
            "Official agency reports sustained employment growth in sustainable energy manufacturing sector.",
            "SHOCKING CONSPIRACY: Space aliens landed in downtown capital and delivered secret holographic treaty!"
        ],
        "label": [1, 0]
    })
    csv_bytes = sample_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download CSV Training Template",
        data=csv_bytes,
        file_name="training_template.csv",
        mime="text/csv"
    )
