# -*- coding: utf-8 -*-
"""bcleg_src.ipynb
# Optional Env Set-up



"""**Step 1: Data load and Visualize:**"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. SETUP ENVIRONMENT AND VERBATIM FILE PATHS
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 14})

path = "./data/" # path of your datafiles

# 1. Load the raw, unedited CSV files
site_inventory = pd.read_csv(os.path.join(path, 'site_inventory.csv'))
pii_detections = pd.read_csv(os.path.join(path, 'pii_detections.csv'))
sharing_links = pd.read_csv(os.path.join(path, 'sharing_links.csv'))
license_assignments = pd.read_csv(os.path.join(path, 'license_assignments.csv'))


# 2. Prep the raw data specifically for Viz 1 (Initial State)
# We fill the blank rows with 'Unclassified' so they show up on our chart
site_inventory['current_label_viz'] = site_inventory['current_label'].fillna('Unclassified')

# 3. Plot Viz 1: The messy, uncleaned baseline
plt.figure(figsize=(10, 5))
order = site_inventory['current_label_viz'].value_counts().index
sns.countplot(data=site_inventory, y='current_label_viz', palette='flare', order=order)
plt.title("Viz 1: Initial Legacy Label State (Before Clean-up)")
plt.xlabel("Number of SharePoint Sites")
plt.ylabel("Legacy Label Name")
plt.tight_layout()
plt.show()

"""**Step 2: Data Clean-up and Visualize:**"""

# Drop the explicit duplicate pass row
pii_clean = pii_detections[pii_detections['sample_context'] != 'duplicate scan pass'].copy()

# Replace 'many' text with a standard high-weight number, then force numeric conversion
pii_clean['match_count'] = pii_clean['match_count'].replace('many', 500)
pii_clean['match_count'] = pd.to_numeric(pii_clean['match_count']).fillna(0).astype(int)
pii_collapsed = pii_clean.groupby('site_id')['detection_type'].apply(lambda x: ', '.join(x)).reset_index()

# Fix the broken text characters in the site names
site_inventory_clean = site_inventory.copy()
site_inventory_clean['site_name'] = site_inventory_clean['site_name'].str.replace('â€"', '–', regex=False)

# Filter out any rows where the 'site_name' starts with 'TOTAL'
site_inventory_clean = site_inventory_clean[~site_inventory_clean['site_name'].str.startswith('TOTAL', na=True)]

# Map fragmented department shorthand to standardized parent categories
dept_mapping = {
    'IT Dept': 'ITD', 'Infrastructure': 'ITD',
    'hansard svcs': 'Hansard', 'Hansard Broadcast': 'Hansard', 'HBS': 'Hansard',
    'Finance & Ops': 'Finance', 'Member Support': 'Member Services'
}
license_clean = license_assignments.copy()
license_clean['department'] = license_clean['department'].replace(dept_mapping).fillna('Unassigned')

# Re-plot Viz 2 using our newly cleaned, standard dataframes
site_inventory_clean['current_label_viz2'] = site_inventory_clean['current_label'].fillna('Unclassified')

# Define the order for Viz 2 based on the value counts of the cleaned data
order = site_inventory_clean['current_label_viz2'].value_counts().index


plt.figure(figsize=(10, 5))
sns.countplot(data=site_inventory_clean, y='current_label_viz2', palette='flare', order = order)
plt.title("Viz 2: Post Clean-up (Labels Unchanged)")
plt.xlabel("Number of SharePoint Sites")
plt.ylabel("Legacy Label Name")
plt.tight_layout()
plt.show()

"""**Step 3: Checking Copilot Blast Radius:**"""

# Create a clear column defining Copilot's initial reach on the cleaned data

def check_initial_copilot_reach(row):
    label = str(row.get('current_label', '')).strip()
    has_anon = str(row.get('has_anonymous_links', '')).strip().lower() == 'yes'

    # 1. Catch the leaked Restricted asset first
    if "Restricted" in label and has_anon:
        return "Restr-Exposed via Link"

    # 2. Catch the securely isolated Restricted assets
    elif "Restricted" in label:
        return "Restr. & Safe"

    # 3. Catch open legacy/unlabelled assets that are leaking via anonymous links
    elif has_anon:
        return "Exposed via Link"

    # 4. Default baseline for standard open legacy assets
    else:
        return "Ingested by Copilot"

# Apply this rule to create our tracking column
site_inventory_clean['copilot_reach'] = site_inventory_clean.apply(check_initial_copilot_reach, axis=1)


# Group by the Copilot reach tier and calculate BOTH count of sites and sum of items
reach_summary = site_inventory_clean.groupby('copilot_reach').agg(
    total_sites=('site_id', 'count'),
    total_items=('item_count', 'sum'),
    site_ids=('site_id', lambda x: list(x))
).reset_index()

# Order the summary for plotting based on total_items in descending order
reach_summary_ordered = reach_summary.sort_values('total_items', ascending=False)

# View the raw aggregated dataframe to verify accuracy
print(reach_summary)

# Create a figure with 2 distinct subplots side-by-side
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Define a custom color palette for risk levels
# darkred for highest risk, then red, orange, green for lowest risk
custom_palette = {'Exposed via Link': 'darkred',
                  'Restr-Exposed via Link': 'red',
                  'Restr. & Safe': 'orange',
                  'Ingested by Copilot': 'green'}

# --- CHART 1: LEFT SUBPLOT (Total Number of Sites Affected) ---
ax1 = sns.barplot(data=reach_summary_ordered, x='copilot_reach', y='total_sites',
                   palette=custom_palette, ax=axes[0],
                   order=reach_summary_ordered['copilot_reach'])
axes[0].set_title("1. Operational Risk: Affected SharePoint Sites", weight='bold', pad=15)
axes[0].set_xlabel("Copilot Accessibility Boundary")
axes[0].set_ylabel("Count of Unique Sites")

# Add precise integer count labels above left bars
for p in ax1.patches:
    ax1.annotate(f"{int(p.get_height())} Sites", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 8), textcoords='offset points', weight='bold')


# --- CHART 2: RIGHT SUBPLOT (Total Number of Files Exposed) ---
ax2 = sns.barplot(data=reach_summary_ordered, x='copilot_reach', y='total_items',
                   palette=custom_palette, ax=axes[1],
                   order=reach_summary_ordered['copilot_reach'])
axes[1].set_title("2. Data Payload Risk: Total Exposed File Volume", weight='bold', pad=15)
axes[1].set_xlabel("Copilot Accessibility Boundary")
axes[1].set_ylabel("Sum of Exposed Items")

# Add precise formatted item labels above right bars
for p in ax2.patches:
    ax2.annotate(f"{int(p.get_height()):,} Files", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 8), textcoords='offset points', weight='bold')

plt.tight_layout()
plt.show()

"""**Step 4: Correcting Labels as per 'INFORMATION_PROTECTION.pptx' guidelines:**"""

import pandas as pd

def apply_labc_information_protection_policy(row):
    """
    Programmatic logic function that scans site attributes line-by-line
    and maps them to the official LABC Information Protection taxonomy.
    """
    # 1. Standardize string parameters to lower-case to avoid any case-sensitivity bugs
    site_name = str(row.get('site_name', '')).lower()
    current_label = str(row.get('current_label', '')).lower()
    detection_type = str(row.get('detection_type', '')).lower()
    has_anon_links = str(row.get('has_anonymous_links', '')).strip().lower() == 'yes'

    # =========================================================================
    # PHASE 1: THE RESTRICTED SCREEN (Extremely Grave Harm Vector)
    # =========================================================================
    # Check slide text triggers or specific technical scan patterns first
    is_restricted = (
        'closed-door' in site_name or
        'closed session' in site_name or
        'leadership briefing' in site_name or
        'confidential minutes' in site_name or
        'reorganization' in site_name or
        'compensation' in site_name or
        'incident response' in site_name or
        'privileged legal' in site_name or
        'legal opinions' in site_name or
        'draft report' in site_name or
        'draft budget' in site_name or
        'privileged_keyword' in detection_type or
        'apikey_secret' in detection_type or
        'security_sensitive' in detection_type or
        'reorg' in detection_type or
        'reorg' in site_name
    )

    if is_restricted:
        # Dynamically calculate the matching descriptor from the slide definitions
        if 'leadership' in site_name or 'briefing' in site_name:
            descriptor = 'Proceedings'
        elif 'legal' in site_name or 'opinion' in site_name or 'privileged' in detection_type:
            descriptor = 'Legal'
        elif 'incident' in site_name or 'security' in site_name or 'apikey' in detection_type:
            descriptor = 'Security'
        elif 'financial' in site_name or 'expense' in site_name or 'budgetpattern' in detection_type:
            descriptor = 'Financial'
        else:
            descriptor = 'Proceedings'

        # Grounded Rule: Restricted content is completely hidden from Copilot's index
        return pd.Series({
            'Target_Parent_Label': 'Restricted',
            'Target_Descriptor': descriptor,
            'Target_Copilot_Scoping': 'Excluded Entirely from Copilot Index'
        })

    # =========================================================================
    # PHASE 2: THE CONFIDENTIAL SCREEN (Serious Harm Vector)
    # =========================================================================
    # Check our newly added slide triggers or the remaining PII scan markers
    is_confidential = (
        'hr' in site_name or
        'personnel' in site_name or
        'vendor' in site_name or
        'contract' in site_name or
        'negotiat' in site_name or
        'draft policy' in site_name or
        'operational' in site_name or
        'financial' in site_name or
        'expense' in site_name or
        'source code' in site_name or
        'built systems' in site_name or
        'audit' in site_name or
        'review' in site_name or
        'sin' in detection_type or
        'pii_bundle' in detection_type or
        'creditcard' in detection_type or
        'budgetpattern' in detection_type or
        'audit_finding' in detection_type or
        'network' in site_name
    )

    if is_confidential:
        # Dynamically assign descriptor categories strictly according to page 7 & 10
        if 'hr' in site_name or 'personnel' in site_name or 'sin' in detection_type or 'pii_bundle' in detection_type or 'creditcard' in detection_type:
            descriptor = 'People'
        elif 'vendor' in site_name or 'contract' in site_name or 'negotiat' in site_name or 'procurement' in site_name:
            descriptor = 'Commercial'
        elif 'financial' in site_name or 'expense' in site_name or 'budgetpattern' in detection_type:
            descriptor = 'Financial'
        elif 'audit' in site_name or 'review' in site_name or 'audit_finding' in detection_type:
            descriptor = 'Audit'
        elif 'source code' in site_name or 'built systems' in site_name or 'network' in site_name:
            descriptor = 'Security'
        elif 'constituency' in site_name:
            descriptor = 'Member Support'
        else:
            descriptor = 'People'

        # Grounded Rule: Confidential content allows access, but AI responses inherit the label
        return pd.Series({
            'Target_Parent_Label': 'Confidential',
            'Target_Descriptor': descriptor,
            'Target_Copilot_Scoping': 'Authorized Access Only (ACL Restructured)'
        })

    # =========================================================================
    # PHASE 3: THE PUBLIC VERIFICATION (No Harm Vector)
    # =========================================================================
    # Check explicit public web / press content channels
    is_public = (
        'public' in current_label or
        'media releases' in site_name or
        'approved' in site_name or
        'job postings' in site_name
    )

    if is_public:
        return pd.Series({
            'Target_Parent_Label': 'Public',
            'Target_Descriptor': 'None',
            'Target_Copilot_Scoping': 'Fully Included',
        })

    # =========================================================================
    # PHASE 4: THE DEFAULT FALLBACK TIER (Mandated by PPTX)
    # =========================================================================
    # Default to Internal. If it has anonymous links active, flag them for revocation.
    scoping = 'Authorized Access Only (Revoke Links)' if has_anon_links else 'Authorized Access Only'

    return pd.Series({
        'Target_Parent_Label': 'Internal',
        'Target_Descriptor': 'None',
        'Target_Copilot_Scoping': scoping,
    })

# 1. Combine your cleaned site inventory and PII detections using the unique 'site_id' column
# We use a 'left' join so we keep all 25 sites, even if they had zero PII detections.
clean_master_df = pd.merge(site_inventory_clean, pii_collapsed, on='site_id', how='left')

# 2. Run the policy function across your newly created master dataframe
remediation_results = clean_master_df.apply(apply_labc_information_protection_policy, axis=1)

# 3. Join the new labels back to your dataset
final_remediated_df = pd.concat([clean_master_df, remediation_results], axis=1)

# 4. View your results to verify it worked perfectly
final_remediated_df[['site_id', 'site_name', 'Target_Parent_Label', 'Target_Descriptor', 'Target_Copilot_Scoping']].head(30)

output_dir = "./output/" # path of your output files
final_remediated_df.to_csv(f"{output_dir}/final_remediated_df.csv", index=False)
print(f"Updated Labels saved to {output_dir}/final_remediated_df.csv")

"""**Step 5: Visualization for New & Updated Label Classification:**"""

# 1. Apply our updated policy rules
remediation_results = clean_master_df.apply(apply_labc_information_protection_policy, axis=1)
final_remediated_df = pd.concat([clean_master_df, remediation_results], axis=1)

# 2. Define the updated Copilot reach buckets
def calculate_updated_copilot_reach(row):
    label = str(row.get('Target_Parent_Label', '')).strip()
    scoping = str(row.get('Target_Copilot_Scoping', '')).strip()

    if label == "Restricted":
        return "Excluded Entirely from Index"
    elif "Revoke" in scoping or "Authorized" in scoping:
        return "Authorized Access Only"
    elif label == "Public":
        return "Fully Included"
    else:
        return "Authorized Access Only"

final_remediated_df['updated_copilot_reach'] = final_remediated_df.apply(calculate_updated_copilot_reach, axis=1)

# 3. Aggregate by Parent Label to double-check the 3/7/9/5 split
label_distribution = final_remediated_df.groupby('Target_Parent_Label').agg(
    total_sites=('site_id', 'count'),
    total_items=('item_count', 'sum'),
    site_list=('site_id', lambda x: sorted(list(x)))
).reset_index()

print("--- EXPLICIT TAXONOMY MATRIX VERIFICATION ---")
print(label_distribution.to_string(index=False))

print("\n--- GO-LIVE REPOSITORY CLASSIFICATION LISTS ---")
for idx, row in label_distribution.iterrows():
    print(f"{row['Target_Parent_Label']}: {row['total_sites']} Sites")
    print(f"   Actual Sites: {row['site_list']}\n")



    import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================================
# SECTION 1: PREP THE GRAPHING METRICS FROM THE COMPLIANCE LAYER
# =========================================================================
# Ensure the parent labels are ordered cleanly from highest restriction to lowest
label_order = ['Restricted', 'Confidential', 'Internal', 'Public']

# Aggregate by our 4 core taxonomy categories to get clean graphing arrays
viz_target_df = final_remediated_df.groupby('Target_Parent_Label').agg(
    total_sites=('site_id', 'count'),
    total_items=('item_count', 'sum')
).reindex(label_order).reset_index()

# =========================================================================
# SECTION 2: DRAW THE MODERN SIDE-BY-SIDE PLOTS
# =========================================================================
# Set up a clean, high-contrast style for presentation slides
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'font.weight': 'normal'
})

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# --- CHART 1: TARGET OPERATIONAL FOOTPRINT (Unique Sites) ---
ax1 = sns.barplot(
    data=viz_target_df,
    x='Target_Parent_Label',
    y='total_sites',
    hue='Target_Parent_Label',
    palette='Blues_r',      # Professional, secure gradient
    legend=False,
    ax=axes[0],
    order=viz_target_df.sort_values('total_sites', ascending=False)['Target_Parent_Label'] # Order by total_sites descending
)
axes[0].set_title("1. Target Operational State: Repositories per Tier", weight='bold', pad=15)
axes[0].set_xlabel("Information Protection Label")
axes[0].set_ylabel("Count of Unique SharePoint Sites")
axes[0].set_ylim(0, 11)     # Leave room at the top for bar text labels

# Annotate Chart 1 with precise integer counts
for p in ax1.patches:
    height = p.get_height()
    if height > 0:
        ax1.annotate(
            f"{int(height)} Sites",
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='center',
            xytext=(0, 10),
            textcoords='offset points',
            weight='bold',
            color='#2c3e50'
        )

# --- CHART 2: TARGET DATA PROTECTION PAYLOAD (File Counts) ---
ax2 = sns.barplot(
    data=viz_target_df,
    x='Target_Parent_Label',
    y='total_items',
    hue='Target_Parent_Label',
    palette='GnBu_r',     # Secure teal gradient to signal controlled risk
    legend=False,
    ax=axes[1],
    order=viz_target_df.sort_values('total_sites', ascending=False)['Target_Parent_Label'] # Order by total_items descending
)
axes[1].set_title("2. Target Compliance Payload: Protected File Volumes", weight='bold', pad=15)
axes[1].set_xlabel("Information Protection Label")
axes[1].set_ylabel("Sum of Tracked Items")
axes[1].set_ylim(0, viz_target_df['total_items'].max() * 1.15) # Dynamically space text headroom

# Annotate Chart 2 with clean comma-separated values
for p in ax2.patches:
    height = p.get_height()
    if height > 0:
        ax2.annotate(
            f"{int(height):,} Files",
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='center',
            xytext=(0, 10),
            textcoords='offset points',
            weight='bold',
            color='#16a085'
        )

# Polish margins and output to screen
plt.tight_layout()
plt.show()

"""**Step 6: Copilot Radius Blast Visualization:**"""

# Create a crisp grouping of Parent Labels vs their actual Copilot Access States
reach_radius_df = final_remediated_df.groupby(['Target_Parent_Label', 'updated_copilot_reach']).agg(
    total_sites=('site_id', 'count'),
    total_items=('item_count', 'sum')
).reset_index()

# Sort the categories to match our standard restriction order
reach_radius_df['Target_Parent_Label'] = pd.Categorical(
    reach_radius_df['Target_Parent_Label'],
    categories=['Restricted', 'Confidential', 'Internal', 'Public'],
    ordered=True
)
reach_radius_df = reach_radius_df.sort_values('Target_Parent_Label')


plt.figure(figsize=(10, 6))

# Draw the blast radius impact map
ax3 = sns.barplot(
    data=reach_radius_df,
    x='Target_Parent_Label',
    y='total_items',
    hue='updated_copilot_reach',
    palette={'Excluded Entirely from Index': '#c0392b',  # Strict Stop/Red
             'Authorized Access Only': '#2980b9',        # Secure Account/Blue
             'Fully Included': '#27ae60'},               # Safe Open/Green
    ax=None,
    order=reach_radius_df.groupby('Target_Parent_Label')['total_items'].sum().sort_values(ascending=False).index
)

# Customize titles to highlight AI Boundary Governance
plt.title("3. Copilot Indexing Blast Radius per Taxonomy Category", weight='bold', pad=15)
plt.xlabel("LABC Information Protection Label")
plt.ylabel("Volume of Ingested Items")
plt.ylim(0, reach_radius_df['total_items'].max() * 1.15) # Room for text annotations

# Add precise labels to show exactly what action is happening to the files
for p in ax3.patches:
    height = p.get_height()
    if height > 0:
        ax3.annotate(
            f"{int(height):,} Items",
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='center',
            xytext=(0, 10),
            textcoords='offset points',
            weight='bold',
            color='#333333',
            fontsize=9
        )

# Position the legend cleanly so it doesn't overlap data bars
plt.legend(title="Copilot Access Boundary State", loc='upper right', frameon=True)
plt.tight_layout()
plt.show()