# Oikos submission workflow

Barry W. Brook (sole author) and Claude work through these steps in order,
from the PI's read to the Oikos submission. Codex is not on this tranche
(board thread 89 is paused) unless Barry reopens it, or Claude asks him to
and he agrees. Git history holds the earlier plans; the scientific record of
the October rework is in `docs/decisions.md`, the three
`docs/oikos_*_review_2026-10-1*.md` audits and `docs/oikos_submission_checklist.md`.

Each step names who acts, what is produced and what closes it. A **one-way**
step is outward-facing and irreversible, and needs Barry's explicit go-ahead.

## Starting state (23 October 2026)

- Branch `claude/oikos-editorial-checkpoint` at `f261c24`, pushed to the
  private remote; `main` is behind at `d0fc7e1`.
- Main PDF (26 pp.) and Supporting information (24 pp.):
  `build/oikos_submission_aug_2026/insurance_hypothesis_blinded_main.pdf` and
  `..._supplementary_info.pdf`. All six document profiles, the golden contract,
  DOCX sanitisation and the identity scans pass.
- Anonymous computational package:
  `~/papers/de_identified_repos/insurance_hypothesis_2026-10-19/ih_package.zip`
  (SHA-256 `a32b9f51…c74796`, 113 MB). It is unaffected by later edits to the
  manuscript.
- The makedoc SI-divider fix sits on makedoc branch `claude/standalone-si-divider`
  (`4cd4809`) and is not yet merged.
- No preprint, public repository, archive or submission exists.

## Journal facts checked on 23 October 2026

From the NSO author guidelines (nso-journals.org/author-guidelines) and the NSO
publishing policy (nordicsocietyoikos.org/publishing-policy):

- The abstract is limited to 300 words (currently 261). No Research Paper word
  limit is stated, and first submissions need not be reformatted.
- The main text must be anonymous. Data and code are required at first
  submission but need not be public. They can go in an "additional file for
  review but not for publication" or behind an anonymous repository link.
- **Each supporting-information file is capped at 50 MB.** The 113 MB package
  therefore needs splitting or an anonymous link (step 6).
- Publication requires a persistent identifier for data and code; a GitHub
  link alone does not qualify, and Zenodo is recommended.
- Preprints are allowed before submission, and the submitted version may be
  posted at any time.
- An AI-use statement goes at the end of the main text. AI tools cannot be
  authors.
- Entered in the submission form: data availability, significance, conflict of
  interest, ethics, funding and acknowledgements. CRediT roles are required
  only at revision.
- Authors must check the PDF that ScholarOne generates before submitting.

## Steps

### 1. Barry's read — Barry

Two sittings are suggested:
- **Sitting 1:** title, abstract, Figs 1–3 and their captions, Introduction and
  Discussion. Is the argument clear, the contribution pitched right, and does it
  sound like you?
- **Sitting 2:** Methods, Results, Table 1 and the Supporting information. Can
  you defend every assumption and interpretation?

Mark problems rather than solving them. "Overstated", "lost here" or "why does
this matter" is enough. Use one format: an annotated PDF, a tracked DOCX or
page-and-line notes. Points that need your judgement in particular:
- **AI statement:** does it describe the division of labour accurately? First
  person singular is correct for a sole author, provided you are content with
  that voice given the AI roles the statement discloses.
- **Discussion claims:** the plausibility and empirical-signature paragraphs
  are the main interpretive claims the paper makes beyond the model.
- **Title:** "Shared environments can destabilise communities with balanced
  opposing responses".

Closed when your notes are returned.

### 2. Integrate the read — Claude, then a short check by Barry

Claude applies the edits in the canonical source and checks affected claims
against the results. Captions, tables, the SI and the cover letter are kept
consistent, and the documents are rebuilt and verified. Claude returns a short
account of the substantive changes and any choices left to you.

Two fixes go in this pass:
- **Author contributions:** NSO forbids listing AI as authors. Name only you
  under Author contributions, and keep the AI roles in the AI statement.
- **Statement placeholders:** fill the funding and acknowledgements text from
  step 3.

Stopping rule: correctness, clarity, attribution and claims must be resolved.
A possible extension becomes new analysis only if your read exposes a concrete
gap in the evidence.

Closed when you approve the changed passages, the abstract and the conclusion.

### 3. Administrative facts — Barry, one batch, any time before step 5

- Funding bodies and grant numbers, or "no specific funding".
- Acknowledgements, or none.
- Affiliation, email and ORCID as they should appear on the title page and
  preprint.
- Conflict-of-interest wording (currently "No competing interests are declared").
- Approval of the AI-use statement (from step 1).

Closed when `docs/questions_for_human.md` is empty.

### 4. Release decisions — Barry, with Claude's recommendations

- **Preprint server and order.** Recommendation: EcoEvoRxiv under CC BY 4.0,
  posted before the Oikos submission so that the cover letter can cite it.
  Posting at submission is the alternative.
- **Public code and data.** Recommendation: make this repository public after
  merging to `main`, so the full history is visible. Archive the computational
  release on Zenodo (code plus the 18 production summaries), with the GitHub
  repository linked from the Zenodo record.
- **Licences.** Recommendation: MIT for code, CC BY 4.0 for the simulated data
  summaries and documentation.
- **Correspondence record.** Optionally publish the Claude–Codex correspondence
  (discussion 89) with the release, as an example of transparent human–AI
  research. Claude would export and redact anything private first.

Closed when the four choices are recorded in `docs/decisions.md`.

### 5. Prepare the public release — Claude; Barry approves

- Merge `claude/oikos-editorial-checkpoint` into `main` by pull request, and
  merge the makedoc fix branch in the makedoc repository.
- Add `LICENSE` files, `CITATION.cff` and Zenodo metadata (`.zenodo.json`).
  Update the README for a public audience, and rerun the full release gate.
- **Barry:** reserve the Zenodo DOI in a draft record. This needs your
  account; the DOI is registered only when the record is published.
- **One-way, Barry's go-ahead:** make the repository public and publish the
  Zenodo record.

Closed when the DOI resolves and the archive replays from a clean download.

### 6. Review files for Oikos — Claude

- **Anonymous review package.** Recommendation: split it into parts of at most
  50 MB (code, specifications and small summaries, plus two data-only parts),
  each with checksums and reassembly instructions. This avoids any account and
  any link that could break or identify you. The alternative is an anonymised
  view-only link (OSF or figshare private link), which needs your account.
  Replay the reassembled split package from a clean extraction.
- **Submission files.** Anonymous main PDF, SI PDF, separate title page, cover
  letter disclosing the preprint, and copy-ready text for the form statements
  (data availability with the Zenodo DOI, significance, conflict of interest,
  ethics, funding, acknowledgements).

Closed when every file passes the identity scans and the checklist is current.

### 7. Preprint — Claude prepares; Barry posts (one-way)

- Claude builds an author-identified PDF from the same source, with the SI
  appended, author details, declarations and the Zenodo DOI. Claude also
  writes a copy-paste sheet: title, plain-text abstract, keywords, author
  metadata and links.
- **Barry** posts it to the chosen server, then sends Claude the URL and DOI.
  Claude checks the posted files and adds reciprocal links to Zenodo and
  GitHub.

### 8. Oikos submission — Barry submits (one-way); Claude checks

- Submit as a Research Paper. The form will ask for suggested or excluded
  reviewers if the portal requires them: Claude researches candidates, and you
  judge conflicts.
- Before the final click, download the PDF that ScholarOne generates. Claude
  checks it for missing material, equation rendering, file order and anonymity.
- After submitting, send Claude the confirmation and manuscript ID. Claude tags
  the submitted commit, archives the receipt and records the exact submitted
  file hashes in the checklist.

## Status

- [ ] 1. Barry's read
- [ ] 2. Integration
- [ ] 3. Administrative facts
- [ ] 4. Release decisions
- [ ] 5. Public release
- [ ] 6. Review files
- [ ] 7. Preprint
- [ ] 8. Submission
