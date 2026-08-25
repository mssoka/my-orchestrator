# Lens report — AUTHZ (IDOR + ownership + internal endpoints)

## Summary

I walked every authenticated route in `server/src/router.gleam` end-to-end (route → handler → SQL) plus the three internal secret-gated endpoints, and read the underlying Squirrel SQL for every object-ownership chain. The tenant boundary is held correctly almost everywhere: vacancy-scoped reads and mutations carry `user_id`/`vacancy.user_id` filters in the SQL itself, direct-id resources (notifications, AI job, PDF report, payment status/verify/consent, billing, invoices, settings, account delete) are all owner-scoped, and the internal endpoints use a constant-time `crypto.secure_compare` against `INTERNAL_SECRET` with fail-closed empty-secret handling and a hard boot-failure in production. All query construction is Squirrel-parameterized (no string-interpolated SQL), so raw route ids are not an injection surface; ids are parsed with `uuid.from_string` at the handler boundary.

I found **three issues, none cross-tenant**: (F1) a single unowned cross-tenant *write* — `auto_close_vacancy` runs without a `user_id` filter in the authenticated vacancy-detail handler before the ownership-scoped read (Low, low exploitability because it can only close an already-expired vacancy whose unguessable UUID the attacker must know); (F2) an inconsistency where PATCH `/status` and the reference-check start/skip/re-enable paths never bind the URL `vacancy_id` to the application's actual vacancy (the row actions already added this exact guard as "W10") — same-owner cross-vacancy confusion only, not a cross-tenant leak; (F3) archiving a vacancy does not hide its public `/apply/:code` content — landlord name and full property address remain reachable to any link-holder indefinitely.

No Critical or High findings. No cross-tenant data egress, no cross-tenant object mutation other than F1's benign-force-close, no internal-endpoint authz weakness.

## Findings table

| ID | Severity | Title | file:line | Confidence |
|----|----------|-------|-----------|------------|
| F1 | Low | `auto_close_vacancy` mutates without an owner filter, before the ownership check | `server/src/vacancy/sql/auto_close_vacancy.sql:1-8`; call site `server/src/vacancy/vacancy_handler.gleam:314` | High |
| F2 | Low | PATCH `/status` + reference start/skip/re-enable never bind URL `vacancy_id` to the application (same-owner cross-vacancy confusion) | `server/src/application/sql/update_application_status.sql:1-7`; `server/src/application/application_detail_handler.gleam:607,616,677`; `server/src/reference_checks/trigger.gleam:1060` | High |
| F3 | Low | Archived vacancies keep serving landlord name + full address on `/apply/:code` | `server/src/application/sql/get_vacancy_for_form.sql:1-16`; `server/src/application/application_handler.gleam:2312`; `server/src/application/form_view.gleam:540` | High |

---

## F1 — `auto_close_vacancy` writes another landlord's row without an owner filter

**Severity:** Low · **Confidence:** High

### Exploit sketch

Landlord A (authenticated) issues `GET /api/v1/vacancies/<B's-vacancy-uuid>` for a vacancy owned by landlord B. `handle_get_detail` runs the auto-close *before* the ownership-scoped read:

1. `sql.auto_close_vacancy(db, vacancy_uuid)` — the SQL is `UPDATE vacancy SET status='closed', closed_via='auto' WHERE id = $1 AND status='active' AND closes_at < now() AND archived_at IS NULL`. There is **no `user_id` filter**.
2. Only *then* does the handler read via `sql.get_by_id(db, vacancy_uuid, user_uuid)` (owner-filtered), which returns 0 rows → 404 to A.

Net effect: A can force B's vacancy from `active` to `closed` — but only if it has **already passed its `closes_at`** (the `closes_at < now()` guard) and only if A knows B's vacancy UUID. Once closed with `closed_via='auto'`, the next daily lifecycle run dispatches the "vacancy closed" notification email to B. No data is read by A; A receives only a 404.

Exploitability is low: vacancy UUIDs are never exposed cross-tenant (every list/detail endpoint is owner-filtered), and the only reachable state transition is one the system would perform anyway on B's next dashboard load or the daily job (`batch_auto_close` / the lifecycle auto-close path). It is still a genuine cross-tenant write with a missing owner filter — the exact defect class this lens exists to find.

### Evidence

`server/src/vacancy/sql/auto_close_vacancy.sql` (whole file):

```sql
--- auto_close_vacancy(vacancy_id: UUID)
UPDATE vacancy
SET status = 'closed', closed_via = 'auto'
WHERE id = $1
  AND status = 'active'
  AND closes_at < now()
  AND archived_at IS NULL
RETURNING id::text
```

`server/src/vacancy/vacancy_handler.gleam:312-325` (note the ordering — the unowned write precedes the owned read):

```gleam
      case sql.auto_close_vacancy(db, vacancy_uuid) {
        Ok(_) -> Nil
        Error(err) -> wisp.log_warning(...)
      }
      response_helpers.with_single_row(
        sql.get_by_id(db, vacancy_uuid, user_uuid),
        context: "fetching vacancy " <> vacancy_id,
        ...
```

Contrast with the sibling fast-path `server/src/vacancy/sql/batch_auto_close.sql`, which correctly carries `WHERE user_id = $1`.

### Remediation

Add the owner predicate to the query and pass `user_id` through:

```sql
--- auto_close_vacancy(vacancy_id: UUID, user_id: UUID)
UPDATE vacancy
SET status = 'closed', closed_via = 'auto'
WHERE id = $1
  AND user_id = $2
  AND status = 'active'
  AND closes_at < now()
  AND archived_at IS NULL
RETURNING id::text
```

and call it as `sql.auto_close_vacancy(db, vacancy_uuid, user_uuid)`. Re-run Squirrel (`bash run_squirrel.sh`). This makes the side-effect write owner-scoped regardless of handler ordering.

---

## F2 — PATCH `/status` and reference start/skip/re-enable don't bind URL `vacancy_id` to the application

**Severity:** Low · **Confidence:** High

### Exploit sketch

Landlord A owns two vacancies, V1 and V2, with application X in V1. A sends `PATCH /api/v1/vacancies/V2/applications/X/status` (or the reference-check `start`/`skip`/`re-enable` verbs under `/vacancies/V2/applications/X/...`).

The handler verifies **two independent facts** — (a) A owns application X (`verify_application_ownership` → app→vacancy→`user_id`), and (b) A owns vacancy V2 (`verify_vacancy_active` → `id`+`user_id`) — but never verifies (c) that X actually *lives in* V2. The status UPDATE is scoped only by `application.id` + `vacancy.user_id`:

```sql
UPDATE application
SET status = $2::application_status
FROM vacancy
WHERE application.id = $1
  AND vacancy.id = application.vacancy_id
  AND vacancy.user_id = $3
```

So the request succeeds and mutates X (in V1) while the URL claims V2. The reference-check skip/re-enable paths likewise act on `app_uuid` (ownership-verified) while ignoring the URL `vacancy_id` entirely.

This is **not cross-tenant**: `verify_application_ownership` guarantees the application always belongs to the requesting landlord, and the UPDATE's `vacancy.user_id = $3` filter is the real boundary. The impact is confined to *same-owner* URL/object confusion — a "misleading 200" and the loss of the invariant "the nested resource is in the vacancy the URL names". The reference-check row actions already fixed this exact gap and documented why it matters — `reference_checks/sql/verify_application_in_vacancy.sql` ("RC4.3 r1 (Perkins W10): bind the path vacancy to the path application … 0 rows = the application does not live in the path vacancy — the handler 404s") — but the fix was not propagated to PATCH `/status` or the trigger verbs.

### Evidence

PATCH `/status` ownership chain — `server/src/application/application_detail_handler.gleam:607,616,677`:

```gleam
          case ai_sql.verify_application_ownership(db, app_uuid, landlord_uuid) {
            Ok(pog.Returned(_, [row])) if row.match_count > 0 ->
              case sql.verify_vacancy_active(db, vacancy_uuid, landlord_uuid) {
                ...
                  apply_status_update(config, app_uuid, landlord_uuid, vacancy_uuid, ...)
```

…which calls `sql.update_application_status(db, app_uuid, new_status, landlord_uuid)` — note `vacancy_uuid` is **not** passed to the UPDATE.

The trigger verbs use the same loose pattern — `server/src/reference_checks/trigger.gleam:1052-1071`:

```gleam
fn run_action_with_prechecks(config, app_uuid, landlord_uuid, vacancy_uuid, action) {
  case ai_sql.verify_application_ownership(db, app_uuid, landlord_uuid) {
    Ok(pog.Returned(_, [row])) if row.match_count > 0 ->
      case app_sql.verify_vacancy_active(db, vacancy_uuid, landlord_uuid) {
        Ok(...) if is_archived -> 422
        _ -> action()
      }
    _ -> 404
  }
}
```

Contrast with the row-action path that *does* bind the vacancy — `server/src/reference_checks/actions_handler.gleam:656-680`:

```gleam
  case sql.verify_application_in_vacancy(db, app_uuid, vacancy_uuid, landlord_uuid) {
    Ok(pog.Returned(_, [row])) if row.match_count > 0 -> ...
```

(`/open` is already fully bound — `auto_transition_on_open.sql` includes `vacancy.id = $3`.)

### Remediation

Replace the two-check pattern in `handle_update_status` and `trigger.gleam`'s `run_action_with_prechecks` with the single `verify_application_in_vacancy(app, vacancy, landlord)` check (and add `AND vacancy.id = $3` to `update_application_status.sql`, mirroring `auto_transition_on_open.sql`). Re-run Squirrel. This makes "application X is in URL vacancy V and owned by me" one atomic predicate instead of two unjoined ones.

---

## F3 — Archiving a vacancy does not hide its public `/apply/:code` content

**Severity:** Low · **Confidence:** High

### Exploit sketch

A vacancy is soft-deleted via `archived_at` ("hidden from dashboard, restorable anytime"). But `GET /apply/:short_code` looks the vacancy up by `short_code` with **no** `status`/`archived_at` filter, and `is_accepting_applications` returns false for an archived vacancy, so the handler renders `view_closed_vacancy_page` — which still includes the full form header: `property_name`, `address_line_1`, `city`, `county`, and `landlord_name` (the landlord's real name). Anyone holding the link (the flyer, a forwarded email, a cached tab, a search-engine snapshot) can see the landlord's name and the property's full address indefinitely, even after the landlord archived the listing intending it to disappear.

Codes are `substr(md5(random()::text), 1, 12)` (48-bit, unguessable — `vacancy/sql/create_vacancy.sql`), so this is confined to link-holders, not brute-force enumerators. It is an availability/intent gap (archive ≠ retract the public listing) plus a mild PII leak of landlord name + address, not a cross-tenant IDOR.

### Evidence

`server/src/application/sql/get_vacancy_for_form.sql` — no status/archived predicate:

```sql
SELECT v.id::text, v.property_name, v.address_line_1, v.city, v.county,
       v.status::text, v.closes_at::text, coalesce(v.archived_at::text,'') AS archived_at,
       v.origin_domain, v.max_applications, v.short_code, l.name AS landlord_name, ...
FROM vacancy v
JOIN landlord l ON l.id = v.user_id
WHERE v.short_code = $1
```

`server/src/application/application_handler.gleam:2312`:

```gleam
pub fn is_accepting_applications(vacancy) -> Bool {
  vacancy.status == "active"
  && string.is_empty(vacancy.archived_at)
  && vacancy.is_expired != "true"
}
```

…and the non-accepting branch renders the closed page whose header (`server/src/application/form_view.gleam:540`) prints `property_name`, the full address, and `landlord_name <> " is accepting applications through RightTenantry"`.

### Remediation

Treat archive as retraction: either (a) have `handle_get_form`/`handle_post_form` render `view_not_found_page` (404) when `archived_at` is non-empty, or (b) strip `landlord_name`/address from the closed page when `archived_at` is set. Decide explicitly whether a restored vacancy should resume serving the closed-vs-open page based on `status`. If "archived ⇒ 404" is chosen, keep the response visually identical to the invalid-code 404 to avoid any code-validity oracle.

---

## Routes verified CLEAN (one line each)

- `GET /api/v1/vacancies` → `list_by_user(user_id)` + `dashboard_stats(user_id)`; `batch_auto_close(user_id)` is owner-scoped.
- `GET /api/v1/vacancies/archived` → `list_archived(user_id)`.
- `GET /api/v1/vacancies/:id` → `get_by_id(id, user_id)` (note F1's pre-read side-effect).
- `GET /api/v1/vacancies/:id/edit` → `get_vacancy_for_edit(id, user_id)`.
- `PATCH /api/v1/vacancies/:id` → `update_vacancy` `WHERE id=$1 AND user_id=$2`.
- `POST /api/v1/vacancies/:id/close` → `close_vacancy(id, user_id)`.
- `POST /api/v1/vacancies/:id/archive` → `archive_vacancy(id, user_id)`.
- `POST /api/v1/vacancies/:id/restore` → `restore_vacancy(id, user_id)`.
- `POST /api/v1/vacancies/:id/publish` → `get_vacancy_for_edit` + `publish_vacancy(id, user_id)`.
- `GET /api/v1/vacancies/:id/applications` → `verify_vacancy_ownership` then `LIMIT 20 OFFSET` list.
- `GET /api/v1/vacancies/:id/awaiting` → `get_by_id` owner check then `list_awaiting_for_vacancy`.
- `GET /api/v1/vacancies/:vid/applications/:aid` → `get_application_detail(app, landlord, vacancy)` (3-way filter).
- `GET …/applications/:aid/documents/:did/download` → `get_document_for_download(doc, app, vacancy, landlord)` (4-way join).
- `POST …/applications/:aid/open` → `verify_vacancy_active` + `auto_transition_on_open(app, landlord, vacancy)` (includes `vacancy.id=$3`) + owner-filtered fallback.
- `PATCH …/applications/:aid/status` → `verify_application_ownership` + `verify_vacancy_active` + `update_application_status(app, status, landlord)` — cross-tenant safe; see F2 for the missing vacancy binding.
- `POST …/applications/bulk-reject` → `bulk_reject_by_ids` `WHERE vacancy.id=$1 AND vacancy.user_id=$2 AND id=ANY($3)`.
- `GET /api/v1/vacancies/:vid/compare` → `get_comparison_details(vacancy, landlord, id1, id2, id3)` owner+`a.id IN` filter.
- `POST …/reference-checks/start` → `get_application_reference_data(app, landlord, vacancy)` (3-way `a.id=$1 AND v.user_id=$2 AND a.vacancy_id=$3`).
- `POST …/reference-checks/:slot/skip` & `/re-enable` → `verify_application_ownership` + `verify_vacancy_active`, mutations scoped to `app_uuid`; cross-tenant safe, see F2.
- `POST …/reference-checks/:call_id/take-over|correct|substitute` → `verify_application_in_vacancy(app, vacancy, landlord)` + `read_owned_row` (call→application binding).
- `GET /api/v1/ai/jobs/:id` → `find_by_id` then `verify_application_ownership` (read-only; ownership immutable).
- `GET /api/v1/vacancies/:vid/scoring-status` → `verify_vacancy_ownership`.
- `GET /api/v1/ai/analyses/:id/pdf` → `get_analysis_for_pdf(id, user_id)` (`WHERE a.id=$1 AND v.user_id=$2`).
- `POST /api/v1/payment/checkout` & `/extension/checkout` → `get_by_id(id, user_id)`.
- `GET /api/v1/payment/status/:vid` → `get_payment_status(vid, user_id)`.
- `GET /api/v1/payment/consent/check` → `get_by_id` owner check then `find_payment_terms_acceptance(user, vacancy, version)`.
- `GET /api/v1/payment/verify` → `verify_payment_for_landlord(session_id, user_id)` (`JOIN vacancy … AND v.user_id=$2::uuid`).
- `GET /api/v1/settings/billing-history` → `list_by_landlord(user_id)`.
- `GET /api/v1/settings/invoices` → `get_landlord_stripe_customer(user_id)`.
- `PATCH /api/v1/settings/profile` → `update_landlord_profile` `WHERE id=$1::uuid`.
- `PATCH /api/v1/settings/notification-preference` → `update_notification_preference` `WHERE id=$1::uuid`.
- `POST /api/v1/settings/change-password` → Supabase login with the session's own `landlord.email` (no foreign id).
- `POST /api/v1/account/delete` → confirm-email gate + all deletes scoped by `user_id`.
- `GET /api/v1/notifications` → `list_by_user(user_id) LIMIT 50`.
- `POST /api/v1/notifications/read-all` → `mark_all_read(user_id)`.
- `POST /api/v1/notifications/:id/read` → `mark_read(id, user_id)`.
- `POST /api/v1/vacancies/:id/bulk-invite` → `find_vacancy_for_invite` + `vacancy.user_id == landlord.id` before any send.
- `POST /api/v1/vacancies/:id/remind-applicants` / `remind-applicant` → same ownership check before the stamp+send transaction.

## Internal endpoints (verified)

- `POST /api/v1/internal/digest` → `require_internal_secret` → `crypto.secure_compare` (constant-time), empty secret ⇒ 500 (fail-closed), missing header/wrong value ⇒ 401.
- `POST /api/v1/internal/lifecycle/verification-reminders` → same guard.
- `POST /api/v1/internal/reference-checks` → same guard.
- Secret sourcing (`server/src/server.gleam:242-250`): `INTERNAL_SECRET` must be set in production or boot fails (`Error("INTERNAL_SECRET must be set in production")`); dev uses a random 64-char value. Empty-string secret is therefore unreachable in prod, and `require_internal_secret` would 500 anyway.
- CSRF skip-list includes `["api","v1","internal",..]` (correct — these rely on the secret, not a session) — `server/src/auth/csrf.gleam`.
- What they do if hit (all secret-gated): digest emails all `daily`-pref landlords with pending notifications; verification-reminders emails unverified landlords; reference-checks runs one cadence-sweep tick (SMS/email sends). No data egress to the caller beyond aggregate counts.

## Other items checked

- **UUID parsing / SQL injection:** every route param is parsed with `uuid.from_string` at the handler boundary (or is the already-validated `landlord.id`); all SQL is Squirrel-generated `pog.query |> pog.parameter(...)` — no dynamic SQL string construction anywhere in `server/src`. `::uuid` casts in the SQL validate format at the DB. No injection surface. Clean.
- **Enumeration/unbounded ops:** `notifications` capped at 50, `applications` at 20/page; `vacancies`/`billing` lists are owner-scoped (no cross-tenant enumeration). `/apply/:code` returns 404 for unknown codes vs 200 for known-but-closed — a validity oracle, but short codes are 48-bit (`md5(random())` prefix) so brute-force enumeration is infeasible. Not a finding.
- **Compare / scoring-status without auth:** both sit behind `require_session` and verify ownership before any work. Clean.
