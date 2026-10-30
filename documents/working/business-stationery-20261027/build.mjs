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
  const italic = opts.italic ? "<w:i/><w:iCs/>" : "";
  const rtl = opts.rtl ? "<w:rtl w:val=\"1\"/>" : "";
  const lang = opts.rtl ? "<w:lang w:val=\"ar-SA\" w:bidi=\"ar-SA\"/>" : "<w:lang w:val=\"en-GB\"/>";
  return "<w:rPr><w:rFonts w:ascii=\"" + font + "\" w:hAnsi=\"" + font + "\" w:eastAsia=\"" + font + "\" w:cs=\"" + font + "\"/>" + italic + "<w:color w:val=\"" + color + "\"/><w:sz w:val=\"" + size + "\"/><w:szCs w:val=\"" + size + "\"/>" + rtl + lang + "</w:rPr>";
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
  return "<w:sdt><w:sdtPr><w:alias w:val=\"" + enc(alias) + "\"/><w:tag w:val=\"field_" + sdtId + "\"/><w:id w:val=\"" + sdtId + "\"/><w:dropDownList>" + list + "</w:dropDownList><w:showingPlcHdr/></w:sdtPr><w:sdtContent>" + run(placeholder, opts) + "</w:sdtContent></w:sdt>";
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
  strong: edge("top", INK, 8) + edge("bottom", BEIGE, 4)
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
  const borders = opts.borders === false
    ? "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/><w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/><w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
    : "<w:tblBorders>" + ["top", "left", "bottom", "right", "insideH", "insideV"].map((s) => edge(s, BEIGE, 4)).join("") + "</w:tblBorders>";
  const indent = opts.indent ? "<w:tblInd w:w=\"" + opts.indent + "\" w:type=\"dxa\"/>" : "";
  const grid = widths.map((w) => "<w:gridCol w:w=\"" + w + "\"/>").join("");
  const mar = "<w:tblCellMar><w:top w:w=\"40\" w:type=\"dxa\"/><w:left w:w=\"85\" w:type=\"dxa\"/><w:bottom w:w=\"40\" w:type=\"dxa\"/><w:right w:w=\"85\" w:type=\"dxa\"/></w:tblCellMar>";
  const tableRows = rows.map((row) => {
    const header = row.header ? "<w:tblHeader w:val=\"true\"/>" : "";
    const height = row.height ? "<w:trHeight w:val=\"" + row.height + "\" w:hRule=\"atLeast\"/>" : "";
    return "<w:tr><w:trPr>" + header + "<w:cantSplit/>" + height + "</w:trPr>" + row.cells.join("") + "</w:tr>";
  }).join("");
  return "<w:tbl><w:tblPr><w:tblW w:w=\"" + widths.reduce((a, b) => a + b, 0) + "\" w:type=\"dxa\"/>" + indent + borders + "<w:tblLayout w:type=\"fixed\"/>" + mar + "<w:tblLook w:firstRow=\"1\" w:lastRow=\"0\" w:firstColumn=\"0\" w:lastColumn=\"0\" w:noHBand=\"0\" w:noVBand=\"1\"/></w:tblPr><w:tblGrid>" + grid + "</w:tblGrid>" + tableRows + "</w:tbl>" + tableGap(opts.keepWithNext);
}

// Metadata 9 pt Inter, Arabic labels 10 pt (letterhead set spec).
function labelCell(en, ar, width, keep) {
  return tc([
    p(en.toUpperCase(), { font: "Inter", size: 18, after: 10, keep }),
    p(ar, { font: "Noto Sans Arabic", size: 20, rtl: true, align: "right", after: 0, keep })
  ], width, { border: "hair" });
}

const valueRun = { font: "Inter", size: 18 };

// A value is a content-control placeholder (ph), a fixed confirmed value (fixed), a dropdown, or raw run XML (inner).
function valueContent(f, keep) {
  const alias = f.alias || (f.ph || f.en).replace(/^Enter /, "");
  let inner;
  if (f.inner) inner = f.inner;
  else if (f.options) inner = dropdown(alias, f.ph, f.options, valueRun);
  else if (f.fixed !== undefined) inner = run(f.fixed, valueRun);
  else inner = sdt(alias, f.ph, valueRun);
  return p("", { after: 0, keep, inner });
}

function valueCell(f, width, keep, span) {
  return tc(valueContent(f, keep), width, { border: "hair", span });
}

const FIELD_W = [2250, 2286, 2250, 2286];
const ITEM_W = [520, 2400, 800, 850, 2250, 2252];

// Fields pair left and right; a field marked full (or the odd last field) takes its own row with the value spanning three columns.
// A short group (up to three rows) stays together; a longer one may break between rows, but its heading always stays with its first two rows.
function fieldRows(sec, fields, keepWithNext = false) {
  const widths = FIELD_W;
  const half = widths[0] + widths[1];
  const rows = sec ? [sectionRow(sec, [2, 2], [half, CONTENT_W - half])] : [];
  const pairs = [];
  for (let i = 0; i < fields.length; i++) {
    const f = fields[i];
    const next = fields[i + 1];
    if (!f.full && next && !next.full) { pairs.push([f, next]); i++; } else pairs.push([f]);
  }
  const total = pairs.length;
  pairs.forEach(([left, right], i) => {
    const keep = total <= 3 ? i < total - 1 || keepWithNext : i === 0 || (keepWithNext && i === total - 1);
    const cells = [labelCell(left.en, left.ar, widths[0], keep)];
    if (right) cells.push(valueCell(left, widths[1], keep), labelCell(right.en, right.ar, widths[2], keep), valueCell(right, widths[3], keep));
    else cells.push(valueCell(left, widths[1] + widths[2] + widths[3], keep, 3));
    rows.push({ cells });
  });
  return tbl(widths, rows, { keepWithNext });
}

// The section heading is the first row of its table so it can never be stranded from the rows below it.
// Jost Regular uppercase over a Beige rule; English left, Arabic right on one line.
function sectionRow(sec, spans, widths, header = false) {
  return { header, cells: [
    tc(p(sec[0].toUpperCase(), { font: "Jost", size: 21, before: 160, after: 40, keep: true, indStart: -85, style: "Heading1" }), widths[0], { border: "band", span: spans[0], valign: "bottom" }),
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
      p(h[0], { font: "Inter", size: 18, color: WHITE, align: enAlign(i), after: 8, keep: true }),
      p(h[1], { font: "Noto Sans Arabic", size: 20, color: WHITE, rtl: true, align: arAlign(i), after: 0, keep: true })
    ], widths[i], { fill: INK, valign: "center" }))
  });
  for (let i = 0; i < ITEM_ROWS; i++) {
    const r = i + 3;
    const cell = (inner, j, align) => tc(p("", { after: 0, keep: true, align, inner }), widths[j], { border: "hair", valign: "center" });
    rows.push({ cells: [
      cell(run(String(i + 1), valueRun), 0, "center"),
      cell(sdt("Description", "Enter Description", valueRun), 1, "left"),
      cell(sdt("Qty", "Enter Qty", valueRun), 2, "center"),
      cell(sdt("Unit", "Enter Unit", valueRun), 3, "center"),
      cell(sdt("Unit Price", "Enter Unit Price", valueRun), 4, "right"),
      cell(field("=C" + r + "*E" + r + " \\# \"#,##0.00\"", "0.00", valueRun), 5, "right")
    ] });
  }
  const labelW = widths.slice(0, 5).reduce((x, y) => x + y, 0);
  totals.forEach((t, idx) => {
    const keep = idx < totals.length - 1;
    const border = t.strong ? "strong" : "hair";
    const ropts = { font: t.strong ? "Jost" : "Inter", size: t.strong ? 21 : 18 };
    let inner;
    if (t.ph) inner = sdt(t.alias || t.en, t.ph, ropts);
    else inner = field(t.instr + " \\# \"#,##0.00\"", "0.00", ropts);
    if (t.bookmark) inner = "<w:bookmarkStart w:id=\"9021\" w:name=\"" + t.bookmark + "\"/>" + inner + "<w:bookmarkEnd w:id=\"9021\"/>";
    // One line per total: English at the start, Arabic at the right edge of the label cell via a right tab.
    const arOpts = { font: "Noto Sans Arabic", size: t.strong ? 22 : 20, rtl: true };
    const labelInner = run(t.en.toUpperCase(), ropts) + "<w:r><w:tab/></w:r>" + run(t.ar, arOpts);
    rows.push({ cells: [
      tc(p("", { after: 0, keep, inner: labelInner, tabRight: labelW - 170 }), labelW, { border, span: 5 }),
      tc(p("", { after: 0, keep, align: "right", inner }), widths[5], { border })
    ] });
  });
  return tbl(widths, rows);
}

const VAT_ROWS = [
  { en: "Subtotal", ar: "المجموع الفرعي", instr: "=SUM(F3:F6)" },
  { en: "VAT rate (%)", ar: "نسبة ضريبة القيمة المضافة", ph: "15", alias: "VAT Rate" },
  { en: "VAT amount (SAR)", ar: "مبلغ ضريبة القيمة المضافة", instr: "=(B7*B8)/100" },
  { en: "Total", ar: "الإجمالي", instr: "=B7+B9", strong: true }
];

// An entry box at least four lines tall, under a bilingual heading row. paragraphs are ready-made w:p strings.
const ENTRY_MIN_HEIGHT = 1300;
function noteBlock(en, ar, paragraphs, height = ENTRY_MIN_HEIGHT) {
  const half = Math.floor(CONTENT_W / 2);
  return tbl([half, CONTENT_W - half], [
    sectionRow([en, ar], [1, 1], [half, CONTENT_W - half]),
    { height, cells: [tc(paragraphs, CONTENT_W, { border: "hair", span: 2, valign: "top" })] }
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
const refField = (en, ar) => ({ en, ar, inner: complexField("DOCPROPERTY RefNo \\* MERGEFORMAT", REF_PLACEHOLDER, valueRun) });
const CURRENCY = { en: "Currency", ar: "العملة", fixed: "SAR" };
const OWNER_CONTACT = "Mashal Abdulrahman, GM / Owner";
const LEGAL_NAME = { en: "Registered Legal Name (Trading Name: GEM)", ar: "الاسم القانوني المسجل", ph: "Enter Registered Legal Name" };
const BUSINESS_ADDRESS = { en: "Business / National Address", ar: "عنوان المنشأة / العنوان الوطني", ph: "Enter Business / National Address" };
const CR_NUMBER = { en: "Commercial Registration No.", ar: "رقم السجل التجاري", ph: "Enter Commercial Registration No." };
const TAX_ID = (en, ar) => ({ en, ar, ph: "Enter Tax Identifier" });
const NOTICE = "Verify payment details through a previously known channel before making payment.";
const NOTICE_AR = "تحقّق من بيانات الدفع عبر وسيلة اتصال معروفة مسبقاً قبل السداد.";
const staticPara = (text, opts = {}) => entryPara(run(text, { font: "Inter", size: 18, ...opts }));
const arabicPara = (text) => p(text, { font: "Noto Sans Arabic", size: 20, rtl: true, align: "right", after: 40, line: 288 });

const docs = [
  {
    filename: "GEM_Request_for_Quotation_Template_working.docx",
    title: "Request for Quotation",
    continued: ["RFQ continued", "تكملة طلب عرض السعر"],
    body:
      titleBlock("Request for Quotation", "طلب تقديم عرض سعر") +
      fieldRows(["Request Details", "بيانات الطلب"], [
        refField("RFQ Number", "رقم طلب عرض السعر"),
        dateField("Issue Date", "تاريخ الإصدار", "Issue Date"),
        LEGAL_NAME,
        BUSINESS_ADDRESS,
        dateField("Response Due", "موعد الرد", "Response Due Date"),
        { en: "Requester", ar: "مقدم الطلب", fixed: OWNER_CONTACT },
        { en: "Requester Email", ar: "بريد مقدم الطلب", fixed: CONTACT_EMAIL },
        { en: "Project / Reference", ar: "المشروع / المرجع", ph: "Enter Project or Reference" },
        { en: "Requester Phone", ar: "هاتف مقدم الطلب", fixed: CONTACT_PHONE },
        CR_NUMBER
      ]) +
      fieldRows(["Supplier Details", "بيانات المورد"], [
        { en: "Supplier Registered Legal Name", ar: "الاسم القانوني المسجل للمورد", ph: "Enter Supplier Registered Legal Name" },
        { en: "Contact Name", ar: "اسم جهة التواصل", ph: "Enter Supplier Contact" },
        { en: "Email", ar: "البريد الإلكتروني", ph: "Enter Supplier Email" },
        { en: "Address", ar: "العنوان", ph: "Enter Supplier Address" },
        { en: "Supplier Quote Reference", ar: "مرجع عرض المورد", ph: "Enter Supplier Quote Reference" },
        { en: "Supplier Phone", ar: "هاتف المورد", ph: "Enter Supplier Phone" },
        { en: "Supplier Confirmation", ar: "تأكيد المورد", ph: "Enter Supplier Confirmation" },
        { en: "Supplier Tax Identifier", ar: "الرقم الضريبي للمورد", ph: "Enter Supplier Tax Identifier" }
      ]) +
      itemsTable(["Items or Services", "البنود أو الخدمات"], [
        { en: "Subtotal", ar: "المجموع الفرعي", instr: "=SUM(F3:F6)" },
        { en: "Total", ar: "الإجمالي", instr: "=B7", strong: true }
      ]) +
      fieldRows(["Delivery and Commercial Response", "التسليم والرد التجاري"], [
        { en: "Delivery Location", ar: "موقع التسليم", ph: "Enter Delivery Address" },
        dateField("Requested Delivery", "موعد التسليم المطلوب", "Requested Delivery Date"),
        { en: "Payment Terms", ar: "شروط الدفع", ph: "Enter Requested Payment Terms" },
        dateField("Quote Valid Until", "صلاحية العرض حتى", "Quote Validity Date"),
        CURRENCY,
        { en: "Lead Time", ar: "مدة التوريد", ph: "Enter Supplier Lead Time" },
        { en: "Prices Are", ar: "الأسعار", ph: "Select VAT treatment", options: ["VAT-inclusive", "VAT-exclusive"], full: true }
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
      fieldRows(["Quotation Details", "بيانات عرض السعر"], [
        refField("Quotation Number", "رقم عرض السعر"),
        dateField("Issue Date", "تاريخ الإصدار", "Issue Date"),
        dateField("Valid Until", "صالح حتى", "Quote Validity Date"),
        CURRENCY,
        { en: "Customer", ar: "العميل", ph: "Enter Customer Name" },
        { en: "Customer Contact", ar: "جهة التواصل", ph: "Enter Customer Contact" },
        { en: "Customer Address", ar: "عنوان العميل", ph: "Enter Customer Address" },
        { en: "Customer Email", ar: "بريد العميل", ph: "Enter Customer Email" },
        { en: "Project / Property", ar: "المشروع / المنشأة", ph: "Enter Project or Property" },
        { en: "Customer PO / Purchase Order", ar: "أمر شراء العميل", ph: "Enter Customer PO Number" }
      ]) +
      fieldRows(["Issuer and Customer Contact", "بيانات الجهة المصدرة والعميل"], [
        LEGAL_NAME,
        { en: "Business Email", ar: "البريد الإلكتروني", fixed: CONTACT_EMAIL },
        BUSINESS_ADDRESS,
        { en: "Sales Contact", ar: "جهة التواصل للمبيعات", ph: "Enter Sales Contact Name / Role" },
        { en: "Business Phone", ar: "هاتف المنشأة", fixed: CONTACT_PHONE },
        TAX_ID("Tax Identifier", "الرقم الضريبي للمنشأة")
      ]) +
      noteBlock("Scope Summary", "ملخص النطاق", [entryPara(sdt("Scope Summary", "Enter scope summary", valueRun))]) +
      noteBlock("Assumptions, Exclusions & Terms", "الافتراضات والاستثناءات والشروط", [entryPara(sdt("Assumptions, Exclusions and Terms", "Enter assumptions, exclusions and terms", valueRun))]) +
      itemsTable(["Pricing", "الأسعار"], VAT_ROWS) +
      fieldRows(["Delivery and Payment", "التسليم والدفع"], [
        { en: "Delivery Location", ar: "موقع التسليم", ph: "Enter Delivery Address" },
        dateField("Estimated Delivery", "موعد التسليم التقديري", "Estimated Delivery Date"),
        { en: "Payment Terms", ar: "شروط الدفع", ph: "Enter Payment Terms" }
      ]) +
      fieldRows(["Customer Acceptance", "قبول العميل"], [
        { en: "Name / Role", ar: "الاسم / الصفة", ph: "Enter Customer Name / Role" },
        dateField("Signature / Date", "التوقيع / التاريخ", "Signature / Date")
      ])
  },
  {
    filename: "GEM_Invoice_Template_working.docx",
    title: "Invoice",
    continued: ["Invoice continued", "تكملة الفاتورة"],
    body:
      titleBlock("Invoice", "فاتورة") +
      fieldRows(["Invoice Details", "بيانات الفاتورة"], [
        refField("Invoice Number", "رقم الفاتورة"),
        dateField("Issue Date", "تاريخ الإصدار", "Issue Date"),
        dateField("Payment Due", "تاريخ الاستحقاق", "Payment Due Date"),
        CURRENCY,
        { en: "Purchase Order", ar: "أمر الشراء", ph: "Enter Customer PO Number" },
        { en: "Related Quotation", ar: "عرض السعر المرتبط", ph: "Enter Quotation Reference" },
        { ...dateField("Supply Date", "تاريخ التوريد", "Supply Date"), full: true },
        { en: "Total Amount Due", ar: "إجمالي المبلغ المستحق", inner: complexField("REF InvoiceTotal", "0.00", valueRun), full: true }
      ]) +
      fieldRows(["Supplier and Customer", "المورد والعميل"], [
        LEGAL_NAME,
        BUSINESS_ADDRESS,
        TAX_ID("Supplier Tax Identifier", "الرقم الضريبي للمورد"),
        { en: "Supplier Contact", ar: "جهة التواصل لدى المورد", fixed: OWNER_CONTACT },
        { en: "Supplier Email", ar: "بريد المورد", fixed: CONTACT_EMAIL },
        { en: "Supplier Phone", ar: "هاتف المورد", fixed: CONTACT_PHONE },
        { en: "Customer", ar: "العميل", ph: "Enter Customer Legal Name" },
        { en: "Billing Address", ar: "عنوان الفوترة", ph: "Enter Customer Billing Address" },
        { en: "Customer Email", ar: "بريد العميل", ph: "Enter Customer Email" },
        { en: "Customer Tax Identifier", ar: "الرقم الضريبي للعميل", ph: "Enter Customer Tax Identifier, if applicable" },
        CR_NUMBER
      ]) +
      itemsTable(["Items or Services", "البنود أو الخدمات"], [
        ...VAT_ROWS.slice(0, 3),
        { ...VAT_ROWS[3], bookmark: "InvoiceTotal" },
        { en: "Amount Paid", ar: "المبلغ المدفوع", ph: "Enter Amount Paid" },
        { en: "Balance Due", ar: "الرصيد المستحق", instr: "=B10-B11", strong: true }
      ]) +
      fieldRows(["Payment Instructions", "تعليمات الدفع"], [
        { en: "Payee / Account Name", ar: "المستفيد / اسم الحساب", ph: "Enter Payee Name" },
        { en: "Bank", ar: "البنك", ph: "Enter Bank Name" },
        { en: "Account Number", ar: "رقم الحساب", ph: "Enter Account Number" },
        { en: "IBAN", ar: "رقم الآيبان (IBAN)", ph: "Enter IBAN" },
        { en: "Payment Reference", ar: "مرجع الدفع", ph: "Enter Payment Reference" },
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
      fieldRows(["Order Details", "بيانات أمر الشراء"], [
        refField("Purchase Order Number", "رقم أمر الشراء"),
        dateField("Order Date", "تاريخ الطلب", "Order Date"),
        { en: "Requester / Buyer Contact", ar: "مقدم الطلب / جهة تواصل المشتري", fixed: OWNER_CONTACT },
        { en: "Requester Email", ar: "بريد مقدم الطلب", fixed: CONTACT_EMAIL },
        { en: "Related Quotation", ar: "عرض السعر المرتبط", ph: "Enter Quotation Reference" },
        { en: "RFQ Reference", ar: "مرجع طلب عرض السعر", ph: "Enter RFQ Reference" },
        CURRENCY,
        { en: "Requester Phone", ar: "هاتف مقدم الطلب", fixed: CONTACT_PHONE }
      ]) +
      fieldRows(["Buyer Details", "بيانات المشتري"], [
        LEGAL_NAME,
        TAX_ID("Buyer Tax Identifier", "الرقم الضريبي للمشتري"),
        BUSINESS_ADDRESS,
        CR_NUMBER
      ]) +
      fieldRows(["Supplier Details", "بيانات المورد"], [
        { en: "Supplier Name", ar: "اسم المورد", ph: "Enter Supplier Registered Name" },
        { en: "Supplier Contact", ar: "جهة التواصل لدى المورد", ph: "Enter Supplier Contact" },
        { en: "Supplier Email", ar: "بريد المورد", ph: "Enter Supplier Email" },
        { en: "Supplier Address", ar: "عنوان المورد", ph: "Enter Supplier Address" },
        { en: "Supplier Phone", ar: "هاتف المورد", ph: "Enter Supplier Phone" },
        { en: "Supplier Tax Identifier", ar: "الرقم الضريبي للمورد", ph: "Enter Supplier Tax Identifier, if applicable" }
      ]) +
      itemsTable(["Items or Services", "البنود أو الخدمات"], VAT_ROWS) +
      fieldRows(["Delivery and Billing", "التسليم والفوترة"], [
        { en: "Deliver To", ar: "جهة التسليم", ph: "Enter Recipient / Department" },
        { en: "Delivery Address", ar: "عنوان التسليم", ph: "Enter Delivery Address" },
        dateField("Requested Delivery Date", "تاريخ التسليم المطلوب", "Requested Delivery Date"),
        { en: "Billing Address", ar: "عنوان الفوترة", ph: "Enter Billing Address" },
        { en: "Shipping / Delivery Terms", ar: "شروط الشحن والتسليم", ph: "Enter Agreed Shipping / Delivery Terms" },
        { en: "Special Instructions", ar: "تعليمات خاصة", ph: "Enter Special Instructions, if any" },
        { en: "Payment Terms", ar: "شروط الدفع", ph: "Enter Agreed Payment Terms" }
      ])
  }
];

if (!fs.existsSync(LOGO)) throw new Error("Approved V3.0 logo asset is missing: " + LOGO);
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
for (const doc of docs) createDocx(doc);
console.log("Created " + docs.length + " editable A4 DOCX templates in " + OUT);
console.log("Embedded exact V3.0 supplied logo: " + path.relative(ROOT, LOGO));
