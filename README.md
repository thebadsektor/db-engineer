# 🔗 Legacy PostgreSQL Foreign Key Recovery

This project aims to reconstruct missing foreign key relationships in a legacy PostgreSQL database using a list of candidate column pairs. These candidates were inferred based on column name patterns and data types across tables.

## 📁 Files

- `fk_candidates.csv` — A CSV list of 4,460 potential foreign key relationships. Each row represents a candidate pair of columns that might form a foreign key.

### CSV Format:

| referencing_table | referencing_column | referenced_table | referenced_column |
|-------------------|--------------------|------------------|-------------------|
| orders            | customer_id        | customers        | customer_id       |
| invoices          | order_id           | orders           | order_id          |
| ...               | ...                | ...              | ...               |

## 🎯 Objective

**Validate and re-establish true foreign key relationships** using data overlap between column pairs.

### Tasks for Jules:

1. **Loop through the rows in `fk_candidates.csv`.**
2. For each row, connect to the PostgreSQL database and:
   - Check if the referencing table contains values that exist in the referenced table.
   - Use a query like:

     ```sql
     SELECT COUNT(*) AS matched
     FROM {referencing_table} r
     JOIN {referenced_table} t ON r.{referencing_column} = t.{referenced_column};
     ```

   - Collect the number of matched records and total referencing rows.
3. If matched count is ≥ 90% of non-null referencing rows:
   - Generate a PostgreSQL `ALTER TABLE` SQL statement to add the foreign key.
   - Use `NOT VALID` if needed to skip immediate validation.
   - Output each generated SQL to `suggested_constraints.sql`.

4. Create a summary report:
   - Columns: candidate status (valid/invalid), confidence score, SQL preview.

## 🛠 Output

- `suggested_constraints.sql` — Safe FK constraints to apply to the DB.
- `validation_report.csv` — FK candidates with validation results and confidence score.

## 🔐 Connection

Database credentials should be configured securely via environment variables or `.env` (not included in this repo).

## ✅ Notes

- Tables may contain dirty or orphaned records — use `NOT VALID` to defer constraint checks if needed.
- This project is meant for use with **Jules by Google** or other agentic coders capable of running SQL + file output tasks.

## 📬 Prompt

---
Use the list of candidate foreign key relationships in fk_candidates.csv. For each row, validate if the referencing column values exist in the referenced table. If ≥90% match, generate a safe ALTER TABLE SQL constraint and write it to suggested_constraints.sql.
---
