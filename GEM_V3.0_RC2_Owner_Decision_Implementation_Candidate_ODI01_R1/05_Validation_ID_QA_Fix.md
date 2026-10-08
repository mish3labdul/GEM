# 05 · Validation-ID QA Fix (ODI01 defect 1)

**Result: fixed.** Cross-document QA item 15 now passes; the suite is **20/20 PASS, 0 FAIL**.

## The defect
In ODI01, item 15 gathered every `VAL-nn` found anywhere in the package documents into one set and required one number to be absent. That number is VAL-18, which is **intentionally unallocated**. This follows the Register convention; the audit finding that called it "missing" was rejected. The package documents correctly say so, and the report that quotes the check's own evidence also names it. The checker therefore failed on the explanation of the rule, not on a violation of it.

## The rule now implemented (`17_scripts/validation_id_checker.py`)
- Allocated IDs are VAL-01 to VAL-21 except VAL-18. Any other number is an **unknown ID** and fails.
- VAL-18 is not created and no surrounding ID is renumbered.
- Each sentence that names the unallocated ID is classified:
  - **EXPLANATORY**: states that the ID is unallocated, not allocated, absent, a numbering gap or not used. **Allowed.**
  - **ACTIVE**: gives it an owner, a status, an evidence requirement, a dependency, a closure or release condition, an approval record, an implementation gate or a pass/fail state. **Fails.**
  - **UNCLASSIFIED**: neither of the above. **Fails** (conservative).
- Negated phrases such as "carries no owner" are removed before the active test, but only inside a sentence that is already explanatory, so "unallocated but must close" still fails.
- It is a structured per-sentence rule, not a substring exception for one report.

## Regression tests
`18_qa_evidence/validation_id_checker_tests.json` holds 15 positive and 15 negative cases, including every case required by the brief. Results (`validation_id_checker_test_results.json`): **30/30 PASS**. Re-run with `python3 17_scripts/run_validation_id_tests.py <fixture> <results>`.

## What the QA item reports now
The package documents, and the Part D candidate prose, are scanned. The item passes only if there are no active or unknown-ID findings and the package documents the unallocated ID. It also confirms that VAL-05, 07, 08, 13, 15 and 20 are listed open in `14` and that no line closes them. Explanatory mentions are counted in the evidence string of item 15 in `12`.

## What did not change
VAL-18 stays unallocated. No validation gate was added, closed or renumbered. VAL-07, VAL-08 and VAL-15 remain open.
