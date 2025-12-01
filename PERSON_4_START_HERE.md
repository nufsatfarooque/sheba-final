# 🎯 PERSON 4: YOUR ACTION PLAN - EXECUTIVE SUMMARY

## WHO YOU ARE
**Widget + Demo Engineer** - You make SHEBA look amazing for judges

## WHAT YOU BUILD (Simplified for 27-30 Hour Hackathon)

### 🎨 **1. Widget** (DONE - Frontend Created ✅)
- **File**: `frontend/public/sheba-widget.js` ← Already created!
- **What it does**: Embeds on any customer portal, shows:
  - Customer name + loyalty score
  - Engagement level
  - Personalized offer
  - Pro tips
- **Status**: Ready to use!

### 🏢 **2. Demo Site** (BUILD NOW - ~2 hours)
- **File**: `frontend/src/pages/DemoSite.jsx`
- **What it does**: Fake "Acme Telecom" customer portal with widget embedded
- **Why**: Shows how customers interact with your product
- **Route**: `http://localhost:5173/demo`

### 💌 **3. Message Gallery** (BUILD AFTER - ~2 hours)
- **File**: `frontend/src/pages/SaveActionGallery.jsx`
- **What it does**: Shows all personalized emails + SMS generated
- **Why**: Judges see the actual retention messages
- **Route**: `http://localhost:5173/save-actions`

### 📖 **4. Demo Narrative** (BUILD LAST - ~1 hour)
- **File**: `frontend/src/pages/DemoNarrative.jsx`
- **What it does**: 6-step walkthrough for judges
- **Why**: Tells the story coherently
- **Route**: `http://localhost:5173/demo-narrative`

---

## 🚀 YOUR NEXT STEPS (Right Now)

### **Step 1: Update App.jsx** (5 min)
Add these routes to `frontend/src/App.jsx`:

```jsx
import DemoSite from './pages/DemoSite';
import SaveActionGallery from './pages/SaveActionGallery';
import DemoNarrative from './pages/DemoNarrative';

// Inside <Routes>:
<Route path="/demo" element={<DemoSite />} />
<Route path="/save-actions" element={<SaveActionGallery />} />
<Route path="/demo-narrative" element={<DemoNarrative />} />
```

### **Step 2: Create DemoSite.jsx** (1.5 hours)
Copy the code from `PERSON_4_ACTIONS.md` → File labeled "Step 2A"
- Create file: `frontend/src/pages/DemoSite.jsx`
- This renders a fake portal with widget embedded
- Test at: http://localhost:5173/demo

**Key Detail**: The widget loads from `http://localhost:5173/sheba-widget.js`

### **Step 3: Test Widget** (30 min)
1. Open http://localhost:5173/demo in browser
2. You should see:
   - Purple gradient box
   - "Hi, [Customer Name]"
   - Loyalty score
   - Tips + offer button
3. If it breaks, check browser console (F12 → Console tab)

### **Step 4: Create SaveActionGallery.jsx** (1.5 hours)
Copy from `PERSON_4_ACTIONS.md` → File labeled "Step 3A"
- Shows grid of personalized messages
- Fetches from backend: `GET /api/v1/save-actions`
- If backend isn't ready, use mock data!

### **Step 5: Create DemoNarrative.jsx** (1 hour)
Copy from `PERSON_4_ACTIONS.md` → File labeled "Step 4A"
- 6-step walkthrough
- Progress bar
- "Next" buttons navigate between pages

### **Step 6: Polish & Test** (1-2 hours)
- Test all routes work
- Check mobile responsiveness
- Create presentation script
- Take screenshots as backup

---

## 📊 Timeline Breakdown

```
Now: 0 hours
├─ Update App.jsx routes (5 min)
│
Hour 1: DemoSite.jsx development
├─ Create file
├─ Add portal HTML structure
├─ Load widget script
├─ Test at /demo route
│
Hour 2: Widget testing + bug fixes
├─ Debug widget loading
├─ Fix styling issues
├─ Verify data displays correctly
│
Hour 3: SaveActionGallery.jsx
├─ Create file
├─ Add mock/real data
├─ Grid layout + click-to-preview
├─ Test at /save-actions route
│
Hour 4: DemoNarrative.jsx
├─ Create file
├─ 6-step walkthrough
├─ Progress bar + buttons
├─ Test navigation
│
Hours 5-6: Polish & Testing
├─ End-to-end testing
├─ Mobile responsiveness
├─ Fix any bugs
├─ Style tweaks
│
Hours 7-8: Presentation Prep
├─ Write presentation script
├─ Screenshot backups
├─ Rehearse demo flow
└─ Final polish
```

---

## 🎬 Demo Flow for Judges (This is your story)

When you demo to judges, walk them through this:

```
1. Start at: http://localhost:5173/demo-narrative
   "Here's our journey..."
   
2. Shows "Step 1: Upload CSV"
   Judge clicks → Goes to /upload
   You say: "Backend automatically analyzes churn risk"

3. Shows "Step 2: Overview"
   Judge sees: 1000 customers, 150 high-risk
   You say: "150 customers about to leave. We do something."

4. Shows "Step 3: ROI"
   Judge sees: $500K revenue at risk, $150K saveable
   You say: "This is why retaining these customers matters"

5. Shows "Step 4: Save Actions"
   Judge clicks → Goes to /save-actions
   You say: "Our system auto-generates personalized messages"
   Click a message: Shows email + SMS preview
   You say: "Takes < 1 second, each saves org thousands"

6. Shows "Step 5: Widget"
   Judge clicks → Goes to /demo
   You say: "The customer sees this on their portal"
   Point out: Loyalty score, offer, tips
   You say: "No more generic emails. Personalized retention."

7. Shows "Step 6: Impact"
   Back at narrative page
   You say: "150 customers engaged, $150K saved, 5 hours of work automated"
```

**Total time: 8-10 minutes** (Perfect for hackathon!)

---

## 🔧 If Backend Isn't Ready

**USE MOCK DATA**. Don't wait!

Example mock for widget:
```javascript
const mockData = {
  customer_name: "Acme Corp",
  customer_id: "cust_acme_001",
  loyalty_score: 8.5,
  engagement_level: "High",
  churn_score: 0.15,
  risk_message: "We love your business! Your engagement has been excellent.",
  recommended_offer: "Get 20% off your next 3 months as a thank you",
  tips: [
    "Your usage is up 25% this month - great!",
    "Refer a friend and get $500 credit",
    "Check out our new premium features"
  ]
};
```

Example mock for messages:
```javascript
const mockActions = [
  {
    customer_id: "cust_456",
    customer_name: "TechCorp Inc",
    churn_score: 0.92,
    revenue_at_risk: 75000,
    projected_saved: 22500,
    email: {
      subject: "TechCorp, we have something special for you",
      body: "Hi TechCorp Team,\n\nWe've noticed you haven't logged in for 45 days..."
    },
    sms: {
      message: "TechCorp - we miss you! Enjoy 30% off to come back. Use code: COMEBACK30"
    }
  }
];
```

**Then swap real data in once backend is ready!**

---

## ✅ Your Success Checklist

**BEFORE Demo:**
- [ ] Widget loads without errors on /demo page
- [ ] Gallery shows message previews on /save-actions
- [ ] Narrative page has all 6 steps on /demo-narrative
- [ ] All routes accessible from main menu
- [ ] Looks good on mobile (open DevTools, check responsive view)
- [ ] No console errors (F12 → Console tab)
- [ ] Presentation script written + timed (< 10 min)
- [ ] Screenshots saved as backup

**DURING Demo:**
- [ ] Walk judges through narrative flow
- [ ] Show actual widget on fake portal
- [ ] Highlight the personalization
- [ ] Show the ROI numbers
- [ ] Explain: "Each customer gets unique message"
- [ ] Wrap up: "This is how churn becomes retention"

---

## 💡 Key Points to Remember

✅ **You're the storyteller**
- Other teams build data + backend + main dashboard
- You make it *look* amazing and tell the story

✅ **Widget is the star**
- It shows the B2B2C value
- It proves customers benefit too
- Make it pretty and fast

✅ **Mock data is OK**
- Judges care about concept + UX, not backend data
- If real data works → bonus points
- Have fallback mocks just in case

✅ **Keep it simple**
- 1 color palette (purple + white)
- Clean layouts
- 3-second load times max
- Mobile-friendly

✅ **Tell a story**
- Not "here's our tech" → "here's how retention works"
- Not "look at the data" → "look at the revenue saved"
- Not "see the widget" → "see how customers experience us"

---

## 📞 If You Get Stuck

**Widget not loading?**
- Check browser console (F12)
- Verify `sheba-widget.js` exists in `frontend/public/`
- Check API key in init config

**Gallery showing no data?**
- Use mock data (don't wait for backend)
- Verify fetch URL is correct
- Check network tab (F12 → Network)

**Routes not working?**
- Verify all files are created in `frontend/src/pages/`
- Check imports in `App.jsx`
- Verify React Router is set up

**Styling looks broken?**
- Check Tailwind is working (if using it)
- Clear browser cache (Ctrl+Shift+R)
- Use inline styles as fallback

---

## 🎯 Final Reminder

You have **27-30 hours** and need **~8 hours** of focused work.

That gives you:
- **8 hours** for building (PERSON_4 work)
- **~4 hours** buffer for bugs/polish/sleep
- **~15-18 hours** while other teams work (you can help or relax)

**Your critical path:**
1. ✅ Widget file created (backend gives you endpoint)
2. ✅ DemoSite.jsx - show widget on fake portal
3. ✅ SaveActionGallery.jsx - show messages
4. ✅ DemoNarrative.jsx - tell the story
5. ✅ Polish + presentation

**You can do this!** 🚀

Questions? Ask the team. Good luck! 🎨✨
