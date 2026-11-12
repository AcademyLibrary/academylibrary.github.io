# Converts the original Office files (ppt/pptx/doc/docx) into PDF (+ Open XML copies of
# legacy .ppt/.doc files) using the locally installed Microsoft Office.
# Output goes to _build\pdf and _build\ox (both git-ignored). Already converted files are skipped.
# Usage:  powershell -ExecutionPolicy Bypass -File tools\convert_office.ps1 [-TimeoutSec 240] [-Only "part of a file name"]
# Note: kept ASCII-only on purpose (Windows PowerShell 5.1 reads BOM-less scripts as ANSI).

param([int]$TimeoutSec = 240, [string]$Only = '')

$ErrorActionPreference = 'Stop'
$root    = Split-Path -Parent $PSScriptRoot
$pdfOut  = Join-Path $root '_build\pdf'
$oxOut   = Join-Path $root '_build\ox'
$sources = Get-Content (Join-Path $PSScriptRoot 'source_dirs.txt') -Encoding UTF8 | Where-Object { $_.Trim() -ne '' }

function Ensure-Dir([string]$file) {
    $d = Split-Path -Parent $file
    if (-not (Test-Path -LiteralPath $d)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
}

$files = foreach ($s in $sources) {
    $dir = Join-Path $root $s
    if (Test-Path -LiteralPath $dir) {
        Get-ChildItem -LiteralPath $dir -Recurse -File |
            Where-Object { $_.Name -notlike '~$*' -and $_.Extension -match '^\.(pptx?|docx?)$' -and
                           (-not $Only -or $_.Name.IndexOf($Only, [StringComparison]::OrdinalIgnoreCase) -ge 0) }
    }
}

$todo = foreach ($f in $files) {
    $rel = $f.FullName.Substring($root.Length + 1)
    $pdf = Join-Path $pdfOut ($rel + '.pdf')
    # legacy binary formats (.ppt/.doc) also get an Open XML copy for text/media extraction
    $ox = $null
    if ($f.Extension -eq '.ppt') { $ox = Join-Path $oxOut ($rel + '.pptx') }
    if ($f.Extension -eq '.doc') { $ox = Join-Path $oxOut ($rel + '.docx') }
    $done = (Test-Path -LiteralPath $pdf) -and (-not $ox -or (Test-Path -LiteralPath $ox)) -and
            ((Get-Item -LiteralPath $pdf).LastWriteTime -gt $f.LastWriteTime)
    if ($done) { Write-Host "skip  $rel"; continue }
    Ensure-Dir $pdf
    if ($ox) { Ensure-Dir $ox }
    [pscustomobject]@{ Src = $f.FullName; Rel = $rel; Pdf = $pdf; Ox = $ox; IsPpt = ($f.Extension -match '^\.pptx?$') }
}

# ---- pass 1: presentations (one PowerPoint instance) ----
$pptItems = @($todo | Where-Object IsPpt)
if ($pptItems.Count) {
    $ppt = New-Object -ComObject PowerPoint.Application
    try {
        foreach ($t in $pptItems) {
            Write-Host "ppt   $($t.Rel)"
            # Open(FileName, ReadOnly, Untitled, WithWindow)
            $p = $ppt.Presentations.Open($t.Src, -1, 0, 0)
            try {
                if ($t.Ox) { $p.SaveCopyAs($t.Ox, 24) }   # ppSaveAsOpenXMLPresentation
                $p.SaveAs($t.Pdf, 32)                     # ppSaveAsPDF
            } catch { Write-Warning "failed: $($t.Rel): $($_.Exception.Message)" }
            finally { $p.Close() }
        }
    } finally { $ppt.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) }
}

# ---- pass 2: Word documents (separate process per file, with a timeout) ----
$helper  = Join-Path $PSScriptRoot 'convert_word_one.ps1'
$jobFile = Join-Path $env:TEMP 'g131_word_job.json'
foreach ($t in @($todo | Where-Object { -not $_.IsPpt })) {
    Write-Host "word  $($t.Rel)"
    $json = @{ src = $t.Src; pdf = $t.Pdf; ox = $t.Ox } | ConvertTo-Json -Compress
    [IO.File]::WriteAllText($jobFile, $json, (New-Object Text.UTF8Encoding $false))
    $before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object Id)
    $proc = Start-Process powershell.exe -PassThru -WindowStyle Hidden -ArgumentList @(
        '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "`"$helper`"", '-JobFile', "`"$jobFile`"")
    if (-not $proc.WaitForExit($TimeoutSec * 1000)) {
        Write-Warning "timeout after ${TimeoutSec}s: $($t.Rel) (pdf not created)"
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | Stop-Process -Force
    } elseif (-not (Test-Path -LiteralPath $t.Pdf)) {
        Write-Warning "failed: $($t.Rel)"
    }
}
Remove-Item -LiteralPath $jobFile -ErrorAction SilentlyContinue
Write-Host 'done'
