param(
    [string]$Owner = "maharshimak",
    [string]$Output = "../portfolio-split",
    [switch]$DryRun,
    [switch]$Publish
)
$ErrorActionPreference = "Stop"
$Arguments = @("$PSScriptRoot/split-portfolio-repos.py", "--owner", $Owner, "--output", $Output)
if ($DryRun) { $Arguments += "--dry-run" }
if ($Publish) { $Arguments += "--publish" }
& python @Arguments
if ($LASTEXITCODE -ne 0) { throw "Migration stopped with exit code ${LASTEXITCODE}" }
