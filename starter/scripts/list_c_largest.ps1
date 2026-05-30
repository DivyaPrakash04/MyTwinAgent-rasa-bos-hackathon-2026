Write-Host "Listing top 50 largest files on C:\`n"
Get-ChildItem C:\ -Recurse -ErrorAction SilentlyContinue -Force |
    Where-Object { -not $_.PSIsContainer } |
    Sort-Object Length -Descending |
    Select-Object @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,2)}}, FullName -First 50 |
    Format-Table -AutoSize

Write-Host "`nTop-level folders under C:\ by size (GB):`n"
Get-ChildItem C:\ -Directory -Force |
    ForEach-Object {
        $folder = $_
        $size = (Get-ChildItem $folder.FullName -Recurse -ErrorAction SilentlyContinue -Force | Where-Object {-not $_.PSIsContainer} | Measure-Object -Property Length -Sum).Sum
        [PSCustomObject]@{Name=$folder.FullName; SizeGB=[math]::Round($size/1GB,2)}
    } |
    Sort-Object SizeGB -Descending |
    Format-Table -AutoSize
