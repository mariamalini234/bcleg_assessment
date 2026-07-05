# Ethics Memo — to the Director

# **MEMORANDUM**

**TO:** Director, Information Technology Department

**FROM:** Senior Data Strategist

**DATE:** July 5, 2026

**SUBJECT:** Privacy and Ethical Risk Assessment: M365 Copilot Pre-Deployment Scan

---

### **1. Executive Summary**

As the Legislative Assembly prepares for the Microsoft 365 Copilot rollout, a rigorous verification of the initial content scan was conducted. Based on empirical evidence from `BCLeg_datafiles_updated.xlsx`, several core assumptions provided by internal teams are factually incorrect or present extreme compliance liabilities. This memo corrects these data discrepancies, outlines our statutory obligations under the *Freedom of Information and Protection of Privacy Act* (FOIPPA), and provides an ethical review of the requested user surveillance strategy.

### **2. Empirical Verification of Internal Claims**

A data audit conducted via `BCLeg_datafiles_updated.xlsx` reveals significant discrepancies from the initial project brief (`2026.LABC.ITD.SR.DATA.STRATEGIST.ASSIGNMENT.pdf`):

* **Licensing & Copilot Eligibility:**
* *Claim:* All 900 staff are uniformly licensed and Copilot-eligible.
* *Fact:* Licensing is highly fragmented. `BCLeg_datafiles_updated.xlsx` confirms that 3 active personnel are on legacy E5 tiers, 3 automated service accounts are on active paid E3 tiers, and 3 disabled accounts are inappropriately flagged as eligible for E7 migration.

* **Social Insurance Number (SIN) Exposure:**
* *Claim:* An early read of the scan suggests 847 files contain SINs.
* *Fact:* There are exactly **448 verified files** containing SIN data. While lower than the initial claim, these files represent a concentrated privacy vector that must be isolated before Copilot indexes the environment.

* **Classification Framework Alignment:**
* *Claim:* Corporate requested classification under the BC Government Protected A / B / C scheme.
* *Fact:* Per `2026.LABC.ITD.SR.DATA.STRATEGIST.ASSIGNMENT.pdf`, our configuration must strictly follow the Assembly's own four-tier framework detailed in `INFORMATION_PROTECTION.pptx`. Adopting provincial government schemes would break existing institutional taxonomy and invalidate current auto-labelling logic.
---

### **3. Legislative Compliance (FOIPPA)**

Under British Columbia's FOIPPA framework, the Assembly is legally required to implement reasonable security arrangements against unauthorized access, collection, or disclosure of personal information.

Because M365 Copilot utilizes semantic search to surface information based on user permissions, a lack of strict data boundaries creates an immediate "permission creep" risk. To satisfy FOIPPA compliance, the Assembly **cannot use provincial classification schemes**; instead, we must deploy the internal sensitivity labels to auto-classify and restrict the 448 exposed SIN files and high-volume PII repositories from the Copilot LLM indexing scope prior to go-live.

---

### **4. Ethical Review of User Surveillance Request**

The directive to generate a "top 10 list" of individuals handling the most personal and HR content to conduct targeted behavioral interventions presents severe ethical and statutory violations:

* **Technical Imprecision:** HR content within our SharePoint infrastructure is managed collaboratively by functional teams and shared groups. Isolating and ranking individual users based on volume is technically impossible and methodologically flawed.
* **Policy & Statutory Violations:** Generating a targeted employee tracking list without explicit corporate policy coverage violates workplace ethics and fair monitoring principles. Furthermore, tracking individuals based on their authorized access to legally protected privacy records constitutes a secondary use of personal data that violates FOIPPA surveillance guardrails.
* **Alternative Remediation:** Rather than an invasive, individualized watchlist, ITD should implement a systemic, non-identifiable monitoring dashboard focused on *repository security status* paired with mandatory, assembly-wide privacy habits training.

---

### **5. Actionable Recommendations**

1. **Remediate Licensing Deficiencies:** Clean up the 3 legacy E5 accounts, isolate the 3 active E3 automated service accounts, and revoke E7 migration flags from the 3 disabled accounts found in `license_assignments.csv`.

2. **Enforce Assembly-Specific Auto-Labelling:** Reject the BC Government Protected A/B/C scheme. Map all content strictly to the four-tier framework within `INFORMATION_PROTECTION.pptx` to auto-label the 448 verified SIN files.

3. **Cancel Individual Surveillance:** Deny the request for the top 10 individual watchlist to maintain alignment with workplace ethics policy and FOIPPA boundaries. Focus instead on fixing the open anonymous sharing links on high-risk repositories.


## **6. Strategic Briefing: High-Risk Sites**

### **1. Site S-022 ("Old Records" / Unclassified Legacy Archive)**

* **The Profile:** A massive, stale repository containing 28,900 files owned by `records@leg.bc.ca` that has not been modified or audited in over 11 years (last modified Dec 30, 2014).
* **The Risk:** It contains a massive, concentrated footprint of **3,300 active PII bundle matches** left completely unlabelled and completely unprotected with **active open anonymous sharing links**. Copilot will instantly index this "dark data" and surface historical employee records, home addresses, or casework to unauthorized users.

### **2. Site S-099 ("Unmapped Legacy Export")**

* **The Profile:** A poorly structured, loose administrative database displaying significant data pipeline anomalies.
* **The Risk:** It contains high-risk, loose **Social Insurance Number (SIN)** records with entirely missing structural metadata. Furthermore, a data corruption issue exists where numerical match metrics were entered as text strings (`match_count = "many"`), causing schema validation failures that blind automated security controls from detecting the true scale of the exposure.

### **3. Site S-101 ("Orphaned Scan Record")**

* **The Profile:** An unmapped repository characterized by "orphaned" scan data and completely missing numeric metrics.
* **The Risk:** This site represents a total governance blind spot. It holds unquantified PII bundles that are completely invisible to standard inventory metrics but fully scannable by Copilot’s LLM. Turning on Copilot creates a severe hidden exposure vector that circumvents standard administrative oversight.

---

## **7. Top 3 Immediate Critical Vulnerabilities (Emergency Patches)**

To prevent severe security breaches, a statutory compliance failure, or a constitutional crisis, these three vulnerabilities must be hard-blocked before Copilot go-live:

| Priority & Vulnerability | Affected Asset / Context | Copilot Blast Radius Risk | Immediate Patch / Mitigation Action |
| --- | --- | --- | --- |
| **1. Credential Leak** *(Security)* | **Site S-009**  <br>

<br>*(IT Security Runbooks)*<br> | **Systemic Network Compromise:** Active plain-text admin API keys, secrets, and database connection strings are exposed. Staff could use Copilot prompts to effortlessly extract these credentials, enabling lateral network attacks.

 | **Emergency Patch:** Immediately purge plain-text secrets from runbooks. Move credentials into an encrypted vault and explicitly exclude Site S-009 from the Copilot index. |
| **2. Massive Unprotected PII Spillage** *(Privacy)* | **Site S-022** <br>

<br>*(Unclassified Legacy Archive)*<br> | **Catastrophic Identity Theft / FOIPPA Breach:** A high-density footprint of 3,300 active PII bundles is exposed via active anonymous sharing links without sensitivity labels. Copilot will leak personal staff data to unauthorized users.

 | **Emergency Patch:** Broad-scale mitigation. Revoke all active anonymous and external sharing links on S-022. Apply an immediate "Restricted" label to isolate the repository from Copilot indexing.

 |
| **3. Legislative Privilege & Legal Exposure** *(Legal)* | **Site S-006** <br>

<br>*(Legal Opinions Library)*<br> | **Loss of Constitutional Immunities:** A highly sensitive parliamentary legal opinion database is exposed via active anonymous external sharing links. Copilot indexing this risks waiving solicitor-client and Legislative Privilege.

 | **Emergency Patch:** Instantly disable all external and anonymous links on S-006. Enforce a "Restricted - Legal" sensitivity tag to guarantee total compartmentalization. |