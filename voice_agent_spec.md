# Voice Appointment Scheduling Agent - MVP Spec

_Focused on "Returning Caller Magic"_

## 1. Product Overview

A phone-based AI agent that provides a **superior patient intake experience** by remembering every previous interaction. The agent collects appointment scheduling information with perfect recall for returning patients, creating a personalized experience that builds trust and reduces friction.

## 2. Core Hypothesis

**"Perfect conversational memory creates a fundamentally better patient experience than starting fresh every call"**

Traditional receptionists forget previous calls. Current AI systems have no memory. Our agent remembers everything, making returning patients feel valued and known.

## 3. Success Criteria (MVP)

- **First-time callers:** Complete data collection in ≤ 5 minutes
- **Returning callers:** Complete data collection in ≤ 2 minutes (due to memory pre-fill)
- **Completion rate ≥ 85%** for all required fields
- **Wow factor:** Returning callers express surprise/delight at being remembered

## 4. Required Data Collection

### First-Time Caller Flow:

1. **Patient name and date of birth**
2. **Insurance information** (payer name and member ID)
3. **Referral status** and referring physician (if applicable)
4. **Chief medical complaint** (reason for visit)
5. **Complete address** with real-time validation via external API
6. **Contact information** (phone number and email)
7. **Appointment selection** from available providers and times

### Returning Caller Magic Flow:

1. **Quick identification** (name + DOB)
2. **Memory recall:** "Hi Sarah! I have all your info from last month..."
3. **Smart confirmation:** "Insurance still Aetna PPO? Address still on Elm Street?"
4. **Update only what changed**
5. **Focus on new complaint** and appointment needs

## 5. Simplified Technical Architecture

```
Phone Call → Twilio → Simple Flask App → AI Agent
                         ↓
Patient Database ← Conversation Memory ← Address Validation API
                         ↓
Email Notifications → Team Distribution List
```

### Core Components:

1. **Twilio Voice** - Phone number and call handling
2. **Modern AI Voice Platform** (Retell/Vapi/Bland) - Handles STT/TTS/conversation
3. **Simple Database** - Patient records and call history
4. **Address Validation** - USPS or Google API for real-time validation
5. **Email Service** - SendGrid for appointment confirmations
6. **Flask Webhook** - Processes completed calls and sends notifications

## 6. Conversation Experience Design

### First-Time Caller:

```
AI: "Hi! I'm here to help schedule your appointment. What's your name and date of birth?"
Patient: "Sarah Johnson, March 15th, 1985"
AI: "Thanks Sarah! Since this is your first time calling, I'll need to collect some information..."
[Standard data collection flow]
AI: "Perfect! I have everything I need. I'll remember all this for next time you call."
```

### Returning Caller Magic:

```
AI: "Hi! What's your name and date of birth?"
Patient: "Sarah Johnson, March 15th, 1985"
AI: "Sarah! Great to hear from you again. I have your Aetna PPO insurance, your address on Elm Street, and Dr. Martinez was your referring cardiologist from last time. Is this a follow-up for your chest pain, or something new?"
Patient: [Wow moment - feels remembered and valued]
```

## 7. Address Validation Flow

```
Patient: "123 Main Street"
AI: "I need the complete address. What city and state?"
Patient: "Springfield"
AI: "Which Springfield? I see several states have a Springfield."
Patient: "Ohio"
AI: [Validates via API] "I found 123 Main Street, Springfield, Ohio 45503. Is that correct?"
```

## 8. Mock Data for Demo

### Fake Doctors:

- Dr. Sarah Chen - Family Medicine (Available: Tomorrow 2 PM, Thursday 10 AM)
- Dr. Michael Rodriguez - Internal Medicine (Available: Tomorrow 4 PM, Friday 9 AM)
- Dr. Emily Thompson - Cardiology (Available: Thursday 3 PM, Friday 2 PM)

### Appointment Slots:

- Morning: 9:00 AM, 10:30 AM, 11:45 AM
- Afternoon: 1:30 PM, 2:45 PM, 4:00 PM
- Available days: Tomorrow, Thursday, Friday

## 9. Post-Call Actions

After successful data collection:

1. **Email confirmation** to patient (if email provided)
2. **Team notification** to: jeff@assorthealth.com, connor@assorthealth.com, cole@assorthealth.com, jciminelli@assorthealth.com, riley@assorthealth.com
3. **Store complete record** for future "returning caller magic"

### Email Template:

```
Subject: New Patient Appointment Scheduled - [Patient Name]

Patient: Sarah Johnson (DOB: 03/15/1985)
Appointment: Tomorrow 2:00 PM with Dr. Sarah Chen
Insurance: Aetna PPO (ID: 123456789)
Complaint: Chest pain
Referral: Dr. Martinez (Cardiology)
Contact: 555-1234, sarah@email.com
```

## 10. Demo Success Metrics

### Quantitative:

- Data collection completion rate
- Call duration comparison (first-time vs returning)
- Address validation accuracy
- Email delivery success

### Qualitative:

- User reactions to being "remembered"
- Conversation flow smoothness
- Error recovery effectiveness

## 11. MVP Constraints (Simplified)

**What we're NOT building:**

- Complex slot-filling algorithms
- Advanced NLP intent recognition
- HIPAA compliance infrastructure
- Scalability for hundreds of calls
- Complex appointment scheduling logic
- Call recording/analytics dashboards

**What we ARE building:**

- Simple, working phone number
- Reliable data collection
- Address validation that works
- Email notifications that send
- Database that remembers patients
- Conversation experience that delights

## 12. 3-Day Implementation Plan

**Day 1:** Set up Twilio + AI voice platform + basic data collection
**Day 2:** Add address validation + email notifications + database storage  
**Day 3:** Implement returning caller memory + polish conversation flow

## 13. The Unique Value Proposition

_"The first AI receptionist that actually remembers you"_

This isn't just about collecting data - it's about creating a relationship and experience that makes patients prefer calling over any other method of scheduling appointments.

---

**Focus:** Prove that conversational memory transforms the patient experience from transactional to personal, leading to higher satisfaction and completion rates.
