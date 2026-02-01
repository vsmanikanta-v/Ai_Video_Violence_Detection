# Abstract

> **Single Source of Truth**: This is the canonical abstract for the AI Video Violence Detection System. Use this version and adapt formatting as needed for different contexts (academic papers, README, documentation).

---

Violence detection in surveillance videos is a critical requirement for ensuring safety in public and institutional environments. Manual monitoring of video feeds is inefficient, error-prone, and not scalable. This project presents an **AI Video Violence Detection System** that analyzes short, pre-recorded surveillance videos to automatically identify violent activities using **deep learning techniques**.

The system employs a **CNN + LSTM architecture** for spatial–temporal video understanding and performs **inference-only execution**, making it suitable for **CPU-only environments**. To improve interpretability, a **Generative AI (GenAI) module** is integrated as a post-processing layer to generate **human-readable incident explanations** based on model outputs.

The solution is implemented using an **N-Tier enterprise architecture** comprising a **React.js frontend**, a **Flask-based RESTful backend**, and a **PostgreSQL database**. Secure access is enforced using **JWT-based authentication** with **Role-Based Access Control (RBAC)**. The project demonstrates how classical deep learning and Generative AI can be combined within a secure, scalable, and academically defendable software system.

The system is optimized for **CPU-only environments** by excluding local model training and supporting **offline analysis of short videos (30–60 seconds)**. This design makes the project suitable for academic evaluation while demonstrating real-world AI system integration.
