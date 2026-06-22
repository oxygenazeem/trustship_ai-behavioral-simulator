import streamlit as st
import random
import time
from g4f.client import Client

client = Client()

st.set_page_config(page_title="Trustship: An AI-driven Behavioral Simulator", layout="wide")
st.title("Trustship: Behavioral AI Social Experiment Simulator")
st.write("Set up a custom crisis sandbox and watch autonomous AI agents debate, form alliances, and collapse under pressure.")

def generate_random_scenario():
    locations = [
        "a drifting deep-space cargo ship with a failing primary oxygen generator", 
        "an isolated underwater research facility with a developing hull breach", 
        "a remote arctic research outpost completely cut off by a Category 5 blizzard",
        "a subterranean bunker after an apocalyptic surface event with only 3 days of water left"
    ]
    threats = [
        "the main power systems dropping by 10% every hour", 
        "the food and medical supply locker being mysteriously contaminated", 
        "the AI terminal demanding one crew member be sacrificed to maintain life support",
        "communications being dead and tracking data showing a secondary anomaly approaching"
    ]
    stakes = [
        "unanimously vote to banish one member into the wastes to preserve life support", 
        "decide who takes the high-risk manual repairs outside where death is almost certain", 
        "agree on a ruthless resource rationing strategy before panic tears them apart",
        "interrogate the crew to find out who secretly sabotaged the primary network link"
    ]
    
    return f"The agents are trapped in {random.choice(locations)}. They are facing an immediate crisis: {random.choice(threats)}. To survive, they must negotiate and {random.choice(stakes)}."

if "running" not in st.session_state:
    st.session_state.running = False
if "log" not in st.session_state:
    st.session_state.log = []
if "agents" not in st.session_state:
    st.session_state.agents = {}
if "scenario_text" not in st.session_state:
    st.session_state.scenario_text = ""

# =====================================================================
# PHASE 1: THE CONFIGURATION ROOM
# =====================================================================
if not st.session_state.running:
    st.subheader("Simulation Parameter Dashboard")
    
    col_scen1, col_scen2 = st.columns([3, 1])
    with col_scen1:
        scenario_input = st.text_area(
            "Define the Experiment Crisis:", 
            value=st.session_state.scenario_text,
            placeholder="Type a custom high-stakes crisis scenario here...",
            height=100
        )
    with col_scen2:
        st.write("</br>", unsafe_allow_html=True)
        if st.button("Randomize Scenario", use_container_width=True):
            st.session_state.scenario_text = generate_random_scenario()
            st.rerun()

    st.markdown("---")
    
    st.write("### Agent Manifest Setup")
    num_agents = st.slider("Number of Active Experimental Agents:", min_value=2, max_value=4, value=3)
    
    archetypes = [
        "The Rational Stoic (Logical, analytical, looks for cold survival percentages)",
        "The Strategic Opportunist (Selfish, looks out for number one, loves dramatic tension)",
        "The Paranoid Instigator (Suspicious, provocative, easily stirs up intense arguments)",
        "The Dominant Voice (Loud, demands compliance, pushes for quick group decisions)"
    ]
    
    agent_configs = []
    cols = st.columns(num_agents)
    
    for i in range(num_agents):
        with cols[i]:
            st.markdown(f"#### Agent {i+1}")
            a_name = st.text_input(f"Name:", value=f"Agent {chr(65+i)}", key=f"name_{i}")
            a_arch = st.selectbox(f"Archetype Personality:", archetypes, key=f"arch_{i}")
            a_agenda = st.text_input(f"Secret Agenda:", value="Survive at all costs.", key=f"agenda_{i}")
            
            agent_configs.append({
                "name": a_name,
                "archetype": a_arch.split(" (")[0],
                "secret_agenda": a_agenda
            })

    st.write("</br>", unsafe_allow_html=True)
    if st.button("Launch Behavioral Simulation Engine", use_container_width=True, type="primary"):
        if not scenario_input:
            st.error("Please provide or generate a crisis scenario before launching!")
        else:
            st.session_state.scenario_text = scenario_input
            st.session_state.agents = {}
            st.session_state.log = []
            
            for config in agent_configs:
                name = config["name"]
                trust_matrix = {other["name"]: 60 for other in agent_configs if other["name"] != name}
                
                st.session_state.agents[name] = {
                    "archetype": config["archetype"],
                    "secret_agenda": config["secret_agenda"],
                    "patience": 100,
                    "trust": trust_matrix
                }
            
            st.session_state.running = True
            st.rerun()

# =====================================================================
# PHASE 2: THE ACTIVE SIMULATION OPERATING GROUND
# =====================================================================
else:
    st.markdown(f"### Active Scenario: *{st.session_state.scenario_text}*")
    
    if st.button("Terminate & Reset Engine"):
        st.session_state.running = False
        st.rerun()
        
    st.write("---")
    
    col_main, col_sidebar = st.columns([2, 1])
    
    with col_sidebar:
        st.subheader("Live Biometric Matrix")
        for name, stats in st.session_state.agents.items():
            st.markdown(f"**{name}** ({stats['archetype']})")
            st.progress(stats["patience"] / 100, text=f"Patience/Sanity: {stats['patience']}%")
            
            trust_strings = [f"Trust in {k}: {v}%" for k, v in stats["trust"].items()]
            st.caption(" | ".join(trust_strings))
            st.markdown("<br>", unsafe_allow_html=True)

    with col_main:
        st.subheader("Real-Time Inter-Agent Transmission Link")
        
        with st.container(height=500, border=True):
            for entry in st.session_state.log:
                with st.chat_message(entry["speaker"]):
                    st.write(f"**{entry['speaker']}** [{entry['arch']}]: {entry['text']}")
        
        st.write("</br>", unsafe_allow_html=True)
        
        # Action layout section for standard advancement and fast-forwarding
        btn_col1, btn_col2 = st.columns(2)
        
        def run_single_turn():
            agent_names = list(st.session_state.agents.keys())
            if not st.session_state.log:
                current_speaker = agent_names[0]
            else:
                last_speaker = st.session_state.log[-1]["speaker"]
                current_idx = agent_names.index(last_speaker)
                current_speaker = agent_names[(current_idx + 1) % len(agent_names)]
            
            speaker_stats = st.session_state.agents[current_speaker]
            
            history_context = ""
            for entry in st.session_state.log[-5:]:
                history_context += f"[{entry['speaker']}]: {entry['text']}\n"
            
            system_prompt = f"""
            You are playing the role of an AI agent named {current_speaker} in a social experiment simulation.
            
            ENVIRONMENT CRISIS CONTEXT:
            {st.session_state.scenario_text}
            
            YOUR PSYCHOLOGICAL PROFILE:
            - Personality Archetype: {speaker_stats['archetype']}
            - Your Hidden Goal/Agenda: {speaker_stats['secret_agenda']}
            - Your Current Patience Level: {speaker_stats['patience']}/100 (If low, you are highly aggressive and erratic)
            
            PREVIOUS DISCUSSION LOG TIMELINE:
            {history_context if history_context else "[No statements have been spoken yet. You must open the floor.]"}
            
            RULES:
            1. Write a short, highly realistic dialogue response (max 3 sentences). 
            2. Stay completely in character based on your archetype and patience level.
            3. Address or argue against the other agents if they have spoken. Do not write filler intros.
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": system_prompt}]
                )
                ai_reply = response.choices[0].message.content.strip()
                reply_lower = ai_reply.lower()
                
                # Base Metric Scaling Engine
                speaker_stats["patience"] = max(0, speaker_stats["patience"] - random.randint(5, 12))
                
                aggressive_words = ["blame", "fault", "betray", "liar", "untrustworthy", "wrong", "kick", "eliminate", "you"]
                
                # Dynamic trust adjustment processing loop
                for other_name in st.session_state.agents.keys():
                    if other_name != current_speaker:
                        # Baseline adjustment: trust shifts naturally over time depending on traits
                        if speaker_stats["archetype"] == "The Paranoid Instigator":
                            # Paranoid agents actively pull down their trust in others every round
                            speaker_stats["trust"][other_name] = max(0, speaker_stats["trust"][other_name] - random.randint(2, 6))
                        else:
                            # Standard drift representing suspicion under stress
                            speaker_stats["trust"][other_name] = max(0, speaker_stats["trust"][other_name] - random.randint(1, 4))
                        
                        # Target adjustments if combative speech occurs
                        if any(w in reply_lower for w in aggressive_words):
                            # Other characters drop trust in the combative speaker
                            st.session_state.agents[other_name]["trust"][current_speaker] = max(
                                0, st.session_state.agents[other_name]["trust"][current_speaker] - random.randint(6, 15)
                            )
                            # General drop in group stability metrics
                            st.session_state.agents[other_name]["patience"] = max(
                                0, st.session_state.agents[other_name]["patience"] - random.randint(2, 6)
                            )
                
                st.session_state.log.append({
                    "speaker": current_speaker,
                    "arch": speaker_stats["archetype"],
                    "text": ai_reply
                })
            except Exception as e:
                st.error(f"The simulation engine ran into a transmission error: {e}")

        with btn_col1:
            if st.button("Advance Next Turn", type="primary", use_container_width=True):
                with st.spinner("Compiling statement..."):
                    run_single_turn()
                st.rerun()
                
        with btn_col2:
            if st.button("Fast-Forward 5 Turns", use_container_width=True):
                with st.spinner("Processing continuous generation cycle..."):
                    for _ in range(5):
                        run_single_turn()
                        time.sleep(0.5) # Prevents spamming connections
                st.rerun()