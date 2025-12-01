# ✅ PERSON 4: YOUR HACKATHON CHECKLIST

Copy this and check off as you go!

---

## 📋 SETUP & PLANNING (Hour 0)

- [ ] Read `PERSON_4_README.md` (this overview)
- [ ] Read `PERSON_4_START_HERE.md` (main guide)
- [ ] Understand your role: Widget + Demo Engineer
- [ ] Know your deliverables: 4 components + presentation
- [ ] Check that backend is running on port 8000
- [ ] Check that frontend is running on port 5173

---

## 🛠️ BUILD PHASE (Hours 1-5)

### TASK 1: Update App.jsx (5 min)
- [ ] Open `frontend/src/App.jsx`
- [ ] Add 3 imports for DemoSite, SaveActionGallery, DemoNarrative
- [ ] Add 3 routes for `/demo`, `/save-actions`, `/demo-narrative`
- [ ] Save file
- [ ] No errors in console? ✅

### TASK 2: Create DemoSite.jsx (1.5 hours)
- [ ] Create new file: `frontend/src/pages/DemoSite.jsx`
- [ ] Copy code from `PERSON_4_COPY_PASTE.md` → TASK 2
- [ ] Save file
- [ ] Test: Go to `http://localhost:5173/demo`
- [ ] Widget loads (purple box with text)? ✅
- [ ] Portal looks like fake company site? ✅
- [ ] No console errors? ✅

### TASK 3: Create SaveActionGallery.jsx (1.5 hours)
- [ ] Create new file: `frontend/src/pages/SaveActionGallery.jsx`
- [ ] Copy code from `PERSON_4_COPY_PASTE.md` → TASK 3
- [ ] Save file
- [ ] Test: Go to `http://localhost:5173/save-actions`
- [ ] Grid of 3 messages shows? ✅
- [ ] Click a message to see email + SMS? ✅
- [ ] Numbers display correctly? ✅
- [ ] No console errors? ✅

### TASK 4: Create DemoNarrative.jsx (1 hour)
- [ ] Create new file: `frontend/src/pages/DemoNarrative.jsx`
- [ ] Copy code from `PERSON_4_COPY_PASTE.md` → TASK 4
- [ ] Save file
- [ ] Test: Go to `http://localhost:5173/demo-narrative`
- [ ] 6 steps display with progress bar? ✅
- [ ] Next/Previous buttons work? ✅
- [ ] View Demo buttons navigate correctly? ✅
- [ ] No console errors? ✅

---

## 🧪 TESTING PHASE (Hour 6)

### Desktop Testing
- [ ] Visit `/demo-narrative` in browser
- [ ] Click through all 6 steps
- [ ] Each "View Demo" button works
- [ ] Widget shows on `/demo`
- [ ] Messages show on `/save-actions`
- [ ] No broken links
- [ ] No console errors (F12 → Console)
- [ ] No missing images/resources

### Mobile Testing
- [ ] Open DevTools (F12)
- [ ] Click responsive mode (Ctrl+Shift+M)
- [ ] Test on iPhone size (375px wide)
- [ ] Test on tablet size (768px wide)
- [ ] All text readable?
- [ ] Buttons clickable?
- [ ] Images scale properly?
- [ ] No horizontal scroll?

### Performance Check
- [ ] Pages load in <2 seconds
- [ ] Widget renders smoothly
- [ ] No lag when scrolling
- [ ] Animations are smooth

---

## 🎬 PRESENTATION PREP (Hours 7-8)

### Demo Script
- [ ] Write: What you'll say for each page
- [ ] Write: How each button click relates to the story
- [ ] Time it: Should be 8-10 minutes total
- [ ] Rehearse: Practice 2-3 times
- [ ] Get feedback: Have teammate listen

### Screenshots (Backup Plan)
- [ ] Screenshot: `/demo-narrative` page
- [ ] Screenshot: `/demo` with widget
- [ ] Screenshot: `/save-actions` with messages
- [ ] Screenshot: `/save-actions` preview modal
- [ ] Save in folder: `docs/demo-screenshots/`

### Presentation Checklist
- [ ] Judges understand: "What is SHEBA?"
- [ ] Judges see: Widget embedded on portal
- [ ] Judges get: Revenue at risk numbers
- [ ] Judges understand: "How is it different?"
- [ ] Judges remember: Key value prop
- [ ] Judges want to know: "How do I try it?"

### Technical Backup
- [ ] Backend team will be nearby?
- [ ] Know what to do if widget breaks?
- [ ] Know what to do if routes don't work?
- [ ] Have internet backup (hotspot)?
- [ ] Monitor battery level

---

## 🔍 FINAL QA (Before Demo)

### Functionality
- [ ] All routes accessible
- [ ] All pages load without errors
- [ ] Widget shows real (or mock) data
- [ ] Messages display nicely
- [ ] Buttons work as expected
- [ ] No dead links

### Appearance
- [ ] Colors consistent (purple/white/green)
- [ ] Fonts look good
- [ ] Spacing looks balanced
- [ ] Widget looks premium
- [ ] Professional appearance

### Browser Console
- [ ] No red errors
- [ ] No warning messages
- [ ] Network requests succeed (or fail gracefully)

### User Experience
- [ ] Clear story flow
- [ ] Intuitive navigation
- [ ] Smooth transitions
- [ ] Fast load times

---

## 📊 FEATURE CHECKLIST

### Widget (sheba-widget.js)
- [ ] ✅ Already created and in `public/` folder
- [ ] Shows customer name
- [ ] Shows loyalty score
- [ ] Shows engagement level
- [ ] Shows personalized offer
- [ ] Shows tips
- [ ] Has claim button
- [ ] Is responsive

### Demo Site (DemoSite.jsx)
- [ ] Looks like real telecom portal
- [ ] Has header with company name
- [ ] Has sidebar with menu items
- [ ] Shows customer cards
- [ ] **Embeds widget below title**
- [ ] Footer with copyright
- [ ] Responsive design

### Message Gallery (SaveActionGallery.jsx)
- [ ] Title + subtitle
- [ ] Stats cards showing totals
- [ ] Grid of messages (3 per row)
- [ ] Click message to select
- [ ] Preview panel shows:
  - [ ] Email subject
  - [ ] Email body
  - [ ] SMS text
  - [ ] Revenue at risk
  - [ ] Projected savings
- [ ] Mobile responsive

### Demo Narrative (DemoNarrative.jsx)
- [ ] Progress bar at top
- [ ] 6 step titles
- [ ] Step descriptions
- [ ] Visual placeholder
- [ ] Previous/Next buttons
- [ ] View Demo link buttons
- [ ] Progress dots
- [ ] Responsive design

---

## 🎯 DEMO DAY FLOW

### 5 Minutes Before Demo
- [ ] Reboot your machine (clear cache)
- [ ] Start backend: `uvicorn app.main:app --port 8000`
- [ ] Start frontend: `npm run dev` at port 5173
- [ ] Test widget loads
- [ ] Test all routes work
- [ ] Clear browser cache

### Demo Starts (8-10 minutes)
- [ ] Start at: `/demo-narrative` homepage
- [ ] Walk through 6 steps in order
- [ ] Explain value at each step
- [ ] Show widget on portal
- [ ] Display generated messages
- [ ] End with: "Questions?"

### During Demo
- [ ] Stay calm
- [ ] Point to UI elements
- [ ] Don't read text verbatim
- [ ] Emphasize the story, not tech
- [ ] Highlight numbers ($150K saved)
- [ ] Show automation benefit

### If Demo Breaks
- [ ] Stay cool
- [ ] Show screenshot backup
- [ ] Say: "This is what it looks like"
- [ ] Continue with narrative
- [ ] Highlight the concept

### After Demo
- [ ] Answer questions
- [ ] Offer to show code
- [ ] Provide contact info
- [ ] Thank judges

---

## 📈 SUCCESS INDICATORS

### Judges Will Ask (Good Signs):
- "How does the personalization work?"
- "What ML model do you use?"
- "How fast is the message generation?"
- "Can we try it?"
- "What's your retention improvement?"
- "How much would this save us?"

### Judges Will Nod (You're Winning):
- At the ROI numbers
- When they see the widget
- When they understand B2B2C model
- When you mention retention rate

### Judges Will Look Confused (Problems):
- If page doesn't load
- If widget doesn't show
- If story isn't clear
- If you can't answer questions

---

## 🎁 Bonus Points (If Time Allows)

- [ ] Add animations to transitions
- [ ] Dark mode toggle
- [ ] More detailed postmortem insights
- [ ] Real data integration working
- [ ] Mobile app for widget
- [ ] API key generation page
- [ ] Demo data seeding script

---

## 🚨 CRITICAL ITEMS (Don't Skip)

**MUST HAVE:**
1. ✅ Widget loads on `/demo` page
2. ✅ Messages show on `/save-actions` page
3. ✅ Demo narrative explains the flow
4. ✅ Story is coherent and compelling
5. ✅ No console errors

**NICE TO HAVE:**
- Mobile responsive
- Real backend data
- Polished animations
- Extra features

**DON'T WORRY ABOUT:**
- Complex ML explanation
- Database schema details
- Deployment infrastructure
- Edge cases

---

## 📝 Notes for Other Team Members

**For Backend Team:**
"I'm using mock data for now. When `/api/v1/widget/customer_view` and `/api/v1/save-actions` endpoints are ready, I can swap them in (5 min work)."

**For Frontend Team:**
"Can I import your styles/components, or should I keep my own styling?"

**For ML Team:**
"Do you have sample output data I can use for testing?"

---

## 🎓 Learning Resources (If Stuck)

**Widget Issues:**
- Check: `frontend/public/sheba-widget.js` file exists
- Read: Comments in the widget file
- Test: Open console, type `window.ShebaWidget`

**Route Issues:**
- Check: `frontend/src/App.jsx` has all imports
- Check: File paths match exactly
- Test: Clear cache (Ctrl+Shift+R)

**Styling Issues:**
- Check: Inline styles in component
- Test: Try styles in browser DevTools
- Fallback: Use simpler CSS

**Data Issues:**
- Use: Mock data in component
- Swap: Real data when ready
- Test: Use browser network tab

---

## ✨ YOU'VE GOT THIS!

You have **7 hours of focused work** to do.
You have **23+ hours of buffer** for everything else.
You have **amazing teammates** who can help.
You have **clear instructions** for everything.

**Start NOW. Good luck! 🚀**

---

**Final Reminder:** This is a hackathon. Perfection ≠ Success. 
- ✅ Functional > Pretty
- ✅ Story > Features  
- ✅ Clear Demo > Complex Tech

Focus on **making judges understand the value** and **showing it works**.

**You're the storyteller. Make it compelling!** 🎬✨

---

**Current Time**: December 2, 2025  
**Hackathon Duration**: 27-30 hours  
**Your Time Allocation**: ~8 hours  
**Status**: Ready to start ✅

**GO BUILD!** 🚀
