# Download VIRTUAL SHIZUOKA 2021 ground LiDAR tiles listed in tiles.txt
# Requires the AWS CLI. No AWS account needed (public bucket).

$base = "s3://virtual-shizuoka/2021/LP/Ground/08/ME/35"
$tiles = Get-Content "$PSScriptRoot\tiles.txt"

New-Item -ItemType Directory -Force -Path ".\raw" | Out-Null

foreach ($tile in $tiles) {
    aws s3 cp --no-sign-request "$base/$tile.zip" ".\raw\"
}

Write-Host "Downloaded $($tiles.Count) tiles to .\raw"
