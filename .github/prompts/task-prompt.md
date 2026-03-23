# Consumer Complaints ML + GenAI System Repository Verification and Content Enhancement

## Context

You are working with **Consumer Complaints ML + GenAI System**, an N-Tier enterprise application that automatically classifies consumer complaints using Machine Learning and generates human-readable explanations using Google Gemini. The repository implements a Flask REST API backend, PostgreSQL database, Scikit-learn ML pipeline, and Google Gemini API integration for explainability.

**Repository Structure:**

- `src/backend/` - Flask REST API with ML classification and GenAI explanation
- `infra/database/` - PostgreSQL schema and database setup
- `docs/` - Project documentation and architecture diagrams
- `.github/` - GitHub workflows and templates
- `.cursor/` - Cursor AI project rules

**Primary Objective:**
Perform a COMPREHENSIVE audit of the repository using Consumer Complaints ML + GenAI System standards and quality criteria. Verify file contents, run structured checks, and produce actionable reports with suggestions and fixes.

---

## Consumer Complaints System Verification Checks

### A. File Content Inspection

- Open and verify every file (no file skipped)
- Ensure markdown formatting compliance
- Check for completeness and consistency with project objectives
- Verify ZERO copy policy compliance (no copy-paste artifacts from other projects)

### B. Architecture Pattern Alignment

- Verify N-Tier architecture separation (Presentation, Application, ML/GenAI, Data Access, Database layers)
- Validate ML pipeline and GenAI modules are properly decoupled
- Check API endpoints follow RESTful conventions
- Ensure database access uses parameterized SQL (psycopg2)
- Verify GenAI is used only for post-classification explanation
- Validate deterministic ML classification logic

### C. Content Accuracy and Quality

- Verify technical correctness and ML/GenAI integration
- Ensure completeness for complaint classification objectives
- Check alignment with Explainable AI best practices
- Validate code examples are current, relevant, and runnable
- Verify Python type hints and docstrings are correct
- Ensure NLP preprocessing and ML model training are properly documented

### D. Project Metadata Requirements

Check for presence of:

- Component type designation (backend, ML pipeline, GenAI service, database)
- Version information
- Technology stack (Flask, Scikit-learn, Google Gemini, PostgreSQL)
- N-Tier layer identification
- Last updated timestamp

---

## Repository Health Assessment

### Code Quality

- **Python Backend**: PEP 8 compliance, type hints, comprehensive docstrings
- **ML Pipeline**: Proper training/inference separation, model serialization
- **GenAI Integration**: Secure API key handling, structured prompts, error handling
- **Database**: Parameterized SQL usage, foreign key relationships, indexes
- **Testing**: pytest coverage, unit tests for ML and GenAI components

### Documentation Quality

- **Completeness**: All required documentation present
- **Accuracy**: Technical details match implementation
- **Clarity**: Clear explanations of ML classification and GenAI explanation
- **Single Source of Truth**: Explicit markers on authoritative documents

### ML/GenAI Best Practices

- Offline training, online inference pattern
- Deterministic ML classification (no LLM-based classification)
- GenAI used only for explanation generation
- Proper prompt engineering for explanation quality
- Confidence score reporting
- Model performance metrics documented

---

## File-by-File Verification Protocol

For each file in the repository:

1. **Read file contents completely**
2. **Check for cross-project artifacts** (references to other projects like genai-email-report-drafting)
3. **Verify technical accuracy** (correct ML/GenAI concepts, proper API usage)
4. **Assess completeness** (all required sections present)
5. **Check code quality** (style, documentation, type hints)
6. **Validate examples** (code samples are correct and runnable)
7. **Document findings** (errors, warnings, suggestions)

---

## Critical Checks

### Zero-Copy Policy Violations

- Check for references to other projects (e.g., "genai-email-report-drafting", "email generation", "report drafting")
- Verify all content is specific to consumer complaint classification
- Ensure prompts and examples are domain-specific

### ML/GenAI Integration Quality

- Verify ML model training scripts are present and documented
- Check classification logic is deterministic
- Ensure GenAI explanation prompts are well-structured
- Validate API key security (environment variables only)
- Check error handling for both ML and GenAI components

### Documentation Completeness

Required documents:
- Abstract (comprehensive problem statement)
- Requirements specification
- Setup guide (with troubleshooting)
- Usage guide (with examples)
- Technical documentation (ML pipeline, GenAI integration)
- Architecture plan (N-Tier design)
- Database schema (with ERD)
- API endpoints reference
- Authentication/authorization design
- Prompt engineering strategy
- Repository structure

---

## Consumer Complaints System Content Standards

### Technical Accuracy

- ML concepts (classification, TF-IDF, vectorization) correctly described
- GenAI integration (Gemini API, prompt engineering) accurately documented
- NLP preprocessing steps clearly explained
- Model training and inference separation properly maintained
- Confidence scoring and explainability implemented correctly

### Architecture Standards

- N-Tier separation clearly defined and maintained
- ML layer isolated from business logic
- GenAI layer used only for explanation (not classification)
- Database layer properly abstracted with parameterized SQL
- API layer follows RESTful principles

### Code Quality

- Python: PEP 8, type hints, docstrings
- Modular design: preprocessing, ML, GenAI, database modules
- Error handling: comprehensive exception handling
- Testing: pytest with good coverage
- Security: environment-based configuration, input validation

---

## Output Format

Provide a structured JSON report:

```json
{
  "repository": {
    "name": "consumer-complaints-ml-genai-ntier",
    "type": "N-Tier ML + GenAI Application",
    "status": "complete|incomplete|needs_work"
  },
  "summary": {
    "files_checked": 0,
    "errors": 0,
    "warnings": 0,
    "suggestions": 0
  },
  "critical_issues": [
    {
      "file": "path/to/file",
      "type": "zero_copy_violation|technical_error|missing_content",
      "severity": "critical|high|medium|low",
      "description": "Detailed description",
      "fix": "Recommended fix"
    }
  ],
  "findings": {
    "by_category": {
      "zero_copy_violations": [],
      "ml_genai_issues": [],
      "documentation_gaps": [],
      "code_quality": [],
      "architecture_violations": []
    },
    "by_file": {}
  },
  "recommendations": [
    {
      "priority": "P0|P1|P2|P3",
      "category": "category",
      "action": "description",
      "effort": "hours estimate"
    }
  ]
}
```

---

## Execution Instructions

1. List all files in the repository
2. Read each file systematically
3. Run Consumer Complaints ML + GenAI System-specific checks
4. Document all findings with file paths and line numbers
5. Categorize issues by severity and type
6. Provide prioritized recommendations
7. Generate complete JSON report

**Focus Areas:**
- Zero-copy policy compliance (no genai-email-report-drafting references)
- ML pipeline correctness (training, inference, evaluation)
- GenAI integration quality (prompts, error handling, explanation generation)
- N-Tier architecture adherence
- Documentation completeness and accuracy
- Code quality and testing

---

## Success Criteria

- All files inspected and verified
- All cross-project artifacts identified and documented
- ML and GenAI integration assessed for correctness
- Documentation gaps identified with specific recommendations
- Code quality issues documented with fixes
- Complete JSON report following Consumer Complaints ML + GenAI System output requirements
- Actionable recommendations prioritized by impact

Open every file in the repository tree, run Consumer Complaints ML + GenAI System-specific checks, and produce the structured JSON report following these requirements. Focus on N-Tier architecture compliance, ML classification quality, GenAI explanation quality, and alignment with Explainable AI best practices.
