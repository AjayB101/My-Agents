import streamlit as st

from agents.error_analyser import generate_error_response
from agents.message_generator import generate_message

# Configure page
st.set_page_config(
    page_title="🤖 Productivity Agent Ecosystem",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for agent selection
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None

# Agent configurations
AGENTS = {
    "message_generator": {
        "name": "📧 Message Generator Agent",
        "description": "Generate professional referral request messages from job posting content",
        "icon": "📧",
        "category": "Communication",
        "status": "Active",
        "color": "#1f77b4"
    },
    "error_analyzer": {
        "name": "🔍 Error Analyzer Agent",
        "description": "Analyze and debug code errors with intelligent suggestions",
        "icon": "🔍",
        "category": "Development",
        "status": "Active",
        "color": "#ff7f0e"
    },
    "code_reviewer": {
        "name": "📝 Code Reviewer Agent",
        "description": "Review code quality, suggest improvements and best practices",
        "icon": "📝",
        "category": "Development",
        "status": "Planned",
        "color": "#2ca02c"
    },
    "task_planner": {
        "name": "📅 Task Planner Agent",
        "description": "Smart task planning and productivity optimization",
        "icon": "📅",
        "category": "Productivity",
        "status": "Planned",
        "color": "#d62728"
    },
    "document_summarizer": {
        "name": "📄 Document Summarizer Agent",
        "description": "Summarize long documents and extract key insights",
        "icon": "📄",
        "category": "Analysis",
        "status": "Planned",
        "color": "#9467bd"
    }
}


def show_agent_dashboard():
    """Display the main agent selection dashboard"""
    st.title("🤖 Productivity Agent Ecosystem")
    st.markdown(
        "Select an agent to boost your productivity and streamline your workflow")

    # Stats overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Agents", len(AGENTS))
    with col2:
        active_count = sum(1 for agent in AGENTS.values()
                           if agent["status"] == "Active")
        st.metric("Active Agents", active_count)
    with col3:
        coming_soon = sum(1 for agent in AGENTS.values()
                          if agent["status"] == "Coming Soon")
        st.metric("Coming Soon", coming_soon)
    with col4:
        planned = sum(1 for agent in AGENTS.values()
                      if agent["status"] == "Planned")
        st.metric("Planned", planned)

    st.markdown("---")

    # Group agents by category
    categories = {}
    for agent_id, agent_info in AGENTS.items():
        category = agent_info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((agent_id, agent_info))

    # Display agents by category
    for category, agents in categories.items():
        st.markdown(f"### {category} Agents")

        cols = st.columns(min(3, len(agents)))
        for idx, (agent_id, agent_info) in enumerate(agents):
            with cols[idx % 3]:
                # Status badge styling
                if agent_info["status"] == "Active":
                    badge_color = "🟢"
                elif agent_info["status"] == "Coming Soon":
                    badge_color = "🟡"
                else:
                    badge_color = "🔴"

                # Agent card
                with st.container():
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {agent_info['color']};
                        border-radius: 10px;
                        padding: 20px;
                        margin: 10px 0;
                        background: linear-gradient(135deg, {agent_info['color']}15, {agent_info['color']}05);
                    ">
                        <h4>{agent_info['icon']} {agent_info['name']}</h4>
                        <p>{agent_info['description']}</p>
                        <small>{badge_color} {agent_info['status']}</small>
                    </div>
                    """, unsafe_allow_html=True)

                    # Button styling based on status
                    if agent_info["status"] == "Active":
                        if st.button(f"Launch {agent_info['icon']}", key=f"launch_{agent_id}", type="primary"):
                            st.session_state.selected_agent = agent_id
                            st.rerun()
                    else:
                        st.button(
                            f"Coming Soon {agent_info['icon']}", key=f"disabled_{agent_id}", disabled=True)

        st.markdown("---")


def show_message_generator():
    """Display the message generator agent interface"""
    st.title("📧 Smart Referral Message Generator")
    st.markdown(
        "Generate professional referral request messages from job posting content")

    # Back button
    if st.button("← Back to Agent Dashboard", type="secondary"):
        st.session_state.selected_agent = None
        st.rerun()

    st.markdown("### 📝 **How to use:**")
    st.info("""
    1. **Go to the job posting** in your browser
    2. **Copy the entire job description** (Ctrl+A, then Ctrl+C)
    3. **Paste it below** in the text area
    4. **Click Generate** to create your referral message
    """)

    # Main input area
    st.markdown("### 📋 **Paste Job Description Here:**")
    job_content = st.text_area(
        "Job Description Content",
        height=300,
        placeholder="""Paste the complete job posting here including:
- Job Title
- Company Name  
- Job Requirements
- Job Description
- Job ID (if available)
- Any other relevant details

Example:
Software Engineer - Google
Job ID: 12345
We are looking for a Software Engineer to join our team...
Requirements: Python, JavaScript, React...
""",
        help="Copy and paste the entire job posting content from the company's website"
    )

    # Character count
    if job_content:
        char_count = len(job_content.strip())
        st.caption(f"📊 Content length: {char_count} characters")

        if char_count < 100:
            st.warning(
                "⚠️ Content seems too short. Please paste the complete job description for better results.")
        elif char_count > 50:
            st.success("✅ Good content length detected!")

    # Generate button and results
    if st.button("🚀 Generate Referral Message", type="primary", use_container_width=True):
        if job_content and len(job_content.strip()) > 50:
            with st.spinner("✍️ Generating your referral message..."):
                try:
                    message = generate_message(job_content)

                    st.success("🎉 Referral message generated successfully!")

                    st.markdown("### 📝 **Your Referral Message:**")
                    st.markdown(
                        "**Copy the message below and personalize it:**")

                    # Display the message in a text area for easy copying
                    st.text_area(
                        "Generated Message",
                        value=message,
                        height=250,
                        key="generated_message",
                        help="Select all (Ctrl+A) and copy (Ctrl+C) this message"
                    )

                    # Add copy button simulation
                    st.markdown(
                        "**✂️ To copy:** Click in the text area above → Press Ctrl+A → Press Ctrl+C")

                except Exception as e:
                    st.error(f"❌ Error generating message: {str(e)}")
                    st.markdown("**Please try:**")
                    st.markdown("- Check your internet connection")
                    st.markdown("- Verify your GROQ API key in the .env file")
                    st.markdown(
                        "- Make sure the job content is properly formatted")
        else:
            st.error(
                "❌ Please paste the job description content (at least 50 characters)")

    # Tips and instructions
    st.markdown("---")
    st.markdown("### 💡 **Tips for Best Results:**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ **Include in your paste:**")
        st.markdown("""
        - Job title
        - Company name
        - Job requirements
        - Job description
        - Job ID/Reference number
        - Location (if mentioned)
        """)

    with col2:
        st.markdown("#### 🎯 **Personalization Tips:**")
        st.markdown("""
        - Replace [Name] with employee's actual name
        - Replace [Your Name] with your name
        - Add how you found their contact
        - Mention mutual connections if any
        - Keep it concise and professional
        """)


def show_error_analyzer():
    """Interactive Error Analyzer Agent"""
    st.title("🔍 Error Analyzer Agent")
    st.caption(
        "This agent helps you analyze and debug code errors with intelligent suggestions.")

    with st.form("error_form"):
        error_message = st.text_area(
            "🛑 Paste the error message here", height=100)
        code_snippet = st.text_area(
            "💻 (Optional) Paste the related code snippet", height=150)
        submitted = st.form_submit_button("Analyze Error")

    if submitted:
        if not error_message.strip():
            st.warning("Please provide an error message.")
        else:
            with st.spinner("Analyzing error..."):
                try:
                    response = generate_error_response(
                        error_message, code_snippet)
                    st.success("✅ Analysis Complete!")
                    st.markdown("### 🧠 Assistant's Debugging Insight")
                    st.markdown(response, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Something went wrong: {e}")

    st.markdown("---")
    if st.button("← Back to Agent Dashboard", type="secondary"):
        st.session_state.selected_agent = None
        st.rerun()

# Sidebar navigation


def show_sidebar():
    """Display sidebar with agent navigation"""
    with st.sidebar:
        st.markdown("## 🤖 Agent Navigator")

        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.selected_agent = None
            st.rerun()

        st.markdown("### Available Agents")

        for agent_id, agent_info in AGENTS.items():
            if agent_info["status"] == "Active":
                if st.button(f"{agent_info['icon']} {agent_info['name'].split(' Agent')[0]}",
                             key=f"sidebar_{agent_id}",
                             use_container_width=True):
                    st.session_state.selected_agent = agent_id
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📊 System Status")
        st.metric("Active Sessions", "1")
        st.metric("Total Tasks Completed", "0")

# Main application logic


def main():
    show_sidebar()

    # Route to appropriate agent or dashboard
    if st.session_state.selected_agent is None:
        show_agent_dashboard()
    elif st.session_state.selected_agent == "message_generator":
        show_message_generator()
    elif st.session_state.selected_agent == "error_analyzer":
        show_error_analyzer()
    else:
        st.error("Agent not found or not implemented yet.")
        if st.button("← Back to Dashboard"):
            st.session_state.selected_agent = None
            st.rerun()


if __name__ == "__main__":
    main()
