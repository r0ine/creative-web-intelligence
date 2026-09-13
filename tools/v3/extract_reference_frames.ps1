param(
  [Parameter(Mandatory=$true)][string]$Video,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [double]$EverySeconds = 0.5
)
$ErrorActionPreference='Stop'
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw 'ffmpeg is required for frame extraction.' }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$fps = 1.0 / $EverySeconds
ffmpeg -hide_banner -loglevel warning -i $Video -vf "fps=$fps" (Join-Path $OutDir 'frame-%05d.png')
Write-Host "Frames written to $OutDir"
