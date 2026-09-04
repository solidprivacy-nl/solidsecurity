# SolidSecurity Synthetic Assurance Kernel Dossier

Source: `model/assurance_kernel_v1.yaml`
Canonical control catalog: `model/sample_controls.yaml`
Canonical assessment results: `model/foundation_enums.yaml`
As-of: 2026-09-02
Data class: synthetic only; no real client data.

## Coverage

| Requirement | Applicability decision | Scope | Status | Coverage | Controls | Assurance state |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-ACCESS-LIFECYCLE | APP-ACCESS | SCOPE-SYNTH-CARE | APPLICABLE | FULL | SS-ACCESS-002, SS-SUP-002 | VERIFIED |
| REQ-ORPHAN-MONITORING | APP-ORPHAN | SCOPE-SYNTH-CARE | APPLICABLE | GAP | none | GAP |
| REQ-RECOVERY-TEST | APP-RECOVERY | SCOPE-SYNTH-CARE | APPLICABLE | FULL | SS-RES-001 | REOPENED |
| REQ-SUPPLIER-GOV | APP-SUPPLIER | SCOPE-SYNTH-CARE | APPLICABLE | PARTIAL | SS-SUP-002 | BLOCKED_CONFLICT |

## Traceability

- `REQ-ACCESS-LIFECYCLE`: `SRC-SYNTH-ACCESS -> REQ-ACCESS-LIFECYCLE -> APP-ACCESS@SCOPE-SYNTH-CARE -> SS-ACCESS-002 -> IMP-ACCESS -> EVID-ACCESS-RECERT,EVID-GOV-REVIEW -> ASM-ACCESS -> RESULT=SATISFACTORY -> REV-ACCESS -> DEC-ACCESS -> VERIFIED`
- `REQ-ACCESS-LIFECYCLE`: `SRC-SYNTH-ACCESS -> REQ-ACCESS-LIFECYCLE -> APP-ACCESS@SCOPE-SYNTH-CARE -> SS-SUP-002 -> IMP-SUPPLIER -> EVID-GOV-REVIEW -> ASM-ACCESS-SUPPLIER -> RESULT=SATISFACTORY -> REV-ACCESS-SUPPLIER -> DEC-ACCESS-SUPPLIER -> VERIFIED`
- `REQ-ORPHAN-MONITORING`: `SRC-SYNTH-SUPPLIER -> REQ-ORPHAN-MONITORING -> APP-ORPHAN@SCOPE-SYNTH-CARE -> GAP(no control mapping)`
- `REQ-RECOVERY-TEST`: `SRC-SYNTH-RESILIENCE -> REQ-RECOVERY-TEST -> APP-RECOVERY@SCOPE-SYNTH-CARE -> SS-RES-001 -> IMP-RECOVERY -> EVID-RECOVERY-OLD -> ASM-RECOVERY -> RESULT=PARTIAL -> REOPENED`
- `REQ-SUPPLIER-GOV`: `SRC-SYNTH-SUPPLIER -> REQ-SUPPLIER-GOV -> APP-SUPPLIER@SCOPE-SYNTH-CARE -> SS-SUP-002 -> IMP-SUPPLIER -> EVID-GOV-REVIEW,EVID-SUPPLIER-ATTESTATION -> ASM-SUPPLIER -> RESULT=PARTIAL -> CONFLICT-SUPPLIER-01:OPEN`

## Kernel demonstrations

- Multi-control obligation: `REQ-ACCESS-LIFECYCLE` -> `SS-ACCESS-002`, `SS-SUP-002`
- Shared control reuse: `SS-SUP-002` -> `REQ-ACCESS-LIFECYCLE`, `REQ-SUPPLIER-GOV`
- Shared evidence reuse: `EVID-GOV-REVIEW` -> `ASM-ACCESS`, `ASM-ACCESS-SUPPLIER`, `ASM-SUPPLIER`
- Orphan requirements: `REQ-ORPHAN-MONITORING`
- Orphan controls: `SS-MON-001`
- Open evidence conflicts: `CONFLICT-SUPPLIER-01`
- Reopened after evidence expiry: `ASM-RECOVERY`
- Generated-policy design-only implementations: `IMP-GENERATED-POLICY`

This dossier is synthetic validation evidence. It is not a legal/compliance verdict, certification, independent assurance statement, or real-client assessment.
