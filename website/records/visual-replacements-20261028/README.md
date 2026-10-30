# Approved visual replacements — 28 October 2026

The owner approved local use of the generated replacement candidates for the English family scene, Arabic RTL family scene, and concentric-arches banner. This records visual approval for local integration. It does not establish source-model terms, third-party rights, public-use clearance, or release approval; the imagery rights gate remains open.

## Sources and canonical outputs

Each approved source PNG is preserved under `approved-png/`; each replaced WebP is preserved under `originals/`. The canonical WebP files in `website/remake/assets/scenes/` were encoded from the approved PNGs with `cwebp -quiet -q 90 -m 6`.

| Asset | Approved PNG SHA-256 | Original WebP SHA-256 | Canonical WebP SHA-256 | Dimensions |
| --- | --- | --- | --- | --- |
| `family.webp` | `0354608ee9f35c7ea348e968ce39913117e8ae9c8f1a763a33398bc038690114` | `628a3908ec84b740d587d24a1dc6d614ecd273fe419acd500571cf62f3e25874` | `5b02c24d18299a5b35300a18582ffbefab7f6ed06d8c720b962d3e1310363654` | 2172×724 |
| `family-rtl.webp` | `f9e91a5caffb2e1d2faeb5c7584c42131324aa1a839ff55c2ff1cef5c1c660d` | `d5280bd78699eaacb4b5f7b2152221760a2dd1ad27d6b8a96028151667fdc4dd` | `22f7c46365560545f33ebc87146cdf7ea644b0783116fc67a82a3ee0b8099932` | 2172×724 |
| `tx-arches.webp` | `935f4efb4ca1a08c14dabd1e61181d1a8d1e8fb9d8b033231a6a77edd2a21e49` | `71dbe7e9ac45ad6ae4edddf274435226ac92c71e52fa8bfd5bd6d36226d68be4` | `37e1a4f6ff624d24008b1cebeb3d5a70345bf9780b55fd838cb8d74394f33988` | 2172×724 |

The `tx-arches` source is the revised candidate requested by the owner, with the arch extended to the lower image edge. The generated candidate was reviewed and approved in conversation on 28 October 2026.

## V09 wall-format revision — 28 October 2026

The owner approved the refined wall-format alternative after review. Its PNG is retained at `candidates/v09-wall-alternative.png` and is now the canonical source at `website/remake/assets/source/format-wall-source.png` (SHA-256 `0af7c148912ab8c1d42532abae41082f763be79b00a5f553e584ab2c09f9534b`, 1536×1024). Responsive outputs were regenerated: `format-wall-480.webp` (SHA-256 `048563df3aeed45a9d3879ba21f8bf0d7f1e7ea598a5f1a739618c85cde0fb17`) and `format-wall-960.webp` (SHA-256 `d176b3f7b64120bacf3f8cbcbca257dc938207679bc16768855bd6799e22b557`). The source it replaced is preserved under `originals/format-wall-source-before-latest-approval.png`. This is visual approval only; product and release gates remain separate.

## Integration boundary

The replacements are local to the current branch `feat/visual-audit-class-b-outpaint`. The rebuilt `dist/` files are generated copies of canonical inputs. No deployment or merge is recorded here. On 28 October 2026, the owner approved the V03 social-share crop and V09 wall-format visual candidate; see `V03-V09-owner-approval-20261028.md`. Visual approval does not establish product specifications or public-use rights.
