-- SolidSecurity M1 PostgreSQL schema contract V1
-- STATUS: DESIGN CONTRACT ONLY. NOT A MIGRATION. DO NOT APPLY TO PRODUCTION.
-- Future migrations may implement this contract only after governed review.

create schema if not exists solidsecurity_contract;

-- Global catalog -------------------------------------------------------------
create table solidsecurity_contract.source (
  source_id uuid primary key,
  title text not null,
  issuer text,
  version text,
  jurisdiction text,
  source_type text not null,
  reference_uri text,
  license_class text,
  verified_at timestamptz
);

create table solidsecurity_contract.framework (
  framework_id uuid primary key,
  source_id uuid references solidsecurity_contract.source(source_id),
  code text not null unique,
  title text not null,
  lifecycle_state text not null
);

create table solidsecurity_contract.requirement (
  requirement_id uuid primary key,
  framework_id uuid not null references solidsecurity_contract.framework(framework_id),
  source_reference text not null,
  summary text not null,
  applicability_rule text,
  effective_date date,
  source_status text not null
);

create table solidsecurity_contract.control (
  control_id text primary key,
  domain text not null,
  title text not null,
  objective text not null,
  lifecycle_state text not null
);

create table solidsecurity_contract.control_assertion (
  assertion_id text primary key,
  control_id text not null references solidsecurity_contract.control(control_id),
  statement text not null,
  materiality text not null,
  lifecycle_state text not null,
  unique(control_id, assertion_id)
);

create table solidsecurity_contract.requirement_control_map (
  mapping_id uuid primary key,
  requirement_id uuid not null references solidsecurity_contract.requirement(requirement_id),
  control_id text not null references solidsecurity_contract.control(control_id),
  relationship text not null,
  coverage text,
  rationale text,
  mapping_status text not null,
  unique(requirement_id, control_id)
);

-- Identity / tenant roots ----------------------------------------------------
create table solidsecurity_contract.user_identity (
  user_id uuid primary key,
  identity_type text not null check (identity_type in ('human','service')),
  auth_provider text not null,
  auth_subject text not null,
  display_name text,
  status text not null,
  created_at timestamptz not null,
  unique(auth_provider, auth_subject)
);

create table solidsecurity_contract.tenant (
  tenant_id uuid primary key,
  name text not null,
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.organization (
  organization_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  legal_name text not null,
  registration_ref text,
  organization_type text,
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.organizational_scope (
  scope_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  organization_id uuid not null references solidsecurity_contract.organization(organization_id),
  name text not null,
  description text,
  scope_type text,
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.membership (
  membership_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  user_id uuid not null references solidsecurity_contract.user_identity(user_id),
  role text not null,
  status text not null,
  created_at timestamptz not null,
  revoked_at timestamptz,
  unique(tenant_id, user_id, role)
);

create table solidsecurity_contract.engagement (
  engagement_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  service_variant text not null,
  status text not null,
  starts_at date,
  ends_at date,
  review_cadence text,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.engagement_scope (
  engagement_scope_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  engagement_id uuid not null references solidsecurity_contract.engagement(engagement_id),
  scope_id uuid not null references solidsecurity_contract.organizational_scope(scope_id),
  unique(engagement_id, scope_id)
);

-- Dossier state --------------------------------------------------------------
create table solidsecurity_contract.applicability_decision (
  applicability_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  scope_id uuid not null references solidsecurity_contract.organizational_scope(scope_id),
  target_type text not null,
  requirement_id uuid references solidsecurity_contract.requirement(requirement_id),
  control_id text references solidsecurity_contract.control(control_id),
  assertion_id text references solidsecurity_contract.control_assertion(assertion_id),
  status text not null,
  rationale text,
  proposed_by_actor_type text,
  reviewed_by_membership_id uuid references solidsecurity_contract.membership(membership_id),
  reviewed_at timestamptz,
  created_at timestamptz not null,
  updated_at timestamptz not null,
  check (num_nonnulls(requirement_id, control_id, assertion_id) = 1)
);

create table solidsecurity_contract.client_implementation (
  implementation_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  scope_id uuid not null references solidsecurity_contract.organizational_scope(scope_id),
  control_id text not null references solidsecurity_contract.control(control_id),
  description text not null,
  owner_membership_id uuid references solidsecurity_contract.membership(membership_id),
  implementation_status text not null,
  declared_at timestamptz,
  source_of_claim text,
  created_at timestamptz not null,
  updated_at timestamptz not null,
  unique(tenant_id, scope_id, control_id)
);

create table solidsecurity_contract.vendor (
  vendor_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  name text not null,
  service text,
  criticality text,
  status text not null,
  owner_membership_id uuid references solidsecurity_contract.membership(membership_id),
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.ai_use_case (
  ai_use_case_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  name text not null,
  purpose text not null,
  provider_vendor_id uuid references solidsecurity_contract.vendor(vendor_id),
  data_classes jsonb not null default '[]'::jsonb,
  user_population text,
  preliminary_classification text,
  human_oversight text,
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.evidence (
  evidence_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  scope_id uuid references solidsecurity_contract.organizational_scope(scope_id),
  title text not null,
  evidence_type text not null,
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.evidence_version (
  evidence_version_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  evidence_id uuid not null references solidsecurity_contract.evidence(evidence_id),
  version_no integer not null check (version_no > 0),
  object_key text not null,
  sha256 char(64) not null check (sha256 ~ '^[0-9a-f]{64}$'),
  byte_size bigint not null check (byte_size >= 0),
  media_type text not null,
  source text,
  captured_by_actor_type text not null,
  captured_by_membership_id uuid references solidsecurity_contract.membership(membership_id),
  captured_at timestamptz not null,
  valid_from timestamptz,
  expires_at timestamptz,
  coverage_scope text,
  coverage_period text,
  population text,
  sample_basis text,
  limitations text,
  sensitivity text not null,
  created_at timestamptz not null,
  unique(tenant_id, evidence_id, version_no),
  unique(tenant_id, object_key)
);

create table solidsecurity_contract.implementation_evidence_link (
  implementation_evidence_link_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  implementation_id uuid not null references solidsecurity_contract.client_implementation(implementation_id),
  evidence_version_id uuid not null references solidsecurity_contract.evidence_version(evidence_version_id),
  relationship text not null,
  created_at timestamptz not null,
  unique(implementation_id, evidence_version_id)
);

create table solidsecurity_contract.assessment (
  assessment_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  scope_id uuid not null references solidsecurity_contract.organizational_scope(scope_id),
  target_type text not null,
  control_id text references solidsecurity_contract.control(control_id),
  assertion_id text references solidsecurity_contract.control_assertion(assertion_id),
  implementation_id uuid references solidsecurity_contract.client_implementation(implementation_id),
  result text not null,
  confidence text,
  rationale text,
  uncertainties text,
  proposed_proof_level smallint check (proposed_proof_level between 0 and 3),
  state text not null,
  assessor_actor_type text not null,
  assessor_membership_id uuid references solidsecurity_contract.membership(membership_id),
  created_at timestamptz not null,
  updated_at timestamptz not null,
  check (num_nonnulls(control_id, assertion_id, implementation_id) >= 1)
);

create table solidsecurity_contract.assessment_evidence_link (
  assessment_evidence_link_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  assessment_id uuid not null references solidsecurity_contract.assessment(assessment_id),
  evidence_version_id uuid not null references solidsecurity_contract.evidence_version(evidence_version_id),
  relationship text not null,
  created_at timestamptz not null,
  unique(assessment_id, evidence_version_id)
);

create table solidsecurity_contract.finding (
  finding_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  assessment_id uuid references solidsecurity_contract.assessment(assessment_id),
  category text not null,
  severity text,
  title text not null,
  description text not null,
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.action (
  action_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  finding_id uuid references solidsecurity_contract.finding(finding_id),
  owner_membership_id uuid references solidsecurity_contract.membership(membership_id),
  title text not null,
  description text,
  priority text,
  due_at timestamptz,
  verification_criteria text,
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.client_request (
  request_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  engagement_id uuid not null references solidsecurity_contract.engagement(engagement_id),
  request_type text not null,
  subject text not null,
  question text,
  requested_from_membership_id uuid references solidsecurity_contract.membership(membership_id),
  due_at timestamptz,
  status text not null,
  created_by_membership_id uuid references solidsecurity_contract.membership(membership_id),
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.client_response (
  response_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  request_id uuid not null references solidsecurity_contract.client_request(request_id),
  responder_membership_id uuid references solidsecurity_contract.membership(membership_id),
  response_text text,
  evidence_version_id uuid references solidsecurity_contract.evidence_version(evidence_version_id),
  created_at timestamptz not null
);

create table solidsecurity_contract.ai_proposal (
  ai_proposal_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  engagement_id uuid references solidsecurity_contract.engagement(engagement_id),
  proposal_type text not null,
  target_type text,
  target_id uuid,
  model_provider text not null,
  model_id text not null,
  policy_version text not null,
  input_refs jsonb not null default '[]'::jsonb,
  output_ref text,
  state text not null check (state in ('PROPOSED','REJECTED','SUPERSEDED','ACCEPTED_AS_INPUT')),
  created_at timestamptz not null
);

create table solidsecurity_contract.review_queue_item (
  review_queue_item_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  object_type text not null,
  object_id uuid not null,
  reason text not null,
  priority text,
  required_review_class text not null,
  assigned_membership_id uuid references solidsecurity_contract.membership(membership_id),
  status text not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.professional_review (
  review_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  review_queue_item_id uuid not null references solidsecurity_contract.review_queue_item(review_queue_item_id),
  reviewer_membership_id uuid not null references solidsecurity_contract.membership(membership_id),
  independence_class text not null,
  decision text not null,
  comments text,
  reviewed_at timestamptz not null,
  created_at timestamptz not null
);

create table solidsecurity_contract.decision (
  decision_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  object_type text not null,
  object_id uuid not null,
  decision_type text not null,
  outcome text not null,
  rationale text,
  authorized_by_membership_id uuid not null references solidsecurity_contract.membership(membership_id),
  effective_at timestamptz not null,
  expires_at timestamptz,
  created_at timestamptz not null
);

create table solidsecurity_contract.approval (
  approval_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  object_type text not null,
  object_id uuid not null,
  approval_type text not null,
  approved_by_membership_id uuid not null references solidsecurity_contract.membership(membership_id),
  outcome text not null,
  comments text,
  approved_at timestamptz not null,
  created_at timestamptz not null
);

create table solidsecurity_contract.report (
  report_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  engagement_id uuid not null references solidsecurity_contract.engagement(engagement_id),
  report_type text not null,
  period_start date,
  period_end date,
  status text not null,
  object_key text,
  sha256 char(64),
  generated_at timestamptz,
  approved_by_membership_id uuid references solidsecurity_contract.membership(membership_id),
  approved_at timestamptz,
  created_at timestamptz not null
);

create table solidsecurity_contract.approved_assertion (
  approved_assertion_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  canonical_wording text not null,
  scope_id uuid not null references solidsecurity_contract.organizational_scope(scope_id),
  valid_from timestamptz,
  expires_at timestamptz,
  review_status text not null,
  review_id uuid references solidsecurity_contract.professional_review(review_id),
  allowed_uses jsonb not null default '[]'::jsonb,
  customer_specific_exclusions text,
  assurance_labels jsonb not null default '{}'::jsonb,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table solidsecurity_contract.approved_assertion_control_link (
  approved_assertion_control_link_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  approved_assertion_id uuid not null references solidsecurity_contract.approved_assertion(approved_assertion_id),
  control_id text not null references solidsecurity_contract.control(control_id),
  assertion_id text,
  created_at timestamptz not null,
  unique(approved_assertion_id, control_id, assertion_id),
  foreign key (control_id, assertion_id)
    references solidsecurity_contract.control_assertion(control_id, assertion_id)
);

create table solidsecurity_contract.approved_assertion_evidence_link (
  approved_assertion_evidence_link_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  approved_assertion_id uuid not null references solidsecurity_contract.approved_assertion(approved_assertion_id),
  evidence_version_id uuid not null references solidsecurity_contract.evidence_version(evidence_version_id),
  created_at timestamptz not null,
  unique(approved_assertion_id, evidence_version_id)
);

create table solidsecurity_contract.audit_event (
  audit_event_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  actor_type text not null,
  actor_membership_id uuid references solidsecurity_contract.membership(membership_id),
  action text not null,
  object_type text,
  object_id uuid,
  metadata_safe jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null
);

create table solidsecurity_contract.recurring_review (
  recurring_review_id uuid primary key,
  tenant_id uuid not null references solidsecurity_contract.tenant(tenant_id),
  object_type text not null,
  object_id uuid not null,
  review_type text not null,
  due_at timestamptz not null,
  cadence text,
  status text not null,
  assigned_membership_id uuid references solidsecurity_contract.membership(membership_id),
  last_completed_at timestamptz,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

-- Runtime implementation requirements (not DDL implemented here):
-- 1. Enable RLS on every tenant-owned table and enforce membership-derived tenant context.
-- 2. Add same-tenant FK/trigger/policy guards where ordinary foreign keys cannot express tenant equality.
-- 3. Evidence object keys are immutable/versioned locators; object-store writes may not replace bytes at an existing tenant/key. Report object keys remain private and tenant-authorized.
-- 4. evidence_version is append-only after ingestion; updates that alter object/hash are forbidden.
-- 5. audit_event metadata excludes raw evidence bodies, secrets and unnecessary prompt content.
-- 6. service/agent identities cannot exercise human-only authoritative review/decision/approval states.
-- 7. approved_assertion links and review_id must resolve within the same tenant as the approved assertion.
