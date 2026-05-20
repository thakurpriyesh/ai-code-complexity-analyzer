import plotly.graph_objects as go

def create_gauge_chart(value, title, max_val, color_steps):
    """Generates a standardized Plotly gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value, title={'text': title},
        gauge={
            'axis': {'range': [None, max_val]}, 
            'bar': {'color': "darkblue"},
            'steps': color_steps
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_radar_chart(features):
    """Generates a radar chart for structural features."""
    categories = ['Loops', 'Conditionals', 'Functions', 'Variables', 'Max Depth']
    values = [features['loops'], features['conditionals'], features['functions'], features['variables'], features['max_depth']]
    
    fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False, height=250, margin=dict(l=30, r=30, t=30, b=20), title="Feature Density")
    return fig

def create_donut_chart(features):
    """Generates a donut chart for code composition."""
    comp_labels = ['Code', 'Comments', 'Blank Lines']
    comp_values = [features['actual_code_lines'], features['comments'], features['blank_lines']]
    
    fig = go.Figure(data=[go.Pie(labels=comp_labels, values=comp_values, hole=.5, marker_colors=['#636EFA', '#00CC96', '#E45756'])])
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20), title="File Composition")
    return fig