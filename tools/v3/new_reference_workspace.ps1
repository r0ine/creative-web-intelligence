param([Parameter(Mandatory=$true)][string]$Name,[string]$Root='reference-workspaces')
$dir=Join-Path $Root $Name
@('input','frames','captures','diffs','notes','spec') | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $dir $_) | Out-Null }
@{
 name=$Name; mode='pixel-close'; sources=@(); viewports=@(); sections=@(); unknowns=@(); created=(Get-Date).ToString('o')
} | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 (Join-Path $dir 'spec/reference-recreation-spec.json')
Write-Host $dir
