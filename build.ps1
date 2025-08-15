$exclude = @("venv", "projeto_leonardo_sales.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "projeto_leonardo_sales.zip" -Force