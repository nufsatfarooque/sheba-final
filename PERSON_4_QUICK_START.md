# 👤 PERSON 4: QUICK START GUIDE
## Your 8-Hour Mission (Widget + Demo Engineer)

---

## ⚡ TL;DR: What You're Building

You're the **storyteller** - making SHEBA shine for judges through:
1. **Widget** - Customers see engagement tips on their portal  
2. **Demo Site** - Fake telecom portal showing the widget  
3. **Message Gallery** - All auto-generated personalized emails/SMS  
4. **Presentation Flow** - Step-by-step walkthrough  

---

## 📁 Files You Need to Create

### **File 1: Widget Component** (2 hours)
```
frontend/src/widgets/sheba-widget.js
```
- 200-line standalone JavaScript file
- Embeddable on any customer portal
- Shows: customer name, loyalty score, engagement tips, offers
- Fetches data from backend `/widget/customer_view` endpoint

**Key:** Make it beautiful, fast-loading, mobile-friendly

---

### **File 2: Widget Guide** (30 min)
```
frontend/public/sheba-widget-guide.html
```
- Integration instructions for customers
- Copy-paste code examples
- Configuration options

---

### **File 3: Demo Site Page** (2 hours)
```
frontend/src/pages/DemoSite.jsx
```
- Fake "Acme Telecom" customer portal
- Shows: dashboard cards, activity, billing
- **Embeds the widget** to show how it looks in real portal
- You'll run this at `/demo` route

---

### **File 4: Save Actions Gallery** (1.5 hours)
```
frontend/src/pages/SaveActionGallery.jsx
```
- Grid of all personalized messages generated
- Click on a message to see:
  - Email subject + body
  - SMS preview
  - Revenue at risk vs projected saved
- Visually compelling for judges

---

### **File 5: Demo Narrative Page** (1.5 hours)
```
frontend/src/pages/DemoNarrative.jsx
```
- 6-step walkthrough page for judges
- "Upload → Analyze → Calculate ROI → Generate Messages → Widget → Impact"
- Each step has button to navigate to actual feature
- Progress bar showing journey

---

### **File 6: Presentation Checklist** (30 min)
```
DEMO_PRESENTATION_CHECKLIST.md
```
- Scripts for what to say/show to judges
- Timing guidelines
- Backup plan if something breaks

---

## 🎯 Implementation Order

### **PHASE 1: Widget (Hours 0-3)**
1. Create `sheba-widget.js` - start with HTML mock data
2. Test in browser console
3. Create `sheba-widget-guide.html`

### **PHASE 2: Demo Site (Hours 3-6)**
1. Create `DemoSite.jsx` - portal HTML structure
2. Load widget script from `/public`
3. Initialize widget on component mount
4. Test at `http://localhost:5173/demo`

### **PHASE 3: Gallery & Narrative (Hours 6-9)**
1. Create `SaveActionGallery.jsx` - fetch from backend
2. Create `DemoNarrative.jsx` - step-by-step flow
3. Update `App.jsx` to add routes

### **PHASE 4: Polish & Presentation (Hours 9-11)**
1. Test all pages end-to-end
2. Create presentation checklist
3. Record backup screenshots
4. Rehearse demo flow

---

## 🔌 Backend Endpoints You Depend On

These are provided by **Person 2** (Backend Engineer).  
You'll call them from your components:

```javascript
// Widget loads this
GET /api/v1/widget/customer_view?api_key={key}&customer_id={id}
// Returns: { customer_name, loyalty_score, engagement_level, risk_message, recommended_offer, tips }

// Gallery loads this
GET /api/v1/save-actions?org_id=demo_org
// Returns: { actions: [ { customer_name, churn_score, revenue_at_risk, projected_saved, email, sms } ] }
```

**If backend isn't ready**, use **mock data** - it doesn't matter for demo!

---

## 💡 Pro Tips

### **Tip 1: Mock Data Strategy**
Don't wait for backend! Create mock objects:
```javascript
const mockData = {
  customer_name: "Acme Corp",
  loyalty_score: 8.5,
  engagement_level: "High",
  risk_message: "We love your business!",
  recommended_offer: "20% off premium plan",
  tips: ["Great usage this month", "Refer a friend for bonus"]
};
```

### **Tip 2: Use Vite's Public Folder**
Put `sheba-widget.js` in `frontend/public/` so it's accessible as:
```
http://localhost:5173/sheba-widget.js
```

### **Tip 3: Design Consistency**
Use this color scheme everywhere:
- Primary: `#667eea` (purple)
- Secondary: `#764ba2` (darker purple)
- Accent: `#22c55e` (green for saves)
- Neutral: `#f5f5f5` (light gray)

### **Tip 4: Keep It Simple**
- No complex animations (keeps site fast)
- Max 3 colors + white/gray
- Font: System fonts (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto`)

### **Tip 5: Test on Mobile**
Your demo site should look good on phone! Use:
```javascript
@media (max-width: 768px) {
  // Responsive styles
}
```

---

## 🐛 Troubleshooting

### **Widget doesn't load**
- Check browser console for CORS errors
- Verify backend is running on `localhost:8000`
- Check API key in init config

### **Mock data vs real data**
- For judges, mock data is **fine** - they care about UX/story
- If backend data works, even better!
- Have fallback mock data just in case

### **Routes not working**
- Make sure `App.jsx` has all routes imported
- Check React Router setup
- Verify file paths match imports

### **Styling looks broken**
- Check CSS in DevTools (F12)
- Clear browser cache (Ctrl+Shift+R)
- Make sure Tailwind is configured (if using it)

---

## 📊 What Judges Will See

```
Demo Narrative Page
  ↓ [Click "View Overview Dashboard"]
Churn Overview
  ↓ [Click "See ROI Dashboard"]  
Retention ROI Dashboard
  ↓ [Click "View Generated Messages"]
Save Actions Gallery
  ↓ [Click "See Widget in Action"]
Demo Site (with embedded widget)
```

**The story:** "Here's how churn is identified, here's the ROI, here's what we tell customers about it, and here's how they see it!"

---

## ✅ Done When...

- [ ] Widget loads on demo site without errors
- [ ] Messages gallery shows pretty previews
- [ ] Demo narrative has all 6 steps
- [ ] All routes work: `/demo`, `/save-actions`, `/demo-narrative`
- [ ] Looks good on both desktop + mobile
- [ ] Presentation script written + timed (<10 min)
- [ ] Backup screenshots saved

---

## 🚀 You're Ready When...

You can do this without looking at notes:
1. Navigate to demo site
2. Point out embedded widget
3. Click through save actions
4. Explain: "System generates personalized messages in <1 second"
5. Show: "Each saves organization thousands"

---

## 📞 When to Ask Other Teams

- **Person 1 (ML)**: "What's the exact format of churn_score + segment data?"
- **Person 2 (Backend)**: "Is `/widget/customer_view` endpoint ready? Can I use mock data meanwhile?"
- **Person 3 (Frontend)**: "Can I import components from dashboard pages?"

**Remember**: You're building the B2B2C showcase. The other teams build the guts. You make it *look* amazing.

Good luck! 🎨✨
