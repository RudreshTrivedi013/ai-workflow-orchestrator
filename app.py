import streamlit as st
import time
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="AI Workflow Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'calendar_events' not in st.session_state:
    st.session_state.calendar_events = []
if 'blog_posts' not in st.session_state:
    st.session_state.blog_posts = []
if 'task_history' not in st.session_state:
    st.session_state.task_history = []

# ─── Enhanced Styling ───────────────────────────────────────────────────────
st.markdown("""
    <style>
        /* Base styles */
        .stApp {
            background: #0f1419;
        }
        
        /* Typography */
        .main-title {
            font-size: 3.2rem;
            font-weight: 900;
            color: #e6e8eb;
            margin-bottom: 0.5rem;
            text-align: center;
            letter-spacing: -1px;
        }
        .subtitle {
            color: #8b949e;
            font-size: 1.25rem;
            text-align: center;
            margin-bottom: 2.5rem;
            font-weight: 500;
        }
        
        /* Cards */
        .card {
            background: #1c2128;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #30363d;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
            margin: 1.5rem 0;
            transition: all 0.3s ease;
        }
        .card:hover {
            background: #21262d;
            border-color: #484f58;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
            transform: translateY(-2px);
        }
        
        /* Event cards */
        .event-card {
            background: linear-gradient(135deg, #21262d 0%, #2d333b 100%);
            color: #e6e8eb;
            padding: 2rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
            border: 1px solid #3d444d;
        }
        .event-card .event-title {
            font-size: 1.65rem;
            font-weight: 700;
            margin-bottom: 1.2rem;
            color: #e6e8eb;
            border-bottom: 2px solid #484f58;
            padding-bottom: 0.8rem;
        }
        .event-card .event-detail {
            display: flex;
            align-items: center;
            margin: 0.7rem 0;
            font-size: 1.05rem;
            color: #adbac7;
        }
        .event-card .event-icon {
            margin-right: 0.9rem;
            font-size: 1.3rem;
            color: #768390;
        }
        
        /* Blog post card */
        .blog-card {
            background: #1c2128;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 2.2rem;
            margin: 1.5rem 0;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            color: #adbac7;
        }
        
        /* Buttons */
        .stButton > button {
            font-weight: 600;
            padding: 0.9rem 2.2rem;
            border-radius: 8px;
            background: #30363d;
            color: #e6e8eb;
            border: 1px solid #484f58;
            transition: all 0.3s ease;
            width: 100%;
            font-size: 1.05rem;
        }
        .stButton > button:hover {
            background: #3d444d;
            border-color: #656d76;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }
        
        /* Stats boxes */
        .stat-box {
            background: #21262d;
            padding: 1.8rem;
            border-radius: 10px;
            border-left: 4px solid #484f58;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            margin: 1rem 0;
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
            color: #e6e8eb;
        }
        .stat-label {
            color: #768390;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        /* History item */
        .history-item {
            background: #21262d;
            padding: 1.2rem 1.6rem;
            border-radius: 8px;
            border-left: 3px solid #484f58;
            margin: 0.8rem 0;
            color: #adbac7;
        }
        
        /* Input fields */
        .stTextInput input, .stTextArea textarea {
            border-radius: 8px;
            border: 1px solid #30363d;
            padding: 1rem;
            background: #0d1117;
            color: #e6e8eb;
            transition: all 0.3s ease;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #484f58;
            box-shadow: 0 0 0 3px rgba(72, 79, 88, 0.2);
            background: #161b22;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            background: #1c2128;
            border-radius: 8px;
            padding: 0.8rem 1.5rem;
            font-weight: 600;
            color: #768390;
            border: 1px solid #30363d;
        }
        .stTabs [aria-selected="true"] {
            background: #30363d;
            color: #e6e8eb;
            border-color: #484f58;
        }
        
        /* Metrics styling */
        [data-testid="stMetricValue"] {
            font-size: 2.2rem;
            font-weight: 800;
            color: #e6e8eb;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: #0d1117;
            border-right: 1px solid #21262d;
        }
        
        /* Success/Warning alerts */
        .stSuccess {
            background: #1c2d1f;
            color: #7ee787;
            font-weight: 600;
            border-radius: 8px;
            border: 1px solid #2d4a30;
        }
        .stWarning {
            background: #2d2416;
            color: #f0bf60;
            font-weight: 600;
            border-radius: 8px;
            border: 1px solid #463915;
        }
        
        /* Text colors */
        .stMarkdown, p, span, div {
            color: #adbac7;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #e6e8eb;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: #1c2128;
            border: 1px solid #30363d;
            border-radius: 8px;
            color: #e6e8eb;
        }
        
        /* Select box styling */
        .stSelectbox > div > div {
            background: #0d1117;
            border: 1px solid #30363d;
            color: #e6e8eb;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #0d1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #484f58;
        }
    </style>
""", unsafe_allow_html=True)

# ─── Enhanced Mock Agents ───────────────────────────────────────────────────

def parse_meeting_details(user_input):
    """Enhanced parsing with more realistic date/time extraction"""
    # Mock intelligent parsing
    keywords = {
        'tomorrow': datetime.now() + timedelta(days=1),
        'next week': datetime.now() + timedelta(days=7),
        'friday': datetime.now() + timedelta(days=(4 - datetime.now().weekday()) % 7),
        'monday': datetime.now() + timedelta(days=(0 - datetime.now().weekday()) % 7),
    }
    
    date = datetime.now() + timedelta(days=random.randint(1, 14))
    for keyword, value in keywords.items():
        if keyword in user_input.lower():
            date = value
            break
    
    # Extract time hints
    time_str = "2:00 PM"
    if "morning" in user_input.lower():
        time_str = "10:00 AM"
    elif "afternoon" in user_input.lower():
        time_str = "2:00 PM"
    elif "evening" in user_input.lower():
        time_str = "6:00 PM"
    
    return date, time_str

def calendar_agent(user_input):
    """Enhanced calendar agent with realistic parsing"""
    time.sleep(0.9)
    
    date, time_str = parse_meeting_details(user_input)
    
    # Generate realistic meeting titles
    meeting_types = [
        "Team Sync – Q4 Planning",
        "Project Kickoff Meeting",
        "Sprint Retrospective",
        "Client Presentation",
        "Strategy Session",
        "Weekly Standup",
        "Design Review"
    ]
    
    title = random.choice(meeting_types)
    if "team" in user_input.lower():
        title = "Team Sync – Q4 Planning"
    elif "client" in user_input.lower():
        title = "Client Presentation"
    elif "review" in user_input.lower():
        title = "Design Review"
    
    event = {
        "title": title,
        "date": date.strftime("%B %d, %Y"),
        "time": f"{time_str} – {(datetime.strptime(time_str, '%I:%M %p') + timedelta(hours=1)).strftime('%I:%M %p')} IST",
        "location": random.choice(["Google Meet", "Zoom", "Microsoft Teams", "Conference Room A"]),
        "participants": random.choice([
            "Alice, Bob, Priya, You",
            "Sarah, Mike, You",
            "Development Team",
            "Marketing Team, You"
        ]),
        "description": user_input or "Team discussion and planning session",
        "created_at": datetime.now().strftime("%I:%M %p")
    }
    
    return event

def blog_agent(topic, tone="professional", length="medium"):
    """Enhanced blog generator with tone and length options"""
    time.sleep(1.2)
    
    if not topic:
        topic = "Artificial Intelligence"
    
    intros = {
        "professional": f"{topic} has become increasingly important in today's technology landscape.",
        "casual": f"Let's talk about {topic} – it's pretty amazing what's happening in this space!",
        "technical": f"Understanding {topic} requires a deep dive into its core principles and applications."
    }
    
    sections = []
    sections.append(f"# {topic}\n")
    sections.append(f"*Generated on {datetime.now().strftime('%B %d, %Y')}*\n")
    sections.append(f"## Introduction\n\n{intros.get(tone, intros['professional'])}\n")
    
    sections.append("## Key Concepts\n")
    sections.append(f"- **Foundation**: Core principles that make {topic} valuable")
    sections.append(f"- **Application**: Real-world use cases and implementations")
    sections.append(f"- **Future Impact**: Where {topic} is headed\n")
    
    if length in ["medium", "long"]:
        sections.append("## Practical Example\n")
        sections.append("```python")
        sections.append("# Quick demonstration")
        sections.append("def demonstrate():")
        sections.append(f"    print('Working with {topic}')")
        sections.append("    return True\n")
        sections.append("result = demonstrate()")
        sections.append("```\n")
    
    if length == "long":
        sections.append("## Best Practices\n")
        sections.append("1. Start with the fundamentals")
        sections.append("2. Build projects to reinforce learning")
        sections.append("3. Stay updated with latest developments")
        sections.append("4. Join communities and collaborate\n")
    
    sections.append("## Conclusion\n")
    sections.append(f"Learning {topic} opens up new opportunities for innovation and growth. "
                   "Start small, stay curious, and keep building.\n")
    
    sections.append("---\n*This is a demo blog post generated by AI Workflow Assistant*")
    
    return "\n".join(sections)

def email_agent(purpose, recipient, context):
    """New email composition agent"""
    time.sleep(0.8)
    
    templates = {
        "follow-up": f"""Subject: Following Up – {context}

Hi {recipient},

I hope this email finds you well. I wanted to follow up on {context}.

I'd love to hear your thoughts and discuss next steps when you have a moment.

Looking forward to hearing from you.

Best regards""",
        
        "introduction": f"""Subject: Introduction – {context}

Hi {recipient},

I hope this message finds you well. I wanted to reach out regarding {context}.

I believe there could be valuable opportunities for collaboration, and I'd love to connect.

Would you be available for a brief conversation sometime this week?

Best regards""",
        
        "thank-you": f"""Subject: Thank You – {context}

Hi {recipient},

Thank you so much for {context}. I really appreciate your time and insights.

This has been incredibly helpful, and I'm excited about the next steps.

Warm regards"""
    }
    
    return templates.get(purpose, templates["follow-up"])

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 AI Assistant")
    st.markdown("---")
    
    # Stats
    st.markdown('<div class="stat-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-number">{len(st.session_state.calendar_events)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-label">Events Created</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="stat-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-number">{len(st.session_state.blog_posts)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-label">Blog Posts</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity
    if st.session_state.task_history:
        st.markdown("### 📊 Recent Activity")
        for task in st.session_state.task_history[-5:]:
            st.markdown(f'<div class="history-item">**{task["type"]}** • {task["time"]}</div>', 
                       unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear All Data"):
        st.session_state.calendar_events = []
        st.session_state.blog_posts = []
        st.session_state.task_history = []
        st.rerun()

# ─── Main UI ─────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">AI Workflow Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">✨ Intelligent automation for calendar, content & communication</div>', 
            unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📅 Calendar", "✍️ Blog Generator", "📧 Email Composer", "📚 History"])

# ─── Calendar Tab ────────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Schedule New Event")
        
        meeting_text = st.text_area(
            "Describe your meeting",
            placeholder="Team meeting next Friday at 11 AM to discuss Q4 roadmap",
            height=100,
            key="cal_input"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🗓️ Create Event", use_container_width=True):
                if meeting_text:
                    with st.spinner("Analyzing and scheduling..."):
                        result = calendar_agent(meeting_text)
                        st.session_state.calendar_events.append(result)
                        st.session_state.task_history.append({
                            "type": "Calendar Event",
                            "time": result["created_at"]
                        })
                    st.success("✅ Event created successfully!")
                    st.rerun()
                else:
                    st.warning("Please describe the meeting first")
        
        with col_b:
            if st.button("🎲 Generate Sample", use_container_width=True):
                samples = [
                    "Team standup tomorrow at 10 AM",
                    "Client presentation next Monday afternoon",
                    "Sprint planning Friday morning with dev team"
                ]
                st.session_state.sample_text = random.choice(samples)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        - Mention **day** (tomorrow, Friday)
        - Add **time** (morning, 3 PM)
        - Include **participants**
        - Note the **purpose**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display events
    if st.session_state.calendar_events:
        st.markdown("### 📆 Scheduled Events")
        for idx, event in enumerate(reversed(st.session_state.calendar_events)):
            st.markdown(f"""
            <div class="event-card">
                <div class="event-title">{event['title']}</div>
                <div class="event-detail">
                    <span class="event-icon">📅</span>
                    <span>{event['date']}</span>
                </div>
                <div class="event-detail">
                    <span class="event-icon">🕒</span>
                    <span>{event['time']}</span>
                </div>
                <div class="event-detail">
                    <span class="event-icon">📍</span>
                    <span>{event['location']}</span>
                </div>
                <div class="event-detail">
                    <span class="event-icon">👥</span>
                    <span>{event['participants']}</span>
                </div>
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                    <strong>Description:</strong> {event['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── Blog Tab ────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Generate Blog Post")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        topic_text = st.text_input(
            "Blog topic",
            placeholder="Prompt Engineering Best Practices",
            key="blog_input"
        )
    
    with col2:
        tone = st.selectbox(
            "Tone",
            ["professional", "casual", "technical"]
        )
    
    with col3:
        length = st.selectbox(
            "Length",
            ["short", "medium", "long"]
        )
    
    if st.button("✍️ Generate Blog Post", use_container_width=True):
        if topic_text:
            with st.spinner("Writing your blog post..."):
                content = blog_agent(topic_text, tone, length)
                post = {
                    "topic": topic_text,
                    "content": content,
                    "created_at": datetime.now().strftime("%B %d, %Y at %I:%M %p")
                }
                st.session_state.blog_posts.append(post)
                st.session_state.task_history.append({
                    "type": "Blog Post",
                    "time": datetime.now().strftime("%I:%M %p")
                })
            st.success("✅ Blog post generated!")
            st.rerun()
        else:
            st.warning("Please enter a topic first")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display blog posts
    if st.session_state.blog_posts:
        st.markdown("### 📝 Generated Posts")
        for idx, post in enumerate(reversed(st.session_state.blog_posts)):
            with st.expander(f"📄 {post['topic']} – {post['created_at']}", expanded=(idx == 0)):
                st.markdown('<div class="blog-card">', unsafe_allow_html=True)
                st.markdown(post['content'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button(f"📋 Copy to Clipboard", key=f"copy_{idx}"):
                    st.code(post['content'], language=None)

# ─── Email Tab ───────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Compose Email")
    
    col1, col2 = st.columns(2)
    
    with col1:
        purpose = st.selectbox(
            "Email purpose",
            ["follow-up", "introduction", "thank-you"]
        )
        recipient = st.text_input("Recipient name", placeholder="John")
    
    with col2:
        context = st.text_input(
            "Context",
            placeholder="our discussion about the project proposal"
        )
    
    if st.button("📧 Generate Email", use_container_width=True):
        if recipient and context:
            with st.spinner("Composing email..."):
                email = email_agent(purpose, recipient, context)
                st.session_state.task_history.append({
                    "type": "Email Draft",
                    "time": datetime.now().strftime("%I:%M %p")
                })
            
            st.markdown('<div class="blog-card">', unsafe_allow_html=True)
            st.code(email, language=None)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─── History Tab ─────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Activity Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Events", len(st.session_state.calendar_events))
    
    with col2:
        st.metric("Blog Posts", len(st.session_state.blog_posts))
    
    with col3:
        st.metric("Total Actions", len(st.session_state.task_history))
    
    if st.session_state.task_history:
        st.markdown("### Recent Activity")
        for task in reversed(st.session_state.task_history):
            st.markdown(f"""
            <div class="history-item">
                <strong>{task['type']}</strong> • Created at {task['time']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No activity yet. Start by creating an event or blog post!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#94a3b8; font-size:0.9rem;'>"
    "🤖 AI Workflow Assistant • Built with Streamlit • Mock Demo v2.0</p>",
    unsafe_allow_html=True
)