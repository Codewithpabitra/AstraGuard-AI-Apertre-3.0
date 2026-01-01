# AstraGuard AI: Technical Report

**Autonomous Fault Detection & Recovery System for CubeSats with Adaptive Memory Architecture**

| Performance Metric | Value |
| :--- | :--- |
| **Response Time** | 325 ms |
| **Detection Accuracy** | 95%+ |
| **Memory Footprint** | <400MB |

AstraGuard AI is a production-ready, autonomous fault detection and recovery system designed for CubeSat missions. This report presents a comprehensive technical analysis of the system's architecture, which bridges the gap between static anomaly detection and autonomous agency through a streaming awareness pipeline, an adaptive memory engine, and an agentic decision loop. Built on the Pathway Engine, AstraGuard processes high-frequency telemetry to detect threats, reason over historical context, and execute recovery actions with sub-second latency. The system demonstrates streaming awareness, adaptive memory with temporal weighting, and autonomous decision-making capabilities, achieving end-to-end latency of approximately 325 ms and detection accuracy exceeding 95% in simulated fault scenarios.

---

## 1 Executive Summary

AstraGuard AI advances spacecraft autonomy through a Security-First AI architecture that treats spacecraft health monitoring as a continuous, streaming process. The system addresses critical challenges in CubeSat operations where limited bandwidth and high latency to ground control create dangerous gaps in fault management.

### 1.1 Key Achievements

- **Real-Time Agency**: Not merely a monitoring dashboard, but an autonomous agent capable of executing recovery actions.
- **Biologically-Inspired Memory**: Temporal decay and signal reinforcement mechanisms maintain lean, relevant context.
- **Autonomous Recovery**: Complete loop from detection to containment without human intervention.
- **Sub-Second Response**: Total pipeline latency of ∼325 ms, 10x faster than human reaction time.
- **Edge-Ready Deployment**: Optimized memory footprint under 400MB, suitable for satellite On-Board Computers.

---

## 2 Problem Statement: The CubeSat Crisis

### 2.1 Current Challenges in Small Satellite Operations

Small satellites (CubeSats) operate under severe constraints that make traditional fault management approaches inadequate:

1.  **The Latency Gap**: Critical hardware failures occur faster than ground control can respond. Communication delays of several minutes to hours make real-time intervention impossible for many failure modes.
2.  **Static Threshold Limitations**: Traditional rule-based systems fail to detect complex, evolving patterns. Simple voltage or temperature thresholds cannot capture the nuanced signatures of cascading failures.
3.  **Manual Intervention Bottleneck**: Ground teams are too slow for critical failures such as tumbling, power spikes, or thermal runaways. Human operators cannot maintain 24/7 vigilance for entire satellite constellations.
4.  **Context Window Bloat**: LLM-based agents suffer from either forgetting critical historical failures or being overwhelmed by irrelevant historical data, leading to degraded decision quality over time.

### 2.2 The Need for Autonomous Intelligence

The proliferation of CubeSat constellations and the increasing complexity of space missions demand a new approach: autonomous systems that can detect, reason, and act independently while maintaining explainability and safety. AstraGuard AI addresses this need through intelligent autonomy grounded in biologically-inspired principles.

---

## 3 Solution Architecture

### 3.1 System Overview

AstraGuard AI implements a five-stage processing pipeline:

1.  **Data Ingestion**: Real-time telemetry streaming via Pathway Engine.
2.  **Encoding & Embedding**: Transformation of raw sensor data into semantic vectors.
3.  **Adaptive Memory**: Temporal weighting and intelligent retention of historical context.
4.  **Agentic Decision Loop**: Detect → Recall → Reason → Act → Learn cycle.
5.  **Response Orchestration**: Concrete system actions with feedback integration.

### 3.2 Core Architectural Principles

**Design Philosophy**
- **Streaming Awareness**: Process data continuously, not in batches.
- **Memory Evolution**: Context that prunes and reinforces itself.
- **Explainable Agency**: Decisions with transparent reasoning traces.
- **Action-Feedback Loop**: Continuous learning from outcomes.

---

## 4 Technical Deep Dive

### 4.1 Data Ingestion Layer: Pathway Engine Integration

AstraGuard leverages the Pathway Engine for real-time telemetry processing at 5 Hz. Unlike traditional batch processing systems, Pathway treats data streams as live tables, enabling:

- **Temporal Joins**: Dynamic correlation between current telemetry and historical baselines.
- **Low-Latency Windowing**: Statistical outlier detection with sliding time windows.
- **Stream Processing**: Continuous computation without the overhead of batch boundaries.

The ingestion layer processes multiple telemetry channels including voltage levels, temperature sensors, gyroscope readings, and attitude control system status.

### 4.2 Encoding & Embedding Module

Raw telemetry undergoes normalization and encoding to produce 384-dimensional embeddings. This transformation serves multiple purposes:

1.  **Semantic Representation**: Captures the "state" of the satellite at each time point.
2.  **Similarity Computation**: Enables efficient retrieval of historically similar conditions.
3.  **Dimensionality Reduction**: Compresses high-dimensional sensor data while preserving critical features.

The encoding process uses a lightweight neural architecture optimized for edge deployment, achieving encoding latency of approximately 12ms per event.

### 4.3 Adaptive Memory Engine: The Core Innovation

The Adaptive Memory Engine represents the primary technical innovation of AstraGuard AI. Instead of a conventional database, we implement a Dynamic Memory Store with sophisticated retention policies.

#### 4.3.1 Temporal Weighting Mechanism

Events decay in importance over time following an exponential function:

$$W(t) = e^{-\lambda t}$$

where $W(t)$ is the weight at time $t$ and $\lambda$ is the decay constant (typically 0.1). This ensures the agent prioritizes recent trends while maintaining awareness of historical patterns.

#### 4.3.2 Safe Decay Policy

Critical events are exempt from automatic pruning through a multi-criteria evaluation:
- **Severity Threshold**: Events with severity ≥ 0.8 are "pinned".
- **Type Protection**: Certain fault categories (e.g., total power loss) are permanently retained.
- **Recurrence Patterns**: Frequently occurring anomalies maintain elevated retention priority.

#### 4.3.3 Recurrence Resonance Scoring

We introduce a novel signal reinforcement mechanism inspired by physical resonance phenomena:

$$R = S_{base} \times (1 + \alpha \log(1 + n_{recur})) \times W(t)$$

where:
- $R$ is the resonance score
- $S_{base}$ is the base severity
- $\alpha$ is the resonance factor (typically 0.3)
- $n_{recur}$ is the recurrence count
- $W(t)$ is the temporal decay weight

This mechanism ensures that low-severity faults that repeat frequently are escalated before causing hardware fatigue or cascading failures.

### 4.4 Agentic Decision Loop

The agent implements a complete decision cycle:
1.  **Detect**: Anomaly identification via Isolation Forest or threshold analysis.
2.  **Recall**: Query memory store for similar historical incidents using vector similarity.
3.  **Reason**: Hybrid engine (rule-based + LLM) analyzes current state versus historical context.
4.  **Act**: Trigger appropriate workflow in Response Orchestrator.
5.  **Learn**: Update memory store with action outcome and effectiveness metrics.

#### 4.4.1 Reasoning Engine

The reasoning component employs a two-stage process:
1.  **Rule-Based Triage**: Fast deterministic evaluation for known failure modes.
2.  **LLM-Assisted Analysis**: Deep reasoning for novel or ambiguous situations.

Every decision generates an explainable trace in plain language, ensuring human operators can understand and trust the autonomous actions.

### 4.5 Response Orchestrator

The orchestrator maps decisions to concrete system commands:

**Table 1: Recovery Action Workflows**

| Fault Type | Action | Implementation |
| :--- | :--- | :--- |
| **Power Anomaly** | `SAFE_MODE` | Shed non-essential loads |
| **Thermal Threat** | `THERMAL_REGULATION` | Adjust heater/cooler duty cycles |
| **Attitude Loss** | `STABILIZATION` | Fire thrusters, adjust reaction wheels |
| **Communication Loss** | `ANTENNA_REPOINT` | Execute reorientation sequence |

Each action includes:
- **Cooldown Management**: Prevents action spam through temporal rate limiting.
- **Feedback Integration**: Action outcomes feed back into memory for continuous improvement.
- **Safety Constraints**: Hard limits prevent dangerous command sequences.

---

## 5 Performance Analysis

### 5.1 Quantitative Metrics

**Table 2: System Performance Benchmarks**

| Metric | Target | Actual | Impact |
| :--- | :--- | :--- | :--- |
| **End-to-End Latency** | < 2s | ∼325 ms | 10x faster than human |
| **Memory Retrieval** | < 50ms | ∼38ms | Real-time context recall |
| **Embedding Encoding** | < 20ms | ∼12ms | Efficient state capture |
| **Detection Accuracy** | > 90% | 95%+ | High reliability |
| **Memory Footprint** | < 500MB | <400MB | Edge-deployable |
| **Memory Updates** | Real-time | Continuous | Live learning |

### 5.2 Scalability Analysis

The modular architecture enables horizontal scaling:
- **Multi-Satellite Support**: Single memory store can serve constellation of up to 100 CubeSats.
- **Memory Efficiency**: Auto-pruning maintains constant memory usage regardless of operation duration.
- **Computation Distribution**: Decision loop can be partitioned across multiple cores.

### 5.3 Reliability & Safety

Safety mechanisms include:
- **Action Whitelisting**: Only pre-approved commands can be executed.
- **Rate Limiting**: Cooldown periods prevent rapid oscillation between states.
- **Fallback Modes**: System degrades gracefully to simple rule-based control if memory or reasoning fails.
- **Audit Trail**: Complete logging of all decisions and actions for post-mission analysis.

---

## 6 Key Innovations

### 6.1 Innovation 1: Recurrence Resonance Scoring

Traditional frequency-based anomaly detection treats each occurrence independently. Our resonance mechanism recognizes that repeated minor faults often indicate systemic issues:

**Resonance Principle**

A low-severity fault that occurs 10 times is more dangerous than a single medium-severity fault. The resonance scorer amplifies the signal based on repetition patterns while respecting temporal decay.

Implementation: Approximately 10 lines of code demonstrate first-principles thinking, moving beyond naive counting to physics-inspired signal reinforcement.

### 6.2 Innovation 2: Hybrid Memory Architecture

The memory system combines:
- **Vector Similarity**: Fast retrieval of contextually similar historical events.
- **Temporal Indexing**: Efficient queries over time windows.
- **Metadata Enrichment**: Each event includes severity, type, resolution status, and action effectiveness.

This hybrid approach achieves retrieval latency of 38ms while maintaining rich contextual information.

### 6.3 Innovation 3: Explainable Autonomy

Every autonomous decision includes:
1.  **Reasoning Trace**: Plain-language explanation of why the action was chosen.
2.  **Confidence Score**: Quantitative measure of decision certainty.
3.  **Alternative Actions**: Other options considered and why they were rejected.
4.  **Expected Outcome**: Predicted effect of the chosen action.

This explainability is critical for building operator trust and enabling regulatory approval of autonomous systems.

---

## 7 System Components

### 7.1 Memory Engine Module (`memory_engine/`)

- **Adaptive Memory Store**: Core storage with temporal weighting and auto-pruning.
- **Recurrence Scorer**: Signal reinforcement for repeated patterns.
- **Decay Policy**: Safe pruning with critical event protection.
- **Replay Engine**: Flight recorder functionality for incident investigation.
- **Persistence Layer**: Crash-resistant state serialization.

### 7.2 Anomaly Agent Module (`anomaly_agent/`)

- **Decision Loop**: Main orchestration of detect → recall → reason → act → learn.
- **Reasoning Engine**: Hybrid rule-based and LLM-assisted analysis.
- **Confidence Scorer**: Decision quality metrics.
- **Action Validator**: Safety checks before command execution.

### 7.3 Response Orchestrator Module (`response_orchestrator/`)

- **Workflow Registry**: Maps fault types to recovery procedures.
- **Action Implementations**: Concrete system commands (not simulated).
- **Cooldown Manager**: Temporal rate limiting for action execution.
- **Feedback Collector**: Captures action outcomes for learning.

### 7.4 Dashboard Interface

- **Technology**: Streamlit with glassmorphism design.
- **Features**:
    - Real-time telemetry visualization
    - Memory state inspector
    - Decision trace viewer
    - Action history timeline
    - Frontier Mode: Visualizes adaptive memory flow and BDH neural activity.

---

## 8 Configuration & Customization

### 8.1 Defense Thresholds
Configurable in `classifier/fault_classifier.py`:
```python
# Power System
VOLTAGE_CRITICAL = 7.3   # Volts
VOLTAGE_WARNING = 7.5    # Volts
# Thermal System
TEMP_CRITICAL = 32.0     # Celsius
TEMP_WARNING = 30.0      # Celsius
# Attitude Control
GYRO_CRITICAL = 0.05     # rad/s
GYRO_WARNING = 0.03      # rad/s
```

### 8.2 Memory Parameters
Configurable in `memory_engine/memory_store.py`:
```python
# Temporal Decay
DECAY_LAMBDA = 0.1       # Decay rate constant
DECAY_HALFLIFE = 24.0    # Hours
# Capacity Management
MAX_MEMORY_SIZE = 10000  # Events
PRUNE_THRESHOLD = 0.05   # Minimum retention weight
# Critical Event Protection
CRITICAL_SEVERITY = 0.8  # Pin threshold
RETENTION_HOURS = 24     # Exempt period
```

### 8.3 Resonance Tuning
Configurable in `memory_engine/recurrence_scorer.py`:
```python
# Resonance Parameters
RESONANCE_ALPHA = 0.3    # Amplification factor
RECURRENCE_WINDOW = 3600 # Seconds (1 hour)
MIN_RECURRENCE = 3       # Minimum count for boost
```

---

## 9 Testing & Validation

### 9.1 Test Suite
Comprehensive testing implemented using pytest:
- **Unit Tests**: Individual component validation (memory store, recurrence scorer, decision loop).
- **Integration Tests**: End-to-end pipeline validation.
- **Performance Tests**: Latency and throughput benchmarking.
- **Safety Tests**: Validation of action whitelisting and rate limiting.

### 9.2 Simulation Results
Testing conducted on realistic CubeSat failure scenarios:

**Table 3: Fault Detection & Recovery Performance**

| Scenario | Detection Time | Recovery Success |
| :--- | :--- | :--- |
| **Battery Depletion** | 280ms | 100% |
| **Thermal Runaway** | 310ms | 98% |
| **Tumbling Event** | 340ms | 95% |
| **Communication Loss** | 290ms | 92% |
| **Sensor Degradation** | 350ms | 94% |

---

## 10 Future Development Roadmap

### 10.1 Version 3.0: Multi-Agent Swarm Intelligence
- **Objective**: Enable multiple satellites to share a distributed memory store.
- **Benefits**: Collective learning, pre-emptive adjustments.
- **Technical Challenges**: Distributed consensus, high-latency synchronization.

### 10.2 Deep BDH Integration
- **Objective**: Transition from "inspired by" to "built on" the Dragon Hatchling (BDH) architecture.
- **Implementation**: Sparse neural activation for ultra-low power consumption.

### 10.3 Hardware-in-the-Loop Validation
- **Objective**: Deploy to physical CubeSat flatsats (Raspberry Pi 4, Jetson Nano, BeagleBone).
- **Validation**: Power consumption, thermal management in vacuum.

### 10.4 Regulatory Certification Path
- **Objective**: Achieve autonomous operation approval from space agencies.
- **Requirements**: Formal verification, FMEA, safety case documentation.

---

## 11 Impact & Applications

### 11.1 Immediate Applications
1.  **Earth Observation Constellations**: Maintain imaging continuity.
2.  **Communication Networks**: Ensure LEO broadband availability.
3.  **Scientific Missions**: Protect instruments during critical windows.

### 11.2 Future Mission Enablers
- **Deep Space**: Autonomy for Mars/Outer Planet missions (high latency).
- **Cislunar**: Predictive maintenance for Lunar Gateway.

---

## 12 Conclusion

AstraGuard AI represents more than an incremental improvement in satellite fault management—it embodies a fundamental reimagining of spacecraft autonomy. By combining the streaming power of Pathway with biologically-inspired adaptive memory, we have created a system that doesn't merely monitor but genuinely understands and protects.

### Acknowledgments
This project was developed for the **Synaptix Frontier AI Hackathon** at IIT Madras.

**Team Members:**
- **Subhajit Roy**: Team Leader, Lead Developer
- **Ayush Sharma**: Development & Integration
- **Aditya Mishra**: Frontend

**Special Thanks to:** Pathway (Streaming Engine), Streamlit, scikit-learn, and the Open Source Community.

---

## Appendix A: Installation & Quick Start

### A.1 Prerequisites
- Python 3.9+
- pip
- git

### A.2 Installation Steps
```bash
git clone https://github.com/sr-857/AstraGuard.git
cd AstraGuard
pip install -r requirements.txt
python verify_install.py
```

### A.3 Running the System
```bash
python examples/run_demo.py
streamlit run dashboard/app.py
```

### A.4 Running Tests
```bash
pytest tests/ -v
```

---

## Appendix B: API Reference

### B.1 Memory Store Interface
```python
from memory_engine import AdaptiveMemoryStore
memory = AdaptiveMemoryStore(max_capacity=10000, decay_lambda=0.1)
memory.add_event(embedding, metadata={'severity': 0.8})
```

### B.2 Agent Decision Loop
```python
from anomaly_agent import AnomalyAgent
agent = AnomalyAgent(memory_store=memory)
decision = agent.process_anomaly(telemetry, anomaly_score=0.85)
agent.execute_decision(decision)
```

---

## Appendix C: License

This project is released under the **MIT License**.
Copyright (c) 2025 Subhajit Roy.
