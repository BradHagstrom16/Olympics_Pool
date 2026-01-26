# CLAUDE.md - AI Assistant Guide for Olympics Pool (Excel Edition)

## Project Overview

This is an **Excel/Google Sheets-based fantasy sports pool** for the 2026 Milano-Cortina Winter Olympics. Players submit their picks via Google Forms, and the game administrator manages scoring through a comprehensive Excel workbook that auto-imports picks, pulls live medal data from Wikipedia, and calculates standings automatically.

**Key Stats:**
- Target: Multiple independent leagues (family, work, friends)
- Pick Deadline: February 6, 2026 at 11:59 PM CT
- Olympics: February 6-22, 2026
- Deployment: Excel workbook template distributed to league administrators

## System Architecture

### High-Level Flow
```
Player Picks → Google Form → CSV Export → Excel Import → 
Medal Data (Wikipedia) → Auto Calculation → Live Leaderboard
```

### Technology Stack

- **Primary Platform:** Microsoft Excel (Microsoft 365)
- **Secondary Platform:** Google Sheets (compatibility mode)
- **Data Collection:** Google Forms
- **Medal Data Source:** Wikipedia (manual import/refresh)
- **Distribution:** Excel template file (.xlsx)

## Workbook Structure (10 Sheets)

### 1. **Instructions**
- League administrator guide
- Setup checklist
- How to import picks from Google Forms
- How to update medal data
- Troubleshooting tips

### 2. **Leaderboard**
- **Auto-sorted** by rank using SORT/ARRAYFORMULA
- Displays: Rank, Player Name, Total Points, Tiebreaker predictions
- Updates automatically when medals change
- No manual sorting required (critical design improvement)

### 3. **Player_Picks**
- Imported from Google Forms CSV
- One row per player
- Columns: Name, Email, Tier 1 Pick, Tier 2 Pick A, Tier 2 Pick B, ..., USA Gold, USA Silver, USA Bronze
- Checkbox responses parsed and mapped to country names

### 4. **Countries**
- Master list of all 71 participating countries
- Columns: Country Name, IOC Code, Tier, Multiplier, Has_Medaled_2010_2022
- Excludes: Russia, ROC, OAR (banned from 2026)
- Source of truth for tier assignments

### 5. **Medals**
- Current medal counts for all countries
- Columns: Country Name, Gold, Silver, Bronze, Total
- Imported/pasted from Wikipedia medal table
- Updates trigger automatic score recalculation

### 6. **Scoring**
- Formula breakdown sheet
- Calculates points per player per country
- Formula: (Gold×3 + Silver×2 + Bronze×1) × Tier Multiplier
- Intermediate calculations for transparency

### 7. **Tiebreakers**
- USA actual medal counts (updated manually from Medals sheet)
- Tiebreaker logic: Closest to USA Gold → Silver → Bronze
- Distance calculations for each player

### 8. **Validation**
- Data integrity checks
- Validates: Correct pick counts per tier, No duplicate picks per player, All countries exist
- Status indicators: ✅ Valid, ❌ Invalid with specific error messages

### 9. **Reference**
- Tier structure table with multipliers
- Scoring formula documentation
- Country list by tier for quick reference
- Game rules summary

### 10. **Admin_Log**
- Change tracking (optional)
- Medal update timestamps
- Notes for league administrator

## Core Game Mechanics

### Tier Structure (6 tiers, 8 total picks)

| Tier | Name | Picks | Multiplier | Example Countries |
|------|------|-------|------------|-------------------|
| 1 | Elite | 1 | ×1 | Norway, Germany, USA, Canada |
| 2 | Strong | 2 | ×2 | Netherlands, Austria, Sweden, France |
| 3 | Competitive | 1 | ×3 | China, Japan, Italy (host) |
| 4 | Emerging | 1 | ×6 | Finland, Czech Republic, Slovenia |
| 5 | Occasional | 1 | ×10 | Poland, Great Britain, Australia |
| 6 | Wildcard | 2 | ×20 | 50+ other countries |

### Scoring Formula

```
Player Total Points = Σ (Country Medal Score)

Country Medal Score = (Gold × 3 + Silver × 2 + Bronze × 1) × Tier Multiplier
```

**Example:** Slovenia (Tier 4) wins 2 gold, 1 silver
```
Score = (2×3 + 1×2 + 0×1) × 6 = 8 × 6 = 48 points
```

### Tiebreaker System

If players have equal points:
1. **First:** Closest to USA's actual Gold medal count
2. **Then:** Closest to USA's actual Silver medal count  
3. **Then:** Closest to USA's actual Bronze medal count
4. **If still tied:** Co-champions

## Excel Formula Patterns

### Key Formula Types Used

#### 1. VLOOKUP for Medal Counts
```excel
=VLOOKUP(PlayerPick, Medals!A:D, 2, FALSE)  # Get gold count
```

#### 2. Auto-Sort Leaderboard (Critical!)
```excel
=SORT(Leaderboard_Data_Range, Points_Column, -1)  # Sort by points descending
```

#### 3. Country Name Mapping from Google Forms
```excel
=IFERROR(INDEX(Countries!A:A, MATCH(FormResponse, Countries!B:B, 0)), "")
```

#### 4. Tiebreaker Distance Calculation
```excel
=ABS(Player_USA_Gold_Guess - Actual_USA_Gold)
```

#### 5. Conditional Formatting for Ranks
```excel
# Top 3 get special highlighting
Rule: =AND($A2<=3, $A2<>"")
```

## Excel vs Google Sheets Compatibility

### Compatible Features
- Basic formulas (SUM, VLOOKUP, IF, IFERROR)
- Named ranges
- Conditional formatting
- Data validation
- Charts

### Excel-Specific (Require Workarounds in Sheets)
- `TEXTSPLIT` → Use SPLIT in Sheets
- `SORT` with multiple criteria → Use SORT with array formulas
- `UNIQUE` → Use unique values via FILTER in Sheets
- Array formulas → Use ARRAYFORMULA in Sheets

### Google Sheets-Specific
- `ARRAYFORMULA` → Manual array entry in Excel (Ctrl+Shift+Enter)
- `IMPORTRANGE` → Not available in Excel
- Real-time collaboration → Excel has limited online co-authoring

### Best Practices for Cross-Platform
1. Test all formulas in both Excel and Google Sheets
2. Use `IFERROR` liberally to handle edge cases
3. Avoid platform-specific functions when possible
4. Document any platform-specific workarounds in Instructions sheet

## Google Forms Integration

### Form Structure
The Google Form should have these questions (in order):

1. **Name** (Short answer, required)
2. **Email** (Email, required)
3. **Tier 1 - Elite** (Multiple choice, 1 selection from 4 countries)
4. **Tier 2 - Strong** (Checkboxes, exactly 2 selections from 6 countries)
5. **Tier 3 - Competitive** (Multiple choice, 1 selection from 3 countries)
6. **Tier 4 - Emerging** (Multiple choice, 1 selection from 3 countries)
7. **Tier 5 - Occasional** (Multiple choice, 1 selection from 5 countries)
8. **Tier 6 - Wildcard** (Checkboxes, exactly 2 selections from 50+ countries)
9. **USA Gold Medal Prediction** (Number, required)
10. **USA Silver Medal Prediction** (Number, required)
11. **USA Bronze Medal Prediction** (Number, required)

### CSV Export Process
1. Google Form → Responses tab → Download as CSV
2. Open CSV in Excel or import to Excel workbook
3. Copy/paste or link to Player_Picks sheet
4. Formulas automatically process the data

### Checkbox Response Parsing
Google Forms checkboxes export as comma-separated values:
```
"Netherlands, France"  # Need to split and map to individual countries
```

Parsing formula pattern:
```excel
=TRIM(LEFT(CheckboxCell, FIND(",", CheckboxCell & ",") - 1))  # First pick
=TRIM(MID(CheckboxCell, FIND(",", CheckboxCell) + 1, 100))    # Second pick
```

## Medal Data Updates

### Wikipedia Medal Table
Source: https://en.wikipedia.org/wiki/2026_Winter_Olympics_medal_table

### Update Process
1. Navigate to Wikipedia medal table
2. Select and copy the table
3. Paste into Excel Medals sheet (Ctrl+V)
4. Use "Paste Special → Values" if formulas interfere
5. Verify country names match Countries sheet exactly
6. Scores auto-recalculate via formulas

### Medal Data Format
```
Country         | Gold | Silver | Bronze | Total
Norway          |  5   |   3    |   2    |  10
Germany         |  4   |   4    |   3    |  11
```

### Country Name Mapping Issues
- Wikipedia: "United States" vs Form: "USA"
- Wikipedia: "Great Britain" vs IOC: "GBR"
- Solution: Use standardized names in Countries sheet, map in formulas

## Critical Design Decisions

### 1. Auto-Sort Leaderboards
**Problem:** Manual sorting throughout the Olympics is tedious and error-prone

**Solution:** Use SORT/ARRAYFORMULA to automatically rank by:
- Total Points (descending)
- USA Gold difference (ascending)
- USA Silver difference (ascending)  
- USA Bronze difference (ascending)

**Implementation:**
```excel
=SORT(Player_Data, Points_Column, -1, Tiebreaker_Column, 1)
```

### 2. Tier Structure Validation
**Problem:** Historical medal data shows tier balance is critical

**Solution:** 6-tier system with multipliers 1-2-3-6-10-20
- Expected value coefficient of variation: 0.014 (excellent)
- Tier 6 intentionally lower EV for "wildcard" risk/reward

### 3. Russia/ROC Exclusion
**Problem:** Russia banned from 2026 Olympics

**Solution:** Completely exclude from all tiers, forms, and data
- 71 countries total (down from ~91 typical participants)
- Historical medal data from 2010-2022 excludes Russia/ROC/OAR

### 4. Cross-Platform Compatibility
**Problem:** Some admins use Excel, others use Google Sheets

**Solution:** Maintain compatibility by:
- Avoiding Microsoft 365-exclusive functions
- Testing in both platforms
- Documenting platform-specific workarounds
- Prioritizing Excel (primary) with Sheets adaptations

## Common Tasks for Claude Code

### Adding Formula to New Column
1. Identify the target sheet and column
2. Use consistent formula patterns from existing columns
3. Apply to all rows (drag down or array formula)
4. Test with sample data
5. Verify cross-platform compatibility

### Enhancing Leaderboard Display
1. Modify SORT formula to include new criteria
2. Add conditional formatting rules for visual hierarchy
3. Ensure auto-sort persists after data changes
4. Test with multiple tied scores

### Improving Data Validation
1. Add new checks to Validation sheet
2. Use COUNTIF to detect duplicates
3. Use SUMIF to verify tier pick counts
4. Return clear ✅/❌ status with error messages

### Creating New Reference Sheets
1. Design data structure (columns, headers)
2. Link to existing data sources (Countries, Medals)
3. Add formulas for calculated values
4. Document purpose in Instructions sheet

### Debugging Formula Errors
1. Check for #N/A, #VALUE!, #REF! errors
2. Verify named ranges are defined correctly
3. Use IFERROR to gracefully handle edge cases
4. Test with empty cells and boundary conditions

## Verification Checklist

Before distributing to league administrators:

### Data Integrity
- [ ] All 71 countries present in Countries sheet
- [ ] Tier assignments match specification
- [ ] Multipliers correct (1, 2, 3, 6, 10, 20)
- [ ] No duplicate countries
- [ ] Russia/ROC/OAR excluded

### Formula Validation
- [ ] Leaderboard auto-sorts correctly
- [ ] Score calculations accurate for all tiers
- [ ] Tiebreaker logic works with tied scores
- [ ] Validation sheet catches all error conditions
- [ ] Medal updates trigger recalculation

### Cross-Platform Testing
- [ ] Test in Excel (Windows)
- [ ] Test in Excel (Mac)
- [ ] Test in Google Sheets
- [ ] Document any platform-specific issues
- [ ] Provide workarounds where needed

### User Experience
- [ ] Instructions clear and complete
- [ ] Setup checklist easy to follow
- [ ] Troubleshooting guide covers common issues
- [ ] Reference sheet helpful
- [ ] Error messages actionable

### Performance
- [ ] Formulas calculate quickly (<2 seconds)
- [ ] No circular reference warnings
- [ ] Named ranges optimize lookups
- [ ] File size reasonable (<5 MB)

## Things to Watch Out For

1. **Country Name Consistency**
   - Wikipedia uses different names than IOC codes
   - Google Forms may have typos in player submissions
   - Always map to standardized names in Countries sheet

2. **Checkbox Parsing**
   - Google Forms Tier 2 and Tier 6 use checkboxes (multi-select)
   - Must split comma-separated values correctly
   - Validate exactly 2 selections for these tiers

3. **Auto-Sort Maintenance**
   - SORT formula must include ALL ranking criteria
   - Tiebreaker columns must be in correct order
   - Test with intentionally tied scores

4. **Formula Portability**
   - TEXTSPLIT doesn't exist in Google Sheets
   - ARRAYFORMULA doesn't work the same in Excel
   - Always test in both platforms

5. **Medal Data Format Changes**
   - Wikipedia may change table structure
   - Country name spellings may vary
   - Always verify paste location and headers

6. **Edge Cases**
   - Player picks country not in list (validation)
   - Player picks same country twice (validation)
   - Tiebreaker predictions are negative numbers
   - Medal counts decrease (doping corrections)

## Statistical Foundation

The tier structure is based on rigorous analysis:

### Historical Data (2010-2022)
- 4 Olympic cycles analyzed
- Medal counts per country tracked
- K-means clustering for optimal groupings
- Silhouette score: 0.695 (excellent separation)

### Expected Values (Per Pick)
| Tier | Avg EV | Strategy |
|------|--------|----------|
| 1 | 58.6 pts | Safe, consistent |
| 2 | 59.5 pts | Balanced |
| 3 | 59.8 pts | Host advantage |
| 4 | 59.0 pts | High upside |
| 5 | 57.5 pts | Moderate risk |
| 6 | 28.6 pts | High risk/reward |

**Coefficient of Variation:** 0.014 (exceptionally balanced)

## File Naming Convention

For version control and distribution:
```
Olympics_Pool_2026_v[X.Y]_[League].xlsx

Examples:
Olympics_Pool_2026_v1.0_Family.xlsx
Olympics_Pool_2026_v1.2_Work.xlsx
Olympics_Pool_2026_v2.0_Friends.xlsx
```

Version numbers:
- **Major (X):** Significant formula changes, sheet additions
- **Minor (Y):** Bug fixes, small enhancements

## Support Resources

### Documentation
- **Instructions sheet** - In-workbook guide
- **Reference sheet** - Quick lookup tables
- **SPECIFICATION.md** - Locked game rules (GitHub)
- **README.md** - Project overview (GitHub)

### External Links
- Wikipedia Medal Table: https://en.wikipedia.org/wiki/2026_Winter_Olympics_medal_table
- Official Olympics: https://olympics.com/en/olympic-games/milano-cortina-2026
- GitHub Repository: https://github.com/BradHagstrom16/Olympics_Pool

## Future Enhancements (Potential)

- [ ] Automated Wikipedia scraping (Excel Power Query)
- [ ] Real-time Google Sheets integration (IMPORTDATA)
- [ ] Historical performance tracking across years
- [ ] Player statistics (best picks, worst picks)
- [ ] What-if scenario calculator
- [ ] Mobile-friendly Google Sheets version
- [ ] Automated email reports to players

## Development Principles

When enhancing the workbook:

1. **Prioritize Simplicity** - League admins aren't Excel experts
2. **Test Thoroughly** - Verify in both Excel and Sheets
3. **Document Changes** - Update Instructions sheet
4. **Validate Data** - Add checks to Validation sheet
5. **Preserve Compatibility** - Don't break existing formulas
6. **Think Multi-League** - Template used by multiple admins
7. **Plan for Errors** - Use IFERROR and clear error messages
8. **Optimize Performance** - Keep file size small, formulas fast

## Claude Code Usage Tips

When working with Claude Code on this project:

1. **Always review the entire workbook structure first**
   - Understand sheet relationships
   - Identify named ranges
   - Note existing formula patterns

2. **Test incrementally**
   - Make one change at a time
   - Verify in Excel before moving to Sheets
   - Use sample data for validation

3. **Preserve existing functionality**
   - Don't overwrite working formulas
   - Back up sheets before major changes
   - Document what was changed and why

4. **Focus on robustness**
   - Handle empty cells gracefully
   - Validate inputs
   - Provide clear error messages

5. **Think about the end user**
   - Is this intuitive for a league admin?
   - Does it require advanced Excel knowledge?
   - Is there clear documentation?

---

**Project Status:** Active Development  
**Target Deployment:** January 2026 (1 month before deadline)  
**Current Version:** v1.0 (Stable baseline with auto-sort)  
**Platform Priority:** Excel primary, Google Sheets secondary
