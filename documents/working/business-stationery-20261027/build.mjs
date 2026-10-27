#!/usr/bin/env node
// Build the GEM business stationery working suite using Node built-ins only.
// Brand source: V3.0 official horizontal ink logo, exact bytes embedded in DOCX.

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
const CONTENT_W = 10000;
const EMU_PER_IN = 914400;
const enc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");

function p(text, opts = {}) {
  const font = opts.font || "Inter";
  const size = opts.size || 19;
  const color = opts.color || INK;
  const align = opts.align || "left";
  const before = opts.before || 0;
  const after = opts.after === undefined ? 35 : opts.after;
  const bold = opts.bold ? "<w:b/><w:bCs/>" : "";
  const italic = opts.italic ? "<w:i/><w:iCs/>" : "";
  const rtl = opts.rtl ? "<w:bidi w:val=\"1\"/>" : "";
  const rrtl = opts.rtl ? "<w:rtl w:val=\"1\"/>" : "";
  const lang = opts.rtl ? "<w:lang w:val=\"ar-SA\" w:eastAsia=\"ar-SA\"/>" : "<w:lang w:val=\"en-GB\"/>";
  const keep = opts.keep ? "<w:keepNext/>" : "";
  const textXml = text ? "<w:r><w:rPr><w:rFonts w:ascii=\"" + font + "\" w:hAnsi=\"" + font + "\" w:eastAsia=\"" + font + "\" w:cs=\"" + font + "\"/>" + bold + italic + rrtl + "<w:color w:val=\"" + color + "\"/><w:sz w:val=\"" + size + "\"/><w:szCs w:val=\"" + size + "\"/>" + lang + "</w:rPr><w:t xml:space=\"preserve\">" + enc(text) + "</w:t></w:r>" : "";
  return "<w:p><w:pPr>" + rtl + "<w:jc w:val=\"" + align + "\"/><w:spacing w:before=\"" + before + "\" w:after=\"" + after + "\" w:line=\"250\" w:lineRule=\"auto\"/>" + keep + "</w:pPr>" + textXml + "</w:p>";
}

function imageParagraph() {
  const cx = Math.round(1.82 * EMU_PER_IN);
  const cy = Math.round(cx * 665 / 2048);
  return "<w:p><w:pPr><w:spacing w:after=\"0\"/><w:jc w:val=\"left\"/></w:pPr><w:r><w:drawing><wp:inline distT=\"0\" distB=\"0\" distL=\"0\" distR=\"0\"><wp:extent cx=\"" + cx + "\" cy=\"" + cy + "\"/><wp:docPr id=\"1\" name=\"GEM horizontal ink logo\"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect=\"1\"/></wp:cNvGraphicFramePr><a:graphic><a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\"><pic:pic><pic:nvPicPr><pic:cNvPr id=\"0\" name=\"GEM horizontal ink logo\"/><pic:cNvPicPr><a:picLocks noChangeAspect=\"1\"/></pic:cNvPicPr></pic:nvPicPr><pic:blipFill><a:blip r:embed=\"rIdLogo\"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"" + cx + "\" cy=\"" + cy + "\"/></a:xfrm><a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>";
}

function tc(content, width, opts = {}) {
  const shade = opts.fill ? "<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"" + opts.fill + "\"/>" : "";
  const valign = opts.valign || "center";
  const borders = opts.bottom ? "<w:tcBorders><w:bottom w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"" + BEIGE + "\"/></w:tcBorders>" : "";
  const pXml = Array.isArray(content) ? content.join("") : content;
  return "<w:tc><w:tcPr><w:tcW w:w=\"" + width + "\" w:type=\"dxa\"/>" + shade + borders + "<w:vAlign w:val=\"" + valign + "\"/></w:tcPr>" + pXml + "</w:tc>";
}

function tbl(widths, rows, opts = {}) {
  const borders = opts.borders === false
    ? "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/><w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/><w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
    : "<w:tblBorders><w:top w:val=\"single\" w:sz=\"4\" w:color=\"" + BEIGE + "\"/><w:left w:val=\"single\" w:sz=\"4\" w:color=\"" + BEIGE + "\"/><w:bottom w:val=\"single\" w:sz=\"4\" w:color=\"" + BEIGE + "\"/><w:right w:val=\"single\" w:sz=\"4\" w:color=\"" + BEIGE + "\"/><w:insideH w:val=\"single\" w:sz=\"4\" w:color=\"" + BEIGE + "\"/><w:insideV w:val=\"single\" w:sz=\"4\" w:color=\"" + BEIGE + "\"/></w:tblBorders>";
  const grid = widths.map((w) => "<w:gridCol w:w=\"" + w + "\"/>").join("");
  const mar = "<w:tblCellMar><w:top w:w=\"75\" w:type=\"dxa\"/><w:left w:w=\"85\" w:type=\"dxa\"/><w:bottom w:w=\"75\" w:type=\"dxa\"/><w:right w:w=\"85\" w:type=\"dxa\"/></w:tblCellMar>";
  const tableRows = rows.map((row) => {
    const header = row.header ? "<w:tblHeader w:val=\"true\"/>" : "";
    return "<w:tr><w:trPr>" + header + "<w:cantSplit/></w:trPr>" + row.cells.join("") + "</w:tr>";
  }).join("");
  return "<w:tbl><w:tblPr><w:tblW w:w=\"" + widths.reduce((a, b) => a + b, 0) + "\" w:type=\"dxa\"/><w:tblLayout w:type=\"fixed\"/>" + borders + mar + "<w:tblLook w:firstRow=\"1\" w:lastRow=\"0\" w:firstColumn=\"0\" w:lastColumn=\"0\" w:noHBand=\"0\" w:noVBand=\"1\"/></w:tblPr><w:tblGrid>" + grid + "</w:tblGrid>" + tableRows + "</w:tbl>";
}

function labelCell(en, ar, width, fill) {
  return tc([
    p(en.toUpperCase(), { font: "Inter", size: 15, bold: true, after: 12 }),
    p(ar, { font: "Noto Sans Arabic", size: 16, bold: true, rtl: true, align: "right", after: 0 })
  ], width, { fill: fill || "F4F1F0", bottom: true });
}

function valueCell(value, width) {
  return tc(p(value, { font: "Inter", size: 18, italic: true, after: 0 }), width, { bottom: true });
}

function fieldRows(fields) {
  const widths = [1650, 3350, 1650, 3350];
  const rows = [];
  for (let i = 0; i < fields.length; i += 2) {
    const left = fields[i];
    const right = fields[i + 1];
    const cells = [
      labelCell(left.en, left.ar, widths[0]),
      valueCell(left.value, widths[1]),
      right ? labelCell(right.en, right.ar, widths[2]) : tc(p("", { after: 0 }), widths[2]),
      right ? valueCell(right.value, widths[3]) : tc(p("", { after: 0 }), widths[3])
    ];
    rows.push({ cells });
  }
  return tbl(widths, rows);
}

function section(en, ar) {
  return tbl([CONTENT_W], [{
    cells: [tc([
      p(en.toUpperCase(), { font: "Jost", size: 17, bold: true, after: 4, keep: true }),
      p(ar, { font: "Noto Sans Arabic", size: 16, bold: true, rtl: true, align: "right", after: 0, keep: true })
    ], CONTENT_W, { fill: BEIGE })]
  }], { borders: false });
}

function pageBreak() {
  return "<w:p><w:pPr><w:spacing w:before=\"0\" w:after=\"0\"/></w:pPr><w:r><w:br w:type=\"page\"/></w:r></w:p>";
}

function titleBlock(kicker, en, ar, note) {
  return p(kicker.toUpperCase(), { font: "Inter", size: 14, bold: true, after: 35, keep: true }) +
    p(en, { font: "Jost", size: 42, after: 0, keep: true }) +
    p(ar, { font: "Noto Sans Arabic", size: 34, rtl: true, align: "right", after: 75, keep: true }) +
    (note ? p(note, { font: "Inter", size: 16, after: 100 }) : "");
}

function lineItems(count = 4) {
  const widths = [500, 3400, 900, 850, 2050, 2300];
  const headers = [
    ["No.", "م"],
    ["Item / Service", "البند / الخدمة"],
    ["Qty", "الكمية"],
    ["Unit", "الوحدة"],
    ["Unit Price", "سعر الوحدة"],
    ["Line Total", "إجمالي البند"]
  ];
  const rows = [];
  rows.push({
    header: true,
    cells: headers.map((h, i) => tc([
      p(h[0], { font: "Inter", size: 14, bold: true, color: WHITE, align: i < 2 ? "left" : "center", after: 8 }),
      p(h[1], { font: "Noto Sans Arabic", size: 14, bold: true, color: WHITE, rtl: true, align: "right", after: 0 })
    ], widths[i], { fill: INK, valign: "center" }))
  });
  for (let i = 0; i < count; i++) {
    const vals = [String(i + 1), "[Description / specification]", "[Qty]", "[Unit]", "[Currency] [Unit Price]", "[Currency] [Line Total]"];
    rows.push({ cells: vals.map((v, j) => tc(p(v, { font: "Inter", size: j === 1 ? 15 : 14, italic: true, align: j === 0 || j === 2 || j === 3 ? "center" : "left", after: 0 }), widths[j], { bottom: true, valign: "center" })) });
  }
  return tbl(widths, rows);
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
  for (const line of lines) {
    const strong = line[0] === "Total" || line[0] === "Balance due";
    rows.push({ cells: [
      tc([
        p(line[0].toUpperCase(), { font: "Inter", size: 15, bold: strong, after: 6 }),
        p(line[1], { font: "Noto Sans Arabic", size: 15, bold: strong, rtl: true, align: "right", after: 0 })
      ], 6500, { fill: strong ? BEIGE : null, bottom: true }),
      tc(p(line[2], { font: "Inter", size: 16, bold: strong, italic: !strong, align: "right", after: 0 }), 3500, { fill: strong ? BEIGE : null, bottom: true })
    ] });
  }
  return tbl([6500, 3500], rows);
}

function noteBlock(en, ar, placeholder) {
  return section(en, ar) + tbl([CONTENT_W], [{
    cells: [tc(p(placeholder, { font: "Inter", size: 16, italic: true, after: 0 }), CONTENT_W, { bottom: true })]
  }]);
}

function headerXml() {
  return "<w:hdr xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">" +
    tbl([4700, 5300], [{
      cells: [
        tc(imageParagraph(), 4700, { valign: "center" }),
        tc([
          p("BUSINESS DOCUMENTS", { font: "Jost", size: 17, bold: true, align: "right", after: 10 }),
          p("INTERNAL REVIEW DRAFT", { font: "Inter", size: 13, bold: true, align: "right", after: 8 }),
          p("مسودة للمراجعة الداخلية", { font: "Noto Sans Arabic", size: 14, bold: true, rtl: true, align: "right", after: 0 })
        ], 5300, { valign: "center" })
      ]
    }], { borders: false }) +
    "<w:p><w:pPr><w:spacing w:before=\"55\" w:after=\"0\"/><w:pBdr><w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"1\" w:color=\"" + BEIGE + "\"/></w:pBdr></w:pPr></w:p>" +
    "</w:hdr>";
}

function footerXml() {
  return "<w:ftr xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">" +
    "<w:p><w:pPr><w:pBdr><w:top w:val=\"single\" w:sz=\"4\" w:space=\"5\" w:color=\"" + BEIGE + "\"/></w:pBdr><w:spacing w:before=\"70\" w:after=\"15\"/></w:pPr>" +
    "<w:r><w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\"/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"13\"/></w:rPr><w:t>[Registered Entity Name] | [Company Address] | contact@mish3l.com | [Business Phone]</w:t></w:r></w:p>" +
    "<w:p><w:pPr><w:bidi w:val=\"1\"/><w:jc w:val=\"right\"/><w:spacing w:after=\"0\"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii=\"Noto Sans Arabic\" w:hAnsi=\"Noto Sans Arabic\" w:cs=\"Noto Sans Arabic\"/><w:rtl/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"13\"/><w:lang w:val=\"ar-SA\"/></w:rPr><w:t>الاسم المسجل: [Registered Entity Name] | العنوان: [Company Address]</w:t></w:r></w:p>" +
    "</w:ftr>";
}

function stylesXml() {
  return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<w:styles xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">" +
    "<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\" w:eastAsia=\"Inter\" w:cs=\"Noto Sans Arabic\"/><w:sz w:val=\"19\"/><w:szCs w:val=\"19\"/><w:lang w:val=\"en-GB\" w:eastAsia=\"ar-SA\"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after=\"35\" w:line=\"250\" w:lineRule=\"auto\"/></w:pPr></w:pPrDefault></w:docDefaults>" +
    "<w:style w:type=\"paragraph\" w:default=\"1\" w:styleId=\"Normal\"><w:name w:val=\"Normal\"/><w:qFormat/><w:rPr><w:rFonts w:ascii=\"Inter\" w:hAnsi=\"Inter\" w:eastAsia=\"Inter\" w:cs=\"Noto Sans Arabic\"/></w:rPr></w:style>" +
    "<w:style w:type=\"paragraph\" w:styleId=\"Title\"><w:name w:val=\"Title\"/><w:basedOn w:val=\"Normal\"/><w:qFormat/><w:rPr><w:rFonts w:ascii=\"Jost\" w:hAnsi=\"Jost\"/><w:color w:val=\"" + INK + "\"/><w:sz w:val=\"42\"/></w:rPr></w:style>" +
    "<w:style w:type=\"paragraph\" w:styleId=\"Heading1\"><w:name w:val=\"heading 1\"/><w:basedOn w:val=\"Normal\"/><w:qFormat/><w:rPr><w:rFonts w:ascii=\"Jost\" w:hAnsi=\"Jost\"/><w:color w:val=\"" + INK + "\"/><w:b/><w:sz w:val=\"22\"/></w:rPr></w:style>" +
    "</w:styles>";
}

function docXml(body) {
  return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\"><w:body>" + body +
    "<w:sectPr><w:headerReference w:type=\"default\" r:id=\"rIdHeader\"/><w:footerReference w:type=\"default\" r:id=\"rIdFooter\"/><w:pgSz w:w=\"" + A4_W + "\" w:h=\"" + A4_H + "\"/><w:pgMar w:top=\"1500\" w:right=\"950\" w:bottom=\"1110\" w:left=\"950\" w:header=\"360\" w:footer=\"420\" w:gutter=\"0\"/><w:cols w:num=\"1\" w:space=\"425\"/><w:docGrid w:linePitch=\"360\"/></w:sectPr></w:body></w:document>";
}

function contentTypes() {
  return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">" +
    "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/><Default Extension=\"xml\" ContentType=\"application/xml\"/><Default Extension=\"png\" ContentType=\"image/png\"/>" +
    "<Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/><Override PartName=\"/word/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml\"/><Override PartName=\"/word/header1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml\"/><Override PartName=\"/word/footer1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml\"/><Override PartName=\"/word/settings.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml\"/><Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/><Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/>" +
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
    "<Relationship Id=\"rIdStyles\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" Target=\"styles.xml\"/><Relationship Id=\"rIdHeader\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/header\" Target=\"header1.xml\"/><Relationship Id=\"rIdFooter\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer\" Target=\"footer1.xml\"/><Relationship Id=\"rIdSettings\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings\" Target=\"settings.xml\"/></Relationships>";
  const headerRels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rIdLogo\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\"media/gem-horizontal-ink.png\"/></Relationships>";
  const title = enc(doc.title + " | GEM Business Stationery Working Suite");
  const core = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
    "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><dc:title>" + title + "</dc:title><dc:subject>Editable bilingual business document template</dc:subject><dc:creator>GEM</dc:creator><cp:keywords>WORKING INTERNAL REVIEW DRAFT</cp:keywords><dc:description>Working template. Business details and external-issue acceptance remain pending.</dc:description><dcterms:created xsi:type=\"dcterms:W3CDTF\">2026-10-27T00:00:00Z</dcterms:created></cp:coreProperties>";
  const app = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\"><Application>GEM stationery template builder</Application></Properties>";
  const settings = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><w:settings xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"><w:updateFields w:val=\"true\"/><w:defaultTabStop w:val=\"720\"/><w:compat><w:compatSetting w:name=\"compatibilityMode\" w:uri=\"http://schemas.microsoft.com/office/word\" w:val=\"15\"/></w:compat></w:settings>";
  const entries = [
    ["[Content_Types].xml", contentTypes()],
    ["_rels/.rels", rels],
    ["docProps/core.xml", core],
    ["docProps/app.xml", app],
    ["word/document.xml", docXml(doc.body)],
    ["word/styles.xml", stylesXml()],
    ["word/header1.xml", headerXml()],
    ["word/footer1.xml", footerXml()],
    ["word/_rels/document.xml.rels", docRels],
    ["word/_rels/header1.xml.rels", headerRels],
    ["word/settings.xml", settings],
    ["word/media/gem-horizontal-ink.png", logo]
  ];
  fs.writeFileSync(path.join(OUT, doc.filename), zip(entries));
}

const docs = [
  {
    filename: "GEM_Business_Letterhead_Template_working.docx",
    title: "Business Letterhead",
    body:
      titleBlock("Template 01 | Correspondence", "Business Correspondence", "مراسلات الأعمال", "Complete the bracketed fields, then replace the body prompt with your letter.") +
      fieldRows([
        { en: "Date", ar: "التاريخ", value: "[Date]" },
        { en: "Reference", ar: "المرجع", value: "[Reference Number]" },
        { en: "Recipient", ar: "المستلم", value: "[Recipient Name]" },
        { en: "Organization", ar: "المنشأة", value: "[Recipient Organization]" },
        { en: "Address", ar: "العنوان", value: "[Recipient Address]" },
        { en: "Subject", ar: "الموضوع", value: "[Subject]" }
      ]) +
      p("Dear [Recipient Name],", { font: "Inter", size: 20, before: 130, after: 100 }) +
      p("[Write your message here. Add or remove paragraphs as needed.]", { font: "Inter", size: 20, after: 120 }) +
      p("Kind regards,", { font: "Inter", size: 20, after: 150 }) +
      p("[Sender Name]", { font: "Inter", size: 20, bold: true, after: 25 }) +
      p("[Role / Title]", { font: "Inter", size: 17, after: 0 })
  },
  {
    filename: "GEM_Request_for_Quotation_Template_working.docx",
    title: "Request for Quotation",
    body:
      titleBlock("Template 02 | Procurement", "Request for Quotation", "طلب تقديم عرض سعر", "Please complete the requester and supplier fields, describe the requirement, and return a priced response by the stated date.") +
      section("Request Details", "بيانات الطلب") +
      fieldRows([
        { en: "RFQ Number", ar: "رقم طلب عرض السعر", value: "[RFQ Number]" },
        { en: "Issue Date", ar: "تاريخ الإصدار", value: "[Issue Date]" },
        { en: "Response Due", ar: "موعد الرد", value: "[Response Due Date]" },
        { en: "Requester", ar: "مقدم الطلب", value: "[Requester Name / Role]" },
        { en: "Requester Email", ar: "بريد مقدم الطلب", value: "[Requester Email]" },
        { en: "Project / Reference", ar: "المشروع / المرجع", value: "[Project or Reference]" }
      ]) +
      section("Supplier Details", "بيانات المورد") +
      fieldRows([
        { en: "Supplier Name", ar: "اسم المورد", value: "[Supplier Name]" },
        { en: "Contact Name", ar: "اسم جهة التواصل", value: "[Supplier Contact]" },
        { en: "Email", ar: "البريد الإلكتروني", value: "[Supplier Email]" },
        { en: "Address", ar: "العنوان", value: "[Supplier Address]" }
      ]) +
      section("Items or Services", "البنود أو الخدمات") +
      lineItems(4) +
      pageBreak() +
      section("Delivery and Commercial Response", "التسليم والرد التجاري") +
      fieldRows([
        { en: "Delivery Location", ar: "موقع التسليم", value: "[Delivery Address]" },
        { en: "Requested Delivery", ar: "موعد التسليم المطلوب", value: "[Requested Delivery Date]" },
        { en: "Payment Terms", ar: "شروط الدفع", value: "[Requested Payment Terms]" },
        { en: "Quote Valid Until", ar: "صلاحية العرض حتى", value: "[Quote Validity Date]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" },
        { en: "Lead Time", ar: "مدة التوريد", value: "[Supplier Lead Time]" }
      ]) +
      noteBlock("Response Instructions", "تعليمات الرد", "Return the completed pricing and delivery information to [Requester Email] by [Response Due Date]. Include product or service specifications and any supporting documents relevant to this request.")
  },
  {
    filename: "GEM_Quotation_Proposal_Template_working.docx",
    title: "Quotation and Proposal",
    body:
      titleBlock("Template 03 | Customer Response", "Quotation and Proposal", "عرض سعر ومقترح", "Describe the requested scope and provide clear prices, delivery details, payment terms, and a validity date.") +
      section("Quotation Details", "بيانات عرض السعر") +
      fieldRows([
        { en: "Quotation Number", ar: "رقم عرض السعر", value: "[Quotation Number]" },
        { en: "Issue Date", ar: "تاريخ الإصدار", value: "[Issue Date]" },
        { en: "Valid Until", ar: "صالح حتى", value: "[Quote Validity Date]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" },
        { en: "Customer", ar: "العميل", value: "[Customer Name]" },
        { en: "Customer Contact", ar: "جهة التواصل", value: "[Customer Contact]" },
        { en: "Project / Property", ar: "المشروع / المنشأة", value: "[Project or Property]" },
        { en: "Prepared By", ar: "إعداد", value: "[Name / Role]" }
      ]) +
      noteBlock("Scope Summary", "ملخص النطاق", "[Summarize the requested work, proposed items or services, and any relevant assumptions supplied by the customer.]") +
      section("Pricing", "الأسعار") +
      lineItems(4) +
      totalsTable(false) +
      pageBreak() +
      section("Issuer and Customer Contact", "بيانات الجهة والعميل") +
      fieldRows([
        { en: "Registered Entity", ar: "الاسم المسجل للمنشأة", value: "[Registered Entity Name]" },
        { en: "Business Email", ar: "البريد الإلكتروني", value: "[Business Email]" },
        { en: "Business Address", ar: "عنوان المنشأة", value: "[Company Address]" },
        { en: "Sales Contact", ar: "جهة التواصل للمبيعات", value: "[Sales Contact Name / Role]" }
      ]) +
      section("Delivery and Payment", "التسليم والدفع") +
      fieldRows([
        { en: "Delivery Location", ar: "موقع التسليم", value: "[Delivery Address]" },
        { en: "Estimated Delivery", ar: "موعد التسليم التقديري", value: "[Estimated Delivery Date]" },
        { en: "Payment Terms", ar: "شروط الدفع", value: "[Payment Terms]" },
        { en: "Quote Valid Until", ar: "صلاحية العرض حتى", value: "[Quote Validity Date]" }
      ]) +
      section("Customer Review", "مراجعة العميل") +
      fieldRows([
        { en: "Name / Role", ar: "الاسم / الصفة", value: "[Customer Name / Role]" },
        { en: "Signature / Date", ar: "التوقيع / التاريخ", value: "[Signature / Date]" }
      ])
  },
  {
    filename: "GEM_Invoice_Template_working.docx",
    title: "Invoice",
    body:
      titleBlock("Template 04 | Accounts", "Invoice", "فاتورة", "Enter the applicable invoice, customer, pricing, tax, due-date, and payment details before issue.") +
      section("Invoice Details", "بيانات الفاتورة") +
      fieldRows([
        { en: "Invoice Number", ar: "رقم الفاتورة", value: "[Invoice Number]" },
        { en: "Issue Date", ar: "تاريخ الإصدار", value: "[Issue Date]" },
        { en: "Payment Due", ar: "تاريخ الاستحقاق", value: "[Payment Due Date]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" },
        { en: "Purchase Order", ar: "أمر الشراء", value: "[Customer PO Number]" },
        { en: "Related Quotation", ar: "عرض السعر المرتبط", value: "[Quotation Reference]" }
      ]) +
      section("Supplier and Customer", "المورد والعميل") +
      fieldRows([
        { en: "Supplier / Issuer", ar: "المورد / الجهة المصدرة", value: "[Registered Entity Name]" },
        { en: "Supplier Address", ar: "عنوان المورد", value: "[Company Address]" },
        { en: "Customer", ar: "العميل", value: "[Customer Legal Name]" },
        { en: "Billing Address", ar: "عنوان الفاتورة", value: "[Customer Billing Address]" },
        { en: "Customer Email", ar: "بريد العميل", value: "[Customer Email]" },
        { en: "Tax Identifier", ar: "الرقم الضريبي", value: "[Tax Identifier, if applicable]" }
      ]) +
      section("Items or Services", "البنود أو الخدمات") +
      lineItems(4) +
      pageBreak() +
      totalsTable(true) +
      section("Payment Instructions", "تعليمات الدفع") +
      fieldRows([
        { en: "Payee / Account Name", ar: "المستفيد / اسم الحساب", value: "[Payee Name]" },
        { en: "Bank", ar: "البنك", value: "[Bank Name]" },
        { en: "Account Number", ar: "رقم الحساب", value: "[Account Number]" },
        { en: "IBAN / Routing", ar: "رقم الآيبان / التوجيه", value: "[IBAN / Routing Details]" },
        { en: "Payment Reference", ar: "مرجع الدفع", value: "[Payment Reference]" },
        { en: "Contact Email", ar: "بريد التواصل", value: "[Accounts Contact Email]" }
      ])
  },
  {
    filename: "GEM_Purchase_Order_Template_working.docx",
    title: "Purchase Order",
    body:
      titleBlock("Template 05 | Procurement", "Purchase Order", "أمر شراء", "Complete all buyer, supplier, delivery, pricing, and authorization fields using approved commercial details.") +
      section("Order Details", "بيانات الطلب") +
      fieldRows([
        { en: "Purchase Order Number", ar: "رقم أمر الشراء", value: "[Purchase Order Number]" },
        { en: "Order Date", ar: "تاريخ الطلب", value: "[Order Date]" },
        { en: "Requester", ar: "مقدم الطلب", value: "[Requester Name / Role]" },
        { en: "Requester Email", ar: "بريد مقدم الطلب", value: "[Requester Email]" },
        { en: "Related Quotation", ar: "عرض السعر المرتبط", value: "[Quotation Reference]" },
        { en: "Currency", ar: "العملة", value: "[Currency Code]" }
      ]) +
      section("Supplier Details", "بيانات المورد") +
      fieldRows([
        { en: "Supplier Name", ar: "اسم المورد", value: "[Supplier Registered Name]" },
        { en: "Supplier Contact", ar: "جهة التواصل لدى المورد", value: "[Supplier Contact]" },
        { en: "Supplier Email", ar: "بريد المورد", value: "[Supplier Email]" },
        { en: "Supplier Address", ar: "عنوان المورد", value: "[Supplier Address]" }
      ]) +
      section("Delivery and Billing", "التسليم والفوترة") +
      fieldRows([
        { en: "Deliver To", ar: "جهة التسليم", value: "[Recipient / Department]" },
        { en: "Delivery Address", ar: "عنوان التسليم", value: "[Delivery Address]" },
        { en: "Requested Delivery Date", ar: "تاريخ التسليم المطلوب", value: "[Requested Delivery Date]" },
        { en: "Billing Address", ar: "عنوان الفوترة", value: "[Billing Address]" },
        { en: "Payment Terms", ar: "شروط الدفع", value: "[Agreed Payment Terms]" },
        { en: "Buyer Contact", ar: "جهة التواصل لدى المشتري", value: "[Buyer Contact]" }
      ]) +
      pageBreak() +
      section("Items or Services", "البنود أو الخدمات") +
      lineItems(4) +
      totalsTable(false) +
      section("Authorization", "الاعتماد") +
      fieldRows([
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
