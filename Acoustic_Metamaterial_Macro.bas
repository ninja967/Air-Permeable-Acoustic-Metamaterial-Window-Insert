' ******************************************************************************
' SolidWorks VBA Macro: Acoustic Metamaterial Window Insert Generator
' Project: Computer-Aided Product Development (CAPD)
' Author: Generated via Antigravity CAD Automation
' Target: SOLIDWORKS 2022 SP01 (Compatible with 2018-2026)
' ******************************************************************************

Option Explicit

Sub main()

    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swPart As SldWorks.PartDoc
    Dim swModelDocExt As SldWorks.ModelDocExtension
    Dim swEqnMgr As SldWorks.EquationMgr
    Dim swFeat As SldWorks.Feature
    Dim boolstatus As Boolean
    Dim longstatus As Long

    Set swApp = Application.SldWorks

    ' 1. Create New Part
    Dim defaultTemplate As String
    defaultTemplate = swApp.GetUserPreferenceStringValue(swDefaultTemplatePart)
    Set swModel = swApp.NewDocument(defaultTemplate, 0, 0, 0)
    
    If swModel Is Nothing Then
        MsgBox "Failed to create part.", vbCritical
        Exit Sub
    End If

    ' Set units to MMGS
    swModel.SetUserPreferenceIntegerValue swUnitSystem, swUnitSystem_MMGS

    ' 2. Populate Global Parametric Equations
    Set swEqnMgr = swModel.GetEquationMgr
    swEqnMgr.Add2 -1, """W_cell"" = 60mm", True
    swEqnMgr.Add2 -1, """H_cell"" = 30mm", True
    swEqnMgr.Add2 -1, """D_cell"" = 60mm", True
    swEqnMgr.Add2 -1, """W_airway"" = 20mm", True
    swEqnMgr.Add2 -1, """t_wall"" = 1.6mm", True
    swEqnMgr.Add2 -1, """N_passes"" = 4", True
    swEqnMgr.Add2 -1, """W_chamber"" = (""W_cell"" - ""W_airway"") / 2", True
    swEqnMgr.Add2 -1, """w_slit"" = (""W_chamber"" - (""N_passes"" + 1) * ""t_wall"") / ""N_passes""", True
    swEqnMgr.Add2 -1, """L_baffle"" = ""H_cell"" - (2 * ""t_wall"") - ""w_slit""", True
    swEqnMgr.Add2 -1, """L_waveguide"" = 100mm", True

    ' 3. Base Block Extrusion (60 x 30 x 60 mm)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.03, -0.015, 0, 0.03, 0.015, 0
    Set swFeat = swModel.FeatureManager.FeatureExtrusion2(True, False, False, 6, 0, 0.06, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    ' 4. Cut Central Airway (20 x 30 x 60 mm)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.01, -0.015, 0, 0.01, 0.015, 0
    Set swFeat = swModel.FeatureManager.FeatureCut3(True, False, False, 6, 0, 0.06, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, 0, 0, False)

    ' 5. Hollow Cavities (depth 56.8 mm, leaving 1.6 mm end-caps)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.0284, -0.0134, 0, -0.0116, 0.0134, 0
    swModel.SketchManager.CreateCornerRectangle 0.0116, -0.0134, 0, 0.0284, 0.0134, 0
    Set swFeat = swModel.FeatureManager.FeatureCut3(True, False, False, 6, 0, 0.0568, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, 0, 0, False)

    ' 6. Extrude Baffles (MidPlane 56.8 mm)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    ' Left Baffles
    swModel.SketchManager.CreateCornerRectangle -0.0162, -0.0134, 0, -0.0146, 0.0104, 0
    swModel.SketchManager.CreateCornerRectangle -0.0208, -0.0104, 0, -0.0192, 0.0134, 0
    swModel.SketchManager.CreateCornerRectangle -0.0254, -0.0134, 0, -0.0238, 0.0104, 0
    ' Right Baffles
    swModel.SketchManager.CreateCornerRectangle 0.0146, -0.0134, 0, 0.0162, 0.0104, 0
    swModel.SketchManager.CreateCornerRectangle 0.0192, -0.0104, 0, 0.0208, 0.0134, 0
    swModel.SketchManager.CreateCornerRectangle 0.0238, -0.0134, 0, 0.0254, 0.0104, 0
    Set swFeat = swModel.FeatureManager.FeatureExtrusion2(True, False, False, 6, 0, 0.0568, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    ' 7. Cut Acoustic Entry Slits (3.0 mm)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.0116, -0.0134, 0, -0.01, -0.0104, 0
    swModel.SketchManager.CreateCornerRectangle 0.01, -0.0134, 0, 0.0116, -0.0104, 0
    Set swFeat = swModel.FeatureManager.FeatureCut3(True, False, False, 6, 0, 0.0568, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, 0, 0, False)

    ' Assign ABS Plastic
    swModel.SetMaterialPropertyName2 "Default", "solidworks materials.sldmat", "ABS"
    
    swModel.ViewZoomtofit2
    MsgBox "Acoustic Metamaterial Unit Cell generated successfully!", vbInformation, "Antigravity CAD"

End Sub
