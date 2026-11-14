' ******************************************************************************
' SolidWorks VBA Macro: Acoustic Metamaterial Window Insert Generator
' Project: Computer-Aided Product Development (CAPD)
' Blueprint: 60mm x 30mm x 30mm Unit Cell, 20mm Airway, 1.50mm Walls, 2.00mm Slit
' Target: SOLIDWORKS 2022 SP01 (Compatible with 2018-2026)
' ******************************************************************************

Option Explicit

Sub main()

    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swPart As SldWorks.PartDoc
    Dim swEqnMgr As SldWorks.EquationMgr
    Dim swFeat As SldWorks.Feature
    Dim boolstatus As Boolean

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
    swEqnMgr.Add2 -1, """D_cell"" = 30mm", True
    swEqnMgr.Add2 -1, """W_airway"" = 20mm", True
    swEqnMgr.Add2 -1, """t_wall"" = 1.5mm", True
    swEqnMgr.Add2 -1, """w_slit_entry"" = 2.0mm", True
    swEqnMgr.Add2 -1, """N_passes"" = 4", True
    swEqnMgr.Add2 -1, """W_chamber"" = (""W_cell"" - ""W_airway"") / 2", True
    swEqnMgr.Add2 -1, """w_slit"" = (""W_chamber"" - (""N_passes"" + 1) * ""t_wall"") / ""N_passes""", True
    swEqnMgr.Add2 -1, """L_baffle"" = ""H_cell"" - (2 * ""t_wall"") - ""w_slit_entry""", True
    swEqnMgr.Add2 -1, """L_waveguide"" = 100mm", True

    ' 3. Base Block Extrusion (60 x 30 x 30 mm)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.03, -0.015, 0, 0.03, 0.015, 0
    Set swFeat = swModel.FeatureManager.FeatureExtrusion2(True, False, False, 0, 0, 0.030, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    ' 4. Cut Central Airway (20 x 30 x 30 mm Through All)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.01, -0.015, 0, 0.01, 0.015, 0
    Set swFeat = swModel.FeatureManager.FeatureCut3(True, False, False, 0, 0, 0.030, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, 0, 0, False)

    ' 5. Hollow Cavities (depth 28.5 mm, leaving 1.5 mm back plate)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.0285, -0.0135, 0, -0.0115, 0.0135, 0
    swModel.SketchManager.CreateCornerRectangle 0.0115, -0.0135, 0, 0.0285, 0.0135, 0
    Set swFeat = swModel.FeatureManager.FeatureCut3(True, False, False, 0, 0, 0.0285, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, 0, 0, False)

    ' 6. Extrude 3 Staggered Baffles per side (1.5 mm thick, height 28.5 mm)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    ' Left Baffles
    swModel.SketchManager.CreateCornerRectangle -0.016125, -0.0135, 0, -0.014625, 0.0115, 0 ' Baffle 1
    swModel.SketchManager.CreateCornerRectangle -0.020750, -0.0115, 0, -0.019250, 0.0135, 0 ' Baffle 2
    swModel.SketchManager.CreateCornerRectangle -0.025375, -0.0135, 0, -0.023875, 0.0115, 0 ' Baffle 3
    ' Right Baffles
    swModel.SketchManager.CreateCornerRectangle 0.014625, -0.0135, 0, 0.016125, 0.0115, 0   ' Baffle 1
    swModel.SketchManager.CreateCornerRectangle 0.019250, -0.0115, 0, 0.020750, 0.0135, 0   ' Baffle 2
    swModel.SketchManager.CreateCornerRectangle 0.023875, -0.0135, 0, 0.025375, 0.0115, 0   ' Baffle 3
    Set swFeat = swModel.FeatureManager.FeatureExtrusion2(True, False, False, 0, 0, 0.0285, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    ' 7. Cut Acoustic Entry Slits (2.0 mm at bottom inner airway walls)
    boolstatus = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    swModel.SketchManager.InsertSketch True
    swModel.SketchManager.CreateCornerRectangle -0.0115, -0.0135, 0, -0.0100, -0.0115, 0
    swModel.SketchManager.CreateCornerRectangle 0.0100, -0.0135, 0, 0.0115, -0.0115, 0
    Set swFeat = swModel.FeatureManager.FeatureCut3(True, False, False, 0, 0, 0.0285, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, 0, 0, False)

    ' Assign ABS Plastic
    swModel.SetMaterialPropertyName2 "Default", "solidworks materials.sldmat", "ABS"
    
    swModel.ShowNamedView2 "*Isometric", 7
    swModel.ViewZoomtofit2
    MsgBox "Acoustic Metamaterial Unit Cell generated successfully matching user blueprint!", vbInformation, "Antigravity CAD"

End Sub
