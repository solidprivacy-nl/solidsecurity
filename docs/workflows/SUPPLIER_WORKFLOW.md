# SolidSecurity Supplier Workflow V1

## Objective

Help small suppliers demonstrate security/compliance to regulated or demanding customers without rebuilding the same answer set for every questionnaire or tender.

## Product concept

**Security & Compliance Passport**

A maintained, evidence-linked dossier of approved facts and control claims that can be reused across customer assurance requests.

## Passport domains

- organization and security ownership;
- certifications/assurance status;
- identity/access/MFA;
- encryption/data handling;
- vulnerability/patch management;
- secure development where relevant;
- backups/continuity;
- incident response;
- privacy/processor/subprocessor information;
- supplier dependencies;
- employee screening/awareness where relevant;
- AI governance/use;
- penetration-test/audit metadata where available;
- relevant NIS2/Cbw supply-chain controls.

## Questionnaire workflow

1. Customer uploads questionnaire/request.
2. AI classifies each question to SolidSecurity controls/facts.
3. System retrieves only approved current answers/evidence.
4. Questions are assigned one of:
   - `ANSWER_REUSED`;
   - `ANSWER_DRAFTED_FROM_APPROVED_EVIDENCE`;
   - `CLIENT_CONFIRMATION_REQUIRED`;
   - `PROFESSIONAL_REVIEW_REQUIRED`;
   - `NEW_GAP`.
5. Client/professional reviews required items.
6. Final response pack is generated with evidence references and validity dates.
7. New reusable facts/answers are versioned only after approval.

## Trust rule

AI must not invent missing controls or evidence to complete a questionnaire. Missing evidence becomes an explicit gap/action.

## Commercial value metrics

Track:

- percentage of questions answered from approved reusable facts;
- professional minutes per questionnaire;
- time-to-response;
- new gaps discovered;
- evidence expiration rate;
- customer/tender outcomes where available.
