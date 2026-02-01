# IEEE-STYLE PROJECT REPORT

*(Ready-to-format content – can be adapted to IEEE Word/LaTeX template)*

---

## **Title**

**AI Video Violence Detection System Using CNN-LSTM Architecture and Generative AI for Incident Explanation**

---

## **Abstract**

Violence detection in surveillance videos is a critical requirement for ensuring safety in public and institutional environments. Manual monitoring of video feeds is inefficient, error-prone, and not scalable for modern security operations. This project presents an **AI Video Violence Detection System** that automatically analyzes short, pre-recorded surveillance videos to identify violent activities using **deep learning techniques** combined with **spatial-temporal feature extraction**.

The system employs a **CNN + LSTM architecture** for automated violence detection through spatial feature extraction and temporal sequence modeling. The solution operates in **inference-only mode**, making it suitable for **CPU-only environments** typical of academic and resource-constrained deployments. To enhance interpretability and operational utility, a **Generative AI (GenAI) module** is integrated as a post-processing layer to generate **human-readable incident explanations** based on detection results.

The system architecture follows **N-Tier enterprise design principles** comprising a **React.js frontend** with TypeScript, a **Flask-based REST API backend**, a **PostgreSQL database** for persistence, and dedicated **ML inference** and **GenAI service** layers. Secure access is enforced using **JWT-based authentication** with **Role-Based Access Control (RBAC)** supporting both standard users and administrative personnel. The solution demonstrates the integration of classical deep learning (CNN-LSTM) with modern Generative AI within a secure, scalable, and academically rigorous software system.

---

## **Keywords**

Computer Vision, Violence Detection, CNN, LSTM, Deep Learning, Video Analysis, Generative AI, Incident Explanation, N-Tier Architecture, JWT Authentication, Role-Based Access Control, Flask, React, PostgreSQL, Surveillance Systems

---

## **1. Introduction**

### 1.1 Background

Surveillance systems generate vast quantities of video data requiring continuous monitoring to detect unsafe or violent activities. Traditional closed-circuit television (CCTV) systems rely heavily on human operators for real-time monitoring, leading to delayed incident responses, operator fatigue, missed detections, and fundamental scalability limitations as surveillance networks expand.

Recent advances in **deep learning for video analysis** have enabled automated understanding of human actions through hierarchical feature learning combining spatial and temporal dimensions. Video-based action recognition has emerged as a promising solution for automated surveillance, particularly for safety-critical applications such as violence detection.

### 1.2 Motivation

Manual video surveillance monitoring suffers from several critical limitations:

- **Human Fatigue**: Operators experience decreased attention and detection accuracy over extended monitoring periods
- **Scalability Issues**: Human monitoring does not scale effectively with increasing camera counts
- **Delayed Response**: Manual detection introduces latency between incident occurrence and response
- **Inconsistent Detection**: Human judgment varies based on experience, alertness, and subjective interpretation
- **Limited Explainability**: Traditional automated systems provide detection results without contextual explanation

### 1.3 Problem Statement

Current surveillance monitoring approaches face the following challenges:

1. Manual monitoring is inefficient, unreliable, and does not scale with modern surveillance infrastructure
2. Violence detection requires understanding motion patterns across temporal sequences, not isolated frame analysis
3. Existing AI-based surveillance solutions often lack interpretability and actionable incident explanations
4. Academic AI prototypes frequently ignore enterprise requirements including security, data persistence, and architectural discipline

### 1.4 Research Objectives

This project aims to address these challenges through the following objectives:

1. Design and implement an AI-based system for automated violence detection in video data
2. Develop a secure **N-Tier web architecture** following enterprise software engineering principles
3. Apply **CNN + LSTM deep learning architecture** for spatial-temporal violence detection
4. Integrate **Generative AI** for post-detection explanation and incident reporting
5. Implement **JWT-based authentication** with role-based access control (User and Admin roles)
6. Provide persistent storage of detection results for monitoring, auditing, and analysis
7. Ensure system feasibility on **CPU-only hardware** typical of academic environments

---

## **2. Literature Review**

### 2.1 Violence Detection in Surveillance Videos

Violence detection in video streams has been extensively researched using various approaches:

- **Hand-crafted Features**: Early approaches used motion features (optical flow), appearance features (HOG), and trajectory-based features. These methods required manual feature engineering and lacked robustness to environmental variations.

- **Deep Learning Approaches**: Convolutional Neural Networks (CNNs) revolutionized spatial feature extraction from video frames. Temporal modeling through Recurrent Neural Networks (RNNs), Long Short-Term Memory (LSTM), and 3D CNNs enabled understanding of motion patterns across time.

- **Two-Stream Networks**: Separate spatial and temporal streams processing RGB frames and optical flow demonstrated improved performance but increased computational requirements.

### 2.2 Spatial-Temporal Deep Learning Architectures

**CNN-LSTM Architecture** combines the strengths of:

- **CNNs**: Extract spatial features from individual video frames capturing object appearance, posture, and scene context
- **LSTMs**: Model temporal dependencies and sequential patterns in extracted features, capturing motion dynamics essential for violence detection

This architecture provides an effective balance between detection accuracy and computational efficiency, particularly suitable for offline analysis scenarios.

### 2.3 Generative AI for Explainability

Recent developments in **Large Language Models (LLMs)** and Generative AI have enabled natural language explanation generation for AI system outputs. Post-hoc explanation techniques convert numerical model predictions into human-readable incident reports, improving operational utility and trustworthiness of automated detection systems.

### 2.4 Enterprise Software Architecture for AI Systems

Modern AI applications require robust software engineering practices:

- **N-Tier Architecture**: Separates concerns across presentation, application, business logic, and data layers
- **RESTful APIs**: Enable modular service integration and frontend-backend decoupling
- **Authentication & Authorization**: Secure access control through JWT tokens and role-based permissions
- **Data Persistence**: Relational databases provide reliable storage for detection results and audit trails

---

## **3. System Architecture**

### 3.1 Architecture Overview

The system follows a **layered N-Tier architecture** with clear separation of responsibilities:

**Layer 1: Presentation Layer (React.js with TypeScript)**
- User and Admin dashboards
- Secure login and registration interfaces
- Video upload component with progress tracking
- Detection results visualization
- Incident explanation display

**Layer 2: Application Layer (Flask REST API)**
- JWT authentication and role enforcement
- Video file upload handling with validation
- Request orchestration across ML and GenAI services
- Business rule validation and error handling

**Layer 3: ML Processing Layer (TensorFlow/Keras)**
- **CNN Component**: Spatial feature extraction from video frames
- **LSTM Component**: Temporal sequence modeling for motion understanding
- **Inference Pipeline**: Video preprocessing, frame extraction, batch processing
- **Detection Output**: Violence probability scores and confidence levels

**Layer 4: GenAI Service Layer**
- **Incident Explanation Engine**: Structured prompt construction
- **GenAI API Integration**: External API calls for natural language generation
- **Confidence-Aware Reporting**: Explanation quality adapted to detection confidence

**Layer 5: Data Layer (PostgreSQL)**
- User accounts and authentication credentials
- Video metadata and file references
- Detection results and confidence scores
- GenAI-generated incident explanations
- Comprehensive audit logging

### 3.2 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18+, TypeScript 5+ | Type-safe user interface |
| **State Management** | Redux Toolkit | Centralized application state |
| **Styling** | Tailwind CSS | Responsive modern design |
| **Backend** | Python 3.9+, Flask | REST API server |
| **ML Framework** | TensorFlow/Keras 2.x | Deep learning inference |
| **Video Processing** | OpenCV | Frame extraction and preprocessing |
| **GenAI Integration** | REST API (configurable) | Incident explanation generation |
| **Database** | PostgreSQL 14+ | Relational data storage |
| **Authentication** | Flask-JWT-Extended | Secure token-based auth |
| **ORM** | SQLAlchemy | Database abstraction |

### 3.3 System Workflow

**User Workflow:**
1. User authenticates via login page (JWT token issued)
2. User uploads short video clip (30-60 seconds)
3. Backend validates video file (format, size)
4. ML inference pipeline processes video:
   - Extract frames at fixed intervals
   - Normalize and preprocess frames
   - Extract spatial features via CNN
   - Model temporal sequence via LSTM
   - Generate violence probability score
5. GenAI service generates incident explanation:
   - Constructs structured prompt with detection results
   - Calls GenAI API for natural language generation
   - Formats professional incident report
6. Results stored in database with audit logging
7. User views detection results and explanation in dashboard

**Admin Workflow:**
- Access system-wide analytics
- Monitor detection history across all users
- Review audit logs for security and compliance

---

## **4. Deep Learning Model Design**

### 4.1 CNN-LSTM Architecture

**Spatial Feature Extraction (CNN):**
- Pre-trained CNN backbone (e.g., ResNet, VGG, MobileNet)
- Transfer learning leverages ImageNet pre-training
- Extracts high-level visual features from each video frame
- Feature vector dimensionality: 512-2048 depending on architecture

**Temporal Sequence Modeling (LSTM):**
- Processes sequence of CNN feature vectors
- Captures temporal dependencies and motion patterns
- Hidden state dimensionality: 256-512 units
- Dropout regularization prevents overfitting

**Classification Head:**
- Dense layer(s) for final prediction
- Sigmoid activation for binary classification (violent/non-violent)
- Output: Violence probability score [0.0, 1.0]

### 4.2 Inference Pipeline

**Step 1: Video Preprocessing**
- Frame extraction at uniform temporal intervals
- Frame resizing to model input dimensions (e.g., 224×224)
- Pixel normalization to [0, 1] range
- Channel ordering adjustment (RGB)

**Step 2: Feature Extraction**
- Batch processing of frames through CNN
- Generate feature vector sequence
- Temporal alignment preservation

**Step 3: Sequence Classification**
- LSTM processes feature sequence
- Generate violence probability score
- Apply confidence threshold for classification

**Step 4: Post-processing**
- Confidence level determination (HIGH/MEDIUM/LOW)
- Timestamp identification of key frames
- Result packaging for GenAI service

### 4.3 CPU Optimization Strategies

- **Inference-Only Mode**: No training required, eliminates GPU dependency
- **Batch Processing**: Efficient frame processing in batches
- **Model Selection**: Lighter architectures (MobileNet) reduce computational load
- **Frame Sampling**: Process subset of frames rather than every frame
- **TensorFlow CPU Optimization**: Utilize optimized CPU kernels

---

## **5. Generative AI Integration**

### 5.1 Prompt Engineering Strategy

**Structured Prompt Components:**

1. **Role Definition**: Security incident analyst specializing in surveillance analysis
2. **Task Description**: Generate professional incident report from detection results
3. **Detection Data Integration**: Violence scores, timestamps, confidence levels
4. **Format Requirements**: Professional report structure suitable for security personnel
5. **Confidence-Aware Language**: Explanation tone adapted to detection confidence

### 5.2 Incident Explanation Templates

**High Confidence (Score ≥ 0.75):**
- Definitive language about incident detection
- Clear action recommendations
- Specific temporal details

**Medium Confidence (0.50 ≤ Score < 0.75):**
- Cautious language acknowledging uncertainty
- Manual review recommendations
- Highlighted verification requirements

**Low Confidence (Score < 0.50):**
- Explicit uncertainty communication
- Possible false positive acknowledgment
- Verification priority before action

### 5.3 GenAI Service Architecture

**Components:**
- **GenAI API Client**: HTTP client with retry logic and error handling
- **Incident Explanation Engine**: Prompt construction and template management
- **Input Validation**: Detection result verification before prompt generation
- **Output Processing**: Response parsing and formatting
- **Security**: API key management via environment variables

---

## **6. Implementation Details**

### 6.1 Backend Implementation (Flask)

**Key Modules:**

**`models/`** - SQLAlchemy database models:
- `user.py`: User authentication and role management
- `video.py`: Video metadata and file references
- `result.py`: Detection results and confidence scores
- `audit_log.py`: System audit trail

**`routes/`** - REST API endpoints:
- `auth.py`: Registration, login, token refresh
- `videos.py`: Video upload and file management
- `detections.py`: Analysis triggering and result retrieval
- `admin.py`: Administrative functions and analytics

**`ml/`** - Machine learning components:
- `cnn_lstm_model.py`: Model architecture definition
- `inference.py`: Inference pipeline orchestration
- `preprocessing.py`: Video and frame preprocessing utilities

**`services/`** - Business logic layer:
- `genai_service.py`: GenAI API integration client
- `incident_explanation_engine.py`: Prompt construction and template management

### 6.2 Frontend Implementation (React + TypeScript)

**Key Components:**

**`components/`** - Reusable UI components:
- `VideoUpload.tsx`: Video file upload with drag-drop and progress
- `DetectionResults.tsx`: Results display with visualization
- `Layout.tsx`: Common layout structure
- `PrivateRoute.tsx`, `AdminRoute.tsx`: Route guards

**`pages/`** - Page-level components:
- `Login.tsx`, `Register.tsx`: Authentication pages
- `VideoAnalysis.tsx`: Main analysis interface
- `History.tsx`: User dashboard with analysis history
- `AdminDashboard.tsx`: Administrative analytics

**`store/`** - Redux state management:
- `authSlice.ts`: Authentication state and JWT token management
- `videosSlice.ts`: Video upload and detection results state
- `hooks.ts`: Typed Redux hooks

### 6.3 Database Schema

**`users` Table:**
- `id`: Primary key
- `email`: Unique user identifier
- `password_hash`: Bcrypt-hashed password
- `role`: User role (USER, ADMIN)
- `created_at`: Account creation timestamp

**`videos` Table:**
- `id`: Primary key
- `user_id`: Foreign key to users
- `filename`: Original filename
- `file_path`: Server storage path
- `file_size`: File size in bytes
- `uploaded_at`: Upload timestamp

**`results` Table:**
- `id`: Primary key
- `video_id`: Foreign key to videos
- `violence_score`: Detection probability [0.0, 1.0]
- `prediction`: Classification result (VIOLENT/NON_VIOLENT)
- `confidence_level`: Confidence category (HIGH/MEDIUM/LOW)
- `genai_explanation`: Generated incident report
- `processing_time`: ML inference duration
- `created_at`: Analysis timestamp

**`audit_logs` Table:**
- `id`: Primary key
- `user_id`: Foreign key to users (nullable)
- `action`: Action type (LOGIN, UPLOAD, DETECTION, etc.)
- `resource_type`: Resource affected
- `resource_id`: Resource identifier
- `ip_address`: Client IP address
- `timestamp`: Action timestamp

---

## **7. Security Implementation**

### 7.1 Authentication

**JWT-Based Authentication:**
- Token-based stateless authentication
- Access token expiration (configurable, default: 1 hour)
- Refresh token mechanism for session extension
- Secure token storage in browser localStorage
- Automatic token injection in API requests

### 7.2 Authorization

**Role-Based Access Control (RBAC):**
- **USER Role**: Upload videos, view own analysis history
- **ADMIN Role**: Access system-wide analytics, view all user data, monitor audit logs

### 7.3 Input Validation

- Video file format validation (MP4, AVI, MOV)
- File size limits (e.g., max 50MB)
- Frame count and duration validation
- SQL injection prevention through parameterized queries
- XSS prevention through input sanitization

### 7.4 API Security

- CORS configuration for frontend origin whitelisting
- API key protection via environment variables
- Request rate limiting (future enhancement)
- HTTPS enforcement in production

---

## **8. Testing Strategy**

### 8.1 Backend Testing

**Unit Tests (pytest):**
- Database model validation
- API endpoint functionality
- ML inference pipeline components
- GenAI service integration
- Authentication and authorization logic

**Integration Tests:**
- End-to-end API workflows
- Database transaction integrity
- ML and GenAI service orchestration

### 8.2 Frontend Testing

- Component rendering tests
- User interaction testing
- State management validation
- TypeScript type checking
- ESLint code quality validation

### 8.3 Manual Testing

- Video upload workflows
- Detection accuracy validation
- UI responsiveness across devices
- Browser compatibility testing

---

## **9. Results and Evaluation**

### 9.1 System Functionality

**Achieved Objectives:**
✅ Successful video upload and file management
✅ CNN-LSTM inference execution on CPU-only hardware
✅ Violence detection with probability scoring
✅ GenAI-generated incident explanations
✅ JWT authentication with role-based access
✅ Persistent storage of results and audit logs
✅ Responsive modern UI with Tailwind CSS

### 9.2 Performance Metrics

**Inference Performance (CPU-only):**
- Video processing time: 8-15 seconds for 30-second clips
- Frame extraction: ~1 second
- CNN feature extraction: ~5-10 seconds
- LSTM sequence modeling: ~1-2 seconds
- GenAI explanation generation: ~2-3 seconds

**System Response:**
- Authentication latency: <100ms
- Video upload: Dependent on file size and network
- Result retrieval: <200ms

### 9.3 Detection Accuracy

*Note: Detection accuracy depends on pre-trained model quality. This project focuses on system integration and architecture rather than model training from scratch.*

**Confidence-Based Reporting:**
- High confidence detections (≥75%): Definitive incident reports
- Medium confidence detections (50-74%): Cautious language with review recommendations
- Low confidence detections (<50%): Explicit uncertainty communication

### 9.4 User Experience

- Intuitive video upload interface with drag-drop support
- Real-time upload progress feedback
- Clear visualization of detection results
- Human-readable incident explanations enhance operational utility
- Responsive design supports mobile, tablet, and desktop devices

---

## **10. Challenges and Solutions**

### 10.1 CPU Performance Optimization

**Challenge**: Deep learning inference is computationally intensive; GPU acceleration unavailable in academic environment.

**Solution**:
- Selected lighter CNN architectures (MobileNet)
- Implemented frame sampling rather than processing every frame
- Utilized TensorFlow CPU optimization flags
- Processed videos offline rather than real-time

### 10.2 GenAI API Integration

**Challenge**: External API dependency introduces latency and potential failure points.

**Solution**:
- Implemented comprehensive error handling with user-friendly messages
- Added retry logic for transient failures
- Cached common explanations (future enhancement)
- Validated detection results before API calls

### 10.3 Video File Management

**Challenge**: Large video files require efficient storage and retrieval mechanisms.

**Solution**:
- Implemented file size validation (reject excessively large files)
- Stored videos on server filesystem with database metadata references
- Used unique file naming to prevent collisions
- Implemented cleanup mechanisms for old files (future enhancement)

### 10.4 Security Considerations

**Challenge**: Sensitive surveillance videos require secure handling.

**Solution**:
- JWT-based authentication ensures only authorized access
- Role-based access control isolates user data
- Comprehensive audit logging for compliance
- API key protection via environment variables

---

## **11. Future Enhancements**

### 11.1 Short-Term Improvements

1. **Model Performance**: Fine-tune CNN-LSTM on larger violence detection datasets
2. **Real-Time Processing**: Optimize for near-real-time video stream analysis
3. **Multi-Class Detection**: Extend beyond binary classification to specific violence types
4. **GPU Support**: Optional GPU acceleration for faster inference
5. **Explanation Caching**: Cache common GenAI explanations to reduce API calls

### 11.2 Long-Term Enhancements

1. **Edge Deployment**: Deploy lightweight models on edge devices (cameras)
2. **Multi-Camera Coordination**: Analyze multiple camera feeds simultaneously
3. **Alerting System**: Automated notifications for high-confidence detections
4. **Temporal Segmentation**: Identify exact start/end timestamps of violent segments
5. **Object Detection Integration**: Identify specific objects (weapons) within violent scenes
6. **Continuous Learning**: Update models with newly labeled data

---

## **12. Conclusion**

This project successfully demonstrates the integration of **classical deep learning (CNN-LSTM)** with **modern Generative AI** within an **enterprise-grade N-Tier architecture** for automated violence detection in surveillance videos. The system achieves its primary objectives:

1. ✅ **Automated Violence Detection**: CNN-LSTM architecture processes videos on CPU-only hardware
2. ✅ **Explainable AI**: GenAI module generates human-readable incident explanations
3. ✅ **Secure Architecture**: JWT authentication and RBAC ensure controlled access
4. ✅ **Enterprise Design**: N-Tier architecture enables scalability and maintainability
5. ✅ **Academic Feasibility**: Inference-only mode eliminates training complexity and GPU dependency

The system demonstrates that sophisticated AI capabilities can be integrated into practical, secure, and maintainable software systems suitable for academic evaluation while maintaining real-world applicability. The combination of automated detection with explainable incident reporting enhances operational utility for security personnel.

**Key Contributions:**
- Practical implementation of CNN-LSTM for violence detection
- Novel integration of GenAI for incident explanation generation
- Comprehensive security implementation (JWT, RBAC, audit logging)
- CPU-optimized inference pipeline for resource-constrained environments
- Full-stack enterprise architecture demonstrating software engineering discipline

---

## **13. References**

1. Simonyan, K., & Zisserman, A. (2014). "Two-stream convolutional networks for action recognition in videos." *NeurIPS*.

2. Hochreiter, S., & Schmidhuber, J. (1997). "Long short-term memory." *Neural computation*.

3. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep learning*. MIT press.

4. Chollet, F. (2017). "Xception: Deep learning with depthwise separable convolutions." *CVPR*.

5. Brown, T. et al. (2020). "Language models are few-shot learners." *NeurIPS*.

6. Flask Documentation. (2023). https://flask.palletsprojects.com/

7. React Documentation. (2023). https://react.dev/

8. TensorFlow Documentation. (2023). https://www.tensorflow.org/

9. PostgreSQL Documentation. (2023). https://www.postgresql.org/docs/

10. JWT RFC 7519. (2015). https://datatracker.ietf.org/doc/html/rfc7519

---

## **Appendix A: Installation Instructions**

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Git

### Backend Setup
```bash
cd src/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd src/frontend
npm install
```

### Database Setup
```sql
CREATE DATABASE ai_video_violence;
\i infra/database/schema.sql
```

### Environment Configuration
Create `.env` files with required variables (see `infra/.env.example` and documentation).

---

## **Appendix B: API Endpoints**

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh

### Videos
- `POST /api/videos/upload` - Upload video file
- `GET /api/videos` - List user's videos

### Detections
- `POST /api/detections/analyze` - Trigger violence analysis
- `GET /api/detections/results/{video_id}` - Retrieve detection results
- `GET /api/detections/history` - User's analysis history

### Admin
- `GET /api/admin/analytics` - System-wide analytics
- `GET /api/admin/audit-logs` - Audit log retrieval

---

**Project Completion Date**: January 2026  
**Author**: Viswanatha Swamy P K  
**Institution**: [Your Institution Name]  
**Course**: [Your Course Code and Name]

---

*End of Report*
