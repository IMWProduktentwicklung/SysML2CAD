VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} Einlesemaske 
   Caption         =   "UserForm1"
   ClientHeight    =   1470
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   8385.001
   OleObjectBlob   =   "Einlesemaske.frx":0000
   StartUpPosition =   1  'Fenstermitte
End
Attribute VB_Name = "Einlesemaske"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub btn_Einlesen_Click()
    ' Erstellen eines File Objektes
    Set StringDatei = CreateObject("Scripting.FileSystemObject")
    
    ' Initialwerte für das Einlesen
    Dim FileName As String
    FileName = txt_File.Value
    
    Const ForAppending = 1
    
    ' Einlesen der STEP Datei
    Set InhaltTxt = StringDatei.opentextfile(FileName, ForAppending, TristateFalse)
    
    Dim InhaltTxtString As String
    InhaltTxtString = InhaltTxt.ReadAll
    
    Dim Delimeter1 As String
    Delimeter1 = "/*!!"
    
    Dim Delimeter2 As String
    Delimeter2 = "*/!!"

    arrText1 = Split(InhaltTxtString, "/*!!")
    arrText2 = Split(arrText1(1), Delimeter2)
    
    ' Ausgeben der Inhalte in der Anforderungsliste
    'MsgBox arrText2(0)
    
    'Zusätzliche Inhalte####################################################
    'Dim oApp As Inventor.Application
    'Set oApp = ThisApplication
    
    'Dim oPartDoc  As PartDocument
    'Set oPartDoc = oApp.ActiveDocument
    
    'Dim oCompDef As PartComponentDefinition
    'Set oCompDef = oPartDoc.ComponentDefinition
    
    'Dim oModelAnnotations As ModelAnnotation
    'Set oModelAnnotations = oCompDef.ModelAnnotations.Application.
 
    'oModelAnnotations.Definition.Text.FormattedText = arrText2(0)
    
    ' Get the design tracking property set for our model state.
    'Dim oSummaryInfo As Inventor.PropertySet
    'Set oSummaryInfo = oPartDoc.PropertySets.Item("Inventor Summary Information")
    
    ' Get the Comments property.
    'Dim oCommentsProperty As Property
    'Set oCommentsProperty = oSummaryInfo.Item("Comments")
    
    ' Set the Member Edit Scope
    'oModelAnnotation.MemberEditScope = kEditActiveMember  'kEditAllMembers for all members
    
    'Set the value
    'oCommentsProperty.Value = "Updating comments via API!"
    
    'ZweiterUmbruch##################################################################################
    Dim doc As Document
    Dim oDef As ComponentDefinition
    Dim oTG As TransientGeometry
    Dim dViewRepMgr As RepresentationsManager
    Dim dWeldView As DesignViewRepresentations
    
    Set InvApp = ThisApplication 'Marshal.GetActiveObject("Inventor.Application")
    Set doc = InvApp.ActiveDocument
    Set oDef = doc.ComponentDefinition
    
    Set oTG = InvApp.TransientGeometry
    
    Set dViewRepMgr = oDef.RepresentationsManager
    Set dWeldView = dViewRepMgr.DesignViewRepresentations
    
    Einlesemaske.Hide
    
    Dim oFace As Face
    Set oFace = InvApp.CommandManager.Pick(SelectionFilterEnum.kPartFaceFilter, "Select a face to attach leader")
    
    Dim oAnnoPlaneDef As AnnotationPlaneDefinition
    Set oAnnoPlaneDef = oDef.ModelAnnotations.CreateAnnotationPlaneDefinitionUsingPlane(oFace.Geometry) 'this line was crashing Inventor
    
    'Set oAnnoPlaneDef = oDef.ModelAnnotations.Item(1).Definition.AnnotationPlaneDefinition 'used the planeDef from an existing annotation for test
    
    Dim oLeaderPoints As ObjectCollection
    Set oLeaderPoints = InvApp.TransientObjects.CreateObjectCollection
    
    Call oLeaderPoints.Add(oTG.CreatePoint(2, 2, 2))
    
    Dim oLeaderIntent As GeometryIntent
    Set oLeaderIntent = oDef.CreateGeometryIntent(oFace)
    
    Call oLeaderPoints.Add(oLeaderIntent)
    
    Dim oLeaderDef As ModelLeaderNoteDefinition
    Set oLeaderDef = oDef.ModelAnnotations.ModelLeaderNotes.CreateDefinition(oLeaderPoints, arrText2(0), oAnnoPlaneDef)
    
    Dim oLeader As ModelLeaderNote
    Set oLeader = oDef.ModelAnnotations.ModelLeaderNotes.Add(oLeaderDef)
    
    'Zusätzliche Inhalte###########################################
    
    ' Schließen der Datei
    InhaltTxt.Close
End Sub


Private Sub StepExport_Click()

    Dim iLogicAuto As Object

    Set iLogicAuto = GetiLogicAddin(ThisApplication)

    If (iLogicAuto Is Nothing) Then Exit Sub

 

    Dim doc As Document

    Set doc = ThisApplication.ActiveDocument

    Dim ruleName As String

    ruleName = "StepExport"

    'Dim rule As Object

    'Set rule = iLogicAuto.GetRule(doc, ruleName)

    'If (rule Is Nothing) Then

     ' Call MsgBox("No rule named " & ruleName & " was found in the document.")
    
      'Exit Sub

    'End If
    

    Dim i As Integer
    
    'i = iLogicAuto.RunRuleDirect(rule)
    i = iLogicAuto.RunExternalRule(doc, ruleName)
    
    ' Hier Schreiben in txt
    
    ' Initialwerte für das Einlesen
    Set StringDatei = CreateObject("Scripting.FileSystemObject")
    Dim FileName As String
    FileName = txt_File.Value
    
    Dim oDef As ComponentDefinition
    Set oDef = doc.ComponentDefinition
    
    
    Dim InhaltTxtString As String
    
    InhaltTxtString = oDef.ModelAnnotations(1).Definition.Text.Text
    
    Open FileName For Append As #1
        Write #1, InhaltTxtString
    
    Close #1
    
End Sub

Function GetiLogicAddin(oApplication As Inventor.Application) As Object

Set addIns = oApplication.ApplicationAddIns

 

Dim addIn As ApplicationAddIn

On Error GoTo NotFound

Set addIn = oApplication.ApplicationAddIns.ItemById("{3bdd8d79-2179-4b11-8a5a-257b1c0263ac}")

 

If (addIn Is Nothing) Then Exit Function

 

addIn.Activate

Set GetiLogicAddin = addIn.Automation

Exit Function

NotFound:

End Function
