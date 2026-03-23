# GitHub Copilot Instructions for Consumer Complaints ML + GenAI System

**Version**: 1.0  
**Last Updated**: January 16, 2026  
**Repository**: `consumer-complaints-ml-genai-ntier`

**Environment**: Windows 11, PowerShell  
**Note**: All commands and scripts should use PowerShell syntax. File paths use Windows format.

---

## 🎯 Repository Purpose

**AI-Based Consumer Complaints Classification System** is an N-Tier enterprise application that automatically classifies consumer complaints using Machine Learning and Natural Language Processing, enhanced with Generative AI for explainable results.

### What This Repository Provides

- **Intelligent Text Classification**: Uses Machine Learning (Scikit-learn) to categorize consumer complaints
- **NLP Processing**: Text preprocessing, TF-IDF vectorization, and feature extraction
- **GenAI Explanations**: Generates human-readable explanations for ML predictions
- **N-Tier Architecture**: Clean separation of presentation, application, ML/AI, data access, and database layers
- **Academic Excellence**: Designed for BE-level projects with clear architectural justification
- **Enterprise-Ready**: Scalable, maintainable, and follows best practices

### Target Audience

- Students building AI/ML projects for academic evaluation
- Developers implementing enterprise text analytics systems
- Organizations handling large volumes of customer complaints
- Engineers learning N-Tier architecture with AI integration

### Business Value

- Automates complaint categorization, reducing manual effort
- Provides confidence scores and explanations for transparency
- Enables faster response times to customer issues
- Maintains historical data for trend analysis
- Demonstrates explainable AI principles

---

## 📁 Repository Structure

> **📖 Single Source of Truth**: For complete and up-to-date repository structure, see [docs/08_repository_structure.md](../docs/08_repository_structure.md)

**Quick Reference:**

```
consumer-complaints-ml-genai-ntier/
├── src/
│   └── backend/
│       ├── app.py                      # Main Flask application
│       ├── config.py                   # Configuration management
│       ├── requirements.txt            # Python dependencies
│       ├── preprocessing/              # Text preprocessing modules
│       │   └── text_cleaner.py
│       ├── ml/                         # Machine Learning modules
│       │   ├── train_model.py
│       │   └── predictor.py
│       ├── genai/                      # GenAI explanation modules
│       │   └── explanation.py
│       ├── database/                   # Database access layer
│       │   └── db.py
│       ├── models/                     # Trained ML models
│       │   └── complaint_classifier.pkl
│       └── dataset/                    # Training and test data
│           ├── raw/
│           └── processed/
├── infra/                      # Infrastructure configuration
│   ├── docker-compose.yml
│   └── database/
│       ├── schema.sql
│       └── README.md
└── docs/                       # Project documentation
```

---

## 🔧 Development Guidelines

### Zero-Copy Policy

- All code must be original and properly customized for this project
- No copy-paste artifacts from other projects
- Ensure all references and naming match this project
- Content must be transformative, not reformative
- Even quotes and key principles must use original phrasing

### Project Focus

This is an **N-Tier enterprise application** that:

- Automatically classifies consumer complaints using Machine Learning
- Preprocesses text using NLP techniques (tokenization, stop-word removal, TF-IDF)
- Predicts complaint categories with confidence scores
- Generates human-readable explanations using Generative AI
- Uses Python Flask for backend API
- Uses PostgreSQL/MySQL for data persistence
- Implements role-based access control (User/Admin)

### Current State

- ✅ N-Tier architecture fully planned
- ✅ ML classification pipeline designed
- ✅ GenAI explanation module designed
- ✅ Database schema defined
- ✅ REST API endpoints specified
- ✅ Architecture documentation complete
- ✅ Requirements specification complete
- 🚧 Implementation in progress (Academic project)

### Repository Accuracy

- Do not invent files, folders, scripts, commands, endpoints, or config paths
- Before referencing a path or command, verify it exists in the repository
- If something is planned but not implemented, say so explicitly
- Only reference real, existing entrypoints and paths
- Update documentation only when there is actual implementation to document

### Code Quality Standards

- **Python (Backend)**: Follow PEP 8 style guide, use type hints, include comprehensive docstrings
- **ML Code**: Clear separation of training and inference, modular pipeline design
- Maintain N-Tier architecture separation
- Clear separation of concerns (Presentation, Application, ML/AI, Data Access, Database layers)

### AI Integration Standards

- Secure API key handling (environment variables only) for GenAI services
- Proper error handling for AI/ML operations
- Structured prompt engineering for consistent explanations
- Input validation before ML inference
- GenAI used only for explanation, not classification

### When Adding Features

1. Maintain N-Tier architecture separation (Presentation, Application, ML/AI, Data Access, Database)
2. Keep ML classification deterministic and explainable
3. Add comprehensive logging for complaint processing
4. Write unit tests for preprocessing, ML, and GenAI modules
5. Update documentation in docs/ directory

### Determinism & Auditability

- **Preserve Determinism**: Same inputs must yield same outputs in ML predictions
- **Avoid Randomness**: No non-deterministic sources (random seeds, unordered iteration, unstable sorting)
- **Use Explicit Seeds**: If randomness is required, use documented seeds with stable ordering
- **Traceable Decisions**: Every classification decision should be traceable to inputs + model + thresholds
- **Audit Logging**: Log all predictions with input features, outputs, and confidence scores
- **Reproducible Results**: Ensure ML training and inference are fully reproducible

### File Naming

- **Python**: Use lowercase with underscores: `text_cleaner.py`, `predictor.py`, `explanation.py`
- **ML Models**: Descriptive names: `complaint_classifier.pkl`, `tfidf_vectorizer.pkl`
- **Database Scripts**: `schema.sql`, `migrations.sql`
- **API Routes**: Use descriptive names: `complaints.py`, `classification.py`
- Keep names descriptive and clear
- Follow existing patterns

### Error Handling

- Use proper exception handling
- Log errors with context
- Provide user-friendly error messages
- Handle ML inference failures gracefully
- Validate all user inputs before processing

### Data Safety

- **No Real Data**: Never add real customer data, PII, credentials, or secrets to the repository
- **Sanitized Samples**: Use minimal, anonymized sample data only
- **Environment Variables**: Add `.env.example` for configuration templates, never commit `.env`
- **Test Data**: Use synthetic or publicly available datasets for testing
- **Anonymization**: Strip any identifiable information from sample complaints
- **Security Files**: Keep `.gitignore` updated to prevent accidental commits of sensitive files

### Change Hygiene

- **Small PRs**: Prefer small, focused pull requests over large, multi-purpose changes
- **Avoid Unrelated Refactors**: Keep refactoring separate from feature additions
- **Update Documentation**: Always update `docs/` when behavior, CLI, or API changes
- **Test Coverage**: Add or adjust tests when adding new features or modifying logic
- **Commit Messages**: Write clear, descriptive commit messages explaining the "why"
- **Version Control**: Review changes before committing to avoid accidental inclusions

### Documentation Accuracy

- Documentation must accurately reflect planned implementation
- Architecture diagrams must match actual system design
- API endpoints must be documented correctly
- No misleading technology descriptions
- ML pipeline must be clearly explained

### Code Maintenance

- Maintain N-Tier architecture separation
- Keep ML training and inference separated
- Ensure offline training, online inference pattern
- Follow RESTful API design principles
- Keep GenAI explanation separate from ML prediction

### Quality Assurance

#### Backend (Python)

- Follows PEP 8 style guide
- Type hints where appropriate
- Comprehensive docstrings
- Proper error handling
- Unit tests written
- No linting errors

#### ML/NLP Modules

- Clear preprocessing pipeline
- Reproducible training process
- Model serialization and versioning
- Performance metrics documented
- Test data validation

#### Testing Requirements

- All modules must have unit tests
- Test coverage should be comprehensive
- Integration tests for end-to-end complaint processing
- Run tests before committing: `pytest tests/`

#### Documentation Quality

- README.md must match actual implementation
- Usage guides must be accurate
- Code comments explain complex ML logic
- Configuration options documented

### Documentation Standards

- Keep README.md accurate and up-to-date
- Document all configuration options
- Maintain usage guides in docs/ directory
- Update technical documentation when code changes
- Include API endpoint documentation
- Document ML model architecture and training process
- Document prompt engineering strategies for GenAI explanations

---

## 🚀 Running the System

> **📖 Complete Setup Instructions**: See [Setup Guide](../docs/03_setup.md) for detailed installation and configuration steps.

### Quick Start Commands

**Backend (using uv - recommended):**

```powershell
cd consumer-complaints-ml-genai-ntier
uv venv && uv pip install -r requirements.txt --link-mode=copy
.venv\Scripts\Activate.ps1
python app.py
```

**Alternative (using pip):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**Database Setup:**

- Using Docker Compose: `docker compose -f infra/docker-compose.yml up -d`
- Or see `infra/database/README.md` for local PostgreSQL setup
- Initialize schema: `psql -U postgres -d consumer_complaints -f infra/database/schema.sql`

**Training ML Model (first time):**

```powershell
python ml/train_model.py
```

**Environment Variables:**

- `DATABASE_URL`: PostgreSQL connection string
- `GEMINI_API_KEY`: API key for Google Gemini explanation service
- See `docs/03_setup.md` for detailed configuration

---

## 📋 Configuration

### Backend Configuration (`config.py`)

- `DATABASE_URL`: PostgreSQL connection string
- `ML_MODEL_PATH`: Path to trained ML model
- `VECTORIZER_PATH`: Path to TF-IDF vectorizer
- `GEMINI_API_KEY`: API key for Google Gemini service (optional)
- `COMPLAINT_CATEGORIES`: List of predefined complaint categories

---

## 🔐 Security Considerations

- **API Keys**: Never commit API keys to repository, use environment variables
- **Input Validation**: Validate all complaint text before processing
- **SQL Injection**: Use parameterized queries (psycopg2)
- **Role-Based Access**: Implement User/Admin access control
- **Data Privacy**: Handle complaint text securely, consider anonymization

See also the **Data Safety** section under Development Guidelines for additional security practices.

---

## 🧠 ML & GenAI Architecture

### Machine Learning Pipeline

1. **Text Preprocessing**: Cleaning, tokenization, stop-word removal
2. **Feature Extraction**: TF-IDF vectorization
3. **Classification**: Scikit-learn classifier (Logistic Regression / SVM)
4. **Confidence Scoring**: Prediction probability output

### GenAI Explanation Module

- **Purpose**: Generate human-readable explanations post-classification
- **Input**: Complaint text + predicted category
- **Output**: Natural language explanation
- **Design Principle**: GenAI does NOT influence ML predictions

The system uses structured prompts for GenAI:

- Role definition (AI explanation assistant)
- Explicit task description (explain ML classification decision)
- Context: complaint text and predicted category
- Output constraints: clear, concise, factual

---

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Documentation**: See `docs/` directory for detailed guides
- **Usage Guide**: See `docs/04_usage.md` for usage instructions
