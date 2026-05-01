$ErrorActionPreference = "Stop"

$python = "python"
$bundledPython = "C:\Users\codex-agent\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path $bundledPython) {
    $python = $bundledPython
}

& $python .\src\thousand_sunny_fleet.py

