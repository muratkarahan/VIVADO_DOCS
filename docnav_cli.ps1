<#
.SYNOPSIS
    DocNav CLI - AMD/Xilinx Documentation Navigator komut satırı aracı

.DESCRIPTION
    DocNav GUI'sine alternatif olarak dokümantasyonu CLI'dan arama ve indirme

.EXAMPLE
    .\docnav_cli.ps1 -Search "AXI DMA"
    .\docnav_cli.ps1 -List -Category "Versal"
    .\docnav_cli.ps1 -Download "UG1304"
    .\docnav_cli.ps1 -Open "UG1304"

.NOTES
    Tarih: 31 Ocak 2026
#>

param(
    [string]$Search,
    [switch]$List,
    [string]$Category,
    [string]$Download,
    [string]$Open,
    [switch]$Categories,
    [switch]$Help
)

$XdocsPath = "C:\Xilinx\DocNav\resources\xdocs.xml"
$DownloadDir = Join-Path $PSScriptRoot "downloaded_docs"

function Get-AllDocuments {
    if (-not (Test-Path $XdocsPath)) {
        Write-Error "DocNav xdocs.xml bulunamadı: $XdocsPath"
        return @()
    }
    
    $content = Get-Content $XdocsPath -Raw
    $xml = [xml]$content
    
    $docs = @()
    foreach ($catalog in $xml.collection.catalog) {
        foreach ($group in $catalog.group) {
            foreach ($doc in $group.document) {
                $docs += [PSCustomObject]@{
                    DocID = $doc.docID
                    Title = $doc.title -replace '\s+', ' '
                    Category = $catalog.label
                    Type = $doc.docType
                    WebURL = $doc.webLocation
                    DownloadURL = $doc.downloadURL
                    Tooltip = $doc.tooltip
                }
            }
        }
    }
    return $docs
}

function Search-Documents {
    param([string]$Query)
    
    $docs = Get-AllDocuments
    $results = $docs | Where-Object { 
        $_.Title -match $Query -or 
        $_.DocID -match $Query -or 
        $_.Tooltip -match $Query -or
        $_.Category -match $Query
    }
    
    if ($results.Count -eq 0) {
        Write-Host "Sonuç bulunamadı: '$Query'" -ForegroundColor Yellow
    } else {
        Write-Host "`n=== $($results.Count) sonuç bulundu: '$Query' ===" -ForegroundColor Green
        $results | Format-Table -AutoSize DocID, Title, Category
    }
    return $results
}

function Show-Categories {
    $docs = Get-AllDocuments
    $categories = $docs | Group-Object Category | Sort-Object Count -Descending
    
    Write-Host "`n=== Kategoriler ===" -ForegroundColor Cyan
    $categories | Format-Table @{N='Kategori';E={$_.Name}}, @{N='Doküman Sayısı';E={$_.Count}} -AutoSize
}

function List-Documents {
    param([string]$CategoryFilter)
    
    $docs = Get-AllDocuments
    
    if ($CategoryFilter) {
        $docs = $docs | Where-Object { $_.Category -match $CategoryFilter }
    }
    
    Write-Host "`n=== Toplam $($docs.Count) doküman ===" -ForegroundColor Green
    $docs | Format-Table -AutoSize DocID, Title, Category
}

function Download-Document {
    param([string]$DocID)
    
    $docs = Get-AllDocuments
    $doc = $docs | Where-Object { $_.DocID -eq $DocID } | Select-Object -First 1
    
    if (-not $doc) {
        Write-Error "Doküman bulunamadı: $DocID"
        return
    }
    
    if (-not $doc.DownloadURL) {
        Write-Error "İndirme linki yok: $DocID"
        return
    }
    
    if (-not (Test-Path $DownloadDir)) {
        New-Item -ItemType Directory -Path $DownloadDir -Force | Out-Null
    }
    
    $fileName = "$($doc.DocID).pdf"
    $outPath = Join-Path $DownloadDir $fileName
    
    Write-Host "İndiriliyor: $($doc.Title)" -ForegroundColor Cyan
    Write-Host "URL: $($doc.DownloadURL)" -ForegroundColor Gray
    
    try {
        Invoke-WebRequest -Uri $doc.DownloadURL -OutFile $outPath -UseBasicParsing
        Write-Host "İndirildi: $outPath" -ForegroundColor Green
    } catch {
        Write-Error "İndirme hatası: $_"
    }
}

function Open-Document {
    param([string]$DocID)
    
    $docs = Get-AllDocuments
    $doc = $docs | Where-Object { $_.DocID -eq $DocID } | Select-Object -First 1
    
    if (-not $doc) {
        Write-Error "Doküman bulunamadı: $DocID"
        return
    }
    
    # Önce local dosya var mı kontrol et
    $localPath = Join-Path $DownloadDir "$DocID.pdf"
    if (Test-Path $localPath) {
        Write-Host "Yerel dosya açılıyor: $localPath" -ForegroundColor Green
        Start-Process $localPath
        return
    }
    
    # Web'de aç
    if ($doc.WebURL) {
        Write-Host "Web'de açılıyor: $($doc.Title)" -ForegroundColor Cyan
        Start-Process $doc.WebURL
    } elseif ($doc.DownloadURL) {
        Write-Host "PDF indirme sayfası açılıyor..." -ForegroundColor Cyan
        Start-Process $doc.DownloadURL
    }
}

function Show-Help {
    Write-Host @"

DocNav CLI - AMD/Xilinx Documentation Navigator Komut Satırı Aracı
===================================================================

KULLANIM:
    .\docnav_cli.ps1 -Search <arama terimi>    Dokümanlarda ara
    .\docnav_cli.ps1 -List                     Tüm dokümanları listele
    .\docnav_cli.ps1 -List -Category <isim>    Kategoriye göre filtrele
    .\docnav_cli.ps1 -Download <DocID>         PDF indir (örn: UG1304)
    .\docnav_cli.ps1 -Open <DocID>             Dokümanı aç (web veya local)
    .\docnav_cli.ps1 -Help                     Bu yardımı göster
    .\docnav_cli.ps1 -Categories               Tüm kategorileri listele

ÖRNEKLER:
    .\docnav_cli.ps1 -Search "AXI DMA"
    .\docnav_cli.ps1 -Search "Zynq"
    .\docnav_cli.ps1 -List -Category "Versal"
    .\docnav_cli.ps1 -Download UG1304
    .\docnav_cli.ps1 -Open UG585
    .\docnav_cli.ps1 -Categories

"@ -ForegroundColor Cyan
}

# Ana mantık
if ($Help) {
    Show-Help
} elseif ($Search) {
    Search-Documents -Query $Search
} elseif ($Categories) {
    Show-Categories
} elseif ($List) {
    if ($Category) {
        List-Documents -CategoryFilter $Category
    } else {
        List-Documents
    }
} elseif ($Download) {
    Download-Document -DocID $Download
} elseif ($Open) {
    Open-Document -DocID $Open
} else {
    Show-Help
}
