Set-StrictMode -Version 3

<#
.SYNOPSIS

.DESCRIPTION

.EXAMPLE

.NOTES

#>
function Publish-SymbolsToBacktrace {
    [CmdletBinding()]
    [OutputType([String])]
    param (
        
    )

    Process {

        $MyInvocation.MyCommand.Parameters | Format-Table -AutoSize @{ Label = "Key"; Expression = { $_.Key }; }, @{ Label = "Value"; Expression = { (Get-Variable -Name $_.Key -EA SilentlyContinue).Value }; } | Out-String | Write-Debug

        $lootJson = Get-Content -Path .\Resources\loot.json -Raw

        $loot = $lootJson | ConvertFrom-Json

        $LootList = [System.Collections.ArrayList]@()


        #Add random common item
        $LootList.Add((Get-Random -InputObject $loot.common))

        Write-Host($LootList)

    }

    
}

Publish-SymbolsToBacktrace