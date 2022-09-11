# Add VMware OVF Tool to PATH variable

$AddedLocation ="C:\program files\VMWare\VMware OVF Tool"
$Reg = "Registry::HKEY_CURRENT_USER\Environment"
$OldPath = (Get-ItemProperty -Path "$Reg" -Name PATH).Path
$NewPath= $OldPath + ’;’ + $AddedLocation
Set-ItemProperty -Path "$Reg" -Name PATH –Value $NewPath

# Add Virtualbox to PATH variable

$AddedLocation ="C:\Program Files\Oracle\VirtualBox"
$Reg = "Registry::HKEY_CURRENT_USER\Environment"
$OldPath = (Get-ItemProperty -Path "$Reg" -Name PATH).Path
$NewPath= $OldPath + ’;’ + $AddedLocation
Set-ItemProperty -Path "$Reg" -Name PATH –Value $NewPath

# install Vmware esxi plugin

vagrant plugin install vagrant-vmware-esxi