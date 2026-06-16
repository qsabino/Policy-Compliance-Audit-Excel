import pandas as pd


# Load Data

expected_clauses = pd.read_csv(
    "data/expected_clauses.csv"
)

publishing_loads = pd.read_csv(
    "data/publishing_loads.csv"
)

clause_library = pd.read_csv(
    "data/clause_library.csv"
)

publishing_loads["Load_Date"] = pd.to_datetime(
    publishing_loads["Load_Date"]
)

clause_library["Expiration_Date"] = pd.to_datetime(
    clause_library["Expiration_Date"]
)


# Audit 1: Unexpected Clause Loaded
# BQ: Did we load clauses that were not required for the policy?

unexpected_clause_loaded = publishing_loads.merge(
    expected_clauses[["Policy_ID", "Clause_ID"]],
    on=["Policy_ID", "Clause_ID"],
    how="left",
    indicator=True
)

unexpected_clause_loaded = unexpected_clause_loaded[
    unexpected_clause_loaded["_merge"] == "left_only"
]

print("\nUnexpected Clause Loaded Shape: ")
print(unexpected_clause_loaded.shape)

unexpected_clause_loaded.to_csv(
    "output/unexpected_clause_loaded.csv",
    index=False
)

print("\nUnexpected Clause Loaded Saved")


# Audit 2: Wrong State Clause
# BQ: Was the loaded clause approved for the policy state?

wrong_state_clause = publishing_loads.merge(
    clause_library[["Clause_ID", "State"]]
    .rename(
        columns={"State": "Clause_State"}
    ),
    on="Clause_ID",
    how="left"
)

wrong_state_clause = wrong_state_clause[
    wrong_state_clause["State"]
    !=
    wrong_state_clause["Clause_State"]
]

print("\n Wrong State Clause Shape:")
print(wrong_state_clause.shape)

wrong_state_clause.to_csv(
    "output/wrong_state_clause.csv",
    index=False
)

print("\n Wrong State Clause Saved:")


# Audit 3: Invalid Product Mapping
# BQ: Was the loaded clause approved for the policy product?

invalid_product_mapping = publishing_loads.merge(
    clause_library[["Clause_ID", "Product"]]
    .rename(
        columns={"Product": "Clause_Product"}
    ),
    on="Clause_ID",
    how="left"
)

invalid_product_mapping = invalid_product_mapping[
    invalid_product_mapping["Product"]
    !=
    invalid_product_mapping["Clause_Product"]
]

print("\nInvalid Product Mapping Shape:")
print(invalid_product_mapping.shape)

invalid_product_mapping.to_csv(
    "output/invalid_product_mapping.csv",
    index=False
)

print("\nInvalid Product Mapping Saved")


# Audit 4: Expired Clause
# BQ: Was the clause expired when loaded?

expired_clause = publishing_loads.merge(
    clause_library[["Clause_ID", "Expiration_Date"]],
    on="Clause_ID",
    how="left"
)

expired_clause = expired_clause[
    expired_clause["Load_Date"]
    >
    expired_clause["Expiration_Date"]
]

print("\nExpired Clause Shape:")
print(expired_clause.shape)

expired_clause.to_csv(
    "output/expired_clause.csv",
    index=False
)

print("\nExpired Clause Saved")


# Audit Summary Table

audit_summary = pd.DataFrame({

    "Audit": [
        "Unexpected Clause Loaded",
        "Wrong State Clause",
        "Invalid Product Mapping",
        "Expired Clause"
    ],

    "Findings": [
        len(unexpected_clause_loaded),
        len(wrong_state_clause),
        len(invalid_product_mapping),
        len(expired_clause)
    ]
})

print("\nAudit Summary")
print(audit_summary)

audit_summary.to_csv(
    "output/audit_summary2.csv",
    index=False
)

print("Audit Summary 2 Saved")