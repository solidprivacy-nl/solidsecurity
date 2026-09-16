# SolidSecurity Synthetic Assurance Kernel Dossier

Source: `model/assurance_kernel_v1.yaml`
As-of: 2026-09-02
Customer-facing: no; synthetic validation only.

## Coverage

| Requirement | Applicability | Coverage | Current result | Controls | Assurance state |
| --- | --- | --- | --- | --- | --- |
| REQ-ACCESS-LIFECYCLE | APP-ACCESS@SCOPE-SYNTH-CARE:APPLICABLE | FULL | SATISFACTORY | SS-ACCESS-002, SS-SUP-002 | VERIFIED |
| REQ-ORPHAN-MONITORING | APP-ORPHAN@SCOPE-SYNTH-CARE:APPLICABLE | GAP | none | none | GAP |
| REQ-RECOVERY-TEST | APP-RECOVERY@SCOPE-SYNTH-CARE:APPLICABLE | FULL | SATISFACTORY | SS-RES-001 | VERIFIED |
| REQ-SUPPLIER-GOV | APP-SUPPLIER@SCOPE-SYNTH-CARE:APPLICABLE | PARTIAL | PARTIAL | SS-SUP-002 | BLOCKED_CONFLICT |

## Current trace paths

- `REQ-ACCESS-LIFECYCLE -> SS-ACCESS-002 -> IMP-ACCESS -> [EVID-ACCESS-RECERT,EVID-GOV-REVIEW] -> ASM-ACCESS[result=SATISFACTORY,proposal=EVIDENCED] -> REV-ACCESS[R2] -> DEC-ACCESS[VERIFIED]`
- `REQ-ACCESS-LIFECYCLE -> SS-SUP-002 -> IMP-SUPPLIER -> [EVID-GOV-REVIEW] -> ASM-ACCESS-SUPPLIER[result=SATISFACTORY,proposal=EVIDENCED] -> REV-ACCESS-SUPPLIER[R2] -> DEC-ACCESS-SUPPLIER[VERIFIED]`
- `REQ-RECOVERY-TEST -> SS-RES-001 -> IMP-RECOVERY -> [EVID-RECOVERY-FRESH] -> ASM-RECOVERY-V2[result=SATISFACTORY,proposal=EVIDENCED] -> REV-RECOVERY-V2[R2] -> DEC-RECOVERY-V2[VERIFIED]`
- `REQ-SUPPLIER-GOV -> SS-SUP-002 -> IMP-SUPPLIER -> [EVID-GOV-REVIEW,EVID-SUPPLIER-ATTESTATION] -> ASM-SUPPLIER[result=PARTIAL,proposal=IMPLEMENTED] -> none -> none`

## Kernel demonstrations

- Multi-control obligation: `REQ-ACCESS-LIFECYCLE` -> `SS-ACCESS-002`, `SS-SUP-002`
- Shared control reuse: `SS-SUP-002` -> `REQ-ACCESS-LIFECYCLE`, `REQ-SUPPLIER-GOV`
- Shared evidence reuse: `EVID-GOV-REVIEW` is linked to and used by multiple assessment paths
- Orphan requirements: `REQ-ORPHAN-MONITORING`
- Orphan controls: `SS-MON-001`
- Open conflict blocks promotion: `CONFLICT-SUPPLIER-01`
- Historical reopened assessment retained but not treated as current: `ASM-RECOVERY-V1`
- Current recovery assessment: `ASM-RECOVERY-V2` -> human review -> `VERIFIED` decision
- Assessment proposals stop at `EVIDENCED`; only the attributable human decision performs `VERIFIED` promotion.
- Canonical unresolved applicability statuses are accepted by the validator but cannot enter downstream assurance until `APPLICABLE`.

This dossier is synthetic validation evidence. It is not a legal/compliance verdict, customer-facing VERIFIED claim, certification, independent assurance statement, or real-client assessment.
