# Source and recorded baseline attribution

The primary native source is the frozen BARR v0.4 B source, copied byte for byte.
Its original MIT license is retained under `native/BARR_v0.4B/LICENSE` and at the repository root.
The related E source retains its original license under `related/BARR_v0.4E/LICENSE`.

The BARR native pair-fusion implementation does not link CHILS. Some preserved
historical result records were produced by the CHILS search source plus an int64
bridge with callbacks disabled. Those result records identify the population and
binary hash used by their original batch. The CHILS source is not redistributed
in this repository; see the source attribution and public reference in the
original experiment protocol. The CHILS-p16 historical records retain their
original identity; F records use CHILS with population 4 and one thread.
