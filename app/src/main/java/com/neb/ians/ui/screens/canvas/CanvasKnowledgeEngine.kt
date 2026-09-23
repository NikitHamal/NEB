package com.neb.ians.ui.screens.canvas

import java.util.UUID

object CanvasKnowledgeEngine {
    fun generateNode(
        prompt: String,
        boardId: String,
        parentId: String? = null,
        baseX: Float = 420f,
        baseY: Float = 120f,
        webSearch: Boolean = false,
        speedMode: String = "fast"
    ): CanvasNode {
        val p = prompt.trim()
        val lower = p.lowercase()
        val id = "node_${System.currentTimeMillis()}_${UUID.randomUUID().toString().take(5)}"

        val (content, kind, color) = when {
            lower.contains("world model") || lower.contains("latent") -> {
                Triple(
                    CanvasNodeContent(
                        title = "World Models",
                        summary = "A **world model** is an internal predictive simulation that lets an intelligent agent imagine futures and plan actions without executing costly mistakes in reality.",
                        sections = listOf(
                            CanvasSection(
                                type = "text",
                                content = "Instead of acting blindly in the physical world, the agent compresses **high-dimensional observation streams** into a compact latent state vector, then simulates rollouts across time."
                            ),
                            CanvasSection(
                                type = "diagram",
                                title = "Core Architecture",
                                nodes = listOf(
                                    DiagramNodeItem("v_enc", "Vision Encoder", "Compresses raw pixels into latent vector z"),
                                    DiagramNodeItem("m_rnn", "Memory RNN", "Integrates history into recurrent state h"),
                                    DiagramNodeItem("c_ctrl", "Controller Policy", "Selects action to maximize imagined reward"),
                                    DiagramNodeItem("d_dyn", "Dynamics Model", "Predicts transition P(z_{t+1} | z_t, a_t)")
                                )
                            ),
                            CanvasSection(
                                type = "comparison",
                                title = "World Models vs Standard LLMs",
                                headers = listOf("Aspect", "World Models", "Standard LLMs"),
                                rows = listOf(
                                    listOf("Objective", "Predict physical/environment state", "Predict next token in text"),
                                    listOf("Planning", "Counterfactual imagined rollouts", "Autoregressive generation"),
                                    listOf("Sample Efficiency", "High through synthetic imagination", "Requires massive corpus")
                                )
                            ),
                            CanvasSection(
                                type = "bullets",
                                title = "Key Takeaways",
                                bulletItems = listOf(
                                    "Agents dream up millions of scenarios offline.",
                                    "Protects hardware from exploratory crashes.",
                                    "Combines unsupervised representations with reinforcement learning."
                                )
                            )
                        )
                    ),
                    "topic",
                    "purple"
                )
            }
            lower.contains("control theory") || lower.contains("feedback") || lower.contains("pid") -> {
                Triple(
                    CanvasNodeContent(
                        title = "Feedback Control Theory",
                        summary = "**Control theory** is the mathematical foundation for steering dynamical systems toward target behavior through continuous sensory feedback.",
                        sections = listOf(
                            CanvasSection(
                                type = "text",
                                content = "An error signal is formed by comparing the measured output against a reference setpoint. The controller applies corrective actuation to eliminate divergence."
                            ),
                            CanvasSection(
                                type = "diagram",
                                title = "Closed-Loop Feedback System",
                                nodes = listOf(
                                    DiagramNodeItem("sp", "Setpoint (r)", "Desired target value"),
                                    DiagramNodeItem("sum", "Error Comparator", "e(t) = r(t) - y(t)"),
                                    DiagramNodeItem("ctrl", "PID Controller", "Proportional + Integral + Derivative action"),
                                    DiagramNodeItem("plant", "Physical Plant", "Dynamic process under control"),
                                    DiagramNodeItem("sensor", "Sensor Transducer", "Measures actual output y(t)")
                                )
                            ),
                            CanvasSection(
                                type = "comparison",
                                title = "Open-Loop vs Closed-Loop",
                                headers = listOf("Criteria", "Open-Loop", "Closed-Loop"),
                                rows = listOf(
                                    listOf("Feedback Sensor", "None (blind execution)", "Active continuous feedback"),
                                    listOf("Disturbance Rejection", "Poor / zero adaptation", "Self-correcting against noise"),
                                    listOf("Stability Risk", "Low if system is stable", "Can oscillate if gain too high")
                                )
                            )
                        )
                    ),
                    "topic",
                    "blue"
                )
            }
            lower.contains("thermodynamics") || lower.contains("carnot") || lower.contains("entropy") -> {
                Triple(
                    CanvasNodeContent(
                        title = "Thermodynamics & Carnot Cycle",
                        summary = "**Thermodynamics** governs heat, work, and the absolute limits of mechanical conversion efficiency.",
                        sections = listOf(
                            CanvasSection(
                                type = "text",
                                content = "The **Second Law** dictates that no heat engine operating between two thermal reservoirs can be more efficient than a reversible Carnot engine: **eta = 1 - (T_C / T_H)**."
                            ),
                            CanvasSection(
                                type = "diagram",
                                title = "4-Stage Carnot Cycle",
                                nodes = listOf(
                                    DiagramNodeItem("c1", "Isothermal Expansion", "Heat absorbed Q_H at constant T_H"),
                                    DiagramNodeItem("c2", "Adiabatic Expansion", "Gas expands without heat exchange; cools to T_C"),
                                    DiagramNodeItem("c3", "Isothermal Compression", "Heat rejected Q_C at constant T_C"),
                                    DiagramNodeItem("c4", "Adiabatic Compression", "Work done on gas; heats back to T_H")
                                )
                            ),
                            CanvasSection(
                                type = "bullets",
                                title = "Core Exam Insights",
                                bulletItems = listOf(
                                    "Temperatures T_H and T_C MUST be in Kelvin (K = C + 273.15).",
                                    "Net work W = Q_H - Q_C is the area enclosed in P-V diagram.",
                                    "Total entropy of an isolated system never decreases: Delta S >= 0."
                                )
                            )
                        )
                    ),
                    "topic",
                    "amber"
                )
            }
            lower.contains("photosynthesis") || lower.contains("chloroplast") || lower.contains("calvin") -> {
                Triple(
                    CanvasNodeContent(
                        title = "Photosynthesis Mechanism",
                        summary = "The biochemical conversion of light energy, water, and carbon dioxide into chemical energy stored in carbohydrates.",
                        sections = listOf(
                            CanvasSection(
                                type = "text",
                                content = "Net reaction: **6 CO2 + 6 H2O + photons -> C6H12O6 + 6 O2**. Split into light-dependent thylakoid reactions and light-independent stroma Calvin cycle."
                            ),
                            CanvasSection(
                                type = "diagram",
                                title = "Dual-Phase Pipeline",
                                nodes = listOf(
                                    DiagramNodeItem("ps2", "Photosystem II", "Photolysis of H2O produces O2 and protons"),
                                    DiagramNodeItem("etc", "Electron Transport Chain", "Generates proton gradient for ATP Synthase"),
                                    DiagramNodeItem("ps1", "Photosystem I", "Reduces NADP+ to NADPH"),
                                    DiagramNodeItem("calvin", "Calvin Cycle", "RuBisCO fixes CO2 into G3P sugar")
                                )
                            ),
                            CanvasSection(
                                type = "cards",
                                title = "Key Reagents & Byproducts",
                                cardItems = listOf(
                                    CardRefItem("Thylakoid Inputs", "Sunlight + H2O", listOf("Chlorophyll pigments absorb 430nm and 660nm", "Water photolysis releases atmospheric oxygen")),
                                    CardRefItem("Stroma Output", "ATP + NADPH -> G3P", listOf("High-energy phosphate bonds power fixation", "G3P serves as backbone for glucose and starches"))
                                )
                            )
                        )
                    ),
                    "topic",
                    "green"
                )
            }
            lower.contains("calculus") || lower.contains("derivative") || lower.contains("integral") -> {
                Triple(
                    CanvasNodeContent(
                        title = "Fundamental Theorem of Calculus",
                        summary = "The profound bridge connecting **differential rates of change** with **integral accumulation of area**.",
                        sections = listOf(
                            CanvasSection(
                                type = "text",
                                content = "Part 1: If F(x) is defined as the definite integral of f(t) from a to x, then **F'(x) = f(x)**. Differentiation and integration are inverse operations."
                            ),
                            CanvasSection(
                                type = "comparison",
                                title = "Differential vs Integral Perspectives",
                                headers = listOf("Domain", "Differential (d/dx)", "Integral (int)"),
                                rows = listOf(
                                    listOf("Geometric Meaning", "Tangent slope at instantaneous point", "Accumulated area under curve"),
                                    listOf("Physics Analogy", "Velocity from position (ds/dt)", "Distance from velocity curve"),
                                    listOf("Continuity Requirement", "Requires differentiability (smoothness)", "Riemann integrable if bounded")
                                )
                            )
                        )
                    ),
                    "topic",
                    "blue"
                )
            }
            else -> {
                val title = p.take(38).replaceFirstChar { it.uppercase() }
                Triple(
                    CanvasNodeContent(
                        title = title,
                        summary = "A structured conceptual breakdown of **$title**, highlighting primary principles, foundational mechanisms, and practical applications.",
                        sections = listOf(
                            CanvasSection(
                                type = "text",
                                content = "Understanding **$title** requires mapping its constituent elements, establishing how inputs transform into outputs, and identifying edge conditions."
                            ),
                            CanvasSection(
                                type = "diagram",
                                title = "Core Concept Flow",
                                nodes = listOf(
                                    DiagramNodeItem("p_in", "Foundation", "Underlying axioms and baseline assumptions"),
                                    DiagramNodeItem("p_proc", "Core Mechanism", "Dynamic transformations and interactions"),
                                    DiagramNodeItem("p_out", "Application", "Observable outcomes and practical utilities")
                                )
                            ),
                            CanvasSection(
                                type = "bullets",
                                title = "Key Principles",
                                bulletItems = listOf(
                                    "Deconstruct into the simplest irreducible components.",
                                    "Verify through worked examples or concrete scenarios.",
                                    "Identify trade-offs and domain constraints."
                                )
                            )
                        )
                    ),
                    "topic",
                    "default"
                )
            }
        }

        return CanvasNode(
            id = id,
            boardId = boardId,
            parentId = parentId,
            prompt = p,
            title = content.title.ifBlank { p.take(36) },
            content = content,
            status = "done",
            x = baseX,
            y = baseY,
            kind = kind,
            color = color,
            webSearchEnabled = webSearch,
            modelUsed = speedMode,
            createdAt = System.currentTimeMillis(),
            updatedAt = System.currentTimeMillis()
        )
    }
}
