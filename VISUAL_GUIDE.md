# 🎨 PERSON 4: VISUAL QUICK START

## Your Mission (TL;DR)

You are building the **customer-facing showcase** for SHEBA.

```
WHAT YOU BUILD:

┌─────────────────────────────────────────────────────────┐
│ Demo Site: Fake Customer Portal                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Acme Telecom Portal                              │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │   │
│  │ ┃  👋 Hi, Customer!                             ┃ │   │
│  │ ┃  Loyalty: ⭐⭐⭐⭐⭐ | Status: 🟢 Good       ┃ │   │
│  │ ┃  🎁 Special Offer: 20% off next 3 months     ┃ │   │
│  │ ┃  💡 Pro Tip: Your engagement is excellent!   ┃ │   │
│  │ ┃  [Claim Now]                                  ┃ │   │
│  │ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │   │
│  │  ↑ This is YOUR WIDGET embedded here ↑          │   │
│  │                                                  │   │
│  │ Dashboard Cards:                                │   │
│  │ [Usage] [Bill] [Status]                         │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

PLUS:

┌─────────────────────────────────────────────────────────┐
│ Message Gallery: Show All Generated Emails/SMS           │
│                                                         │
│ [TechCorp - Risk 92%] [RetailGo - Risk 85%]           │
│ [FinanceFlow - Risk 78%]                               │
│                                                         │
│ Click TechCorp:                                         │
│ Email: "We'd love to serve TechCorp better..."         │
│ SMS: "TechCorp, we have a special offer..."            │
│ Revenue at Risk: $75K → Projected Save: $22.5K        │
└─────────────────────────────────────────────────────────┘

PLUS:

┌─────────────────────────────────────────────────────────┐
│ Demo Narrative: 6-Step Walkthrough for Judges           │
│                                                         │
│ [====●════════] Step 2 of 6                             │
│                                                         │
│ 🎯 Churn Analysis                                       │
│ "150 high-risk customers identified in seconds"        │
│                                                         │
│ [← Previous] [View Dashboard →] [Next →]              │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Your 4 Tasks (Exact Code Locations)

### TASK 1: Update App.jsx (5 min)
```
File: frontend/src/App.jsx
Add: 3 imports + 3 routes
See: PERSON_4_COPY_PASTE.md → TASK 1
Test: Routes appear in sidebar? ✓
```

### TASK 2: Create DemoSite.jsx (1.5 hours)
```
File: frontend/src/pages/DemoSite.jsx (NEW)
Code: PERSON_4_COPY_PASTE.md → TASK 2
Test: http://localhost:5173/demo
      Purple widget box appears? ✓
```

### TASK 3: Create SaveActionGallery.jsx (1.5 hours)
```
File: frontend/src/pages/SaveActionGallery.jsx (NEW)
Code: PERSON_4_COPY_PASTE.md → TASK 3
Test: http://localhost:5173/save-actions
      3 message cards appear? ✓
      Click shows email/SMS? ✓
```

### TASK 4: Create DemoNarrative.jsx (1 hour)
```
File: frontend/src/pages/DemoNarrative.jsx (NEW)
Code: PERSON_4_COPY_PASTE.md → TASK 4
Test: http://localhost:5173/demo-narrative
      Progress bar works? ✓
      Next button advances? ✓
```

---

## 🎯 What Judges Will See

```
DAY 0: Upload CSV
│
├─→ Backend analyzes churn
│
DAY 1: Identify At-Risk Customers
│     "150 out of 1000 are high-risk"
│
├─→ Calculate Retention ROI
│
DAY 2: Generate Retention Actions
│     "System creates personalized messages"
│     "Takes <1 second per customer"
│
├─→ Show Customer Experience
│
DAY 3: Widget on Customer Portal
│     "Customer sees this engagement tip"
│     "Feels personalized, not generic"
│
RESULT: $150K Revenue Saved
        150 Customers Retained
        5 Hours of Manual Work Automated
```

---

## 🔄 Data Flow (How It Works)

```
BACKEND                    YOUR JOB                 JUDGES SEE
═════════════════════════════════════════════════════════════

1. Upload CSV
   ↓
2. Analyze Churn         DemoSite.jsx
   ↓                     ├─ Shows fake portal
3. Score Customers       ├─ Embeds widget
   ↓                     └─ Displays data
4. Generate Messages     SaveActionGallery.jsx
   ↓                     ├─ Grid of messages
5. Create Widget View    ├─ Click to preview
   ↓                     └─ Shows email/SMS
6. ROI Dashboard
   ↓                     DemoNarrative.jsx
7. Postmortem Insights   ├─ 6-step walkthrough
   ↓                     ├─ Progress bar
   DATA READY            └─ Story told
```

---

## 📱 Routes You're Creating

```
http://localhost:5173/

├─ /demo-narrative           ← Start here (YOUR PAGE)
│  └─ 6-step walkthrough
│     ├─ [View Upload] → /upload (Person 3)
│     ├─ [View Dashboard] → /dashboard (Person 3)
│     ├─ [View ROI] → /dashboard/roi (Person 3)
│     ├─ [View Messages] → /save-actions (YOUR PAGE)
│     ├─ [View Widget] → /demo (YOUR PAGE)
│     └─ [Done]
│
├─ /demo                     ← Demo site (YOUR PAGE)
│  └─ Fake Acme portal
│     └─ Widget embedded
│
└─ /save-actions             ← Message gallery (YOUR PAGE)
   └─ Grid of personalized messages
```

---

## ⏰ Timeline

```
NOW                           HACKATHON END
└─ Hour 0                    └─ Hour 27-30
   │                            │
   ├─ 0-1: Read docs            │ ← Demo starts!
   │                            │
   ├─ 1-2: Update App.jsx ✓     │
   │                            │
   ├─ 2-4: Build DemoSite ✓     │
   │                            │
   ├─ 4-6: Build Gallery ✓      │
   │                            │
   ├─ 6-7: Build Narrative ✓    │
   │                            │
   ├─ 7-8: Polish & present ✓   │
   │                            │
   └─ 8-27: Help others / relax │

   Buffer: ~20 hours
   Your work: ~8 hours
   Time to spare: ~19 hours ✓
```

---

## 🚨 Critical Success Factors

```
MUST WORK:
┌─────────────────────┐
│ ✓ Widget loads      │  Without this, demo fails
│ ✓ No console errors │  Judges look in dev tools
│ ✓ Story is clear    │  They should get the point
│ ✓ All routes load   │  Smooth flow
│ ✓ Mobile works      │  Professional appearance
└─────────────────────┘

NICE TO HAVE:
┌─────────────────────┐
│ ○ Real backend data │  Mock data is OK
│ ○ Animations        │  Not required
│ ○ Polished styling  │  Works > Pretty
└─────────────────────┘

DON'T WORRY ABOUT:
┌─────────────────────┐
│ ✗ Complex UI        │  Simple works
│ ✗ Edge cases        │  Demo path only
│ ✗ Performance opt   │  <2 sec load OK
└─────────────────────┘
```

---

## 📚 Documentation Hierarchy

```
┌─ START HERE ────────────────────┐
│ PERSON_4_README.md              │ ← Overview
│ └─ PERSON_4_START_HERE.md       │ ← Action plan
│    └─ PERSON_4_COPY_PASTE.md    │ ← CODE HERE
│       ├─ TASK 1: App.jsx        │
│       ├─ TASK 2: DemoSite.jsx   │
│       ├─ TASK 3: Gallery.jsx    │
│       └─ TASK 4: Narrative.jsx  │
│
└─ IF YOU GET STUCK ──────────────┐
│ PERSON_4_QUICK_START.md         │ ← Troubleshooting
│ PERSON_4_ACTIONS.md             │ ← Deep dive
│ CHECKLIST.md                    │ ← Progress tracking
│ FILES_CREATED.md                │ ← This guide
└─────────────────────────────────┘
```

---

## 💡 Pro Tips

```
🎨 Make it pretty:
   - Use consistent colors (purple #667eea)
   - Good spacing + typography
   - Professional appearance
   
⚡ Keep it fast:
   - No heavy animations
   - <2 second load times
   - Responsive images
   
📱 Mobile first:
   - Test on small screens
   - Touch-friendly buttons
   - No horizontal scroll
   
🎯 Tell a story:
   - Each page shows progression
   - Clear call-to-action
   - Revenue numbers prominent
   
🔄 Use mock data:
   - Don't wait for backend
   - Swap real data later
   - Judges won't know difference
```

---

## ✅ Quick Checklist

```
Before you code:
☐ Read PERSON_4_README.md (10 min)
☐ Read PERSON_4_COPY_PASTE.md (20 min)
☐ Understand Task 1-4

While coding:
☐ Create files one by one
☐ Test after each file
☐ Check console for errors

Before demo:
☐ All routes work
☐ Widget shows
☐ Messages display
☐ Mobile looks good
☐ No errors in console
☐ Presentation script ready
☐ Screenshots saved

During demo:
☐ Walk through /demo-narrative
☐ Show widget on /demo
☐ Click message on /save-actions
☐ Explain the value
☐ Answer questions
```

---

## 🎬 Your Demo Pitch (30 seconds)

```
"This is SHEBA - automated churn prediction and retention.

Here's how it works:

1. Company uploads customer data
2. We identify 150 at-risk customers in seconds
3. System calculates: $500K revenue at-risk, $150K saveable
4. We auto-generate personalized emails and SMS
5. Customers see this on their portal [show widget]
6. Result: $150K revenue saved, 5 hours of manual work automated

And it's generalizable - works with ANY company's data."

Time: 30 seconds
Impact: Judge understands full story
Next: Questions?
```

---

## 🏁 You're Ready!

Everything is set up:
✅ Widget file created  
✅ Documentation written  
✅ Code templates ready  
✅ Routes planned  
✅ Mock data provided  

**All you need to do:** Copy, paste, test, polish! 🚀

---

**Next step:** Open `PERSON_4_README.md` and start TASK 1! 🎨✨
