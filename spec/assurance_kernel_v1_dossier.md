# SolidSecurity Synthetic Assurance Kernel Dossier

Source: `model/assurance_kernel_v1.yaml`
As-of: 2026-09-02
Data class: synthetic only; no real client data.

## Coverage

| Requirement | Applicability | Coverage | Controls | Assurance state |
| --- | --- | --- | --- | --- |
| REQ-ACCESS-LIFECYCLE | APPLICABLE | FULL | SS-ACCESS-002, SS-SUP-002 | VERIFIED |
| REQ-ORPHAN-MONITORING | APPLICABLE | GAP | none | GAP |
| REQ-RECOVERY-TEST | APPLICABLE | FULL | SS-RES-001 | REOPENED |
| REQ-SUPPLIER-GOV | APPLICABLE | PARTIAL | SS-SUP-002 | BLOCKED_CONFLICT |

## Traceability

- `REQ-ACCESS-LIFECYCLE`: `SRC-SYNTH-ACCESS -> REQ-ACCESS-LIFECYCLE -> SS-ACCESS-002 -> IMP-ACCESS -> EVID-ACCESS-RECERT,EVID-GOV-REVIEW -> ASM-ACCESS -> REV-ACCESS -> DEC-ACCESS -> VERIFIED`
- `REQ-ORPHAN-MONITORING`: `SRC-SYNTH-SUPPLIER -> REQ-ORPHAN-MONITORING -> GAP(no control mapping)`
- `REQ-RECOVERY-TEST`: `SRC-SYNTH-RESILIENCE -> REQ-RECOVERY-TEST -> SS-RES-001 -> IMP-RECOVERY -> EVID-RECOVERY-OLD -> ASM-RECOVERY -> REOPENED`
- `REQ-SUPPLIER-GOV`: `SRC-SYNTH-SUPPLIER -> REQ-SUPPLIER-GOV -> SS-SUP-002 -> IMP-SUPPLIER -> EVID-GOV-REVIEW -> ASM-SUPPLIER -> CONFLICT_DETECTED`

## Kernel demonstrations

- Multi-control obligation: `REQ-ACCESS-LIFECYCLE` -> `SS-ACCESS-002`, `SS-SUP-002`
- Shared control reuse: `SS-SUP-002` -> `REQ-ACCESS-LIFECYCLE`, `REQ-SUPPLIER-GOV`
- Shared evidence reuse: `EVID-GOV-REVIEW` -> `ASM-ACCESS`, `ASM-SUPPLIER`
- Orphan requirements: `REQ-ORPHAN-MONITORING`
- Orphan controls: none
- Evidence conflicts: `ASM-SUPPLIER`
- Reopened after evidence expiry: `ASM-RECOVERY`
- Generated-policy design-only implementations: `IMP-GENERATED-POLICY`

This dossier is synthetic validation evidence. It is not a legal/compliance verdict, certification, independent assurance statement, or real-client assessment.
