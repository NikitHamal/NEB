#!/usr/bin/env python3
"""Dataset generator for Needle 2 local LLM fine-tuning & RL (DPO/RLHF) on p5.js art generation.

Outputs JSONL formatted training data with queries, reasoning steps, tool calls, and answers
for training the 45M Needle model to generate p5.js visual artwork.
"""

import json
import random
import os

PROMPTS = [
    ("paint a glowing cosmic nebula", "generative", "neon", "high"),
    ("draw a hypnotic mandala pattern", "pattern", "cyberpunk", "high"),
    ("create a fractal tree swaying in wind", "fractal", "pastel", "medium"),
    ("draw a sunset wave landscape", "landscape", "warm", "medium"),
    ("make an abstract flow field drawing", "generative", "vibrant", "high"),
    ("paint a dark cyberpunk geometric artwork", "abstract", "cyberpunk", "extreme"),
    ("draw a minimalist monochrome line painting", "abstract", "monochrome", "low"),
    ("make a vibrant p5js interactive artwork", "generative", "vibrant", "medium"),
    ("paint a cool ocean wave drawing with p5.js", "landscape", "cool", "high"),
    ("draw a futuristic glowing geometric mandala", "pattern", "neon", "extreme"),
]

VARIATIONS = [
    "Can you {}?",
    "Please {} with p5.js.",
    "Use p5js to {}.",
    "I want you to {}.",
    "Hey, {}",
    "Could you generate code to {}?",
]


def generate_samples(num_samples=250):
    samples = []
    for _ in range(num_samples):
        prompt_tuple = random.choice(PROMPTS)
        prompt_text, style, palette, complexity = prompt_tuple
        pattern = random.choice(VARIATIONS)
        query = pattern.format(prompt_text)

        reasoning = (
            f"User wants p5.js artwork of '{prompt_text}'. "
            f"Mapped to generate_p5_art with style='{style}', color_palette='{palette}', complexity='{complexity}'."
        )

        sample = {
            "query": query,
            "tools": [
                {
                    "name": "generate_p5_art",
                    "parameters": {
                        "prompt": prompt_text,
                        "style": style,
                        "color_palette": palette,
                        "complexity": complexity,
                    },
                }
            ],
            "answers": [
                {
                    "name": "generate_p5_art",
                    "arguments": {
                        "prompt": prompt_text,
                        "style": style,
                        "color_palette": palette,
                        "complexity": complexity,
                    },
                }
            ],
            "reasoning": reasoning,
        }
        samples.append(sample)
    return samples


def main():
    output_path = os.path.join(os.path.dirname(__file__), "p5_needle_dataset.jsonl")
    samples = generate_samples(250)
    with open(output_path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")
    print(f"Generated {len(samples)} p5.js Needle training samples to {output_path}")


if __name__ == "__main__":
    main()
