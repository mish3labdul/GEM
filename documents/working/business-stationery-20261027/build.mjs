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
const enc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");

// Regular weights only: the letterhead set specifies no bold synthesis, and no Bold font files are recorded in the brand kit.
function p(text, opts = {}) {
  const font = opts.font || "Inter";
  const size = opts.size || 18;
  const color = opts.color || INK;
  // Arabic paragraphs use logical alignment: "right" (visual) is the start edge, "left" the end edge.
  const requested = opts.align || "left";
  const align = opts.rtl ? ({ left: "end", right: "start" }[requested] || requested) : requested;
  const before = opts.before || 0;
  const after = opts.after === undefined ? 35 : opts.after;
  const line = opts.line ? "w:line=\"" + opts.line + "\" w:lineRule=\"exact\"" : "w:line=\"250\" w:lineRule=\"auto\"";
  const italic = opts.italic ? "<w:i/><w:iCs/>" : "";
  const bidi = opts.rtl ? "<w:bidi w:val=\"1\"/>" : "";
  const rtl = opts.rtl ? "<w:rtl w:val=\"1\"/>" : "";
  const lang = opts.rtl ? "<w:lang w:val=\"ar-SA\" w:bidi=\"ar-SA\"/>" : "<w:lang w:val=\"en-GB\"/>";
  const keep = opts.keep ? "<w:keepNext/>" : "";
  const ind = opts.indStart ? "<w:ind w:start=\"" + opts.indStart + "\"/>" : "";
  const pStyle = opts.style ? "<w:pStyle w:val=\"" + opts.style + "\"/>" : "";
  const textXml = text ? "<w:r><w:rPr><w:rFonts w:ascii=\"" + font + "\" w:hAnsi=\"" + font + "\" w:eastAsia=\"" + font + "\" w:cs=\"" + font + "\"/>" + italic + "<w:color w:val=\"" + color + "\"/><w:sz w:val=\"" + size + "\"/><w:szCs w:val=\"" + size + "\"/>" + rtl + lang + "</w:rPr><w:t xml:space=\"preserve\">" + enc(text) + "</w:t></w:r>" : "";
  return "<w:p><w:pPr>" + pStyle + keep + bidi + "<w:spacing w:before=\"" + before + "\" w:after=\"" + after + "\" " + line + "/>" + ind + "<w:jc w:val=\"" + align + "\"/></w:pPr>" + textXml + "</w:p>";
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
    return "<w:tr><w:trPr>" + header + "<w:cantSplit/></w:trPr>" + row.cells.join("") + "</w:tr>";
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

function valueCell(value, width, keep, span) {
  return tc(p(value, { font: "Inter", size: 18, italic: true, after: 0, keep }), width, { border: "hair", span });
}

const FIELD_W = [2250, 2286, 2250, 2286];
const ITEM_W = [520, 2400, 800, 850, 2250, 2252];
const TOTAL_W = [5900, 3172];

// A short group (up to three rows) stays together; a longer one may break between rows, but its heading always stays with its first two rows.
function fieldRows(sec, fields, keepWithNext = false) {
  const widths = FIELD_W;
  const half = widths[0] + widths[1];
  const rows = sec ? [sectionRow(sec, [2, 2], [half, CONTENT_W - half])] : [];
  const total = Math.ceil(fields.length / 2);
  for (let i = 0; i < fields.length; i += 2) {
    const left = fields[i];
    const right = fields[i + 1];
    const keep = total <= 3 ? i / 2 < total - 1 || keepWithNext : i === 0 || (keepWithNext && i / 2 === total - 1);
    const cells = [labelCell(left.en, left.ar, widths[0], keep)];
    if (right) {
      cells.push(valueCell(left.value, widths[1], keep), labelCell(right.en, right.ar, widths[2], keep), valueCell(right.value, widths[3], keep));
    } else {
      // Odd final field spans the remaining three columns.
      cells.push(valueCell(left.value, widths[1] + widths[2] + widths[3], keep, 3));
    }
    rows.push({ cells });
  }
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
function titleBlock(kicker, en, ar, note) {
  const half = Math.floor(CONTENT_W / 2);
  const wide = CONTENT_W + 170 - half; // table sits 85 twips outside each margin so the text edges align with it
  const titleRow = tbl([half, wide], [{ cells: [
    tc(p(en, { font: "Jost", size: 42, after: 0, keep: true, style: "Title" }), half, { valign: "bottom" }),
    tc(p(ar, { font: "Noto Sans Arabic", size: 34, rtl: true, align: "right", after: 0, keep: true }), wide, { valign: "bottom" })
  ] }], { borders: false, keepWithNext: true, indent: -85 });
  return p(kicker.toUpperCase(), { font: "Inter", size: 18, after: 35, keep: true }) +
    titleRow +
    (note ? p(note, { font: "Inter", size: 21, line: 336, before: 60, after: 60 }) : "");
}

// Item rows stay together; withTotals also keeps the table on the same page as the totals that follow.
function lineItems(sec, count = 4, withTotals = false) {
  const widths = ITEM_W;
  const headers = [
    ["No.", "م"],
    ["Item / Service", "البند / الخدمة"],
    ["Qty", "الكمية"],
    ["Unit", "الوحدة"],
    ["Unit Price", "سعر الوحدة"],
    ["Line Total", "إجمالي البند"]
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
  for (let i = 0; i < count; i++) {
    const keep = i < count - 1 || withTotals; // keep the table whole, and attached to any totals below it
    const vals = [String(i + 1), "[Description]", "[Qty]", "[Unit]", "[Currency] [Unit Price]", "[Currency] [Line Total]"];
    rows.push({ cells: vals.map((v, j) => tc(p(v, { font: "Inter", size: 18, italic: true, align: j === 0 || j === 2 || j === 3 ? "center" : j >= 4 ? "right" : "left", after: 0, keep }), widths[j], { border: "hair", valign: "center" })) });
  }
  return tbl(widths, rows, { keepWithNext: withTotals });
}

function totalsTable(invoice = false) {
  const rows = [];
  const lines = [
    ["Subtotal", "المجموع الفرعي", "[Currency] [Subtotal]"],
    ["Tax / VAT (if applicable)", "الضريبة عند انطباقها", "[Applicable Tax Name] / [Rate %] / [Tax Amount]"],
    ["Total", "الإجمالي", "[Currency] [Total Amount]"]
  ];
  if (invoice) {
    lines.push(["Amount paid", "المبلغ المدفوع", "[Currency] [Amount Paid]"]);
    lines.push(["Balance due", "الرصيد المستحق", "[Currency] [Balance Due]"]);
  }
  lines.forEach((line, idx) => {
    const strong = line[0] === "Total" || line[0] === "Balance due";
    const keep = idx < lines.length - 1;
    const border = strong ? "strong" : "hair";
    rows.push({ cells: [
      tc([
        p(line[0].toUpperCase(), { font: strong ? "Jost" : "Inter", size: strong ? 21 : 18, after: 6, keep }),
        p(line[1], { font: "Noto Sans Arabic", size: strong ? 22 : 20, rtl: true, align: "right", after: 0, keep })
      ], TOTAL_W[0], { border }),
      tc(p(line[2], { font: "Inter", size: strong ? 21 : 18, italic: !strong, align: "right", after: 0, keep }), TOTAL_W[1], { border })
    ] });
  });
  return tbl(TOTAL_W, rows);
}

function noteBlock(en, ar, placeholder) {
  const half = Math.floor(CONTENT_W / 2);
  return tbl([half, CONTENT_W - half], [
    sectionRow([en, ar], [1, 1], [half, CONTENT_W - half]),
    { cells: [tc(p(placeholder, { font: "Inter", size: 18, italic: true, line: 288, after: 0 }), CONTENT_W, { border: "hair", span: 2 })] }
  ]);
}

const NS = "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\"";

// First-page header: logo, then the fixed tagline (Jost Regular 10.5 pt, 38 twip expanded spacing), as in the letterhead set.
function headerFirstXml() {
  const tagline = "<w:p><w:pPr><w:spacing w:before=\"680\" w:after=\"227\" w:line=\"300\" w:lineRule=\"exact\"/><w:jc w:val=\"left\"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=\"Jost\" w:hAnsi=\"Jost\" w:eastAsia=\"Jost\" w:cs=\"Jost\"/><w:color w:val=\"" + INK + "\"/><w:spacing w:val=\"38\"/><w:sz w:val=\"21\"/><w:szCs w:val=\"21\"/><w:lang w:val=\"en-GB\"/></w:rPr><w:t>HOSPITALITY, IN PERFECT PROPORTION</w:t></w:r></w:p>";
  return "<w:hdr " + NS + ">" + imageParagraph() + tagline + "</w:hdr>";
}

// Continuation header: quiet identifier and reference only.
function headerContinuationXml() {
  const run = (text) => "<w:r><w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\" w:eastAsia=\"Inter\" w:cs=\"Inter\"/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"16\"/><w:szCs w:val=\"16\"/><w:lang w:val=\"en-GB\"/></w:rPr><w:t xml:space=\"preserve\">" + text + "</w:t></w:r>";
  return "<w:hdr " + NS + "><w:p><w:pPr><w:spacing w:after=\"0\" w:line=\"240\" w:lineRule=\"auto\"/><w:jc w:val=\"left\"/></w:pPr>" + run("GEM™") + run("    [REFERENCE NUMBER]") + "</w:p></w:hdr>";
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
// Line 1 carries address, contact placeholders and the page number on a right tab; line 2 carries the working and issue status.
function footerXml() {
  const line = (inner, rule, tab) => "<w:p><w:pPr>" + (rule ? "<w:pBdr><w:top w:val=\"single\" w:sz=\"4\" w:space=\"6\" w:color=\"" + BEIGE + "\"/></w:pBdr>" : "") + (tab ? "<w:tabs><w:tab w:val=\"right\" w:pos=\"" + CONTENT_W + "\"/></w:tabs>" : "") + "<w:spacing w:after=\"30\" w:line=\"252\" w:lineRule=\"exact\"/><w:jc w:val=\"left\"/></w:pPr>" + inner + "</w:p>";
  return "<w:ftr " + NS + ">" +
    line(footerRun("GEM\u2122   [ADDRESS] \u00B7 [CITY] \u00B7 [COUNTRY] \u00B7 [POSTAL CODE]   [T]   [E]   [W]") + "<w:r><w:tab/></w:r>" + footerRun("Page ") + pageField("PAGE") + footerRun(" of ") + pageField("NUMPAGES"), true, true) +
    line(footerRun("WORKING APPLICATION / PENDING VALIDATION \u00B7 EXTERNAL ISSUE RESTRICTED (D8 PENDING)")) +
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
    "<Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/><Override PartName=\"/word/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml\"/><Override PartName=\"/word/header1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml\"/><Override PartName=\"/word/header2.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml\"/><Override PartName=\"/word/footer1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml\"/><Override PartName=\"/word/footer2.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml\"/><Override PartName=\"/word/settings.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml\"/><Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/><Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/>" +
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
    "<Relationship Id=\"rIdDocument\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/><Relationship Id=\"rIdCore\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/><Relationship Id=\"rIdApp\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties\" Target=\"docProps/app.xml\"/></Relationships>";
  const docRels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">" +
    "<Relationship Id=\"rIdStyles\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" Target=\"styles.xml\"/><Relationship Id=\"rIdHeaderFirst\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/header\" Target=\"header1.xml\"/><Relationship Id=\"rIdHeader\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/header\" Target=\"header2.xml\"/><Relationship Id=\"rIdFooterFirst\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer\" Target=\"footer1.xml\"/><Relationship Id=\"rIdFooter\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer\" Target=\"footer2.xml\"/><Relationship Id=\"rIdSettings\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings\" Target=\"settings.xml\"/></Relationships>";
  const headerRels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rIdLogo\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\"media/gem-horizontal-ink.png\"/></Relationships>";
  const title = enc(doc.title + " | GEM Business Stationery Working Suite");
  const core = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><dc:title>" + title + "</dc:title><dc:subject>Editable bilingual business document template</dc:subject><dc:creator>GEM</dc:creator><cp:keywords>WORKING INTERNAL REVIEW DRAFT</cp:keywords><dc:description>Working template. Business details and external-issue acceptance remain pending.</dc:description><dcterms:created xsi:type=\"dcterms:W3CDTF\">2026-10-27T00:00:00Z</dcterms:created></cp:coreProperties>";
  const app = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\"><Application>GEM stationery template builder</Application></Properties>";
  const settings = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><w:settings xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"><w:defaultTabStop w:val=\"720\"/><w:compat><w:compatSetting w:name=\"compatibilityMode\" w:uri=\"http://schemas.microsoft.com/office/word\" w:val=\"15\"/></w:compat></w:settings>";
  const entries = [
    ["[Content_Types].xml", contentTypes()],
    ["_rels/.rels", rels],
    ["docProps/core.xml", core],
    ["docProps/app.xml", app],
    ["word/document.xml", docXml(doc.body)],
    ["word/styles.xml", stylesXml()],
    ["word/header1.xml", headerFirstXml()],
    ["word/header2.xml", headerContinuationXml()],
    ["word/footer1.xml", footerXml()],
    ["word/footer2.xml", footerXml()],
    ["word/_rels/document.xml.rels", docRels],
    ["word/_rels/header1.xml.rels", headerRels],
    ["word/settings.xml", settings],
    ["word/media/gem-horizontal-ink.png", logo]
  ];
  fs.writeFileSync(path.join(OUT, doc.filename), zip(entries));
}

const docs = [
  {
    filename: "GEM_Request_for_Quotation_Template_working.docx",
    title: "Request for Quotation",
    body:
      titleBlock("Template 01 | Procurement", "Request for Quotation", "طلب تقديم عرض سعر", "Please complete the requester and supplier fields, describe the requirement, and return a priced response by the stated date. Suppliers complete the unit price and line total columns.") +
      fieldRows(["Request Details", "بيانات الطلب"], [
        { en: "RFQ Number", ar: "رقم طلب عرض السعر", value: "[RFQ Number]" },
        { en: "Issue Date", ar: "تاريخ الإصدار", value: "[Issue Date]" },
        { en: "Requesting Organization", ar: "الجهة الطالبة", value: "[Requesting Organization]" },
        { en: "Organization Address", ar: "عنوان الجهة الطالبة", value: "[Requesting Organization Address]" },
        { en: "Response Due", ar: "موعد الرد", value: "[Response Due Date]" },
        { en: "Requester", ar: "مقدم الطلب", value: "[Requester Name / Role]" },
        { en: "Requester Email", ar: "بريد مقدم الطلب", value: "[Requester Email]" },
        { en: "Project / Reference", ar: "المشروع / المرجع", value: "[Project or Reference]" }
      ]) +
      fieldRows(["Supplier Details", "بيانات المورد"], [
        { en: "Supplier Name", ar: "اسم المورد", value: "[Supplier Name]" },
        { en: "Contact Name", ar: "اسم جهة التواصل", value: "[Supplier Contact]" },
        { en: "Email", ar: "البريد الإلكتروني", value: "[Supplier Email]" },
        { en: "Address", ar: "العنوان", value: "[Supplier Address]" }
      ]) +
      lineItems(["Items or Services", "البنود أو الخدمات"], 4) +
      fieldRows(["Delivery and Commercial Response", "التسليم والرد التجاري"], [
        { en: "Delivery Location", ar: "موقع التسليم", value: "[Delivery Address]" },
        { en: "Requested Delivery", ar: "موعد التسليم المطلوب", value: "[Requested Delivery Date]" },
        { en: "Payment Terms", ar: "شروط الدفع", value: "[Requested Payment Terms]" },
        { en: "Quote Valid Until", ar: "صلاحية العرض حتى", value: "[Quote Validity Date]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" },
        { en: "Lead Time", ar: "مدة التوريد", value: "[Supplier Lead Time]" }
      ], true) +
      noteBlock("Response Instructions", "تعليمات الرد", "Return the completed pricing and delivery information to [Requester Email] by [Response Due Date]. Include product or service specifications and any supporting documents relevant to this request.")
  },
  {
    filename: "GEM_Quotation_Proposal_Template_working.docx",
    title: "Quotation and Proposal",
    body:
      titleBlock("Template 02 | Customer Response", "Quotation and Proposal", "عرض سعر ومقترح", "Describe the requested scope and provide clear prices, delivery details, payment terms, and a validity date.") +
      fieldRows(["Quotation Details", "بيانات عرض السعر"], [
        { en: "Quotation Number", ar: "رقم عرض السعر", value: "[Quotation Number]" },
        { en: "Issue Date", ar: "تاريخ الإصدار", value: "[Issue Date]" },
        { en: "Valid Until", ar: "صالح حتى", value: "[Quote Validity Date]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" },
        { en: "Customer", ar: "العميل", value: "[Customer Name]" },
        { en: "Customer Contact", ar: "جهة التواصل", value: "[Customer Contact]" },
        { en: "Customer Address", ar: "عنوان العميل", value: "[Customer Address]" },
        { en: "Customer Email", ar: "بريد العميل", value: "[Customer Email]" },
        { en: "Project / Property", ar: "المشروع / المنشأة", value: "[Project or Property]" },
        { en: "Prepared By", ar: "إعداد", value: "[Name / Role]" }
      ]) +
      noteBlock("Scope Summary", "ملخص النطاق", "[Summarize the requested work, proposed items or services, and any relevant assumptions supplied by the customer.]") +
      lineItems(["Pricing", "الأسعار"], 4, true) +
      totalsTable(false) +
      fieldRows(["Issuer and Customer Contact", "بيانات الجهة والعميل"], [
        { en: "Registered Entity", ar: "الاسم المسجل للمنشأة", value: "[Registered Entity Name]" },
        { en: "Business Email", ar: "البريد الإلكتروني", value: "[Business Email]" },
        { en: "Business Address", ar: "عنوان المنشأة", value: "[Company Address]" },
        { en: "Sales Contact", ar: "جهة التواصل للمبيعات", value: "[Sales Contact Name / Role]" },
        { en: "Business Phone", ar: "هاتف المنشأة", value: "[Business Phone]" },
        { en: "Tax Identifier", ar: "الرقم الضريبي للمنشأة", value: "[Issuer Tax Identifier, if applicable]" }
      ]) +
      fieldRows(["Delivery and Payment", "التسليم والدفع"], [
        { en: "Delivery Location", ar: "موقع التسليم", value: "[Delivery Address]" },
        { en: "Estimated Delivery", ar: "موعد التسليم التقديري", value: "[Estimated Delivery Date]" },
        { en: "Payment Terms", ar: "شروط الدفع", value: "[Payment Terms]" }
      ]) +
      fieldRows(["Customer Review", "مراجعة العميل"], [
        { en: "Name / Role", ar: "الاسم / الصفة", value: "[Customer Name / Role]" },
        { en: "Signature / Date", ar: "التوقيع / التاريخ", value: "[Signature / Date]" }
      ])
  },
  {
    filename: "GEM_Invoice_Template_working.docx",
    title: "Invoice",
    body:
      titleBlock("Template 03 | Accounts", "Invoice", "فاتورة", "Enter the applicable invoice, customer, pricing, tax, due-date, and payment details before issue.") +
      fieldRows(["Invoice Details", "بيانات الفاتورة"], [
        { en: "Invoice Number", ar: "رقم الفاتورة", value: "[Invoice Number]" },
        { en: "Issue Date", ar: "تاريخ الإصدار", value: "[Issue Date]" },
        { en: "Payment Due", ar: "تاريخ الاستحقاق", value: "[Payment Due Date]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" },
        { en: "Purchase Order", ar: "أمر الشراء", value: "[Customer PO Number]" },
        { en: "Related Quotation", ar: "عرض السعر المرتبط", value: "[Quotation Reference]" }
      ]) +
      fieldRows(["Supplier and Customer", "المورد والعميل"], [
        { en: "Supplier / Issuer", ar: "المورد / الجهة المصدرة", value: "[Registered Entity Name]" },
        { en: "Supplier Address", ar: "عنوان المورد", value: "[Company Address]" },
        { en: "Supplier Tax Identifier", ar: "الرقم الضريبي للمورد", value: "[Supplier Tax Identifier, if applicable]" },
        { en: "Supplier Contact", ar: "جهة التواصل لدى المورد", value: "[Supplier Contact]" },
        { en: "Supplier Email", ar: "بريد المورد", value: "[Supplier Email]" },
        { en: "Supplier Phone", ar: "هاتف المورد", value: "[Supplier Phone]" },
        { en: "Customer", ar: "العميل", value: "[Customer Legal Name]" },
        { en: "Billing Address", ar: "عنوان الفاتورة", value: "[Customer Billing Address]" },
        { en: "Customer Email", ar: "بريد العميل", value: "[Customer Email]" },
        { en: "Customer Tax Identifier", ar: "الرقم الضريبي للعميل", value: "[Customer Tax Identifier, if applicable]" }
      ]) +
      lineItems(["Items or Services", "البنود أو الخدمات"], 4, true) +
      totalsTable(true) +
      fieldRows(["Payment Instructions", "تعليمات الدفع"], [
        { en: "Payee / Account Name", ar: "المستفيد / اسم الحساب", value: "[Payee Name]" },
        { en: "Bank", ar: "البنك", value: "[Bank Name]" },
        { en: "Account Number", ar: "رقم الحساب", value: "[Account Number]" },
        { en: "IBAN / Routing", ar: "رقم الآيبان / التوجيه", value: "[IBAN / Routing Details]" },
        { en: "Payment Reference", ar: "مرجع الدفع", value: "[Payment Reference]" },
        { en: "Contact Email", ar: "بريد التواصل", value: "[Accounts Contact Email]" }
      ]) +
      noteBlock("Notes and Terms", "الملاحظات والشروط", "[Notes and terms to be confirmed by the owner before issue.]")
  },
  {
    filename: "GEM_Purchase_Order_Template_working.docx",
    title: "Purchase Order",
    body:
      titleBlock("Template 04 | Procurement", "Purchase Order", "أمر شراء", "Complete all buyer, supplier, delivery, pricing, and authorization fields using approved commercial details.") +
      fieldRows(["Order Details", "بيانات الطلب"], [
        { en: "Purchase Order Number", ar: "رقم أمر الشراء", value: "[Purchase Order Number]" },
        { en: "Order Date", ar: "تاريخ الطلب", value: "[Order Date]" },
        { en: "Requester", ar: "مقدم الطلب", value: "[Requester Name / Role]" },
        { en: "Requester Email", ar: "بريد مقدم الطلب", value: "[Requester Email]" },
        { en: "Related Quotation", ar: "عرض السعر المرتبط", value: "[Quotation Reference]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" }
      ]) +
      fieldRows(["Buyer Details", "بيانات المشتري"], [
        { en: "Buyer Legal Entity", ar: "اسم المشتري المسجل", value: "[Registered Entity Name]" },
        { en: "Buyer Tax Identifier", ar: "الرقم الضريبي للمشتري", value: "[Buyer Tax Identifier, if applicable]" }
      ]) +
      fieldRows(["Supplier Details", "بيانات المورد"], [
        { en: "Supplier Name", ar: "اسم المورد", value: "[Supplier Registered Name]" },
        { en: "Supplier Contact", ar: "جهة التواصل لدى المورد", value: "[Supplier Contact]" },
        { en: "Supplier Email", ar: "بريد المورد", value: "[Supplier Email]" },
        { en: "Supplier Address", ar: "عنوان المورد", value: "[Supplier Address]" },
        { en: "Supplier Phone", ar: "هاتف المورد", value: "[Supplier Phone]" },
        { en: "Supplier Tax Identifier", ar: "الرقم الضريبي للمورد", value: "[Supplier Tax Identifier, if applicable]" }
      ]) +
      fieldRows(["Delivery and Billing", "التسليم والفوترة"], [
        { en: "Deliver To", ar: "جهة التسليم", value: "[Recipient / Department]" },
        { en: "Delivery Address", ar: "عنوان التسليم", value: "[Delivery Address]" },
        { en: "Requested Delivery Date", ar: "تاريخ التسليم المطلوب", value: "[Requested Delivery Date]" },
        { en: "Billing Address", ar: "عنوان الفوترة", value: "[Billing Address]" },
        { en: "Payment Terms", ar: "شروط الدفع", value: "[Agreed Payment Terms]" },
        { en: "Buyer Contact", ar: "جهة التواصل لدى المشتري", value: "[Buyer Contact]" },
        { en: "Shipping / Delivery Terms", ar: "شروط الشحن والتسليم", value: "[Agreed Shipping / Delivery Terms]" },
        { en: "Special Instructions", ar: "تعليمات خاصة", value: "[Special Instructions, if any]" }
      ]) +
      lineItems(["Items or Services", "البنود أو الخدمات"], 4, true) +
      totalsTable(false) +
      fieldRows(["Authorization", "الاعتماد"], [
        { en: "Requested By", ar: "مقدم الطلب", value: "[Name / Role / Date]" },
        { en: "Approved By", ar: "المعتمد", value: "[Name / Role / Date]" }
      ])
  }
];

if (!fs.existsSync(LOGO)) throw new Error("Approved V3.0 logo asset is missing: " + LOGO);
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
for (const doc of docs) createDocx(doc);
console.log("Created " + docs.length + " editable A4 DOCX templates in " + OUT);
console.log("Embedded exact V3.0 supplied logo: " + path.relative(ROOT, LOGO));
