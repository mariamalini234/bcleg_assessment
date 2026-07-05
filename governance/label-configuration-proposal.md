# Label Configuration Proposal

# Instructions
> Map the scanned content to the four labels (Public / Internal / Confidential / Restricted)
> and the eight descriptors. Propose auto-labelling rules and Copilot scoping for go-live.
> Ground each choice in the provided deck.


## Kindly Note: 
The provided output file named 'BCLeg_datafiles_updated.xlsx' has the scanned sites marked with respective labels and descriptors.

## Label mapping

Based on the multi-layered analysis of the Assembly's 24 operational repositories, the scanned content is mapped across the four official parent classifications and eight descriptor profiles to enforce clear boundaries at go-live:

Public (3 Sites): Applied to finalized, external-facing content where disclosure causes No Harm.

Mapped Descriptors: None.

Internal (5 Sites): Applied to standard operational data where disclosure causes Minimal Harm.

Mapped Descriptors: None.

Confidential (9 Sites): Applied to sensitive operational and asset layers where disclosure causes Serious Harm.

Mapped Descriptors: People (HR/Personnel), Commercial (Vendors/Contracts), Financials (Pre-publish financial documents), Audit (Findings/Incident reports), and Security (Internal source code).

Restricted (7 Sites): Applied to high-consequence data vectors where disclosure causes Extremely Grave Harm.

Mapped Descriptors: Proceedings (Closed-door committee/In-camera briefs), Legal (Privileged opinions), Financials (Draft budgets/Audits before finalization), and Security (Incident response details).

## Auto-labelling rules

To eliminate administrative blind spots, the automated policy engine evaluates repository text patterns and security scan telemetry simultaneously using a strict, top-down priority hierarchy:

Rule 1: Restricted Tier (Extremely Grave Harm Vector)
Text Trigger Criteria: Site name, folder paths, or document metadata contain: closed-door, closed session, leadership briefing, confidential minutes, reorganization, compensation, incident response, privileged legal, legal opinions, draft report, or draft budget.

Scanner Telemetry Criteria: Matches privileged_keyword, apikey_secret, security_sensitive, or reorg.

Action: Programmatically assign Restricted parent label and attach the corresponding contextual descriptor.

Rule 2: Confidential Tier (Serious Harm Vector)
Text Trigger Criteria: If Rule 1 passes, look for: hr, hr records, personnel, vendor, contract, negotiat*, draft policy, operational, financial, expense, audit, review, or built systems.

Scanner Telemetry Criteria: Matches sin, pii_bundle, creditcard, budgetpattern, or audit_finding.

Action: Programmatically assign Confidential parent label, attach the specific sub-descriptor, and inject the mandatory visual modifications (e.g., "Assembly Confidential" Watermark and Header/Footer differentiators).

Rule 3: Public Verification (No Harm Vector)
Text Trigger Criteria: If preceding rules pass, look for explicit markers: public website, media releases approved, job postings, hansard, or press.

Action: Programmatically assign Public parent label.

Rule 4: Standard Internal Fallback
Criteria: Any active asset that remains clean, unvetted, or fails to trigger the rules above.

Action: Programmatically assign Internal parent label. If has_anonymous_links is flagged as Yes, automatically trigger a high-priority Access Control List (ACL) remediation ticket to revoke the link.

## Copilot and agent scoping

At go-live, data visibility within the Microsoft 365 Copilot semantic index and any custom retrieval-augmented agents is dictated entirely by these automated taxonomy boundaries:

Public Ingestion State (Fully Included): Broadly indexed and accessible to all users. Copilot can freely synthesize, query, and surface this data across any enterprise prompt.

Internal Ingestion State (Authorized Access Only): Ingested into the tenant index, but strictly bounded by account-specific permissions. Users can only surface these files via Copilot if they have direct, verified read access on the asset's corrected Access Control List (ACL). All open anonymous links are severed to crush the baseline blast radius.

Confidential Ingestion State (Authorized Access Only + Label Inheritance): Fully ingested under tight ACL constraints. Crucially, when Copilot generates an answer or synthesizes an agent brief using these sources, the downstream AI output automatically inherits the Confidential security label, and auto-applied persistent visual watermarking.

Restricted Ingestion State (Excluded Entirely): Completely blocked and isolated from the Copilot semantic index pipeline. Even if an executive user has full administrative rights to a closed-door proceeding file, Copilot cannot read, parse, or surface the content, entirely eliminating the risk of data leakage via prompt engineering.

## Sample-document labels
| Document | Label | Descriptor | Reason |
|---|---|---|---|
| leadership_pack_draft.txt | Restricted | People, Proceedings, Financials, Audit | This is a highly restricted document with minimal audience and DO NOT FORWARD clause. Releasing by mistake would cause extremely grave consequences.|
| procurement_card_review.txt | Confidential | People, Commercial, Financials | This document is a draft internal audit document and not yet shared with concerned teams/individuals. Releasing by mistake would cause Serious Harm.|
| media_release_approved.txt | Public | None | This is an Approved Public Media Release memo by Communications Office. Releasing by mistake would not cause any harm. |

