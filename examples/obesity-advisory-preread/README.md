# Exemplar — obesity advisory board pre-read, rebuilt

A ten-slide advisory pre-read that a workshop agent originally produced as
text boxes with hand-indented lines and no charts. This spec carries **the
same content, with no facts added**, rebuilt through the bundled engine:
native charts for the STEP and withdrawal trials, stat cards for regain,
persistence and SELECT, a two-column simulated safety intake, a gap → decision
table and advisory questions, each with a design kicker and a source line.

Real-trial evidence is cited by PMID/NCT as supplied in the original deck; it
has not been re-verified here. ADIPOSYN and all `SYN:` records are fictional
workshop material. The engine's warning about the missing `approval_status` is
deliberate: the original deck did not state one, and a reviewer must add it.

```bash
python3 skills/medical-slide-deck/scripts/ma_render.py bootstrap
python3 skills/medical-slide-deck/scripts/ma_render.py deck \
    examples/obesity-advisory-preread/deck.json \
    --out outputs/obesity-preread.pptx --preview outputs/preview
```
