; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#ifndef VERSION
  #define VERSION "0.0.0"
#endif
#ifndef ONLY_64_BIT
  #define ONLY_64_BIT "x64"
#endif


#define MyAppName "EditX Pro"
#define MyAppPublisher "EditX Pro"
#define MyAppURL ""
#define MyAppExeName "launch.exe"
             
[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{4BB0DCDC-BC24-49EC-8937-72956C33A470}
AppName={#MyAppName}
AppVersion={#VERSION}
VersionInfoVersion={#VERSION}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright (c) 2019 {#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\COPYING
OutputBaseFilename=MagicVideoX
ArchitecturesInstallIn64BitMode={#ONLY_64_BIT}
ArchitecturesAllowed={#ONLY_64_BIT}
ChangesEnvironment=yes
Compression=lzma
SolidCompression=yes
WizardSmallImageFile=installer-logo.bmp
SetupIconFile=..\xdg\openshot-qt.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
SignedUninstaller=yes
SignedUninstallerDir=..\build\

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "armenian"; MessagesFile: "compiler:Languages\Armenian.islu"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "corsican"; MessagesFile: "compiler:Languages\Corsican.isl"
Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "greek"; MessagesFile: "compiler:Languages\Greek.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "nepali"; MessagesFile: "compiler:Languages\Nepali.islu"
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "scottishgaelic"; MessagesFile: "compiler:Languages\ScottishGaelic.isl"
Name: "serbiancyrillic"; MessagesFile: "compiler:Languages\SerbianCyrillic.isl"
Name: "serbianlatin"; MessagesFile: "compiler:Languages\SerbianLatin.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
; Remove previous installed versions of Magic
Type: filesandordirs; Name: "{app}\*"
Type: dirifempty; Name: "{app}\*"
Type: files; Name: "{group}\EditX Pro"

[Registry]
; Remove previously installed registry keys (no longer needed)
Root: HKLM; Subkey: "System\CurrentControlSet\Control\Session Manager\Environment"; ValueName:"QT_PLUGIN_PATH"; ValueType: none; Flags: deletevalue;
Root: HKLM; Subkey: "System\CurrentControlSet\Control\Session Manager\Environment"; ValueName:"MAGICK_CONFIGURE_PATH"; ValueType: none; Flags: deletevalue;

[Files]
; Add all frozen files from cx_Freeze build
Source: "..\build\exe.mingw-3.6\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Launch after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure DeleteInvalidFiles();
begin
  if (FileExists (ExpandConstant('{sys}\zlib1.dll'))) then
  begin
    RenameFile(ExpandConstant('{sys}\zlib1.dll'), ExpandConstant('{sys}\zlib1.DELETE'));
  end;
  if (FileExists (ExpandConstant('{win}\system32\zlib1.dll'))) then
  begin
    RenameFile(ExpandConstant('{win}\system32\zlib1.dll'), ExpandConstant('{win}\system32\zlib1.DELETE'));
  end;
  if (FileExists (ExpandConstant('{syswow64}\zlib1.dll'))) then
  begin
    RenameFile(ExpandConstant('{syswow64}\zlib1.dll'), ExpandConstant('{syswow64}\zlib1.DELETE'));
  end;
end;