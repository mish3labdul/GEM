#!/usr/bin/env node
// Build the GEM business stationery working suite using Node built-ins only.
// Brand source: V3.0 official horizontal ink logo, exact bytes embedded in DOCX.
// Page geometry, masthead, footer and type settings follow GEM Letterhead Set v1.1 Application Revision 03
// (archive/baseline-v3.0/GEM_Letterhead_Set_v1.1_Application_Revision_03/00_source/rev03/spec.py).

import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import { fileURLToPath } from "node:url";

const OUT = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(OUT, "../../..");
const LOGO = path.join(ROOT, "archive/baseline-v3.0/GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal/png/gem-horizontal-ink-2048.png");
const INK = "12171D";
const BEIGE = "BCACA7";
const WHITE = "FFFFFF";
const A4_W = 11906;
const A4_H = 16838;
const MARGIN_X = 1417; // 25 mm sides
const CONTENT_W = A4_W - 2 * MARGIN_X; // 160 mm writing width
const LOGO_CX = 1152000; // 32 mm, as in the letterhead set
const LOGO_CY = 374062;
const REF_PLACEHOLDER = "Enter reference number";
// Contact facts confirmed by the owner for stationery on 30 Oct 2026.
const CONTACT_EMAIL = "contact@mish3l.com";
const CONTACT_PHONE = "+966114502929";
const CONTACT_LINE = "GEM\u2122 \u00B7 Riyadh, Saudi Arabia \u00B7 " + CONTACT_EMAIL + " \u00B7 " + CONTACT_PHONE;
const enc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");

// Regular weights only: the letterhead set specifies no bold synthesis, and no Bold font files are recorded in the brand kit.
function runProps(opts = {}) {
  const font = opts.font || "Inter";
  const size = opts.size || 18;
  const color = opts.color || INK;
  const track = opts.track ? "<w:spacing w:val=\"" + opts.track + "\"/>" : "";
  const italic = opts.italic ? "<w:i/><w:iCs/>" : "";
  const rtl = opts.rtl ? "<w:rtl w:val=\"1\"/>" : "";
  const lang = opts.rtl ? "<w:lang w:val=\"ar-SA\" w:bidi=\"ar-SA\"/>" : "<w:lang w:val=\"en-GB\"/>";
  return "<w:rPr><w:rFonts w:ascii=\"" + font + "\" w:hAnsi=\"" + font + "\" w:eastAsia=\"" + font + "\" w:cs=\"" + font + "\"/>" + italic + "<w:color w:val=\"" + color + "\"/>" + track + "<w:sz w:val=\"" + size + "\"/><w:szCs w:val=\"" + size + "\"/>" + rtl + lang + "</w:rPr>";
}

function run(text, opts = {}) {
  return "<w:r>" + runProps(opts) + "<w:t xml:space=\"preserve\">" + enc(text) + "</w:t></w:r>";
}

function p(text, opts = {}) {
  // Arabic paragraphs use logical alignment: "right" (visual) is the start edge, "left" the end edge.
  const requested = opts.align || "left";
  const align = opts.rtl ? ({ left: "end", right: "start" }[requested] || requested) : requested;
  const before = opts.before || 0;
  const after = opts.after === undefined ? 35 : opts.after;
  const line = opts.line ? "w:line=\"" + opts.line + "\" w:lineRule=\"exact\"" : "w:line=\"250\" w:lineRule=\"auto\"";
  const bidi = opts.rtl ? "<w:bidi w:val=\"1\"/>" : "";
  const keep = opts.keep ? "<w:keepNext/>" : "";
  const ind = opts.indStart ? "<w:ind w:start=\"" + opts.indStart + "\"/>" : "";
  const tabs = opts.tabRight ? "<w:tabs><w:tab w:val=\"right\" w:pos=\"" + opts.tabRight + "\"/></w:tabs>" : "";
  const pStyle = opts.style ? "<w:pStyle w:val=\"" + opts.style + "\"/>" : "";
  const textXml = opts.inner || (text ? run(text, opts) : "");
  return "<w:p><w:pPr>" + pStyle + keep + tabs + bidi + "<w:spacing w:before=\"" + before + "\" w:after=\"" + after + "\" " + line + "/>" + ind + "<w:jc w:val=\"" + align + "\"/></w:pPr>" + textXml + "</w:p>";
}

// Word content control (plain text): the placeholder is real text, selectable and replaced when typed over.
let sdtId = 1000;
function sdt(alias, placeholder, opts = {}) {
  sdtId += 1;
  return "<w:sdt><w:sdtPr><w:alias w:val=\"" + enc(alias) + "\"/><w:tag w:val=\"field_" + sdtId + "\"/><w:id w:val=\"" + sdtId + "\"/><w:text/></w:sdtPr><w:sdtContent>" + run(placeholder, opts) + "</w:sdtContent></w:sdt>";
}

function dropdown(alias, placeholder, items, opts = {}) {
  sdtId += 1;
  const list = items.map((i) => "<w:listItem w:displayText=\"" + enc(i) + "\" w:value=\"" + enc(i) + "\"/>").join("");
  return "<w:sdt><w:sdtPr><w:alias w:val=\"" + enc(alias) + "\"/><w:tag w:val=\"field_" + sdtId + "\"/><w:id w:val=\"" + sdtId + "\"/><w:showingPlcHdr/><w:dropDownList>" + list + "</w:dropDownList></w:sdtPr><w:sdtContent>" + run(placeholder, opts) + "</w:sdtContent></w:sdt>";
}

// Simple field. Unlocked on purpose: a locked field would ignore Ctrl+A, F9 and never recalculate.
function field(instr, cached, opts = {}) {
  return "<w:fldSimple w:instr=\"" + enc(instr) + "\">" + run(cached, opts) + "</w:fldSimple>";
}

// Complex field, needed to wrap a DOCPROPERTY or REF result in a bookmark-safe run sequence.
function complexField(instr, cached, opts = {}) {
  const r = runProps(opts);
  return "<w:r>" + r + "<w:fldChar w:fldCharType=\"begin\"/></w:r><w:r>" + r + "<w:instrText xml:space=\"preserve\"> " + instr + " </w:instrText></w:r><w:r>" + r + "<w:fldChar w:fldCharType=\"separate\"/></w:r>" + run(cached, opts) + "<w:r>" + r + "<w:fldChar w:fldCharType=\"end\"/></w:r>";
}

function imageParagraph() {
  return "<w:p><w:pPr><w:spacing w:after=\"0\" w:line=\"240\" w:lineRule=\"auto\"/><w:jc w:val=\"left\"/></w:pPr><w:r><w:drawing><wp:inline distT=\"0\" distB=\"0\" distL=\"0\" distR=\"0\"><wp:extent cx=\"" + LOGO_CX + "\" cy=\"" + LOGO_CY + "\"/><wp:docPr id=\"1\" name=\"GEM horizontal ink logo\" descr=\"GEM trademark horizontal logo. Supplied official vector kit; production-master acceptance pending.\"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect=\"1\"/></wp:cNvGraphicFramePr><a:graphic><a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\"><pic:pic><pic:nvPicPr><pic:cNvPr id=\"0\" name=\"GEM horizontal ink logo\"/><pic:cNvPicPr><a:picLocks noChangeAspect=\"1\"/></pic:cNvPicPr></pic:nvPicPr><pic:blipFill><a:blip r:embed=\"rIdLogo\"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"" + LOGO_CX + "\" cy=\"" + LOGO_CY + "\"/></a:xfrm><a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>";
}

const edge = (side, color, sz) => "<w:" + side + " w:val=\"single\" w:sz=\"" + sz + "\" w:space=\"0\" w:color=\"" + color + "\"/>";
const noEdge = (side) => "<w:" + side + " w:val=\"nil\"/>";

// Cell border presets. Beige and Ink appear only as rules, never as fills.
const CELL_BORDERS = {
  hair: edge("bottom", BEIGE, 4),
  band: noEdge("top") + noEdge("left") + edge("bottom", BEIGE, 8) + noEdge("right"),
  strong: edge("top", INK, 8) + edge("bottom", BEIGE, 4),
  head: edge("bottom", INK, 8),
  rule: edge("top", INK, 8) + edge("bottom", BEIGE, 4),
  box: edge("top", BEIGE, 4) + edge("left", BEIGE, 4) + edge("bottom", BEIGE, 4) + edge("right", BEIGE, 4)
};

function tc(content, width, opts = {}) {
  const shade = opts.fill ? "<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"" + opts.fill + "\"/>" : "";
  const valign = opts.valign || "center";
  const borders = opts.border ? "<w:tcBorders>" + CELL_BORDERS[opts.border] + "</w:tcBorders>" : "";
  const span = opts.span ? "<w:gridSpan w:val=\"" + opts.span + "\"/>" : "";
  const pXml = Array.isArray(content) ? content.join("") : content;
  return "<w:tc><w:tcPr><w:tcW w:w=\"" + width + "\" w:type=\"dxa\"/>" + span + borders + shade + "<w:vAlign w:val=\"" + valign + "\"/></w:tcPr>" + pXml + "</w:tc>";
}

// Word merges adjacent tables, so every table is followed by a 1 pt separator paragraph.
// keepWithNext carries a keep-with-next chain across the separator.
function tableGap(keepWithNext) {
  return "<w:p><w:pPr>" + (keepWithNext ? "<w:keepNext/>" : "") + "<w:spacing w:before=\"0\" w:after=\"0\" w:line=\"20\" w:lineRule=\"exact\"/><w:rPr><w:sz w:val=\"2\"/><w:szCs w:val=\"2\"/></w:rPr></w:pPr></w:p>";
}

function tbl(widths, rows, opts = {}) {
  const borders = opts.borders !== true
    ? "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/><w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/><w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
    : "<w:tblBorders>" + ["top", "left", "bottom", "right", "insideH", "insideV"].map((s) => edge(s, BEIGE, 4)).join("") + "</w:tblBorders>";
  const indent = opts.indent ? "<w:tblInd w:w=\"" + opts.indent + "\" w:type=\"dxa\"/>" : "";
  const grid = widths.map((w) => "<w:gridCol w:w=\"" + w + "\"/>").join("");
  const padTop = opts.padTop === undefined ? 40 : opts.padTop;
  const padBottom = opts.padBottom === undefined ? 40 : opts.padBottom;
  const mar = "<w:tblCellMar><w:top w:w=\"" + padTop + "\" w:type=\"dxa\"/><w:left w:w=\"85\" w:type=\"dxa\"/><w:bottom w:w=\"" + padBottom + "\" w:type=\"dxa\"/><w:right w:w=\"85\" w:type=\"dxa\"/></w:tblCellMar>";
  const tableRows = rows.map((row) => {
    const header = row.header ? "<w:tblHeader w:val=\"true\"/>" : "";
    const height = row.height ? "<w:trHeight w:val=\"" + row.height + "\" w:hRule=\"atLeast\"/>" : "";
    return "<w:tr><w:trPr>" + header + "<w:cantSplit/>" + height + "</w:trPr>" + row.cells.join("") + "</w:tr>";
  }).join("");
  return "<w:tbl><w:tblPr><w:tblW w:w=\"" + widths.reduce((a, b) => a + b, 0) + "\" w:type=\"dxa\"/>" + indent + borders + "<w:tblLayout w:type=\"fixed\"/>" + mar + "<w:tblLook w:firstRow=\"1\" w:lastRow=\"0\" w:firstColumn=\"0\" w:lastColumn=\"0\" w:noHBand=\"0\" w:noVBand=\"1\"/></w:tblPr><w:tblGrid>" + grid + "</w:tblGrid>" + tableRows + "</w:tbl>" + tableGap(opts.keepWithNext);
}

// Type scale, from the Part B tokens: labelSmall 12 px / arabicLabel 16 px is a 1.33 ratio, so an 8 pt Latin label pairs with a 10.5 pt Arabic label.
// Uppercase Latin labels carry 0.08 em tracking (13 twips at 8 pt); section headings 0.16 em (eyebrow); Arabic is never tracked.
const LABEL = { font: "Inter", size: 16, track: 13 };
const LABEL_AR = { font: "Noto Sans Arabic", size: 21, rtl: true };
const valueRun = { font: "Inter", size: 18 };
const COL_W = 4336;
const GUTTER = 400;
const FIELD_W = [COL_W, GUTTER, COL_W];
const ITEM_W = [520, 2400, 800, 850, 2250, 2252];
const CELL_PAD = 170; // left plus right cell margin

// English label at the start and Arabic label at the end of one line, via a right tab.
function labelLine(en, ar, width, keep) {
  return p("", { after: 30, keep, tabRight: width - CELL_PAD, inner: run(en.toUpperCase(), LABEL) + "<w:r><w:tab/></w:r>" + run(ar, LABEL_AR) });
}

// A value is a content-control placeholder (ph), a fixed confirmed value (fixed), a dropdown, or raw run XML (inner).
function valueContent(f, keep) {
  const alias = f.alias || (f.ph || f.en).replace(/^Enter /, "");
  const ropts = { ...valueRun, ...(f.run || {}) };
  let inner;
  if (f.inner) inner = f.inner;
  else if (f.options) inner = dropdown(alias, f.ph, f.options, ropts);
  else if (f.fixed !== undefined) inner = run(f.fixed, ropts);
  else inner = sdt(alias, f.ph, ropts);
  return p("", { after: 0, keep, inner });
}

// One field: bilingual label line over its value, closed by a Beige hairline. No cell boxes.
function fieldCell(f, width, keep, span) {
  return tc([labelLine(f.en, f.ar, width, keep), valueContent(f, keep)], width, { border: "hair", span, valign: "top" });
}

const gutterCell = () => tc(p("", { after: 0 }), GUTTER);
const emptyCell = (width) => tc(p("", { after: 0 }), width);
const FIELD_PAD = { padTop: 50, padBottom: 70 };

// Fields pair left and right across a gutter; a field marked full (or the odd last field) takes its own row across both columns.
// A short group (up to three rows) stays together; a longer one may break between rows, but its heading always stays with its first two rows.
function fieldRows(sec, fields, keepWithNext = false) {
  const rows = sec ? [sectionRow(sec, [1, 2], [COL_W, GUTTER + COL_W])] : [];
  const pairs = [];
  for (let i = 0; i < fields.length; i++) {
    const f = fields[i];
    const next = fields[i + 1];
    if (!f.full && next && !next.full) { pairs.push([f, next]); i++; } else pairs.push([f]);
  }
  const total = pairs.length;
  pairs.forEach(([left, right], i) => {
    const keep = total <= 3 ? i < total - 1 || keepWithNext : i === 0 || (keepWithNext && i === total - 1);
    if (right) rows.push({ cells: [fieldCell(left, COL_W, keep), gutterCell(), fieldCell(right, COL_W, keep)] });
    else rows.push({ cells: [fieldCell(left, CONTENT_W, keep, 3)] });
  });
  return tbl(FIELD_W, rows, { keepWithNext, ...FIELD_PAD });
}

// A heading cell: Jost uppercase (tracked) at the start, Arabic at the end, over a Beige rule.
function bandCell(en, ar, width, span) {
  const inner = run(en.toUpperCase(), { font: "Jost", size: 21, track: 34 }) + "<w:r><w:tab/></w:r>" + run(ar, { font: "Noto Sans Arabic", size: 22, rtl: true });
  return tc(p("", { before: 160, after: 40, keep: true, tabRight: width - CELL_PAD, inner, style: "Heading1" }), width, { border: "band", span, valign: "bottom" });
}

// Two parties side by side (for example Supplier and Customer), each a stack of fields under its own heading.
function parties(headL, headR, left, right, keepWithNext = false) {
  const rows = [{ cells: [bandCell(headL[0], headL[1], COL_W), tc(p("", { after: 0 }), GUTTER), bandCell(headR[0], headR[1], COL_W)] }];
  const n = Math.max(left.length, right.length);
  for (let i = 0; i < n; i++) {
    const keep = i === 0 || (keepWithNext && i === n - 1);
    rows.push({ cells: [
      left[i] ? fieldCell(left[i], COL_W, keep) : emptyCell(COL_W),
      gutterCell(),
      right[i] ? fieldCell(right[i], COL_W, keep) : emptyCell(COL_W)
    ] });
  }
  return tbl(FIELD_W, rows, { keepWithNext, ...FIELD_PAD });
}

// Summary strip under the title: four key facts, the last one emphasised. Ink rule above, Beige rule below.
function summaryStrip(cells) {
  const w = CONTENT_W / 4;
  const row = cells.map((f, i) => {
    const big = i === cells.length - 1 && f.big;
    const valueField = { ...f, run: big ? { font: "Jost", size: 30 } : {} };
    return tc([
      p("", { after: 0, keep: true, inner: run(f.en.toUpperCase(), LABEL) }),
      p(f.ar, { ...LABEL_AR, align: "right", after: 40, keep: true }),
      valueContent(valueField, true)
    ], w, { border: "rule", valign: "top" });
  });
  return tbl([w, w, w, w], [{ cells: row }], { keepWithNext: true, padTop: 90, padBottom: 100 });
}

// The section heading is the first row of its table so it can never be stranded from the rows below it.
// Jost Regular uppercase (tracked) over a Beige rule; English left, Arabic right on one line.
function sectionRow(sec, spans, widths, header = false) {
  return { header, cells: [
    tc(p(sec[0].toUpperCase(), { font: "Jost", size: 21, track: 34, before: 160, after: 40, keep: true, indStart: -85, style: "Heading1" }), widths[0], { border: "band", span: spans[0], valign: "bottom" }),
    tc(p(sec[1], { font: "Noto Sans Arabic", size: 22, rtl: true, align: "right", before: 160, after: 40, keep: true, indStart: -85 }), widths[1], { border: "band", span: spans[1], valign: "bottom" })
  ] };
}

// English title left and Arabic title right on one line, to save vertical space on forms.
function titleBlock(en, ar) {
  const half = Math.floor(CONTENT_W / 2);
  const wide = CONTENT_W + 170 - half; // table sits 85 twips outside each margin so the text edges align with it
  return tbl([half, wide], [{ cells: [
    tc(p(en, { font: "Jost", size: 42, after: 0, keep: true, style: "Title" }), half, { valign: "bottom" }),
    tc(p(ar, { font: "Noto Sans Arabic", size: 34, rtl: true, align: "right", after: 0, keep: true }), wide, { valign: "bottom" })
  ] }], { borders: false, keepWithNext: true, indent: -85 });
}

// Items and totals share one table so Word table formulas (=C3*E3, =SUM(F3:F6), =B7+B9) address them by row and column.
// Rows: 1 section heading, 2 column headings, 3 to 6 items, 7 onward totals (a merged A to E label cell and one amount cell).
const ITEM_ROWS = 4;
function itemsTable(sec, totals) {
  const widths = ITEM_W;
  const headers = [
    ["No.", "م"],
    ["Item / Service", "البند / الخدمة"],
    ["Qty", "الكمية"],
    ["Unit", "الوحدة"],
    ["Unit Price (SAR)", "سعر الوحدة"],
    ["Line Total (SAR)", "إجمالي البند"]
  ];
  const enAlign = (i) => (i < 2 ? "left" : i < 4 ? "center" : "right");
  const arAlign = (i) => (i === 2 || i === 3 ? "center" : "right");
  const left = widths[0] + widths[1] + widths[2];
  const rows = [sectionRow(sec, [3, 3], [left, CONTENT_W - left], true)];
  rows.push({
    header: true,
    cells: headers.map((h, i) => tc([
      p(h[0].toUpperCase(), { ...LABEL, align: enAlign(i), after: 20, keep: true }),
      p(h[1], { ...LABEL_AR, align: arAlign(i), after: 0, keep: true })
    ], widths[i], { border: "head", valign: "bottom" }))
  });
  for (let i = 0; i < ITEM_ROWS; i++) {
    const r = i + 3;
    const cell = (inner, j, align) => tc(p("", { after: 0, keep: true, align, inner }), widths[j], { border: "hair", valign: "center" });
    rows.push({ cells: [
      cell(run(String(i + 1), valueRun), 0, "center"),
      cell(sdt("Description", "Enter Description", valueRun), 1, "left"),
      cell(sdt("Qty", "0", valueRun), 2, "center"),
      cell(sdt("Unit", "Unit", valueRun), 3, "center"),
      cell(sdt("Unit Price", "0.00", valueRun), 4, "right"),
      cell(field("=C" + r + "*E" + r + " \\# \"#,##0.00\"", "0.00", valueRun), 5, "right")
    ] });
  }
  const labelW = widths.slice(0, 5).reduce((x, y) => x + y, 0);
  totals.forEach((t, idx) => {
    const keep = idx < totals.length - 1;
    const border = t.strong ? "rule" : "hair";
    const ropts = t.strong ? { font: "Jost", size: 24 } : { font: "Inter", size: 18 };
    let inner;
    if (t.ph) inner = sdt(t.alias || t.en, t.ph, ropts);
    else inner = field(t.instr + " \\# \"#,##0.00\"", "0.00", ropts);
    if (t.bookmark) inner = "<w:bookmarkStart w:id=\"9021\" w:name=\"" + t.bookmark + "\"/>" + inner + "<w:bookmarkEnd w:id=\"9021\"/>";
    // One line per total: English at the start, Arabic at the right edge of the label cell via a right tab.
    const arOpts = { font: "Noto Sans Arabic", size: t.strong ? 24 : 21, rtl: true };
    const labelInner = run(t.en.toUpperCase(), t.strong ? { ...ropts, track: 20 } : LABEL) + "<w:r><w:tab/></w:r>" + run(t.ar, arOpts);
    rows.push({ cells: [
      tc(p("", { after: 0, keep, inner: labelInner, tabRight: labelW - 170 }), labelW, { border, span: 5 }),
      tc(p("", { after: 0, keep, align: "right", inner }), widths[5], { border })
    ] });
  });
  return tbl(widths, rows, { padTop: 50, padBottom: 60 });
}

const VAT_ROWS = [
  { en: "Subtotal", ar: "المجموع الفرعي", instr: "=SUM(F3:F6)" },
  { en: "VAT rate (%)", ar: "نسبة ضريبة القيمة المضافة", ph: "15", alias: "VAT Rate" },
  { en: "VAT amount (SAR)", ar: "مبلغ ضريبة القيمة المضافة", instr: "=(B7*B8)/100" },
  { en: "Total", ar: "الإجمالي", instr: "=B7+B9", strong: true, bookmark: "DocTotal" }
];

// An entry box at least four lines tall, under a bilingual heading row. paragraphs are ready-made w:p strings.
const ENTRY_MIN_HEIGHT = 1300;
function noteBlock(en, ar, paragraphs, height = ENTRY_MIN_HEIGHT) {
  const left = 5800;
  return tbl([left, CONTENT_W - left], [
    sectionRow([en, ar], [1, 1], [left, CONTENT_W - left]),
    { height, cells: [tc(paragraphs, CONTENT_W, { border: "box", span: 2, valign: "top" })] }
  ]);
}

const entryPara = (inner, opts = {}) => p("", { after: 40, line: 288, inner, ...opts });

const NS = "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\"";

// First-page header: logo, then the fixed tagline (Jost Regular 10.5 pt, 38 twip expanded spacing), as in the letterhead set.
function headerFirstXml() {
  const tagline = "<w:p><w:pPr><w:spacing w:before=\"680\" w:after=\"227\" w:line=\"300\" w:lineRule=\"exact\"/><w:jc w:val=\"left\"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=\"Jost\" w:hAnsi=\"Jost\" w:eastAsia=\"Jost\" w:cs=\"Jost\"/><w:color w:val=\"" + INK + "\"/><w:spacing w:val=\"38\"/><w:sz w:val=\"21\"/><w:szCs w:val=\"21\"/><w:lang w:val=\"en-GB\"/></w:rPr><w:t>HOSPITALITY, IN PERFECT PROPORTION</w:t></w:r></w:p>";
  return "<w:hdr " + NS + ">" + imageParagraph() + tagline + "</w:hdr>";
}

// Continuation header: quiet identifier and reference only. The reference follows the RefNo document property, so it matches the body.
function headerContinuationXml(doc) {
  const o = { font: "Inter", size: 16 };
  const en = p("", { after: 0, line: 240, inner: run("GEM\u2122 \u00B7 " + doc.continued[0].toUpperCase() + " \u00B7 ", o) + complexField("DOCPROPERTY RefNo \\* MERGEFORMAT", REF_PLACEHOLDER, o) });
  const ar = p(doc.continued[1], { font: "Noto Sans Arabic", size: 16, rtl: true, align: "right", after: 0, line: 240 });
  return "<w:hdr " + NS + ">" + en + ar + "</w:hdr>";
}

function footerRun(text) {
  return "<w:r><w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\" w:eastAsia=\"Inter\" w:cs=\"Inter\"/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"18\"/><w:szCs w:val=\"18\"/><w:lang w:val=\"en-GB\"/></w:rPr><w:t xml:space=\"preserve\">" + enc(text) + "</w:t></w:r>";
}

function pageField(instr) {
  const rPr = "<w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\" w:cs=\"Inter\"/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"18\"/><w:szCs w:val=\"18\"/></w:rPr>";
  return "<w:r>" + rPr + "<w:fldChar w:fldCharType=\"begin\"/></w:r><w:r>" + rPr + "<w:instrText xml:space=\"preserve\"> " + instr + " \\* MERGEFORMAT </w:instrText></w:r><w:r>" + rPr + "<w:fldChar w:fldCharType=\"separate\"/></w:r>" +
    footerRun("1") + "<w:r>" + rPr + "<w:fldChar w:fldCharType=\"end\"/></w:r>";
}

// Compact form frame: a two-line footer (the letterhead set allows up to four lines), Inter Regular 9 pt on 12.6 pt exact leading.
// Line 1 carries the confirmed contact facts and the page number on a right tab; line 2 carries the issue restriction in both languages.
function footerXml() {
  const line = (inner, rule, tab) => "<w:p><w:pPr>" + (rule ? "<w:pBdr><w:top w:val=\"single\" w:sz=\"4\" w:space=\"6\" w:color=\"" + BEIGE + "\"/></w:pBdr>" : "") + (tab ? "<w:tabs><w:tab w:val=\"right\" w:pos=\"" + CONTENT_W + "\"/></w:tabs>" : "") + "<w:spacing w:after=\"30\" w:line=\"252\" w:lineRule=\"exact\"/><w:jc w:val=\"left\"/></w:pPr>" + inner + "</w:p>";
  const ar = { font: "Noto Sans Arabic", size: 18, rtl: true };
  return "<w:ftr " + NS + ">" +
    line(footerRun(CONTACT_LINE) + "<w:r><w:tab/></w:r>" + footerRun("Page ") + pageField("PAGE") + footerRun(" of ") + pageField("NUMPAGES"), true, true) +
    line(footerRun("NOT FOR EXTERNAL ISSUE \u00B7 ") + run("غير مخصص للإصدار الخارجي", ar) + footerRun(" \u00B7 PENDING VALIDATION (D8)")) +
    "</w:ftr>";
}

function stylesXml() {
  return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<w:styles xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">" +
    "<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\" w:eastAsia=\"Inter\" w:cs=\"Noto Sans Arabic\"/><w:sz w:val=\"18\"/><w:szCs w:val=\"18\"/><w:lang w:val=\"en-GB\" w:bidi=\"ar-SA\"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after=\"35\" w:line=\"250\" w:lineRule=\"auto\"/></w:pPr></w:pPrDefault></w:docDefaults>" +
    "<w:style w:type=\"paragraph\" w:default=\"1\" w:styleId=\"Normal\"><w:name w:val=\"Normal\"/><w:qFormat/><w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\" w:eastAsia=\"Inter\" w:cs=\"Noto Sans Arabic\"/></w:rPr></w:style>" +
    "<w:style w:type=\"paragraph\" w:styleId=\"Title\"><w:name w:val=\"Title\"/><w:basedOn w:val=\"Normal\"/><w:qFormat/><w:rPr><w:rFonts w:ascii=\"Jost\" w:hAnsi=\"Jost\"/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"42\"/></w:rPr></w:style>" +
    "<w:style w:type=\"paragraph\" w:styleId=\"Heading1\"><w:name w:val=\"heading 1\"/><w:basedOn w:val=\"Normal\"/><w:qFormat/><w:rPr><w:rFonts w:ascii=\"Jost\" w:hAnsi=\"Jost\"/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"21\"/></w:rPr></w:style>" +
    "</w:styles>";
}

function docXml(body) {
  return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<w:document " + NS + "><w:body>" + body +
    "<w:sectPr><w:headerReference w:type=\"first\" r:id=\"rIdHeaderFirst\"/><w:headerReference w:type=\"default\" r:id=\"rIdHeader\"/><w:footerReference w:type=\"first\" r:id=\"rIdFooterFirst\"/><w:footerReference w:type=\"default\" r:id=\"rIdFooter\"/><w:pgSz w:w=\"" + A4_W + "\" w:h=\"" + A4_H + "\"/><w:pgMar w:top=\"1701\" w:right=\"" + MARGIN_X + "\" w:bottom=\"1417\" w:left=\"" + MARGIN_X + "\" w:header=\"1020\" w:footer=\"680\" w:gutter=\"0\"/><w:cols w:num=\"1\" w:space=\"425\"/><w:titlePg/><w:docGrid w:linePitch=\"360\"/></w:sectPr></w:body></w:document>";
}

function contentTypes() {
  return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">" +
    "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/><Default Extension=\"xml\" ContentType=\"application/xml\"/><Default Extension=\"png\" ContentType=\"image/png\"/>" +
    "<Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/><Override PartName=\"/word/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml\"/><Override PartName=\"/word/header1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml\"/><Override PartName=\"/word/header2.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml\"/><Override PartName=\"/word/footer1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml\"/><Override PartName=\"/word/footer2.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml\"/><Override PartName=\"/word/settings.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml\"/><Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/><Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/><Override PartName=\"/docProps/custom.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.custom-properties+xml\"/>" +
    "</Types>";
}

function crc32(buf) {
  let crc = 0xffffffff;
  for (let i = 0; i < buf.length; i++) {
    crc ^= buf[i];
    for (let j = 0; j < 8; j++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function zip(entries) {
  const local = [];
  const central = [];
  let offset = 0;
  for (const [name, dataValue] of entries) {
    const nameBuf = Buffer.from(name, "utf8");
    const raw = Buffer.isBuffer(dataValue) ? dataValue : Buffer.from(dataValue, "utf8");
    const packed = zlib.deflateRawSync(raw, { level: 9 });
    const crc = crc32(raw);
    const lh = Buffer.alloc(30);
    lh.writeUInt32LE(0x04034b50, 0);
    lh.writeUInt16LE(20, 4);
    lh.writeUInt16LE(0x0800, 6);
    lh.writeUInt16LE(8, 8);
    lh.writeUInt32LE(crc, 14);
    lh.writeUInt32LE(packed.length, 18);
    lh.writeUInt32LE(raw.length, 22);
    lh.writeUInt16LE(nameBuf.length, 26);
    const localPart = Buffer.concat([lh, nameBuf, packed]);
    local.push(localPart);
    const ch = Buffer.alloc(46);
    ch.writeUInt32LE(0x02014b50, 0);
    ch.writeUInt16LE(20, 4);
    ch.writeUInt16LE(20, 6);
    ch.writeUInt16LE(0x0800, 8);
    ch.writeUInt16LE(8, 10);
    ch.writeUInt32LE(crc, 16);
    ch.writeUInt32LE(packed.length, 20);
    ch.writeUInt32LE(raw.length, 24);
    ch.writeUInt16LE(nameBuf.length, 28);
    ch.writeUInt32LE(0, 38);
    ch.writeUInt32LE(offset, 42);
    central.push(Buffer.concat([ch, nameBuf]));
    offset += localPart.length;
  }
  const centralBytes = Buffer.concat(central);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(entries.length, 8);
  end.writeUInt16LE(entries.length, 10);
  end.writeUInt32LE(centralBytes.length, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...local, centralBytes, end]);
}

function createDocx(doc) {
  const logo = fs.readFileSync(LOGO);
  const rels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">" +
    "<Relationship Id=\"rIdDocument\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/><Relationship Id=\"rIdCore\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/><Relationship Id=\"rIdApp\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties\" Target=\"docProps/app.xml\"/><Relationship Id=\"rIdCustom\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties\" Target=\"docProps/custom.xml\"/></Relationships>";
  const docRels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">" +
    "<Relationship Id=\"rIdStyles\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" Target=\"styles.xml\"/><Relationship Id=\"rIdHeaderFirst\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/header\" Target=\"header1.xml\"/><Relationship Id=\"rIdHeader\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/header\" Target=\"header2.xml\"/><Relationship Id=\"rIdFooterFirst\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer\" Target=\"footer1.xml\"/><Relationship Id=\"rIdFooter\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer\" Target=\"footer2.xml\"/><Relationship Id=\"rIdSettings\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings\" Target=\"settings.xml\"/></Relationships>";
  const headerRels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rIdLogo\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\"media/gem-horizontal-ink.png\"/></Relationships>";
  const title = enc(doc.title + " | GEM Business Stationery Working Suite");
  const core = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><dc:title>" + title + "</dc:title><dc:subject>Editable bilingual business document template</dc:subject><dc:creator>GEM</dc:creator><cp:keywords>WORKING INTERNAL REVIEW DRAFT</cp:keywords><dc:description>Working template. Business details and external-issue acceptance remain pending.</dc:description><dcterms:created xsi:type=\"dcterms:W3CDTF\">2026-10-27T00:00:00Z</dcterms:created></cp:coreProperties>";
  const app = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\"><Application>GEM stationery template builder</Application></Properties>";
  const customProps = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/custom-properties\" xmlns:vt=\"http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes\"><property fmtid=\"{D5CDD505-2E9C-101B-9397-08002B2CF9AE}\" pid=\"2\" name=\"RefNo\"><vt:lpwstr>" + REF_PLACEHOLDER + "</vt:lpwstr></property></Properties>";
  const settings = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><w:settings xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"><w:defaultTabStop w:val=\"720\"/><w:compat><w:compatSetting w:name=\"compatibilityMode\" w:uri=\"http://schemas.microsoft.com/office/word\" w:val=\"15\"/></w:compat></w:settings>";
  const entries = [
    ["[Content_Types].xml", contentTypes()],
    ["_rels/.rels", rels],
    ["docProps/core.xml", core],
    ["docProps/app.xml", app],
    ["docProps/custom.xml", customProps],
    ["word/document.xml", docXml(doc.body)],
    ["word/styles.xml", stylesXml()],
    ["word/header1.xml", headerFirstXml()],
    ["word/header2.xml", headerContinuationXml(doc)],
    ["word/footer1.xml", footerXml()],
    ["word/footer2.xml", footerXml()],
    ["word/_rels/document.xml.rels", docRels],
    ["word/_rels/header1.xml.rels", headerRels],
    ["word/settings.xml", settings],
    ["word/media/gem-horizontal-ink.png", logo]
  ];
  fs.writeFileSync(path.join(OUT, doc.filename), zip(entries));
}

// Shared field definitions. ph is a content-control placeholder; fixed is a value the owner confirmed for stationery.
const DATE_HINT = " - DD/MM/YYYY (Gregorian)";
const dateField = (en, ar, what) => ({ en, ar, ph: "Enter " + what + DATE_HINT, alias: what + " | DD/MM/YYYY (Gregorian)" });
const stripDate = (en, ar, what) => ({ en, ar, ph: "DD/MM/YYYY (Gregorian)", alias: what + " | DD/MM/YYYY (Gregorian)" });
const refField = (en, ar) => ({ en, ar, inner: complexField("DOCPROPERTY RefNo \\* MERGEFORMAT", REF_PLACEHOLDER, valueRun) });
const totalRef = (en, ar) => ({ en, ar, inner: complexField("REF DocTotal", "0.00", { font: "Jost", size: 30 }), big: true });
const CURRENCY = { en: "Currency", ar: "العملة", fixed: "SAR" };
const OWNER_CONTACT = "Mashal Abdulrahman, GM / Owner";
const LEGAL_NAME = { en: "Legal Name", ar: "الاسم القانوني المسجل", ph: "Enter Registered Legal Name (Trading Name: GEM)", alias: "Registered Legal Name" };
const BUSINESS_ADDRESS = { en: "Address", ar: "عنوان المنشأة / العنوان الوطني", ph: "Enter Business / National Address", alias: "Business / National Address" };
const CR_NUMBER = { en: "Commercial Reg. No.", ar: "رقم السجل التجاري", ph: "Enter Commercial Registration No." };
const TAX_ID = (en, ar) => ({ en, ar, ph: "Enter Tax Identifier" });
const NOTICE = "Verify payment details through a previously known channel before making payment.";
const NOTICE_AR = "تحقّق من بيانات الدفع عبر وسيلة اتصال معروفة مسبقاً قبل السداد.";
const staticPara = (text, opts = {}) => entryPara(run(text, { font: "Inter", size: 18, ...opts }));
const arabicPara = (text) => p(text, { font: "Noto Sans Arabic", size: 21, rtl: true, align: "right", after: 40, line: 288 });
const text = (en, ar, ph, extra = {}) => ({ en, ar, ph, ...extra });

const docs = [
  {
    filename: "GEM_Request_for_Quotation_Template_working.docx",
    title: "Request for Quotation",
    continued: ["RFQ continued", "تكملة طلب عرض السعر"],
    body:
      titleBlock("Request for Quotation", "طلب تقديم عرض سعر") +
      summaryStrip([
        refField("RFQ Number", "رقم طلب عرض السعر"),
        stripDate("Issue Date", "تاريخ الإصدار", "Issue Date"),
        stripDate("Response Due", "موعد الرد", "Response Due Date"),
        { ...CURRENCY, run: { font: "Jost", size: 30 }, big: true }
      ]) +
      parties(["Requester", "مقدم الطلب"], ["Supplier", "المورد"], [
        LEGAL_NAME,
        BUSINESS_ADDRESS,
        { en: "Contact", ar: "مقدم الطلب", fixed: OWNER_CONTACT },
        { en: "Email", ar: "البريد الإلكتروني", fixed: CONTACT_EMAIL },
        { en: "Phone", ar: "الهاتف", fixed: CONTACT_PHONE },
        CR_NUMBER
      ], [
        text("Legal Name", "الاسم القانوني المسجل للمورد", "Enter Supplier Registered Legal Name"),
        text("Address", "العنوان", "Enter Supplier Address"),
        text("Contact Name", "اسم جهة التواصل", "Enter Supplier Contact"),
        text("Email", "البريد الإلكتروني", "Enter Supplier Email"),
        text("Phone", "الهاتف", "Enter Supplier Phone"),
        text("Tax Identifier", "الرقم الضريبي للمورد", "Enter Supplier Tax Identifier")
      ]) +
      fieldRows(["Request Reference", "مرجع الطلب"], [
        text("Project / Reference", "المشروع / المرجع", "Enter Project or Reference"),
        text("Supplier Quote Ref.", "مرجع عرض المورد", "Enter Supplier Quote Reference"),
        text("Supplier Confirmation", "تأكيد المورد", "Enter Supplier Confirmation")
      ]) +
      itemsTable(["Items or Services", "البنود أو الخدمات"], [
        { en: "Subtotal", ar: "المجموع الفرعي", instr: "=SUM(F3:F6)" },
        { en: "Total", ar: "الإجمالي", instr: "=B7", strong: true }
      ]) +
      fieldRows(["Delivery and Response", "التسليم والرد التجاري"], [
        text("Delivery Location", "موقع التسليم", "Enter Delivery Address"),
        dateField("Requested Delivery", "موعد التسليم المطلوب", "Requested Delivery Date"),
        text("Payment Terms", "شروط الدفع", "Enter Requested Payment Terms"),
        dateField("Quote Valid Until", "صلاحية العرض حتى", "Quote Validity Date"),
        text("Lead Time", "مدة التوريد", "Enter Supplier Lead Time"),
        { en: "Prices Are", ar: "الأسعار", ph: "Select VAT treatment", options: ["VAT-inclusive", "VAT-exclusive"] }
      ], true) +
      noteBlock("Response Instructions", "تعليمات الرد", [
        staticPara("Complete the supplier details, each requested item, prices, VAT selection, delivery and commercial fields, and supplier confirmation. Return this RFQ by the response due date."),
        arabicPara("يرجى استكمال بيانات المورد والبنود المطلوبة والأسعار وخيار ضريبة القيمة المضافة وبيانات التسليم والشروط التجارية وتأكيد المورد، ثم إعادة طلب عرض السعر قبل موعد الرد.")
      ], 0)
  },
  {
    filename: "GEM_Quotation_Proposal_Template_working.docx",
    title: "Quotation and Proposal",
    continued: ["Quotation continued", "تكملة عرض السعر"],
    body:
      titleBlock("Quotation and Proposal", "عرض سعر ومقترح") +
      summaryStrip([
        refField("Quotation Number", "رقم عرض السعر"),
        stripDate("Issue Date", "تاريخ الإصدار", "Issue Date"),
        stripDate("Valid Until", "صالح حتى", "Quote Validity Date"),
        totalRef("Total (SAR)", "الإجمالي")
      ]) +
      parties(["Issuer", "الجهة المصدرة"], ["Customer", "العميل"], [
        LEGAL_NAME,
        BUSINESS_ADDRESS,
        TAX_ID("Tax Identifier", "الرقم الضريبي للمنشأة"),
        text("Sales Contact", "جهة التواصل للمبيعات", "Enter Sales Contact Name / Role"),
        { en: "Email", ar: "البريد الإلكتروني", fixed: CONTACT_EMAIL },
        { en: "Phone", ar: "هاتف المنشأة", fixed: CONTACT_PHONE }
      ], [
        text("Customer", "العميل", "Enter Customer Name"),
        text("Address", "عنوان العميل", "Enter Customer Address"),
        text("Contact", "جهة التواصل", "Enter Customer Contact"),
        text("Email", "بريد العميل", "Enter Customer Email")
      ]) +
      fieldRows(["Quotation Details", "بيانات عرض السعر"], [
        text("Project / Property", "المشروع / المنشأة", "Enter Project or Property"),
        text("Customer PO", "أمر شراء العميل", "Enter Customer PO Number")
      ]) +
      noteBlock("Scope Summary", "ملخص النطاق", [entryPara(sdt("Scope Summary", "Enter scope summary", valueRun))]) +
      noteBlock("Assumptions, Exclusions & Terms", "الافتراضات والاستثناءات والشروط", [entryPara(sdt("Assumptions, Exclusions and Terms", "Enter assumptions, exclusions and terms", valueRun))]) +
      itemsTable(["Pricing", "الأسعار"], VAT_ROWS) +
      fieldRows(["Delivery and Payment", "التسليم والدفع"], [
        text("Delivery Location", "موقع التسليم", "Enter Delivery Address"),
        dateField("Estimated Delivery", "موعد التسليم التقديري", "Estimated Delivery Date"),
        text("Payment Terms", "شروط الدفع", "Enter Payment Terms")
      ]) +
      fieldRows(["Customer Acceptance", "قبول العميل"], [
        text("Name / Role", "الاسم / الصفة", "Enter Customer Name / Role"),
        dateField("Signature / Date", "التوقيع / التاريخ", "Signature / Date")
      ])
  },
  {
    filename: "GEM_Invoice_Template_working.docx",
    title: "Invoice",
    continued: ["Invoice continued", "تكملة الفاتورة"],
    body:
      titleBlock("Invoice", "فاتورة") +
      summaryStrip([
        refField("Invoice Number", "رقم الفاتورة"),
        stripDate("Issue Date", "تاريخ الإصدار", "Issue Date"),
        stripDate("Payment Due", "تاريخ الاستحقاق", "Payment Due Date"),
        totalRef("Total Due (SAR)", "إجمالي المبلغ المستحق")
      ]) +
      parties(["Supplier", "المورد"], ["Customer", "العميل"], [
        LEGAL_NAME,
        BUSINESS_ADDRESS,
        TAX_ID("Tax Identifier", "الرقم الضريبي للمورد"),
        CR_NUMBER,
        { en: "Contact", ar: "جهة التواصل لدى المورد", fixed: OWNER_CONTACT },
        { en: "Email", ar: "بريد المورد", fixed: CONTACT_EMAIL },
        { en: "Phone", ar: "هاتف المورد", fixed: CONTACT_PHONE }
      ], [
        text("Customer", "العميل", "Enter Customer Legal Name"),
        text("Billing Address", "عنوان الفوترة", "Enter Customer Billing Address"),
        text("Tax Identifier", "الرقم الضريبي للعميل", "Enter Customer Tax Identifier, if applicable"),
        text("Email", "بريد العميل", "Enter Customer Email")
      ]) +
      fieldRows(["References", "المراجع"], [
        text("Purchase Order", "أمر الشراء", "Enter Customer PO Number"),
        text("Related Quotation", "عرض السعر المرتبط", "Enter Quotation Reference"),
        dateField("Supply Date", "تاريخ التوريد", "Supply Date"),
        CURRENCY
      ]) +
      itemsTable(["Items or Services", "البنود أو الخدمات"], [
        ...VAT_ROWS.slice(0, 3),
        { en: "Total", ar: "الإجمالي", instr: "=B7+B9", bookmark: "DocTotal" },
        { en: "Amount Paid", ar: "المبلغ المدفوع", ph: "0.00", alias: "Amount Paid" },
        { en: "Balance Due", ar: "الرصيد المستحق", instr: "=B10-B11", strong: true }
      ]) +
      fieldRows(["Payment Instructions", "تعليمات الدفع"], [
        text("Payee", "المستفيد / اسم الحساب", "Enter Payee Name"),
        text("Bank", "البنك", "Enter Bank Name"),
        text("Account Number", "رقم الحساب", "Enter Account Number"),
        text("IBAN", "رقم الآيبان (IBAN)", "Enter IBAN"),
        text("Payment Reference", "مرجع الدفع", "Enter Payment Reference"),
        { en: "Contact Email", ar: "بريد التواصل", fixed: CONTACT_EMAIL }
      ]) +
      noteBlock("Notes and Terms", "الملاحظات والشروط", [
        entryPara(sdt("Payment Terms and Notes", "Enter payment terms and notes", valueRun)),
        staticPara(NOTICE),
        arabicPara(NOTICE_AR)
      ])
  },
  {
    filename: "GEM_Purchase_Order_Template_working.docx",
    title: "Purchase Order",
    continued: ["Purchase Order continued", "تكملة أمر الشراء"],
    body:
      titleBlock("Purchase Order", "أمر شراء") +
      summaryStrip([
        refField("PO Number", "رقم أمر الشراء"),
        stripDate("Order Date", "تاريخ الطلب", "Order Date"),
        stripDate("Requested Delivery", "تاريخ التسليم المطلوب", "Requested Delivery Date"),
        totalRef("Total (SAR)", "الإجمالي")
      ]) +
      parties(["Buyer", "المشتري"], ["Supplier", "المورد"], [
        LEGAL_NAME,
        BUSINESS_ADDRESS,
        TAX_ID("Tax Identifier", "الرقم الضريبي للمشتري"),
        CR_NUMBER,
        { en: "Requester", ar: "مقدم الطلب / جهة تواصل المشتري", fixed: OWNER_CONTACT },
        { en: "Email", ar: "بريد مقدم الطلب", fixed: CONTACT_EMAIL },
        { en: "Phone", ar: "هاتف مقدم الطلب", fixed: CONTACT_PHONE }
      ], [
        text("Supplier Name", "اسم المورد", "Enter Supplier Registered Name"),
        text("Address", "عنوان المورد", "Enter Supplier Address"),
        text("Tax Identifier", "الرقم الضريبي للمورد", "Enter Supplier Tax Identifier, if applicable"),
        text("Contact", "جهة التواصل لدى المورد", "Enter Supplier Contact"),
        text("Email", "بريد المورد", "Enter Supplier Email"),
        text("Phone", "هاتف المورد", "Enter Supplier Phone")
      ]) +
      fieldRows(["References", "المراجع"], [
        text("Related Quotation", "عرض السعر المرتبط", "Enter Quotation Reference"),
        text("RFQ Reference", "مرجع طلب عرض السعر", "Enter RFQ Reference"),
        CURRENCY
      ]) +
      itemsTable(["Items or Services", "البنود أو الخدمات"], VAT_ROWS) +
      fieldRows(["Delivery and Billing", "التسليم والفوترة"], [
        text("Deliver To", "جهة التسليم", "Enter Recipient / Department"),
        text("Delivery Address", "عنوان التسليم", "Enter Delivery Address"),
        text("Billing Address", "عنوان الفوترة", "Enter Billing Address"),
        text("Shipping Terms", "شروط الشحن والتسليم", "Enter Agreed Shipping / Delivery Terms"),
        text("Special Instructions", "تعليمات خاصة", "Enter Special Instructions, if any"),
        text("Payment Terms", "شروط الدفع", "Enter Agreed Payment Terms")
      ])
  }
];

if (!fs.existsSync(LOGO)) throw new Error("Approved V3.0 logo asset is missing: " + LOGO);
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
for (const doc of docs) createDocx(doc);
console.log("Created " + docs.length + " editable A4 DOCX templates in " + OUT);
console.log("Embedded exact V3.0 supplied logo: " + path.relative(ROOT, LOGO));
