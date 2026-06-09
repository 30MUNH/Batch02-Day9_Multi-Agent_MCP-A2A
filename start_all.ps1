# PowerShell script to start all Legal Multi-Agent System services on Windows
# Registry must be first, then leaf agents, then orchestrators

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"

# Create logs directory if it doesn't exist
if (!(Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Force -Path "logs"
}

Write-Host "Starting Registry service on port 10000..."
$registryProc = Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m registry" -NoNewWindow -PassThru -RedirectStandardOutput "logs\registry.log" -RedirectStandardError "logs\registry_error.log"
Start-Sleep -Seconds 2

Write-Host "Starting Tax Agent on port 10102..."
$taxProc = Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m tax_agent" -NoNewWindow -PassThru -RedirectStandardOutput "logs\tax_agent.log" -RedirectStandardError "logs\tax_agent_error.log"

Write-Host "Starting Compliance Agent on port 10103..."
$complianceProc = Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m compliance_agent" -NoNewWindow -PassThru -RedirectStandardOutput "logs\compliance_agent.log" -RedirectStandardError "logs\compliance_agent_error.log"
Start-Sleep -Seconds 3

Write-Host "Starting Law Agent on port 10101..."
$lawProc = Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m law_agent" -NoNewWindow -PassThru -RedirectStandardOutput "logs\law_agent.log" -RedirectStandardError "logs\law_agent_error.log"
Start-Sleep -Seconds 3

Write-Host "Starting Customer Agent on port 10100..."
$customerProc = Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m customer_agent" -NoNewWindow -PassThru -RedirectStandardOutput "logs\customer_agent.log" -RedirectStandardError "logs\customer_agent_error.log"

Write-Host ""
Write-Host "All services started in the background:"
Write-Host "  Registry:         http://localhost:10000 (PID: $($registryProc.Id))"
Write-Host "  Customer Agent:   http://localhost:10100 (PID: $($customerProc.Id))"
Write-Host "  Law Agent:        http://localhost:10101 (PID: $($lawProc.Id))"
Write-Host "  Tax Agent:        http://localhost:10102 (PID: $($taxProc.Id))"
Write-Host "  Compliance Agent: http://localhost:10103 (PID: $($complianceProc.Id))"
Write-Host ""
Write-Host "Logs are saved in the 'logs/' folder."
Write-Host "Run test_client.py to send a query:"
Write-Host "  python test_client.py"
Write-Host ""
Write-Host "To stop all services, run:"
Write-Host "  Stop-Process -Id $($registryProc.Id), $($taxProc.Id), $($complianceProc.Id), $($lawProc.Id), $($customerProc.Id) -Force"
