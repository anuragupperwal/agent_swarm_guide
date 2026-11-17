# Loop to Swarm: build progress

A visual study guide to agents, agent harnesses and agent swarms. Open `index.html` in a browser.
This file tracks which chapters exist, so work can resume in any later session.

Status key: `todo` · `partial` (cut off mid-page) · `draft` (complete, passes tools/check.py) · `done` (also: every figure looked at in a browser, worked numbers recomputed, uncertain facts checked. Not re-verified line by line against every cited source)

## Curriculum

| # | File | Title | Part / Level | Status |
|---|------|-------|--------------|--------|
| 01 | chapters/01-llm-as-a-component.html | The LLM as a component | 1 Foundations / L1 | done |
| 02 | chapters/02-workflows-vs-agents.html | Workflows vs agents | 1 Foundations / L1 | done |
| 03 | chapters/03-agent-loop.html | The agent loop | 1 Foundations / L1 | done |
| 04 | chapters/04-tool-use.html | Tool use in depth | 1 Foundations / L1 | done |
| 05 | chapters/05-reasoning-and-planning.html | Reasoning and planning patterns | 2 Thinking & memory / L2 | done |
| 06 | chapters/06-context-engineering.html | Context engineering | 2 Thinking & memory / L2 | done |
| 07 | chapters/07-memory.html | Memory systems | 2 Thinking & memory / L2 | done |
| 08 | chapters/08-agent-harness.html | What a harness is | 3 The harness / L3 | done |
| 09 | chapters/09-control-flow-and-state.html | Control flow and state | 3 The harness / L3 | done |
| 10 | chapters/10-concurrency.html | Concurrency for agents | 3 The harness / L3 | done |
| 11 | chapters/11-reliability.html | Reliability engineering | 3 The harness / L3 | done |
| 12 | chapters/12-security.html | Security and safety | 3 The harness / L3 | done |
| 13 | chapters/13-observability-and-evals.html | Observability and evaluation | 3 The harness / L3 | done |
| 14 | chapters/14-why-multi-agent.html | Why multiple agents (and why not) | 4 Multi-agent / L4 | done |
| 15 | chapters/15-topologies.html | Multi-agent topologies | 4 Multi-agent / L4 | done |
| 16 | chapters/16-spawning-and-delegation.html | Spawning and recursive delegation | 4 Multi-agent / L4 | done |
| 17 | chapters/17-communication.html | Communication and coordination | 4 Multi-agent / L4 | done |
| 18 | chapters/18-swarm-intelligence.html | Swarm intelligence: from ants to LLMs | 4 Multi-agent / L4 | done |
| 19 | chapters/19-multi-agent-failures.html | How multi-agent systems fail | 4 Multi-agent / L4 | done |
| 20 | chapters/20-swarm-harness-architecture.html | Designing a swarm harness | 5 Putting it together / L5 | done |
| 21 | chapters/21-framework-landscape.html | The framework landscape | 5 Putting it together / L5 | done |
| 22 | chapters/22-interview-bank.html | Review and interview bank | 5 Putting it together / L5 | done |
| G | glossary.html | Glossary | reference | done |

Shared files: `index.html` (home, concept stack, mind map), `assets/style.css`, `assets/guide.js`.

## Chapter scope (the contract each chapter is written against)

**01 The LLM as a component.** Tokens and the generation loop; statelessness; the context window as the only memory; request/response anatomy; stop_reason as the first control-flow branch; structured output still needs validation; latency and cost; input tokens across an agent run grow with the square of the step count; non-determinism; a table mapping model limitations to harness responsibilities.

**02 Workflows vs agents.** The augmented LLM. Workflow patterns: prompt chaining, routing, parallelization (sectioning and voting), orchestrator-workers, evaluator-optimizer. Agents. Who owns the control flow. The autonomy spectrum. When not to build an agent. Round 2 Q1 checkpoint.

**03 The agent loop.** Minimum anatomy: model, instructions, tools, loop, state, stop condition, environment. Loop pseudocode. Trajectories. Stop conditions: natural end, max steps, budget, goal check. Agent vs function. A step-by-step trace. Round 2 Q1 checkpoint.

**04 Tool use in depth.** Tool definition: name, description, JSON Schema. The tool_use → execute → tool_result protocol and tool_use_id pairing. Parallel tool calls (all results go back in one message). Errors as observations (is_error). Tool design as an agent-computer interface. Granularity. Strict schemas. Tool choice. An MCP introduction. Tools that spawn agents (preview of ch16).

**05 Reasoning and planning patterns.** CoT, self-consistency, ReAct, plan-and-execute, ReWOO, LLMCompiler, Reflexion, Self-Refine, Tree of Thoughts, LATS. Native reasoning (thinking) models and what they change. A cost-vs-reliability decision table.

**06 Context engineering.** What fills the window; the attention budget, lost in the middle and context rot; ordering and the prompt-cache prefix; just-in-time retrieval vs preloading; compaction and clearing old tool results; structured notes; subagents as context isolation; the token growth math.

**07 Memory systems.** The CoALA taxonomy (working, episodic, semantic, procedural); in-context vs external memory. Write and read policies, with the Generative Agents recency, importance and relevance scoring. Embedding and vector-store basics. MemGPT paging. File-based memory. Consolidation. Memory risks: staleness, conflicts, provenance, poisoning. Private vs shared memory.

**08 What a harness is.** Harness vs framework vs scaffold vs SDK. Components: loop driver, model client, tool registry and executor, context manager, state store, permissions and sandbox, budget meter, tracer, human-in-the-loop. A request-lifecycle sequence. Claude Code as a worked example. "Model proposes, harness disposes." A swarm harness is a harness of harnesses.

**09 Control flow and state.** The agent lifecycle as a state machine. Explicit vs implicit control flow. Graphs: nodes, edges, conditional edges. State and reducers. Checkpoints and replay. Durable execution and idempotency. Human-in-the-loop interrupts. Event sourcing.

**10 Concurrency for agents.** I/O-bound vs CPU-bound work. Process vs thread vs coroutine vs function call (Round 2 Q2 checkpoint). The event loop and await points. create_task, gather, TaskGroup and structured concurrency. Cancellation, timeouts, semaphores. Races across an await (check-then-act on a budget). Blocking calls.

**11 Reliability engineering.** A failure taxonomy; errors as values; retries with backoff and jitter; idempotency; timeouts at every level; budgets and where they are enforced; validating LLM output; guardrails; circuit breakers; graceful degradation and partial results; loop detection. Round 2 Q3 checkpoint.

**12 Security and safety.** The agent threat model. Direct vs indirect prompt injection, and why it remains unsolved. The lethal trifecta. Least privilege and capability scoping. Sandboxing and egress control. Human approval. Treating output as untrusted. The dual-LLM pattern and CaMeL. Secrets. Multi-agent risks: injection spreading between agents, and spawning as privilege escalation.

**13 Observability and evaluation.** Logs, metrics and traces; the span model; a spawn-tree trace; the OpenTelemetry GenAI conventions; what to record. Outcome vs trajectory vs component evals. Graders: code, LLM-as-judge (and its biases), human. pass@k vs pass^k. Running each eval N times. Benchmarks and their caveats. The single-agent baseline.

**14 Why multiple agents (and why not).** Context isolation, parallelism, specialization. Evidence from Anthropic's multi-agent research system. Costs: tokens, coordination latency, error compounding, information loss. A decision checklist.

**15 Multi-agent topologies.** Pipeline, router, orchestrator-worker, hierarchical, network/mesh, blackboard, handoff, debate/voting, market/contract net. A comparison table. Hybrids. Where the project sits.

**16 Spawning and recursive delegation.** Subagent-as-tool. The spawn lifecycle: propose, validate, create, register, schedule, run, return, aggregate. Create vs run. What a child receives. The return contract. Context passing and the telephone game. Limits and the growth math, sum of f^d (Round 2 Q3 checkpoint). Budget pools. Aggregation. Termination.

**17 Communication and coordination.** Shared state vs message passing. Mailboxes and queues. Request/reply vs fire-and-forget. Addressing and discovery. Message schemas. Pub/sub and blackboards. Handoffs. Deadlock, livelock and duplicate work. Consensus and voting. Speech acts and contract net. MCP vs A2A. Growth in the number of channels.

**18 Swarm intelligence.** Boids, ant colony optimization and stigmergy, particle swarm optimization. Emergence. LLM "swarms": OpenAI Swarm handoffs, agent societies, debate. What transfers to LLM agents and what doesn't.

**19 How multi-agent systems fail.** The MAST taxonomy (3 categories, 14 modes). Concrete swarm failures, the signals each leaves in a trace, and a mitigation table.

**20 Designing a swarm harness.** Requirements. A reference component diagram. The sequence of one run. Data models as fields to consider. Open design decisions, written as questions with options; the guide does not make the decisions. A map to Stages 0–9 of the plan. What production adds.

**21 The framework landscape.** Concept → framework mapping for LangGraph, the OpenAI Agents SDK, the Claude Agent SDK, AutoGen/AG2, CrewAI, Strands and smolagents, plus MCP and A2A. How to evaluate a framework. Build vs adopt.

**22 Review and interview bank.** Concept questions by chapter. Whiteboard prompts. System design questions with an answer framework. Red flags. A spaced-repetition schedule.

## Log
- 2026-11-16: Folder and curriculum created. The first build attempt stopped because the disk was full (ENOSPC).
- 2026-11-16: Shared design system (assets/), home page with concept stack and mind map, and Chapter 01 written. Chapters 02–22 and the glossary are being written in parallel, in seven groups of three; each group writes its chapters in order. If a session ends partway, any chapter still marked `todo` here has not been checked yet: open the file if it exists, or write it from the scope above using Chapter 01 as the template.
- 2026-11-17: Disk space freed. Home and Chapter 01 checked in headless Chrome (desktop, phone at 375px, light and dark): no overflow and no broken structure. Fixed a mislabelled run in Figure 1.6, the steps grid, and added a "scroll sideways" hint for wide figures on phones. Static checker saved as `tools/check.py`; run `python3 -I tools/check.py .` from this folder after adding a chapter.
- 2026-11-17: The spending budget ran out while the parallel agents were writing, and all of them stopped. 04 turned out complete. 09, 13, 19 and 22 were cut off mid-page; 07, 10 and the glossary were never started. Second pass: three fresh agents write 07, 10 and the glossary, and the four partial chapters get their endings by hand.
- 2026-11-17: Guide complete. 07, 10 and the glossary were written by fresh agents, and the endings of 09, 13, 19 and 22 by hand (19 gained Figure 19.5, 22 gained Drills 3 and 4 and Figure 22.5). Every figure was looked at in headless Chrome. Fixed label collisions or overflow in 7.1, 11.1, 11.3, 15.3, 15.7, 15.8, 16.2, 16.4, 20.4 and 22.5, and a wrong colour name in the 16.3 caption. Reading times for 07, 10 and 17 were raised to match their length. All 24 pages pass tools/check.py, the prev/next chain is intact, and no page scrolls sideways at 375px.

## Re-checking after an edit

From this folder:
- `python3 -I tools/check.py .`: tags, ids, links, anchors, undefined classes, template parts.
- `python3 -I tools/chain.py .`: the prev/next chain, done toggles and word counts.
- Figure text overlap (needs Google Chrome): `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --allow-file-access-from-files --virtual-time-budget=4000 --dump-dom "file://$PWD/tools/svglint.html?page=$PWD/chapters/NN-name.html"`. The result is in the `<pre id="out">` element. `tools/phone.html?page=...` does the same for horizontal overflow at 375px.
