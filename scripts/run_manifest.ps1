param(
    [string]$Config = "config/project.json"
)

$scriptPath = Join-Path $PSScriptRoot "generate_manifest.py"
python $scriptPath --config $Config
