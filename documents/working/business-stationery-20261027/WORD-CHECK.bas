Attribute VB_Name = "GEMWordCheck"
Option Explicit

' Edit SOURCE_FOLDER to the folder that holds the four DOCX files (keep the trailing slash).
Private Const SOURCE_FOLDER As String = "/Users/mediacenter1/Documents/GEM-Web-remake/.repo-sync/gem-business-stationery/documents/working/business-stationery-20261027/"

Private Sub SetCellText(ByVal tbl As Table, ByVal rowNo As Long, ByVal colNo As Long, ByVal value As String)
    Dim target As Range
    Set target = tbl.Cell(rowNo, colNo).Range
    target.Text = value & Chr(13) & Chr(7)
End Sub

Private Function CellValue(ByVal tbl As Table, ByVal rowNo As Long, ByVal colNo As Long) As String
    Dim value As String
    value = tbl.Cell(rowNo, colNo).Range.Text
    value = Replace(value, Chr(13), "")
    value = Replace(value, Chr(7), "")
    value = Replace(value, Chr(160), "")
    CellValue = Trim(value)
End Function

Private Function FindItemsTable(ByVal doc As Document) As Table
    Dim tbl As Table
    For Each tbl In doc.Tables
        If InStr(1, tbl.Range.Text, "Line Total", vbTextCompare) > 0 And _
           InStr(1, tbl.Range.Text, "Unit Price", vbTextCompare) > 0 Then
            Set FindItemsTable = tbl
            Exit Function
        End If
    Next tbl
End Function

Private Function NormalizedAmount(ByVal value As String) As String
    value = Replace(value, ",", "")
    value = Replace(value, " ", "")
    NormalizedAmount = value
End Function

Public Sub WORD_CHECK()
    Dim names As Variant, qty As Variant, price As Variant
    Dim tempFolder As String, resultsPath As String, fileName As Variant
    Dim doc As Document, tbl As Table, f As Field, i As Long
    Dim outFile As Integer, lineValues As String, subtotal As String
    Dim vatAmount As String, total As String, balance As String

    names = Array("GEM_Invoice_Template_working.docx", _
                  "GEM_Purchase_Order_Template_working.docx", _
                  "GEM_Quotation_Proposal_Template_working.docx", _
                  "GEM_Request_for_Quotation_Template_working.docx")
    qty = Array("2", "3", "4", "5")
    price = Array("10", "20", "30", "40")
    tempFolder = Environ$("TMPDIR") & "GEM_WORD_CHECK/"
    If Dir(tempFolder, vbDirectory) = "" Then MkDir tempFolder
    resultsPath = SOURCE_FOLDER & "WORD-CHECK-RESULTS.txt"
    outFile = FreeFile
    Open resultsPath For Output As #outFile

    For Each fileName In names
        FileCopy SOURCE_FOLDER & CStr(fileName), tempFolder & CStr(fileName)
        Set doc = Documents.Open(FileName:=tempFolder & CStr(fileName), ReadOnly:=False, AddToRecentFiles:=False)
        doc.Activate
        Set tbl = FindItemsTable(doc)
        If tbl Is Nothing Then
            Print #outFile, CStr(fileName) & ": FAIL - item table not found"
            doc.Close SaveChanges:=wdDoNotSaveChanges
            GoTo NextDocument
        End If

        For i = 0 To 3
            SetCellText tbl, i + 3, 3, CStr(qty(i))
            SetCellText tbl, i + 3, 5, CStr(price(i))
        Next i
        If CStr(fileName) <> "GEM_Request_for_Quotation_Template_working.docx" Then
            SetCellText tbl, 8, 2, "15"
        End If
        If CStr(fileName) = "GEM_Invoice_Template_working.docx" Then
            SetCellText tbl, 11, 2, "100"
        End If

        For Each f In ActiveDocument.Fields
            f.Locked = False
        Next f
        ActiveDocument.Fields.Update
        For Each f In ActiveDocument.Fields
            f.Update
        Next f

        lineValues = NormalizedAmount(CellValue(tbl, 3, 6)) & " / " & _
                     NormalizedAmount(CellValue(tbl, 4, 6)) & " / " & _
                     NormalizedAmount(CellValue(tbl, 5, 6)) & " / " & _
                     NormalizedAmount(CellValue(tbl, 6, 6))
        subtotal = NormalizedAmount(CellValue(tbl, 7, 2))
        If CStr(fileName) = "GEM_Request_for_Quotation_Template_working.docx" Then
            total = NormalizedAmount(CellValue(tbl, 8, 2))
            Print #outFile, CStr(fileName) & ": lines " & lineValues & "; subtotal " & subtotal & "; total " & total
        Else
            vatAmount = NormalizedAmount(CellValue(tbl, 9, 2))
            total = NormalizedAmount(CellValue(tbl, 10, 2))
            If CStr(fileName) = "GEM_Invoice_Template_working.docx" Then
                balance = NormalizedAmount(CellValue(tbl, 12, 2))
                Print #outFile, CStr(fileName) & ": lines " & lineValues & "; subtotal " & subtotal & "; VAT " & vatAmount & "; total " & total & "; balance " & balance
            Else
                Print #outFile, CStr(fileName) & ": lines " & lineValues & "; subtotal " & subtotal & "; VAT " & vatAmount & "; total " & total
            End If
        End If
        doc.Close SaveChanges:=wdDoNotSaveChanges
NextDocument:
    Next fileName
    Close #outFile
    MsgBox "Word check complete. Results: " & resultsPath, vbInformation
End Sub
