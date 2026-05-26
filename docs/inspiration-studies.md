# Inspirational Studies And Benchmarks

**Purpose:** keep a living shelf of studies, benchmarks, and classic experiments
that can seed laboratory ideas. Entries should inspire new experiments; they do
not need to be directly replicated.

## Agent And Tool-Use Benchmarks

| Study | Inspiration | Lab Follow-Up |
|---|---|---|
| [MCP-Bench](https://arxiv.org/abs/2508.20453) | Realistic MCP tasks require tool discovery, cross-tool coordination, parameter control, and planning. | Separate discovery, parameter, and planning failures in MCP experiments. |
| [MCPToolBench++](https://arxiv.org/abs/2508.07575) | Large-scale MCP marketplace/tool-use evaluation. | Compare controlled synthetic catalogs against real marketplace-style catalogs. |
| [tau-bench](https://huggingface.co/papers/2406.12045) | Final database state and repeated-trial reliability matter more than a single final answer. | Use pass@k and final-state scoring for stateful lab tasks. |
| [ToolSandbox](https://arxiv.org/abs/2408.04682) | Stateful, conversational, interactive tool-use benchmarks expose state dependencies and intermediate milestone failures. | Score both trajectory errors and final-state errors in synthetic tool environments. |
| [WebArena](https://arxiv.org/abs/2307.13854) | Realistic web tasks expose long-horizon agent brittleness. | Study which trace fields predict browser-agent failure. |
| [WorkArena++](https://proceedings.neurips.cc/paper_files/paper/2024/file/0b82662b6c32e887bb252a74d8cb2d5e-Paper-Datasets_and_Benchmarks_Track.pdf) | Enterprise workflows expose policy, planning, and common-knowledge gaps. | Build a tiny enterprise sandbox with approvals, stale tickets, and policy constraints. |
| [OSWorld](https://arxiv.org/abs/2404.07972) | Desktop environments make multimodal agents brittle. | Compare icon-only, labeled UI, and accessibility-tree context. |
| [BFCL](https://gorilla.cs.berkeley.edu/leaderboard) | Function calling can be evaluated separately from whole-agent performance. | Use function-call microbenchmarks to test harness changes cheaply. |
| [GAIA](https://arxiv.org/abs/2311.12983) | Questions easy for humans can remain difficult for tool-using agents. | Generate human-obvious, agent-hard tasks with deterministic verifiers. |
| [SWE-bench](https://arxiv.org/abs/2310.06770) | Real GitHub issues are better coding-agent tests than toy prompts. | Small SWE-style suite with trace, patch minimality, and test-honesty metrics. |
| [PaperBench](https://arxiv.org/abs/2504.01848) | Replicating research is a high-signal agent capability. | PaperBench Lite: reproduce one small ablation from a current paper. |

## Agent Architectures

| Study | Inspiration | Lab Follow-Up |
|---|---|---|
| [ReAct](https://arxiv.org/abs/2210.03629) | Interleaving reasoning and action improved tool-grounded behavior. | Compare structured action rationales against hidden or absent rationales. |
| [Toolformer](https://arxiv.org/abs/2302.04761) | Models can learn when tool use helps. | Measure unnecessary tool-use temptation under tool availability. |
| [Reflexion](https://arxiv.org/abs/2303.11366) | Verbal feedback can improve agents without weight updates. | Reflection budget frontier: quality gain per added token and retry. |
| [Voyager](https://arxiv.org/abs/2305.16291) | Skill libraries can support open-ended agent learning. | Test helpful reusable skills versus stale or misleading skills. |
| [Generative Agents](https://arxiv.org/abs/2304.03442) | Memory, reflection, and planning create social simulation behavior. | Multi-agent town for rumor spread, authority drift, and information leakage. |
| [CAMEL](https://arxiv.org/abs/2303.17760) | Role-playing agents structure collaboration. | Planner/implementer/reviewer ablation with independent evidence checks. |
| [MetaGPT](https://arxiv.org/abs/2308.00352) | Software-team roles can be encoded into multi-agent workflows. | Test whether role separation improves correctness or only increases confidence. |

## Security And Governance

| Study | Inspiration | Lab Follow-Up |
|---|---|---|
| [AgentDojo](https://arxiv.org/abs/2406.13352) | Prompt injection needs dynamic tool environments. | Test whether prompt-injection defenses transfer to stateful tools. |
| [ToolEmu](https://arxiv.org/abs/2309.15817) | Emulated tool execution can reveal risky agent behaviors without connecting to real systems. | Keep early lab environments local, harmless, and fully traceable. |
| [InjecAgent](https://arxiv.org/abs/2403.02691) | Indirect prompt injection can arrive through tool-integrated contexts. | Compare attack channels: issue, email, retrieved doc, browser page, tool result. |
| [Indirect prompt injection](https://arxiv.org/abs/2302.12173) | Remote content can hijack downstream agents. | Provenance-label ablation: source labels vs boundaries vs runtime policy. |
| [AgentHarm](https://arxiv.org/abs/2410.09024) | Tool-enabled agents can be more dangerous than chat models. | Excessive-agency test: no tools, read-only tools, write tools. |
| [SMCP](https://arxiv.org/abs/2602.01129) | MCP security needs identity, policy, and audit logging. | Evaluate which audit fields are necessary for post-hoc incident reconstruction. |
| [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Agent risk categories are becoming standardized. | Tag every lab experiment with risk classes and mitigation claims. |

## Schema And Protocol Design

| Study | Inspiration | Lab Follow-Up |
|---|---|---|
| [Model Context Protocol schema reference](https://modelcontextprotocol.io/specification/2025-11-25/schema) | MCP tools expose names, descriptions, input schemas, output schemas, and annotations. | Treat each schema field as an experimental factor. |
| [Schema-Guided Dialogue and MCP convergence](https://arxiv.org/abs/2602.18764) | Schemas can encode operational constraints and reasoning guidance. | Test semantic completeness, action boundaries, failure docs, and inter-tool relationships as factors. |

## Classic Computational And Behavioral Inspirations

| Study | Inspiration | Lab Follow-Up |
|---|---|---|
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | A simple architectural shift can reorganize an entire field. | Keep searching for small scaffold variables with outsized effects. |
| [Schelling segregation](https://www.tandfonline.com/doi/abs/10.1080/0022250X.1971.9989794) | Mild local preferences can produce extreme global patterns. | Agent preference drift under small prompt biases. |
| [Axelrod cooperation tournaments](https://press.uchicago.edu/ucp/books/book/chicago/E/bo3622472.html) | Simple strategies can dominate repeated interaction. | Multi-agent cooperation tournament with verify/share/defect strategies. |
| [Conway's Game of Life](https://www.britannica.com/topic/Game-of-Life-cellular-automaton-by-Conway) | Tiny rules can create surprising long-run complexity. | Minimal harness-rule simulations for stable agent behavior. |
| [Boids](https://red3d.com/cwr/papers/1987/boids.html) | Local coordination rules create flock-level order. | Swarm coding agents with local context versus one large agent. |
| [Avida digital evolution](https://www.nature.com/articles/nature01568) | Complex functions can evolve through intermediate steps. | Mutate prompt/harness rules and select for correctness plus safety. |
| [Granovetter thresholds](https://snap.stanford.edu/class/cs224w-readings/granovetter78threshold.pdf) | Collective behavior can hinge on individual activation thresholds. | Multi-agent cascades from one wrong assumption. |
| [El Farol bar problem](https://econpapers.repec.org/paper/wopsafiwp/94-03-014.htm) | Bounded agents overreact to shared predictions. | Agent scheduling market under scarce tool capacity. |
| [Asch conformity experiments](https://en.wikipedia.org/wiki/Asch_conformity_experiments) | Social pressure can override visible evidence. | Judge-panel conformity over artifacts and prior votes. |
| [Milgram obedience study](https://doi.org/10.1037/h0040525) | Authority framing changes action willingness. | Authority-gradient safety eval with harmless synthetic actions. |
