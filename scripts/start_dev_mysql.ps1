$mysqld = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe"
if (-not (Test-Path $mysqld)) {
    throw "MySQL Server 8.0 was not found at $mysqld"
}

$datadir = Join-Path $env:TEMP "bureaucrazy-mysql-data"
$listening = Get-NetTCPConnection -LocalPort 3307 -State Listen -ErrorAction SilentlyContinue
if ($listening) {
    Write-Output "MySQL is already listening on port 3307."
    exit 0
}

if (-not (Test-Path (Join-Path $datadir "mysql"))) {
    New-Item -ItemType Directory -Force -Path $datadir | Out-Null
    & $mysqld --initialize-insecure --datadir="$datadir"
}

Write-Output "Starting MySQL on 127.0.0.1:3307"
& $mysqld --datadir="$datadir" --port=3307 --bind-address=127.0.0.1 --mysqlx=0 --console