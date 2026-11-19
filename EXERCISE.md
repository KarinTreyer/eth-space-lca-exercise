# Exercise: a quick screening LCA related to FireSat II

Exercise prepared for the ETH Zürich Space Systems Master, Core Course 1 - Life Cycle Assessment, 25 November 2026. 
Exercise prepared by karin.treyer@psi.ch

## Recap: FireSat II Mission Statement
To develop and deploy a low-cost, near real-time satellite system to detect, identify, and monitor forest fires across the United States and Canada. 
This system will provide data directly to fire management officers and firefighters in the field, improving response times and effectiveness.


## The situation

You are part of the environmental sustainability team of FireSat II. The Preliminary Design Review (PDR) is being planned.
The project manager asks three questions:

1. **Where** are the potential environmental hotspots of FireSat II?
2. **How sure** are we about them?
3. **Which one design or programme decision** would reduce the impacts most - without just shifting them to another life cycle stage or another impact category?

A first data collection exists: `data/FireSat2_LCI.xlsx`. It was put together in a hurry by a colleague using AI based on the information in the FireSat II Mission Briefing pdf document. Every inventory line has a data quality rating (DQR) from 1 (rough guess) to 4 (very good), and many lines are rated 1 or 2.
Your team improves the inventory of one part of the mission **where it matters**, and answers the three
questions for that part. At the end we put the mission back together.

## Learning goals

After this exercise you can:

1. **Formulate goal and scope** of a space mission LCA or an individual element/component of a mission: intended application, target audience, functional unit, system
   boundary, allocation and impact categories (ISO 14044, ESA LCA Handbook).
2. **Build and improve an inventory**: choose fitting background datasets, check units and mass balances, and
   **document every data source and its quality** so that someone else can follow and reproduce it.
3. **Run an LCA with Brightway** in a Jupyter notebook and **explore datasets with Activity Browser**.
4. **Interpret results**: find hotspots, judge whether the data behind them are good enough, test
   alternatives with what-if variants, and spot burden shifting.
5. **Name the limits** of the result - what your LCA cannot (yet) say about space missions.
6. **Use AI critically** for data collection.
7. **Communicate** the results of a LCA and related robustness/uncertainty to a decision maker on 1-3 pptx slides.
And you have worked with the ESA LCA Handbook.

## What you use

| What | What for |
|---|---|
| `notebooks/01_firesat_lca.ipynb` | Import, calculation, all plots. Run it top to bottom ("Run All"), then look at it. You only need to write code in the cells marked ✏️. `lca_helpers.py` contains the plotting functions - you do not need to read it. |
| `data/FireSat2_LCI.xlsx` | **The file your team edits.** Sheets: `goal_scope` (your goal and scope), `lci` (the inventory), `mass_budget` (SMAD numbers), `dqr_guide` (how to rate data quality). |
| Activity Browser | Brightway GUI. Finding datasets, reading their documentation (comment field), looking at their supply chain (graph explorer) - for ecoinvent datasets. The 25 ESA datasets are aggregated for legal reasons: you see their names and can calculate with them, but not their content (see README). Copy names, reference products, locations and units from here into the Excel. The calculation runs in the notebook. You can also play around in AB to see results if you find time. |
| ESA LCA Handbook (ESSB-HB-U-005, Issue 2, Dec 2025) | ISO-based LCA rules tailored to space LCA. See the section list below. |
| FireSat II Mission Briefing / SMAD | Masses, power, orbit, mission duration. |
| Literature, user's guides, AI | Launcher user's guides, test facility data sheets, papers, e.g. the DLR *Inventory of Global Emissions by Launchers 2024* (Herberhold et al. 2026) for launch emissions per kg of propellant. |
| The lecture slides | Your FireSat goal-and-scope answers, data quality, atmospheric impacts. |

**ESA LCA Handbook - where to look**
Download: https://esamultimedia.esa.int/docs/spacesafety/Space_System_Life_Cycle_Assessment_Guidelines.pdf 

| Topic | Section |
|---|---|
| Functional unit of a mission | 6.2.1.1 (mission FU and service FU, Table 6-1) |
| System boundaries of a mission | 6.2.1.2 |
| Cut-off criteria, allocation (e.g. shared launch) | 6.2.2.3, 6.2.2.4.2 |
| Space segment: boundaries, buy-to-fly ratio | 6.3.1.2, 6.3.2.1.1 |
| Office work, staff travel, testing, cleanroom allocation | 6.3.2.4.1 - 6.3.2.4.4 |
| Launch vehicle: functional unit, boundaries, data | 6.4.2, 6.4.3 |
| Ground stations: yearly impacts and allocation to a mission | 6.5.2.4.2, 6.5.2.4.3 |
| Data quality rating | Annex B |

## Teams and work packages

Each team takes one work package. In the sheet `lci`, the header of each activity shows its team letter.

| Team | Work package | Starting questions |
|---|---|---|
| **A** | **Space segment** - spacecraft bill of materials (payload, structure, power, avionics, ADCS, propulsion, propellant) | Is the split of the 26 kg payload sensible? Is one ~20 t CO₂-eq hydrazine tank plausible for 3 kg of propulsion dry mass? Which ESA datasets fit the electronics better? Ecodesign: structure material, solar array, "green" propellant (how much LMP-103S do you need for the same Δv?). |
| **B** | **AIT and engineering** - test models, thermal vacuum and acoustic tests, cleanroom, office work, travel | Which model philosophy (STM, EM, PFM, FM) does FireSat II need? How long are the tests and how big is the chamber? Where is FireSat II built and tested (electricity mix)? How many people work how many years on it? |
| **C** | **Launch** - 2 dedicated Minotaur IV vs. rideshare | Check the Minotaur IV masses (propellant, cases). Who carries the impacts of decommissioned ICBM motors? How do you allocate a launcher that is ~90 % empty? Complete the Falcon 9 rideshare variant (its exhaust is missing) and compare. |
| **D** | **Ground segment and end of life** | How much antenna time does FireSat II really need? Is 20 kW for mission operations realistic (it is currently a large contributor)? End of life: is the 183 m/s disposal Δv needed at 700 km? What does the re-entry of 86 kg emit? Add a re-entry activity with its flows. |

Form groups of ca. 3 members and pick one work package. Teams working on the same work package will compare their results at the end.

**Roles inside the team** (rotate if you like):

- *Data scout*: literature, ESA LCA Handbook, AI.
- *Modeller*: edits the Excel.
- *Analyst*: runs the notebook and Activity Browser.
- *Reviewer = all*: check plausibility, units and DQR, and prepares the slide.

## Timeline

| Time | Step | What |
|---|---|---|
| 14:15-14:45 | 0 | Introduction, demo: Introduction to this exercise, short demo of the jupyter notebook / Activity Browser. |
| 14:45-15:00 | 1 | Get started: Form groups, choose work package, split roles, start to discuss goal and scope |
| *15:00-15:15* | | *Break* |
| 15:15-16:00 | 2-4 | Work on goal & scope, inventory, impact assessment and interpretation - iterate. Prepare slides.|
| *16:00-16:15* | | *Break* |
| 16:15-16:45 | | Each team presents/discusses challenges (4 min). We put the mission back together. |
| 16:45 | | Wrap-up and feedback |

## Step by step

### Step 0 - Get started

1. Open `notebooks/01_firesat_lca.ipynb` and run all cells. It must finish without errors and print the result
   table in section 4.
2. Look at the plots of section 5: where is **your** work package in the mission result?
   Then zoom in: in section 4 ("Mission or work package?"), set `SYSTEM` to your team letter (e.g. `SYSTEM = "B"`)
   and re-run sections 4 and 5. Now the plots show only your work package. Work like this during the afternoon,
   and switch back to `SYSTEM = "mission"` to see what your changes mean for the whole mission (you need both on your slide).
3. Split the roles.

### Step 1 - Goal and scope - ISO 14044, phase 1

Fill in the sheet `goal_scope`. Start from your morning answers.

The draft functional unit for the whole mission is *one FireSat II mission (2 spacecraft, 8 years) in fulfilment of its
requirements*. Keep it unless you have a good reason to change it - all teams need the same functional unit to
put the mission back together. But you should in addition formulate a functional unit for the work you are focussing on.

Questions to answer:

- **Intended application and audience:** Which decision does this study support, and who reads it?
  Is it a comparison that will be published (a "comparative assertion" in ISO terms)?
- **Functional unit:** What function does FireSat II provide? Compare the mission functional unit with the
  service functional unit in the Handbook (Table 6-1). Which one helps the project manager more, and which one
  would you need to compare FireSat II with fire detection from aircraft? // What is the function of your work package item?
- **Reference flows:** What exactly is needed to fulfil the functional unit in your work package (how many
  spacecraft and test models, launches, years of operation, person-years)?
- **System boundary:** What is inside and outside your work package? Which cut-off do you apply, and why? Which project phases do you include?
  Make a quick sketch (it can go on your slide).
- **Allocation:** Which parts are shared with other missions (launcher, test facilities, cleanroom, ground
  station)? Which allocation rule do you use, and what does the Handbook recommend?
- **Impact categories:** The workbook uses the minimum set of the Handbook plus ozone depletion. Which
  environmental effects of a space mission are *not* covered by these categories?
- **Data quality requirements:** Which DQR score is good enough for a PDR decision?

### Step 2 - Life cycle inventory (main part) - ISO 14044, phase 2

**Choose what to improve first.** Use the priority plot (notebook section 5c): lines with a large contribution
and a low DQR come first. Improving a line that contributes 0.1 % does not change any conclusion. Plan few
improvements as you have limited time.

**How to change the inventory:**

1. Find the line in the sheet `lci`.
2. Change the amount, or replace the dataset. Copy name, reference product, location and unit exactly from
   Activity Browser or from `h.search("...")` in the notebook. You can also add lines or whole activities
   (copy an existing activity block as template).
3. **Read the dataset's documentation** (comment field in Activity Browser) before you use it. Check its unit:
   per kg, per unit, per hour, per year? For the aggregated ESA datasets you only have name, unit and location:
   check the unit, and calculate the score of 1 unit - is it plausible?
4. Rate the line: `dqr_amount`, `dqr_activity`, `dqr_background_ds` (sheet `dqr_guide`).
5. Describe where the number comes from in `source`, and your assumptions and calculation in `comment`. 
    Or add the raw data in sheet "raw data" and link to that original cell
6. Save the Excel and re-run the notebook from section 3.

**Good documentation rules:**

- `source` is specific enough that someone else can find the number again: author, year, title or document,
  page or table. "Internet" or "ESA" is not a source.
- `comment` shows the calculation, e.g. `2 x 14 days x 24 h x 12 kW = 8064 kWh`. 
  Or even better - place the calculation in the "raw data" sheet and link to it.
- All three DQR columns are filled in (if you don't have time, de-prioritise the "background dataset" one). A line you did not check keeps its low rating.
- Keep the old value in the comment (`was 77,800 kg`). You may want to compare before/after your work results.

**Using AI is allowed.** Treat an AI answer like a guess from a colleague: ask for the source, check the
source, and rate honestly. An AI number you could not verify gets `dqr_amount = 1` and
`source = "AI (tool name), not verified"`. Note which tool helped and where it was wrong.

Questions to answer:

- Which entries did you improve first, and why those?
- Does each dataset represent what you model (material, technology, geography, unit)? Where did you have to use
  a proxy?
- Does your inventory add up? E.g. the bill of materials of team A against the mass budget (sheet
  `mass_budget`), the propellant mass of team C against the launcher's user's guide.
- Which data would you ask the industry partner for?

### Step 3 - Impact assessment - ISO 14044, phase 3

Brightway does the calculation. You do not need to change anything, but you need to understand what comes out.

Run notebook section 4 and check with `res.check()` that all contributions add up to the total.

Questions to answer:

- What is the unit of each impact category, and what is the reference substance (e.g. kg CO₂-eq, kg CFC-11-eq)?
- Which emissions of FireSat II get **no** characterisation factor (section 5e)? What does that mean for the
  launch and re-entry results?

### Step 4 - Interpretation - ISO 14044, phase 4

Interpretation is not the last step: you go back and forth between steps 2, 3 and 4. After every inventory
change, look at the plots again.

| ISO element | Notebook | Questions to answer |
|---|---|---|
| **Significant issues** (hotspots) | 5a, 5b | Which stage and which inventory lines dominate? Is the ranking the same for climate change and for resource use? |
| **Data quality** | 5b (colours), 5c, 5d | Is the data behind the hotspots good enough? Or did you potentially miss a hotspot due to incomplete data/using a proxy? How did the contribution-weighted DQR of your stage change (before → after)? |
| **Sensitivity** | 5f (7a, 7b optional) | Change at least one assumption or design choice with `what_if` (your own variant in the ✏️ cell). How much does the mission result change? Optional: tornado chart of several assumptions (7a) and the mission lifetime as a parameter (7b). |
| **Burden shifting** | 5f | Does your variant improve **all** impact categories, or does it shift the impact to another category or stage? |
| **Completeness** | 5e | What is missing in the inventory or in the impact assessment? |
| **Consistency** | - | Do you use the same assumptions as the other teams (functional unit, electricity mix, number of spacecraft)? Ask them. |
| **Conclusions and limitations** | - | What can you recommend for the PDR, and what can you not say with this data? |

### Step 5 - Visualise and communicate

Export your results with notebook section 5g (`results_firesat2.xlsx`) and place them in your "FireSat2_LCI excel file, sheet "LCIA" (sometimes convenient to have everything together to share with project partners or a colleague), or take the plots from the notebook.

**Your slides (2 slides per team, ca. 4 minutes incl. discussion):**

1. **What you changed:** the 3-5 most important lines, before → after (amount and DQR).
2. **Result:** the stage plot or the what-if table for the whole mission after your change. Did the hotspot
   move?
3. **How sure:** contribution-weighted DQR of your stage (section 5d), before → after.
4. **Recommendation for the PDR:** one decision, with its trade-off (does it get better in all impact
   categories?).
5. **What we cannot say/challenges:** one thing the LCA does not capture (hint: section 5e) / challenges you met.

Good figures:

- State the functional unit and the unit on the axis ("t CO₂-eq per mission").
- Show shares **and** absolute values, or say what 100 % is.
- Show data quality next to the result (e.g. the hotspot plot with DQR colours).
- Round sensibly: a screening LCA with DQR 2 does not have three significant digits.
- Do not add up impact categories that have different units.



## Quality checklist

- [ ] The notebook runs from top to bottom without errors, and `res.check()` passes.
- [ ] Every line you changed has a `source`, a `comment` and all three DQR values.
- [ ] Units checked: kg vs. t, hour vs. day, man-hour vs. man-year, per unit vs. per kg.
- [ ] The result makes sense compared to the mass budget and the morning lecture (orders of magnitude).
- [ ] At least one what-if variant, looked at in all impact categories.
- [ ] One limitation on the slide.

## Optional challenge

Section 6 of the notebook: something is wrong with the ESA cleanroom dataset. Find out what, and estimate how
large the error would have been if you had used it.

Section 7 of the notebook: test your result as shown in the lecture - a tornado chart (which assumption moves the
result most: a choice or a data uncertainty?) and the mission lifetime as a parameter (is a longer mission better
or worse? it depends on the functional unit).
