# This scripts converts a list of DVDs ($List) located in $DIR. The DVDs can be in a directory, ISO or IMG formats.
Clear-Host
# This script will work on this directory, Needs to be changed for each directory
#

#$Dir = "\\MICROSERVER\Recorded TV\"
#$Dir = "\\MICROSERVER\Recorded TV\"
#$ConvertedDir = "C:\Users\Tariq\Videos\Converted"
#$Duplicates = "C:\Users\Tariq\Videos\Duplicates"

#
$Dir="\\MICROSERVER\D (Storage)\complete\"
$ConvertedDir = "\\MICROSERVER\D (Storage)\Converted"
$Duplicates = "\\MICROSERVER\D (Storage)\Duplicates"
#


# Other variables. Likely won't need to be changed for most reruns.
$List = Get-ChildItem $Dir -include "*.avi", "*.mkv", "*.img", "*.iso", "*.wmv", "*.mts", "*.rmvb" -Name -Recurse | Sort -property LastWriteTime
$HandbrakeCLI = "\\MICROSERVER\D (Storage)\Software\PortableApps\HandBrakeCLI.exe"
$Preset = "--preset=`"AppleTV`""
#$Preset = "--preset=`"High Profile`""

# Uncomment when need to work against same directory from different computers
#[array]::Reverse($List)

$count = 1
$total = $List.Count
$ScriptStart = $(get-date)
# Check the paths set above
if ($(Test-Path $Dir) -ne "true" -or $(Test-Path $HandbrakeCLI) -ne "true") {
	Write-Host "ERROR: $Dir does not exist. Please check and correct" -ForegroundColor White -BackgroundColor Red
}
$string = $List -join "`r`n"
Write-Host "$string" -foregroundcolor White -backgroundcolor Black
Write-Host "Processing $total files..." -foregroundcolor White -backgroundcolor Black
	

 
# Process for each file
foreach ($Item in $List) {
	$ItemStart = $(Get-Date)
	Write-Host "$count of $total - $ItemStart :	Processing $Item..." -foregroundcolor White -backgroundcolor Black
	
# Set OutputFile variable, need to check for extension and change to mp4
	if ($Item -like "*.avi") {
		$OutputFile = $Item.Replace('.avi', '.mp4')
	}
	if ($Item -like "*.mkv") {
		$OutputFile = $Item.Replace('.mkv', '.mp4')
	}
	if ($Item -like ".*iso") {
		$OutputFile = $Item.Replace('.iso', '.mp4')
		}
	if ($Item -like "*.img") {
		$OutputFile = $Item.Replace('.img', '.mp4')
	}
	if ($Item -like "*.wmv") {
		$TestDir = Test-Path $OutputFile.Replace('.mp4', '')
	}

# Get the Movie name without the extension and year. Only checking for 2010 & 2011 since these are most common	
	$MovieNameYear = $OutputFile.Replace('.mp4', '')
	if ($MovieNameYear -like "*(2011)*") {
		$MovieName = $MovieNameYear.Replace(' (2011)', '') 
	}
		elseif ($MovieNameYear -like "*(2010)*") {
		$MovieName = $MovieNameYear.Replace(' (2010)', '') 
	} else {
		$MovieName = $MovieNameYear
		}
	
	$TestDirYear = "\\MICROSERVER\Videos\Movies\" + $MovieNameYear
	$TestDir = "\\MICROSERVER\Videos\Movies\" + $MovieName
	
	$InputFile = "$Dir$Item"
	
	if ($(Test-Path $TestDirYear) -eq "true" -or $(Test-Path $TestDir) -eq "true") {
		Write-Host "$MovieName exists in \\MICROSERVER\Videos\Movies, skipping the conversion..." -foregroundcolor White -backgroundcolor DarkGreen
		Move-Item $InputFile $Duplicates -Force
	} else {
		Write-Host "	Movie Name = $MovieName"
		Write-Host "	Input File = $InputFile"
		Write-Host "	Output File  = $Dir$OutputFile"
		& $HandbrakeCLI "-i" $InputFile "-o" $Dir$OutputFile $Preset 2>&1 >$null
		Move-Item $InputFile $ConvertedDir
		
		$ts = $(Get-Date) - $ItemStart
		$ElapsedTime = [String]::Format("{0}:{1}", $ts.Hours, $ts.Minutes);
		Write-Host "... $ElapsedTime to process $Item" -foregroundcolor White -backgroundcolor black
		}
	$count = $count + 1	
}	
$ts = $(Get-Date) - $ScriptStart
$ElapsedTime = [String]::Format("{0} Days, {1} Hours and {2} Minutes", $ts.Days, $ts.Hours, $ts.Minutes);
Write-Host "Processed $total files in completed in $ElapsedTime" -foregroundcolor White -backgroundcolor black	