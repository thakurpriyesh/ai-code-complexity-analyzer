import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

import streamlit as st
import pandas as pd
from streamlit_ace import st_ace

# --- Moduler Imports ---
from models.model_pipeline import train_model
from src.extraction import extract_features_heuristics, get_actual_complexity
from src.visualization import create_gauge_chart, create_radar_chart, create_donut_chart

# --- UI Layout (Centered) ---
st.set_page_config(page_title="ComplexityIQ", layout="centered")

st.title("🧠 ComplexityIQ")
st.markdown("Paste your code below for deep structural analysis, bug risk prediction, and maintainability scoring.")

# Input Section
language_choice = st.selectbox("Select Language", ["Python", "Java", "C++", "JavaScript"])
mode_map = {"Python": "python", "Java": "java", "C++": "c_cpp", "JavaScript": "javascript"}

user_code = st_ace(
    language=mode_map[language_choice],
    theme="monokai",
    keybinding="vscode",
    font_size=14,
    tab_size=4,
    min_lines=15,
    placeholder="Write or paste your code here... (Press Ctrl/Cmd + Enter to apply)"
)

# Analysis Section
if user_code:
    # 1. Load the Model Pipeline (from models/model_pipeline.py)
    model = train_model()
    
    # 2. Extract Features (from src/extraction.py)
    features = extract_features_heuristics(user_code, language_choice)
    actual_complexity = get_actual_complexity(user_code, language_choice)
    
    feature_vector = pd.DataFrame([{
        'loops': features['loops'], 'conditionals': features['conditionals'], 
        'functions': features['functions'], 'variables': features['variables'], 
        'classes': features['classes'], 'max_depth': features['max_depth']
    }])
    
    # 3. Predictions
    predicted_complexity = model.predict(feature_vector)[0]
    maintainability = max(0, min(100, 100 - (predicted_complexity * 2.5) + (features['comments'] * 2)))

    st.markdown("---")
    st.header("Analysis Results")
    
    # Core Metrics - Row 1
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Complexity (ML)", round(predicted_complexity, 2))
    m2.metric("Actual Complexity (Radon)", actual_complexity)
    m3.metric("Lines of Code", features['total_lines'])

    # Core Metrics - Row 2
    risk_color = "green"
    risk = "Low"
    if predicted_complexity > 5:
        risk_color = "orange"
        risk = "Medium"
    if predicted_complexity > 10:
        risk_color = "red"
        risk = "High"

    m4, m5, m6 = st.columns(3)
    m4.metric("Maintainability Score", f"{round(maintainability)}/100")
    m5.metric("Est. Time Complexity", features['time_complexity'])
    m6.markdown(f"**Bug Risk:** <span style='color:{risk_color}; font-size: 18px;'>{risk}</span>", unsafe_allow_html=True)

    # 4. Generate Visualizations (from src/visualization.py)
    st.markdown("### Complexity Visualizations")
    g1, g2 = st.columns(2)
    
    with g1:
        comp_steps = [
            {'range': [0, 5], 'color': "lightgreen"},
            {'range': [5, 15], 'color': "navajowhite"},
            {'range': [15, 30], 'color': "salmon"}
        ]
        fig_comp = create_gauge_chart(
            predicted_complexity, "Complexity Score", max(20, predicted_complexity + 5), comp_steps
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with g2:
        maint_steps = [
            {'range': [0, 40], 'color': "salmon"},
            {'range': [40, 75], 'color': "navajowhite"},
            {'range': [75, 100], 'color': "lightgreen"}
        ]
        fig_maint = create_gauge_chart(
            maintainability, "Maintainability", 100, maint_steps
        )
        st.plotly_chart(fig_maint, use_container_width=True)

    # Structural Breakdown
    st.markdown("### Structural Breakdown")
    c1, c2 = st.columns(2)
    
    with c1:
        fig_radar = create_radar_chart(features)
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with c2:
        fig_donut = create_donut_chart(features)
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # Text Data & Suggestions
    with st.expander("View Raw Extracted Features & Counts"):
        st.json(features)
        
    st.markdown("### Actionable Suggestions")
    if features['max_depth'] >= 3:
        st.warning("⚠️ Deep nesting detected. Consider extracting logic into separate functions to lower time complexity.")
    elif features['loops'] > 3:
        st.info("💡 High loop count. Verify if any loops can be optimized or replaced with map/filter operations.")
    else:
        st.success("✅ Code structure looks highly maintainable.")

# --- Information Footer ---
st.markdown("---")
st.markdown("## Glossary & Technical Details")

st.markdown("### Terms Explained")
st.markdown("""
* **Cyclomatic Complexity:** A software metric used to indicate the complexity of a program. It is a quantitative measure of the number of linearly independent paths through a program's source code. A lower score means the code is easier to test, maintain, and less prone to bugs.
* **Maintainability Score:** A heuristic measurement (0-100) determining how easy the code is to support and change. It penalizes high complexity and rewards good commenting practices.
* **Estimated Time Complexity:** A Big-O notation estimate ($O(n)$, $O(n^2)$, etc.) based on the maximum nesting depth of iterative loops within the code block. 
""")

st.markdown("### Model Details")
st.markdown("""
* **Algorithm:** Random Forest Regressor (`scikit-learn`). 
* **Hyperparameters:** 100 Estimators, Max Depth of 10.
* **Feature Extraction:** AST-inspired heuristics mapping loops, conditionals, functions, assignments, and nested depth control flows.
""")

st.markdown("### Dataset Used")
st.markdown("""
* **Data Source:** A procedurally generated synthetic dataset containing **5,000 records**. 
* **Modeling:** The distributions of variables (loops, lines, depth) are mathematically modeled after the **PROMISE Software Engineering Repository** and standard defect-prediction benchmarks (like Defects4J) to ensure realistic weightings without requiring heavy local CSV downloads.
""")