# 2026 Milano-Cortina Winter Olympics Pool
## Final Specification Document

**Status:** 🔒 LOCKED  
**Version:** 1.0  
**Last Updated:** December 16, 2024  
**Validated:** Full statistical validation complete

---

## 1. GAME OVERVIEW

**Name:** 2026 Milano-Cortina Winter Olympics Pool

**Concept:** Players select 8 countries across 6 tiers to build their fantasy team. Points are earned when selected countries win medals, with lower-tier countries earning higher point multipliers to balance the game.

**Target Audience:** 20-30 players via shared link

**Entry Fee:** Free (bragging rights)

---

## 2. KEY DATES

| Event | Date/Time |
|-------|-----------|
| Olympics Start | February 6, 2026 |
| Olympics End | February 22, 2026 |
| **Pick Deadline** | **February 6, 2026 at 11:59 PM Central Time** |
| First Event | February 7, 2026 at 10:05 AM CET |

---

## 3. TIER STRUCTURE

| Tier | Name | Countries | Picks Required |
|------|------|-----------|----------------|
| **1** | Elite | Norway, Germany, United States, Canada | 1 |
| **2** | Strong | Netherlands, Austria, Sweden, France, Switzerland, South Korea | 2 |
| **3** | Competitive | China, Japan, Italy | 1 |
| **4** | Emerging | Finland, Czech Republic, Slovenia | 1 |
| **5** | Occasional | Poland, Great Britain, Australia, Slovakia, Latvia | 1 |
| **6** | Wildcard | New Zealand, Ukraine, Hungary, Kazakhstan, Croatia, Belgium, Spain, Estonia, Liechtenstein, + all other participating countries | 2 |

**Total Picks:** 8 (1 + 2 + 1 + 1 + 1 + 2)

### Country Assignments

**Tier 1 - Elite (4 countries)**
- Norway
- Germany  
- United States
- Canada

**Tier 2 - Strong (6 countries)**
- Netherlands
- Austria
- Sweden
- France
- Switzerland
- South Korea

**Tier 3 - Competitive (3 countries)**
- China
- Japan
- Italy *(2026 Host Nation)*

**Tier 4 - Emerging (3 countries)**
- Finland
- Czech Republic
- Slovenia

**Tier 5 - Occasional (5 countries)**
- Poland
- Great Britain
- Australia
- Slovakia
- Latvia

**Tier 6 - Wildcard (9+ countries)**
- New Zealand
- Ukraine
- Hungary
- Kazakhstan
- Croatia
- Belgium
- Spain
- Estonia
- Liechtenstein
- *Any other participating country not listed in Tiers 1-5*

### Excluded Countries
- Russia / ROC / AIN - Banned from 2026 Olympics
- Belarus - Expected to compete as AIN

---

## 4. SCORING SYSTEM

### Medal Weights
| Medal | Base Points |
|-------|-------------|
| Gold | 3 |
| Silver | 2 |
| Bronze | 1 |

### Tier Multipliers
| Tier | Multiplier | Gold | Silver | Bronze |
|------|------------|------|--------|--------|
| 1 | ×1 | 3 | 2 | 1 |
| 2 | ×2 | 6 | 4 | 2 |
| 3 | ×3 | 9 | 6 | 3 |
| 4 | ×6 | 18 | 12 | 6 |
| 5 | ×10 | 30 | 20 | 10 |
| 6 | ×20 | 60 | 40 | 20 |

### Scoring Rules
- A medal is a medal - team events and individual events count the same
- 1 gold medal = 1 gold medal's worth of points, regardless of event type
- Scores based on official medal table counts per country
- No retroactive adjustments for doping disqualifications after Games conclude

---

## 5. TIEBREAKER SYSTEM

At registration, users submit predictions for USA's medal count:
1. USA Gold medal count guess
2. USA Silver medal count guess
3. USA Bronze medal count guess

**Tiebreaker Resolution (in order):**
1. Closest to actual USA Gold count
2. If still tied: Closest to actual USA Silver count
3. If still tied: Closest to actual USA Bronze count
4. If still tied: Co-champions

---

## 6. USER EXPERIENCE

### Registration
- Open signup (anyone with site link can register)
- Email required
- Password required (min 6 characters)
- Display name optional

### Pick Submission
- All 8 picks submitted together (tier-by-tier selection on one page)
- Picks can be edited unlimited times before deadline
- Tiebreaker guesses submitted with picks
- Deadline: February 6, 2026 at 11:59 PM Central Time

### Pick Visibility
- **Before deadline:** Users can see who has registered, but NOT their picks
- **After deadline:** All picks visible to all users

### Tier 6 Selection UI
- Scrollable list of all Tier 6 countries
- Search/filter box to find countries quickly
- Countries that have NOT medaled in last 4 Winter Olympics marked with ⚪

### Tier 6 Warning Display
> **⚠️ Wildcard Tier Notice**  
> Not all countries in Tier 6 have recent Olympic medal history. Countries marked with ⚪ have not won a medal in the last four Winter Olympics (2010–2022). Choose wisely—or boldly.

---

## 7. LEADERBOARD

### Display Elements
- Rank
- Player name
- Total points
- Individual country scores (expandable/detail view)
- "Last updated" timestamp

### During Games
- Updates when medal data is refreshed
- Shows current standings based on medals won so far

### After Games
- Final standings
- Tiebreaker applied if needed
- Winner highlighted

---

## 8. EDGE CASES

| Scenario | Handling |
|----------|----------|
| Country withdraws before Games | Counts as 0 points (users notified manually) |
| Country not in Tier 1-5 participates | Automatically Tier 6 |
| Medal stripped for doping (after Games) | No retroactive adjustment |
| Mixed nationality team medals | Ignore (scoring based on medal table by country) |
| Identical picks AND tiebreaker | Co-champions |

---

## 9. ADMIN FEATURES

### Required at Launch
- View all users
- View all picks (after deadline)
- Manual medal count entry/update (API backup)
- Reset user password
- Trigger score recalculation

### Nice to Have (Future)
- Email notifications
- Monetary prize tracking
- Historical data (for future years)

---

## 10. TECHNICAL REQUIREMENTS

### Stack
- **Framework:** Flask (Python)
- **Database:** SQLite
- **Frontend:** Bootstrap 5
- **Hosting:** PythonAnywhere

### Medal Data
- **Primary:** Automated via API (research closer to Games)
- **Fallback:** Manual admin entry
- **Reference:** Excel automation from Summer Olympics

### Timezone
- All deadlines in Central Time (America/Chicago)
- Display "Last updated" timestamps to users

---

## 11. STATISTICAL VALIDATION

| Element | Status | Evidence |
|---------|--------|----------|
| 6-Tier Structure | ✅ Optimal | K-means elbow analysis |
| Country Assignments | ✅ Optimal | Silhouette score 0.695 |
| Tier 3/4 Split | ✅ Justified | 48% variance reduction |
| 8-Pick Structure | ✅ Optimal | Balanced differentiation |
| Scoring (×1-2-3-6-10-20) | ✅ Locked | EV CV 0.21 |
| 3:2:1 Medal Ratio | ✅ Optimal | Alternatives tested |

### Expected Values by Tier
| Tier | Avg EV per Pick |
|------|-----------------|
| 1 | 58.6 pts |
| 2 | 59.5 pts |
| 3 | 59.8 pts |
| 4 | 59.0 pts |
| 5 | 57.5 pts |
| 6 | 28.6 pts |

*Tier 6 intentionally lower EV - "wildcard" risk/reward dynamic*

### Portfolio Analysis (8 picks)
- **Expected Total:** ~411 points
- **Best Possible (historical):** ~650 points
- **Worst Possible:** ~200 points

---

## 12. FUTURE CONSIDERATIONS

- Monetary prize option (code hooks for later)
- Email notifications for deadline reminders
- Mobile app version
- Summer Olympics 2028 adaptation
- Historical leaderboards across years

---

*Specification locked December 16, 2024*
*Ready for development*
