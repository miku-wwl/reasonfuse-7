param(
    [ValidateSet("verify", "demo", "demo-loop", "demo-denied")]
    [string]$Mode = "verify"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot ".."))
Set-Location $repoRoot

switch ($Mode) {
    "verify" { python -m competition.phase7.evaluation }
    "demo" { python -m competition.phase7.demo.run }
    "demo-loop" { python -m competition.phase7.demo.run --fault loop }
    "demo-denied" { python -m competition.phase7.demo.run --approval DENIED }
}
