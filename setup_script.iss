[Setup]
AppName=Sigma PDV
AppVersion=1.0
AppPublisher=Felipe S. Rodrigues
AppContact=felipesgs@proton.me
AppPublisherURL=https://github.com/FlpsRodri
AppSupportURL=https://github.com/FlpsRodri
PrivilegesRequired=admin

DefaultDirName={localappdata}\Sigma PDV
DefaultGroupName=Sigma PDV
OutputDir=.
OutputBaseFilename=Sigma PDV
SetupIconFile=favicon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Sigma_PDV.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Xml_DB.sql"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist; Check: ShouldInstallDatabase
Source: "favicon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sigma PDV"; Filename: "{app}\Sigma_PDV.exe"
Name: "{userstartup}\Sigma PDV"; Filename: "{app}\Sigma_PDV.exe"
Name: "{commondesktop}\Sigma PDV"; Filename: "{app}\Sigma_PDV.exe"

[Run]
Filename: "{app}\Sigma_PDV.exe"; Description: "Iniciar Scanner de xml e busca de produtos"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\Arq"
Type: filesandordirs; Name: "{app}\NFE"
Type: filesandordirs; Name: "{app}\Log"
Type: files; Name: "{app}\Xml_DB.sql"
Type: dirifempty; Name: "{app}"

[Code]
var
  PreserveDatabase: Boolean;

function ShouldInstallDatabase(): Boolean;
begin
  // Só instala o banco se o usuário NÃO quiser preservar os dados
  Result := not PreserveDatabase;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  SourcePath, BackupPath, DateStr: string;
begin
  if CurStep = ssInstall then
  begin
    SourcePath := ExpandConstant('{app}\Xml_DB.sql');

    if FileExists(SourcePath) then
    begin
      if MsgBox('Um banco de dados já existe. Deseja manter os dados atuais?', mbConfirmation, MB_YESNO) = IDYES then
      begin
        PreserveDatabase := True;
      end
      else
      begin
        if MsgBox('Deseja criar um backup do banco de dados atual antes de sobrescrevê-lo?', mbConfirmation, MB_YESNO) = IDYES then
        begin
          DateStr := GetDateTimeString('yyyy-mm-dd', '-', ':');
          BackupPath := ExpandConstant('{app}\Xml_DB_') + DateStr + '.sql';

          if not FileCopy(SourcePath, BackupPath, False) then
            MsgBox('Erro ao criar o backup do banco de dados.', mbError, MB_OK);
        end;
      end;
    end;
  end;
end;
