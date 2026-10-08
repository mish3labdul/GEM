import Foundation
import PDFKit
let a = CommandLine.arguments
guard a.count > 1, let d = PDFDocument(url: URL(fileURLWithPath: a[1])) else { print("ERR"); exit(1) }
var out = ""
for i in 0..<d.pageCount { out += (d.page(at: i)?.string ?? "") + "\n" }
print(out)
if a.count > 2 {
  for q in a[2...] {
    let hits = d.findString(q, withOptions: [])
    print("SEARCH[\(q)] hits=\(hits.count)")
  }
}
