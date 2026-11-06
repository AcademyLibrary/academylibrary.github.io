# Helper for convert_office.ps1: converts ONE Word document (runs in its own process so that
# the caller can enforce a timeout). The job file is a small UTF-8 JSON: {src, pdf, ox}.
param([Parameter(Mandatory = $true)][string]$JobFile)

$ErrorActionPreference = 'Stop'
$job  = Get-Content -LiteralPath $JobFile -Encoding UTF8 -Raw | ConvertFrom-Json
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    # Open(FileName, ConfirmConversions, ReadOnly, AddToRecentFiles)
    $d = $word.Documents.Open($job.src, $false, $true, $false)
    try {
        if ($job.ox) { $d.SaveAs2($job.ox, 16) }   # wdFormatDocumentDefault (docx) - fast, do it first
        $d.ExportAsFixedFormat($job.pdf, 17)       # wdExportFormatPDF
    } finally { $d.Close(0) }
} finally {
    $word.Quit(0)
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}
