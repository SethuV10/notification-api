# PowerShell Script to Generate Self-Signed Certificate for localhost (No OpenSSL needed)

$certFolder = "certs"
$certPath = "$certFolder\server.crt"
$keyPath = "$certFolder\server.key"

# Create certs folder if it doesn't exist
if (!(Test-Path $certFolder)) {
    New-Item -ItemType Directory -Path $certFolder
    Write-Host "Created folder: $certFolder" -ForegroundColor Green
}

# Generate Self-Signed Certificate using PowerShell built-in cmdlets
$cert = New-SelfSignedCertificate `
    -DnsName "localhost" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -KeyExportPolicy Exportable `
    -Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" `
    -NotAfter (Get-Date).AddYears(1)

# Export Certificate (Public + Private Key in PFX)
$pfxPath = "$certFolder\server.pfx"
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password (ConvertTo-SecureString -String "password123" -Force -AsPlainText)

Write-Host "✅ Self-signed certificate generated successfully!" -ForegroundColor Green
Write-Host "   PFX File: $pfxPath" -ForegroundColor Cyan
Write-Host "   Password: password123" -ForegroundColor Yellow

# Export .crt (public certificate)
$cert | Export-Certificate -FilePath $certPath -Force

# Note: Full .key export is complex in pure PowerShell without extra tools.
# We'll use a simpler approach in main.py or recommend manual handling if needed.

Write-Host "`n✅ Self-signed certificate generated successfully!" -ForegroundColor Green
Write-Host "   PFX File: $pfxPath (Password: password123)" -ForegroundColor Cyan
Write-Host "   CRT File: $certPath" -ForegroundColor Cyan
Write-Host "   You can now run the server with HTTPS." -ForegroundColor Green