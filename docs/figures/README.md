# Editable BARR pair-fusion diagrams

The figure uses three parallel vertical columns: population control, analytical pair screening, and structured recovery. Each column follows its own content length rather than sharing a full-height frame. The algorithm is frozen BARR candidate B.

| Language | Editable source | Vector PDF | Preview |
|---|---|---|---|
| 中文 | [draw.io](barr-pair-fusion-zh.drawio) | [PDF](barr-pair-fusion-zh.drawio.pdf) | [PNG](barr-pair-fusion-zh.png) |
| English | [draw.io](barr-pair-fusion.drawio) | [PDF](barr-pair-fusion.drawio.pdf) | [PNG](barr-pair-fusion.png) |

Box widths, heights, typography, and nested enclosures express the hierarchy. The exact gain formula and the archive-before-refinement step use large type and heavy dark frames. The bounded solver has a distinct enclosure containing its Kernel, response-factor elimination, fallback, and full-graph verification steps. Routine operations use narrower, lighter boxes; decisions use diamonds; call sites use predefined-process shapes. This hierarchy remains visible in grayscale.

Small native vector structures show the four-member population, a pair with a shared selected blocker, and response-factor tables feeding bounded elimination. These are schematic mechanisms, not sampled numerical states. Muted teal and purple provide supplementary accents for analytical screening and structured recovery; remaining operations use black/gray text and borders on white or transparent backgrounds.

Solid arrows show control flow, including explicit loop back-edges. Dashed arrows in the column gutters and lower routing band show each subalgorithm's call/expansion and returned values. The main controller initializes and increments iteration count `k`, checks the global deadline and optional round limit `K`, then returns its feasible historical incumbent. The frozen 360-second protocol leaves `K` unset and terminates on the deadline. The scout has its own all-seed cursor and deadline loop. All main-search operations are serial.

The draw.io sources contain editable native shapes and connectors. PDFs, SVGs and PNGs were exported with draw.io Desktop. The PDFs and SVGs embed the editable diagram; the PNGs are previews. See [figure-manifest.json](figure-manifest.json) for file hashes. Mathematical model and three algorithms: [PDF](../barr_model_algorithm.pdf), [LaTeX](../barr_model_algorithm.tex).
