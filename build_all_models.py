"""
Complete Master Generator updated to EXACT user image specifications:
- W_cell = 60.00 mm
- H_cell = 30.00 mm
- D_cell = 30.00 mm (unit cell depth)
- W_airway = 20.00 mm
- t_wall = 1.50 mm (all walls and baffles)
- w_slit_entry = 2.00 mm (acoustic entry slit doorway)
- 3 Staggered Baffles per side (1.50 mm thick) creating 4 folded passes
- Open-Top Labyrinth Cutaway / Cassette Tray matching the exact 3D render in the user's blueprint
- 3x3 Modular Panel (180 x 180 x 30 mm) with 5.0 mm mounting flange
- Acoustic Air Domain with 100 mm waveguide ports
"""

import os
import win32com.client

OUT_DIR = os.path.abspath(r"c:\Users\sarat\Downloads\New folder")

def build_all(sw):
    partTemplate = sw.GetUserPreferenceStringValue(8)

    # ==========================================================
    # 1. UNIT CELL (Solid_Metamaterial_Frame)
    # ==========================================================
    print("\n--- Generating Solid_Metamaterial_Frame (User Blueprint Spec) ---")
    doc = sw.NewDocument(partTemplate, 0, 0, 0)
    doc.SetUserPreferenceIntegerValue(10, 3)

    eqMgr = doc.GetEquationMgr
    eqs = [
        '"W_cell" = 60mm',
        '"H_cell" = 30mm',
        '"D_cell" = 30mm',
        '"W_airway" = 20mm',
        '"t_wall" = 1.5mm',
        '"w_slit_entry" = 2.0mm',
        '"N_passes" = 4',
        '"W_chamber" = ("W_cell" - "W_airway") / 2',
        '"w_slit" = ("W_chamber" - ("N_passes" + 1) * "t_wall") / "N_passes"',
        '"L_baffle" = "H_cell" - (2 * "t_wall") - "w_slit_entry"',
        '"L_waveguide" = 100mm'
    ]
    for eq in eqs:
        eqMgr.Add2(-1, eq, True)

    def draw_rect(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # Base Block: 60 x 30 x 30 mm
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-30.0, -15.0, 30.0, 15.0)
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 0, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    # Central Airway: 20 mm Through All
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-10.0, -15.0, 10.0, 15.0)
    doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )

    # Cavities: Depth 28.5 mm (1.5 mm back plate retained)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-28.5, -13.5, -11.5, 13.5)
    draw_rect(11.5, -13.5, 28.5, 13.5)
    doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )

    # Baffles: 3 staggered baffles (1.5 mm thick, height 28.5 mm)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    # Left chamber
    draw_rect(-16.125, -13.5, -14.625, 11.5) # Baffle 1
    draw_rect(-20.750, -11.5, -19.250, 13.5) # Baffle 2
    draw_rect(-25.375, -13.5, -23.875, 11.5) # Baffle 3
    # Right chamber
    draw_rect(14.625, -13.5, 16.125, 11.5)  # Baffle 1
    draw_rect(19.250, -11.5, 20.750, 13.5)  # Baffle 2
    draw_rect(23.875, -13.5, 25.375, 11.5)  # Baffle 3
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    # Entry Slits: 2.0 mm at bottom
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-11.5, -13.5, -10.0, -11.5)
    draw_rect(10.0, -13.5, 11.5, -11.5)
    doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )

    doc.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "ABS")

    # Save
    p1 = os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.SLDPRT")
    doc.SaveAs3(p1, 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.STEP"), 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.STL"), 0, 2)

    # Renders
    try:
        doc.ViewDisplayShadedWithEdges()
    except:
        pass
    doc.ShowNamedView2("*Isometric", 7)
    doc.ViewZoomtofit2()
    doc.SaveAs3(os.path.join(OUT_DIR, "render_unit_cell_iso.png"), 0, 2)
    doc.ShowNamedView2("*Front", 1)
    doc.ViewZoomtofit2()
    doc.SaveAs3(os.path.join(OUT_DIR, "render_unit_cell_front.png"), 0, 2)
    sw.CloseDoc(doc.GetTitle)
    print("Solid_Metamaterial_Frame saved and rendered.")

    # ==========================================================
    # 2. MODULAR 3x3 PANEL (Modular_Window_Panel_3x3)
    # ==========================================================
    print("\n--- Generating Modular_Window_Panel_3x3 (User Blueprint Spec) ---")
    doc2 = sw.NewDocument(partTemplate, 0, 0, 0)
    doc2.SetUserPreferenceIntegerValue(10, 3)

    def draw_rect2(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc2.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # Base Panel: 180 x 30 x 180 mm (along X and Z)
    doc2.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc2.SketchManager.InsertSketch(True)
    draw_rect2(-90.0, -15.0, 90.0, 15.0)
    doc2.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.180, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    # 3 Central Airway Ducts (20 mm wide)
    doc2.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc2.SketchManager.InsertSketch(True)
    for col in [-60.0, 0.0, 60.0]:
        draw_rect2(col - 10.0, -15.0, col + 10.0, 15.0)
    doc2.FeatureManager.FeatureCut3(
        True, False, False, 6, 0, 0.180, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )

    # Hollow 3x3 cavities (each cell depth 28.5 mm, leaving 1.5 mm divider/cap)
    for row in [-60.0, 0.0, 60.0]:
        doc2.SelectByID("Front Plane", "PLANE", 0, 0, 0)
        doc2.SketchManager.InsertSketch(True)
        for col in [-60.0, 0.0, 60.0]:
            draw_rect2(col - 28.5, -13.5, col - 11.5, 13.5)
            draw_rect2(col + 11.5, -13.5, col + 28.5, 13.5)
        if row == 0.0:
            doc2.FeatureManager.FeatureCut3(
                True, False, False, 6, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                0, 0, False
            )
        elif row == 60.0:
            doc2.FeatureManager.FeatureCut3(
                True, False, False, 0, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0315, False
            )
        elif row == -60.0:
            doc2.FeatureManager.FeatureCut3(
                True, True, False, 0, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0315, True
            )

    # 3x3 Baffles
    for row in [-60.0, 0.0, 60.0]:
        doc2.SelectByID("Front Plane", "PLANE", 0, 0, 0)
        doc2.SketchManager.InsertSketch(True)
        for col in [-60.0, 0.0, 60.0]:
            draw_rect2(col - 16.125, -13.5, col - 14.625, 11.5)
            draw_rect2(col - 20.750, -11.5, col - 19.250, 13.5)
            draw_rect2(col - 25.375, -13.5, col - 23.875, 11.5)
            draw_rect2(col + 14.625, -13.5, col + 16.125, 11.5)
            draw_rect2(col + 19.250, -11.5, col + 20.750, 13.5)
            draw_rect2(col + 23.875, -13.5, col + 25.375, 11.5)
        if row == 0.0:
            doc2.FeatureManager.FeatureExtrusion2(
                True, False, False, 6, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, True, True, True,
                0, 0, False
            )
        elif row == 60.0:
            doc2.FeatureManager.FeatureExtrusion2(
                True, False, False, 0, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, True, True, True,
                3, 0.0315, False
            )
        elif row == -60.0:
            doc2.FeatureManager.FeatureExtrusion2(
                True, True, False, 0, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, True, True, True,
                3, 0.0315, True
            )

    # 3x3 Entry Slits
    for row in [-60.0, 0.0, 60.0]:
        doc2.SelectByID("Front Plane", "PLANE", 0, 0, 0)
        doc2.SketchManager.InsertSketch(True)
        for col in [-60.0, 0.0, 60.0]:
            draw_rect2(col - 11.5, -13.5, col - 10.0, -11.5)
            draw_rect2(col + 10.0, -13.5, col + 11.5, -11.5)
        if row == 0.0:
            doc2.FeatureManager.FeatureCut3(
                True, False, False, 6, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                0, 0, False
            )
        elif row == 60.0:
            doc2.FeatureManager.FeatureCut3(
                True, False, False, 0, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0315, False
            )
        elif row == -60.0:
            doc2.FeatureManager.FeatureCut3(
                True, True, False, 0, 0, 0.0570, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0315, True
            )

    # 5.0 mm Perimeter Mounting Flange
    doc2.SelectByID("Top Plane", "PLANE", 0, 0, 0)
    doc2.SketchManager.InsertSketch(True)
    doc2.SketchManager.CreateCornerRectangle(-0.095, -0.095, 0, 0.095, 0.095, 0)
    doc2.SketchManager.CreateCornerRectangle(-0.090, -0.090, 0, 0.090, 0.090, 0)
    doc2.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.010, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    doc2.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "ABS")

    p2 = os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.SLDPRT")
    doc2.SaveAs3(p2, 0, 2)
    doc2.SaveAs3(os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.STEP"), 0, 2)
    doc2.SaveAs3(os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.STL"), 0, 2)

    try:
        doc2.ViewDisplayShadedWithEdges()
    except:
        pass
    doc2.ShowNamedView2("*Isometric", 7)
    doc2.ViewZoomtofit2()
    doc2.SaveAs3(os.path.join(OUT_DIR, "render_panel_3x3_iso.png"), 0, 2)
    doc2.ShowNamedView2("*Front", 1)
    doc2.ViewZoomtofit2()
    doc2.SaveAs3(os.path.join(OUT_DIR, "render_panel_3x3_front.png"), 0, 2)
    sw.CloseDoc(doc2.GetTitle)
    print("Modular_Window_Panel_3x3 saved and rendered.")

    # ==========================================================
    # 3. ACOUSTIC AIR DOMAIN (Acoustic_Air_Domain)
    # ==========================================================
    print("\n--- Generating Acoustic_Air_Domain (User Blueprint Spec) ---")
    doc3 = sw.NewDocument(partTemplate, 0, 0, 0)
    doc3.SetUserPreferenceIntegerValue(10, 3)

    def draw_rect3(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc3.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # Upstream duct: 60 x 100 x 30 mm (Y in [-115, -15])
    doc3.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc3.SketchManager.InsertSketch(True)
    draw_rect3(-30.0, -115.0, 30.0, -15.0)
    doc3.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    # Downstream duct: 60 x 100 x 30 mm (Y in [15, 115])
    doc3.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc3.SketchManager.InsertSketch(True)
    draw_rect3(-30.0, 15.0, 30.0, 115.0)
    doc3.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    # Central Airway: 20 x 30 x 30 mm (Y in [-15, 15])
    doc3.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc3.SketchManager.InsertSketch(True)
    draw_rect3(-10.0, -15.0, 10.0, 15.0)
    doc3.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    # Entry Slits (2.0 mm)
    doc3.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc3.SketchManager.InsertSketch(True)
    draw_rect3(-11.5, -13.5, -10.0, -11.5)
    draw_rect3(10.0, -13.5, 11.5, -11.5)
    doc3.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    # Serpentine Folded Passages (3.125 mm wide passes, 2.0 mm turns)
    doc3.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc3.SketchManager.InsertSketch(True)
    # Left passages
    draw_rect3(-14.625, -13.5, -11.500, 13.5) # Pass 1
    draw_rect3(-19.250,  11.5, -14.625, 13.5) # Turn 1
    draw_rect3(-19.250, -13.5, -16.125, 13.5) # Pass 2
    draw_rect3(-23.875, -13.5, -16.125, -11.5) # Turn 2
    draw_rect3(-23.875, -13.5, -20.750, 13.5) # Pass 3
    draw_rect3(-28.500,  11.5, -20.750, 13.5) # Turn 3
    draw_rect3(-28.500, -13.5, -25.375, 13.5) # Pass 4
    # Right passages
    draw_rect3(11.500, -13.5, 14.625, 13.5)  # Pass 1
    draw_rect3(14.625,  11.5, 19.250, 13.5)  # Turn 1
    draw_rect3(16.125, -13.5, 19.250, 13.5)  # Pass 2
    draw_rect3(16.125, -13.5, 23.875, -11.5) # Turn 2
    draw_rect3(20.750, -13.5, 23.875, 13.5)  # Pass 3
    draw_rect3(20.750,  11.5, 28.500, 13.5)  # Turn 3
    draw_rect3(25.375, -13.5, 28.500, 13.5)  # Pass 4

    doc3.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )

    doc3.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "Air")

    p3 = os.path.join(OUT_DIR, "Acoustic_Air_Domain.SLDPRT")
    doc3.SaveAs3(p3, 0, 2)
    doc3.SaveAs3(os.path.join(OUT_DIR, "Acoustic_Air_Domain.STEP"), 0, 2)
    doc3.SaveAs3(os.path.join(OUT_DIR, "Acoustic_Air_Domain.STL"), 0, 2)

    try:
        doc3.ViewDisplayShadedWithEdges()
    except:
        pass
    doc3.ShowNamedView2("*Isometric", 7)
    doc3.ViewZoomtofit2()
    doc3.SaveAs3(os.path.join(OUT_DIR, "render_air_domain_iso.png"), 0, 2)
    doc3.ShowNamedView2("*Front", 1)
    doc3.ViewZoomtofit2()
    doc3.SaveAs3(os.path.join(OUT_DIR, "render_air_domain_front.png"), 0, 2)
    sw.CloseDoc(doc3.GetTitle)
    print("Acoustic_Air_Domain saved and rendered.")

    print("\nALL MODELS REBUILT EXACTLY TO USER IMAGE BLUEPRINT!")

if __name__ == "__main__":
    sw = win32com.client.Dispatch('SldWorks.Application')
    sw.Visible = True
    build_all(sw)
