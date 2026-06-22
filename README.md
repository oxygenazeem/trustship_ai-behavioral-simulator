# Trustship: An AI-driven Behavioral Simulator

Trustship is an interactive, multi-agent simulation sandbox built using Python and Streamlit. The application orchestrates multiple autonomous AI personalities trapped in localized crisis scenarios. Using a turn-based execution loop, agents negotiate, form alliances, and collapse under psychological pressure while the engine calculates their relationship matrices and sanity metrics in real-time.

### [Try simulation now!](https://www.trustship.streamlit.app)

## Core Features

* **Dynamic Configuration Room:** Customize the entire experiment by adjusting the number of active agents, individual starting archetypes, and hidden agendas.
* **Algorithmic Trust & Patience Engines:** Metrics dynamically scale based on turn-by-turn dialogue analysis, simulating psychological drift and escalating group tension.
* **Turn-Based or Fast-Forward Execution:** Advance the social experiment systematically turn-by-turn or leverage the fast-forward engine to execute continuous cycles.
* **Scrollable HUD Interface:** A pristine visual dashboard featuring a locked biometric monitoring sidebar and an isolated, scrollable inter-agent terminal feed.

---

## System Architecture

The simulation runs on a localized state-tracking loop managed entirely through Streamlit's Session State framework.

Every agent retains a profile state dictionary that keeps memory across execution cycles:
- **Patience (0-100%):** Decays incrementally per action sequence. Reaching low levels triggers more aggressive and erratic dialogue patterns.
- **Trust Vectors (0-100%):** Tracks individual inter-agent relationship statuses, fluctuating dynamically based on combative dialogue patterns and archetype variables.

---

## Installation

If you would like to install the following program locally, please complete the following steps:

1. Clone the repository to your workspace
2. Install the necessary dependencies: `pip install streamlit g4f requests`
3. Launch the local operation server by typing this in the terminal: `python -m streamlit run trustship.py`

## Supported Character Archetypes

* **The Rational Stoic**: Analytical, logical, and prioritizes strict survival percentages.
* **The Strategic Opportunist**: Selfish, self-serving, and looks out for personal leverage.
* **The Paranoid Instigator**: Suspicious and provocative; drives arguments and distrust.
* **The Dominant Voice**: Loud, aggressive, and demands swift team compliance.

## License

Distributed under the MIT license. See `LICENSE` for more information.
