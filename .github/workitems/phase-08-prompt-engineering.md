# Work Item WI-008: Phase 8 - Prompt Engineering Strategy

## Status
- [x] Done
- [ ] Not started
- [ ] In progress
- [ ] Blocked

## Goal

Design and implement effective prompt templates for generating high-quality, factual explanations using Google Gemini.

## Core Principle

- Prompts must enforce **factual grounding** — explanations must reference actual complaint content
- Prevent hallucinations by providing explicit constraints
- Maintain consistent explanation quality and format

## Scope

### 1. Prompt Template Design

- Role definition (AI Explainability Assistant)
- Task description (explain classification decision)
- Context injection (complaint text + category)
- Output constraints (length, tone, format)

### 2. Template Variants

- Standard explanation (2-3 sentences)
- Confidence-aware explanation (adjust tone for low confidence)
- High-confidence explanation (more assertive)

### 3. Parameter Tuning

- Temperature settings
- Max token limits
- Safety settings

## Acceptance Criteria

- Explanations are factual and relevant
- Output format is consistent
- No hallucinations about complaint content
- Templates handle edge cases

## Prompt Components

```text
ROLE: You are an AI assistant specialized in explaining ML decisions.

TASK: Generate a clear, factual explanation (2-3 sentences) for why
      this complaint was classified into this category.

CONTEXT:
- Complaint: {complaint_text}
- Predicted Category: {category}
- Confidence: {confidence}

CONSTRAINTS:
- Only reference content from the complaint
- Use professional, neutral tone
- Be specific about keywords/patterns that led to classification
```

## Files Created/Modified

- `src/backend/genai/explanation.py` - Prompt templates

## Success Criteria

- Explanations consistently high quality
- No made-up details
- Appropriate length (2-3 sentences)
- Professional tone maintained
