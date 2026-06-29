# Usage Guide: AI Video Violence Detection System

**Project:** AI Video Violence Detection System  
**Purpose:** How to use the application for video violence detection  
**For Setup Instructions:** See [Setup Guide](03_setup.md)

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Registration](#user-registration)
3. [Uploading and Analyzing Videos](#uploading-and-analyzing-videos)
4. [Viewing Detection Results](#viewing-detection-results)
5. [Understanding Detection Results](#understanding-detection-results)
6. [Admin Features](#admin-features)
7. [API Usage](#api-usage)
8. [Best Practices](#best-practices)

---

## Getting Started

Before using the application, ensure you have completed the setup process described in the [Setup Guide](03_setup.md).

**Quick Access:**

1. Ensure backend is running on `http://localhost:8000`
2. Ensure frontend is running (typically `http://localhost:5173`)
3. Open your browser and navigate to the frontend URL
4. You'll see the **landing page** (hero, features, tech stack). Use **Log in** or **Register** in the header to authenticate; then access Upload, History, and (if admin) Admin. The UI flow matches sibling projects (Gen AI Email, Consumer Complaints): Landing → Login/Register → App.

---

## User Registration

### Creating a New Account

1. From the **landing page**, click **Register** in the header (or use the "Get started" CTA)
2. Enter username, email, and a secure password (role defaults to USER)
3. Click "Create account"
4. You'll be automatically logged in and redirected to the landing page (with app nav: Upload, History, etc.)

**Role Types:**

- **USER:** Can upload videos, analyze, and view own history and detection results
- **ADMIN:** Same user capabilities plus access to **Admin dashboard** (`/api/admin/stats`, `/api/admin/audit-logs` with pagination)

**Password Requirements:**

- Minimum 8 characters (recommended)
- Use a strong, unique password

### Logging In

1. From the landing page, click **Log in** in the header (or use the "Get started" CTA)
2. Enter your **username** and password
3. Click "Sign in"
4. You'll be redirected to the page you came from (or the landing page with app nav)

**Note:** Your session is maintained via JWT tokens stored in browser localStorage.

---

## Uploading and Analyzing Videos

### Step-by-Step Process

1. **Navigate to Upload** — When logged in, use the **Upload** link in the header (or go to `/upload`)
2. **Select Video File**
   - Supported formats: MP4, AVI, MOV, WebM, MKV
   - Maximum file size: 2 MB (configurable)
   - Recommended duration: 30–60 seconds
   - Click "Choose File" and select your video

3. **Upload Video**
   - Click "Upload" button
   - Wait for upload to complete
   - System will automatically start analysis

4. **Processing Status**
   - System extracts frames from video
   - CNN-LSTM model performs violence detection
   - GenAI generates incident explanation
   - Processing typically takes 10-30 seconds depending on video length

5. **View Results**
   - Results are displayed automatically after processing
   - You can view detection score, prediction, and explanation

### Video Requirements

**Supported Formats:**

- MP4 (recommended)
- AVI
- MOV
- WebM
- MKV

**Size Limits:**

- Maximum file size: 2 MB (configurable)
- Recommended duration: 30–60 seconds

**Quality Recommendations:**

- Clear video quality for better detection accuracy
- Adequate lighting
- Minimal motion blur

---

## Viewing Detection Results

### Detection Result Components

Each detection result includes:

1. **Violence Score**
   - Numerical score from 0.0 to 1.0
   - Higher scores indicate higher probability of violence
   - Threshold typically set at 0.5

2. **Prediction**
   - **VIOLENT:** Violence detected in video
   - **NON_VIOLENT:** No violence detected

3. **Confidence Level**
   - **HIGH:** Score ≥ 0.8 or ≤ 0.2 (high confidence detection)
   - **MEDIUM:** Score ≥ 0.6 or ≤ 0.4 (moderate confidence, review recommended)
   - **LOW:** Score between 0.4 and 0.6 (borderline, manual review required)

4. **Key Frame Timestamps**
   - Array of timestamps (in seconds) where violence was detected
   - Helps identify specific moments in video

5. **GenAI Incident Explanation**
   - Human-readable summary of detected incident
   - Explains what was detected and when
   - Provides recommendations for security personnel

6. **Processing Information**
   - Processing time
   - Video metadata (duration, format, size)

### Understanding Confidence Levels

**High Confidence (≥ 0.8 or ≤ 0.2):**

- Strong indicators of violence (or non-violence) detected
- Immediate review recommended for violent predictions
- Action may be required

**Medium Confidence (≥ 0.6 or ≤ 0.4):**

- Potential violence detected
- Manual review strongly recommended
- Verify before taking action

**Low Confidence (0.4–0.6):**

- Borderline prediction — model is uncertain
- Review video to verify
- May be ambiguous or borderline activity

---

## Understanding Detection Results

### Example: High Confidence Violent Detection

**Violence Score:** 0.87  
**Prediction:** VIOLENT  
**Confidence Level:** HIGH  
**Key Frames:** Detected at 12s, 18s, 25s, 32s

**GenAI Explanation:**
> "A violent incident was detected with high confidence (87%) in the surveillance video. The system identified aggressive physical interactions at multiple timestamps (12s, 18s, 25s, 32s) throughout the 45-second video clip. Security personnel should review this footage immediately and take appropriate action."

### Example: Medium Confidence Detection

**Violence Score:** 0.62  
**Prediction:** VIOLENT  
**Confidence Level:** MEDIUM  
**Key Frames:** Detected at 28s, 35s

**GenAI Explanation:**
> "Potential violent activity was detected with moderate confidence (62%) in the surveillance video. The system identified suspicious interactions at timestamps 28s and 35s. Due to the moderate confidence level, manual review of these specific segments is strongly recommended before taking action."

### Example: Non-Violent Detection

**Violence Score:** 0.15  
**Prediction:** NON_VIOLENT  
**Confidence Level:** HIGH

**GenAI Explanation:**
> "No violent activity was detected in the surveillance video. The system analyzed the 50-second clip with high confidence (85%) and found no indicators of violence. The video appears to show normal activity."

---

## Admin Features

### Admin Dashboard

Admin users have access to the **Admin** page in the app (backed by `/api/admin/stats` and `/api/admin/audit-logs`):

1. **Activity metrics** — aggregate counts: users, videos, detection results, audit log entries
2. **Recent audit logs** — tabular view of recent actions (paginated via `limit` and `offset` on the API; the UI loads a fixed default page)

There is no separate “all users’ videos” browser or export in the current frontend; use the API or database for deeper analysis if needed.

### Admin Workflow

1. Log in as an admin user
2. Open **Admin** in the navigation
3. Review aggregate metrics and audit log entries

---

## API Usage

### Authentication

**POST /api/auth/register**

```json
{
  "username": "john_doe",
  "email": "user@example.com",
  "password": "SecurePass123",
  "role": "USER"
}
```

**POST /api/auth/login**

```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

### Video Upload

**POST /api/videos/upload**

- Requires: JWT Bearer token
- Content-Type: multipart/form-data
- Body: video file

### Get Detection Results

**GET /api/detections/result/{result_id}**

- Requires: JWT Bearer token
- Returns: Detection result and GenAI explanation for a specific result

**GET /api/detections/video/{video_id}**

- Requires: JWT Bearer token
- Returns: All detection results for a specific video

### Get Video History

**GET /api/videos/history**

- Requires: JWT Bearer token
- Returns: Full list of the current user’s videos with nested detection results (newest first). Pagination query parameters are **not** implemented on this endpoint.

---

## Best Practices

### Video Upload Tips

- **Use clear, well-lit videos** for better detection accuracy
- **Keep videos short** (30-60 seconds) for faster processing
- **Use MP4 format** for best compatibility
- **Ensure adequate resolution** without excessive file size

### Interpreting Results

- **High confidence detections:** Review immediately
- **Medium confidence detections:** Manual review recommended
- **Low confidence detections:** Likely false positives, verify before action

### Security

- **Protect your account:** Use strong passwords
- **Review results carefully:** System provides assistance, not absolute truth
- **Follow organizational policies:** Use detection results as one input for decision-making

---

## Related Documentation

- [Setup Guide](03_setup.md) - Installation and configuration
- [Technical Documentation](05_technical.md) - Technical implementation details
- [Architecture Plan](06_architecture_plan.md) - System architecture
- [Authentication Guide](09_authentication_authorization.md) - Security documentation

---