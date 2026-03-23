# Work Item WI-020: Phase 20 - Complaint Submission UI (Future)

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Implement a user-friendly complaint submission form in the React frontend.

## Scope

### 1. Form Components

- Text area for complaint
- Submit button
- Validation feedback
- Loading indicator

### 2. UX Features

- Character count
- Example complaints
- Clear/reset button
- Success confirmation

### 3. API Integration

- POST to /api/classify
- Handle success response
- Handle error states
- Display results

## Wireframe

```text
┌──────────────────────────────────────┐
│  Submit Your Complaint               │
├──────────────────────────────────────┤
│ ┌──────────────────────────────────┐ │
│ │                                  │ │
│ │  [Complaint text area]           │ │
│ │                                  │ │
│ └──────────────────────────────────┘ │
│        Characters: 150 / 2000        │
│                                      │
│  [ Clear ]        [ Submit ]         │
└──────────────────────────────────────┘
```

## Acceptance Criteria

- Form validates input
- Submission triggers API call
- Results displayed after classification
- Error states handled gracefully

## Dependencies

- Requires WI-019 (React Scaffold)

## Success Criteria

- User can submit complaint
- Classification results displayed
- Professional, responsive design
