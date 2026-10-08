# Editable BARR pair-fusion diagrams

The figure uses three parallel vertical columns: population control, analytical pair screening, and structured recovery. The algorithm is frozen BARR candidate B.

| Language | Editable source | Vector PDF | Preview |
|---|---|---|---|
| 中文 | [draw.io](barr-pair-fusion-zh.drawio) | [PDF](barr-pair-fusion-zh.drawio.pdf) | [PNG](barr-pair-fusion-zh.png) |
| English | [draw.io](barr-pair-fusion.drawio) | [PDF](barr-pair-fusion.drawio.pdf) | [PNG](barr-pair-fusion.png) |

Muted teal marks the analytical pair scout, its certificates and positive-witness archive step. Muted purple marks structured expansion and recovery. Remaining operations use black/gray text and borders on white or transparent backgrounds.

Solid arrows show control flow, including explicit loop back-edges. Colored dashed arrows show each subalgorithm's call/expansion and returned values. The main controller initializes and increments iteration count `k`, checks the global deadline and optional round limit `K`, then returns its feasible historical incumbent. The frozen 360-second protocol leaves `K` unset and terminates on the deadline. The scout has its own all-seed cursor and deadline loop. All main-search operations are serial.

The draw.io sources contain editable native shapes and connectors. PDFs, SVGs and PNGs were exported with draw.io Desktop. The PDFs and SVGs embed the editable diagram; the PNGs are previews. See [figure-manifest.json](figure-manifest.json) for file hashes. Mathematical model and three algorithms: [PDF](../barr_model_algorithm.pdf), [LaTeX](../barr_model_algorithm.tex).
