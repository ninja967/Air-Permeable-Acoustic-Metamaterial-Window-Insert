"""
Master SolidWorks Automation Script: Air-Permeable Acoustic Metamaterial
Generates all 3 models with VERIFIED CUTS AND EXTRUSIONS:
1. Solid_Metamaterial_Frame (Unit cell matching user blueprint)
2. Modular_Window_Panel_3x3 (3x3 architectural cassette with perimeter flange)
3. Acoustic_Air_Domain (Inverse acoustic fluid domain with simulation waveguides)
"""

import os
import sys
import win32com.client

OUT_DIR = os.path.abspath(r"c:\Users\sarat\Downloads\New folder")

def build_unit_cell(sw, partTemplate):
    print("\n==================================================")
    print(" 1. GENERATING Solid_Metamaterial_Frame.SLDPRT")
    print("==================================================")
    doc = sw.NewDocument(partTemplate, 0, 0, 0)
    if not doc:
        raise RuntimeError("Failed to create part document")
    doc.SetUserPreferenceIntegerValue(10, 3) # MMGS

    # Parametric Global Equations
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
    print("Parametric global equations added.")

    def draw_rect(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # 1. Base Block: 60 x 30 x 30 mm extruded into -Z
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-30.0, -15.0, 30.0, 15.0)
    f1 = doc.FeatureManager.FeatureExtrusion2(
        True, False, True, 0, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    assert f1 is not None, "Feature 1 (Base Block) failed!"
    print(f"Created Feature 1: {f1.Name} (Solid Base Block 60x30x30mm)")

    # 2. Cut 1: Central Airway: 20 mm wide, Through All in Z
    # Height Y: -13.5 to +15.0 (leaves 1.5 mm monolithic base floor at bottom)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-10.0, -13.5, 10.0, 15.0)
    f2 = doc.FeatureManager.FeatureCut3(
        True, False, False, 1, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f2 is not None, "Feature 2 (Central Airway Cut) failed!"
    print(f"Created Feature 2: {f2.Name} (Central Airway Cut 20mm Through All)")

    # 3. Cut 2: Resonator Cavities (Left & Right) to depth 28.5 mm (leaving 1.5 mm back plate)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-28.5, -13.5, -11.5, 13.5)
    draw_rect(11.5, -13.5, 28.5, 13.5)
    f3 = doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f3 is not None, "Feature 3 (Resonator Cavities Cut) failed!"
    print(f"Created Feature 3: {f3.Name} (Resonator Cavities Cut depth 28.5mm)")

    # 4. Boss 2: 3 Staggered Baffles per side (extruded 28.5 mm into -Z)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    # Left chamber
    draw_rect(-16.125, -13.5, -14.625, 11.5) # Baffle 1 (bottom attached, 2mm top gap)
    draw_rect(-20.750, -11.5, -19.250, 13.5) # Baffle 2 (top attached, 2mm bottom gap)
    draw_rect(-25.375, -13.5, -23.875, 11.5) # Baffle 3 (bottom attached, 2mm top gap)
    # Right chamber
    draw_rect(14.625, -13.5, 16.125, 11.5)  # Baffle 1
    draw_rect(19.250, -11.5, 20.750, 13.5)  # Baffle 2
    draw_rect(23.875, -13.5, 25.375, 11.5)  # Baffle 3
    f4 = doc.FeatureManager.FeatureExtrusion2(
        True, False, True, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    assert f4 is not None, "Feature 4 (Baffles Extrusion) failed!"
    print(f"Created Feature 4: {f4.Name} (3 Staggered Baffles per side, 1.5mm thick)")

    # 5. Cut 3: Entry Slits (2.0 mm wide cut at bottom of inner airway walls)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-11.5, -13.5, -10.0, -11.5)
    draw_rect(10.0, -13.5, 11.5, -11.5)
    f5 = doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f5 is not None, "Feature 5 (Entry Slits Cut) failed!"
    print(f"Created Feature 5: {f5.Name} (2.0mm Acoustic Entry Slits Cut)")

    doc.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "ABS")

    # Save
    p_sldprt = os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.SLDPRT")
    if os.path.exists(p_sldprt):
        try:
            os.remove(p_sldprt)
        except:
            pass
    doc.SaveAs3(p_sldprt, 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.STEP"), 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.STL"), 0, 2)

    # High-Res Renders
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
    print("SUCCESS: Solid_Metamaterial_Frame built and saved with all cuts verified!")

def build_modular_panel(sw, partTemplate):
    print("\n==================================================")
    print(" 2. GENERATING Modular_Window_Panel_3x3.SLDPRT")
    print("==================================================")
    doc = sw.NewDocument(partTemplate, 0, 0, 0)
    if not doc:
        raise RuntimeError("Failed to create part document")
    doc.SetUserPreferenceIntegerValue(10, 3)

    def draw_rect(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # 1. Base Panel: 180 x 180 x 30 mm with 5mm Mounting Flange (190 x 190 mm outer)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-95.0, -95.0, 95.0, 95.0) # 190 x 190 mm perimeter flange
    f1 = doc.FeatureManager.FeatureExtrusion2(
        True, False, True, 0, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    assert f1 is not None, "Panel Base Extrusion failed!"
    print(f"Created Feature 1: {f1.Name} (Base Panel with Flange 190x190x30mm)")

    # 2. Cut 3 Vertical Airway Ducts (20 mm wide Through All)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    for col_x in [-60.0, 0.0, 60.0]:
        draw_rect(col_x - 10.0, -90.0, col_x + 10.0, 90.0)
    f2 = doc.FeatureManager.FeatureCut3(
        True, False, False, 1, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f2 is not None, "Airway Ducts Cut failed!"
    print(f"Created Feature 2: {f2.Name} (3 Central Airway Ducts 20mm Through All)")

    # 3. Cut 3x3 Resonator Cavities (Left and Right of each airway, depth 28.5 mm into -Z)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    for row_y in [-60.0, 0.0, 60.0]:
        for col_x in [-60.0, 0.0, 60.0]:
            draw_rect(col_x - 28.5, row_y - 13.5, col_x - 11.5, row_y + 13.5)
            draw_rect(col_x + 11.5, row_y - 13.5, col_x + 28.5, row_y + 13.5)
    f3 = doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f3 is not None, "3x3 Cavities Cut failed!"
    print(f"Created Feature 3: {f3.Name} (18 Resonator Cavities Cut depth 28.5mm)")

    # 4. Boss 2: 3x3 Staggered Baffles (18 chambers x 3 baffles = 54 baffles, extruded 28.5 mm)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    for row_y in [-60.0, 0.0, 60.0]:
        for col_x in [-60.0, 0.0, 60.0]:
            # Left chamber baffles
            draw_rect(col_x - 16.125, row_y - 13.5, col_x - 14.625, row_y + 11.5)
            draw_rect(col_x - 20.750, row_y - 11.5, col_x - 19.250, row_y + 13.5)
            draw_rect(col_x - 25.375, row_y - 13.5, col_x - 23.875, row_y + 11.5)
            # Right chamber baffles
            draw_rect(col_x + 14.625, row_y - 13.5, col_x + 16.125, row_y + 11.5)
            draw_rect(col_x + 19.250, row_y - 11.5, col_x + 20.750, row_y + 13.5)
            draw_rect(col_x + 23.875, row_y - 13.5, col_x + 25.375, row_y + 11.5)
    f4 = doc.FeatureManager.FeatureExtrusion2(
        True, False, True, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    assert f4 is not None, "3x3 Baffles Extrusion failed!"
    print(f"Created Feature 4: {f4.Name} (54 Staggered Baffles across 3x3 array)")

    # 5. Cut 4: Entry Slits (2.0 mm wide cut into airway walls for all 18 chambers)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    for row_y in [-60.0, 0.0, 60.0]:
        for col_x in [-60.0, 0.0, 60.0]:
            draw_rect(col_x - 11.5, row_y - 13.5, col_x - 10.0, row_y - 11.5)
            draw_rect(col_x + 10.0, row_y - 13.5, col_x + 11.5, row_y - 11.5)
    f5 = doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f5 is not None, "3x3 Entry Slits Cut failed!"
    print(f"Created Feature 5: {f5.Name} (18 Acoustic Entry Slits Cut)")

    doc.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "ABS")

    # Save
    p_sldprt = os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.SLDPRT")
    if os.path.exists(p_sldprt):
        try:
            os.remove(p_sldprt)
        except:
            pass
    doc.SaveAs3(p_sldprt, 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.STEP"), 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.STL"), 0, 2)

    # Renders
    try:
        doc.ViewDisplayShadedWithEdges()
    except:
        pass
    doc.ShowNamedView2("*Isometric", 7)
    doc.ViewZoomtofit2()
    doc.SaveAs3(os.path.join(OUT_DIR, "render_panel_3x3_iso.png"), 0, 2)

    doc.ShowNamedView2("*Front", 1)
    doc.ViewZoomtofit2()
    doc.SaveAs3(os.path.join(OUT_DIR, "render_panel_3x3_front.png"), 0, 2)

    sw.CloseDoc(doc.GetTitle)
    print("SUCCESS: Modular_Window_Panel_3x3 built and saved with all cuts verified!")

def build_air_domain(sw, partTemplate):
    print("\n==================================================")
    print(" 3. GENERATING Acoustic_Air_Domain.SLDPRT")
    print("==================================================")
    doc = sw.NewDocument(partTemplate, 0, 0, 0)
    if not doc:
        raise RuntimeError("Failed to create part document")
    doc.SetUserPreferenceIntegerValue(10, 3)

    def draw_rect(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # 1. Main Duct (including 100mm upstream + 30mm cell + 100mm downstream = 230mm total waveguide)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-10.0, -115.0, 10.0, 115.0) # 20mm wide x 230mm long waveguide
    f1 = doc.FeatureManager.FeatureExtrusion2(
        True, False, True, 0, 0, 0.030, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    assert f1 is not None, "Air Domain Duct Extrusion failed!"
    print(f"Created Feature 1: {f1.Name} (Central Air Duct with 100mm Waveguides)")

    # 2. Side Chamber Fluid Blocks (Left & Right, depth 28.5 mm into -Z)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-28.5, -13.5, -10.0, 13.5)
    draw_rect(10.0, -13.5, 28.5, 13.5)
    f2 = doc.FeatureManager.FeatureExtrusion2(
        True, False, True, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    assert f2 is not None, "Air Domain Side Chamber Extrusion failed!"
    print(f"Created Feature 2: {f2.Name} (Side Chamber Fluid Blocks)")

    # 3. Cut Inner Dividing Walls (leaving 2.0 mm entry slit open at bottom Y: -13.5 to -11.5)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-11.5, -11.5, -10.0, 13.5)
    draw_rect(10.0, -11.5, 11.5, 13.5)
    f3 = doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f3 is not None, "Cut Inner Dividing Walls failed!"
    print(f"Created Feature 3: {f3.Name} (Cut Inner Dividing Walls leaving Entry Slit)")

    # 4. Cut 3 Staggered Baffles per side (1.5 mm thick, depth 28.5 mm)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    # Left
    draw_rect(-16.125, -13.5, -14.625, 11.5)
    draw_rect(-20.750, -11.5, -19.250, 13.5)
    draw_rect(-25.375, -13.5, -23.875, 11.5)
    # Right
    draw_rect(14.625, -13.5, 16.125, 11.5)
    draw_rect(19.250, -11.5, 20.750, 13.5)
    draw_rect(23.875, -13.5, 25.375, 11.5)
    f4 = doc.FeatureManager.FeatureCut3(
        True, False, False, 0, 0, 0.0285, 0,
        False, False, False, False, 0, 0,
        False, False, False, False,
        False, False, True, False,
        False, False, 0, 0, False
    )
    assert f4 is not None, "Cut Baffles failed!"
    print(f"Created Feature 4: {f4.Name} (Cut Baffles forming 4 Serpentine Passes)")

    doc.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "Air")

    # Save
    p_sldprt = os.path.join(OUT_DIR, "Acoustic_Air_Domain.SLDPRT")
    if os.path.exists(p_sldprt):
        try:
            os.remove(p_sldprt)
        except:
            pass
    doc.SaveAs3(p_sldprt, 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Acoustic_Air_Domain.STEP"), 0, 2)
    doc.SaveAs3(os.path.join(OUT_DIR, "Acoustic_Air_Domain.STL"), 0, 2)

    # Renders
    try:
        doc.ViewDisplayShadedWithEdges()
    except:
        pass
    doc.ShowNamedView2("*Isometric", 7)
    doc.ViewZoomtofit2()
    doc.SaveAs3(os.path.join(OUT_DIR, "render_air_domain_iso.png"), 0, 2)

    doc.ShowNamedView2("*Front", 1)
    doc.ViewZoomtofit2()
    doc.SaveAs3(os.path.join(OUT_DIR, "render_air_domain_front.png"), 0, 2)

    sw.CloseDoc(doc.GetTitle)
    print("SUCCESS: Acoustic_Air_Domain built and saved with all fluid channels verified!")

def main():
    print("Connecting to SolidWorks Application...")
    sw = win32com.client.Dispatch("SldWorks.Application")
    sw.Visible = True
    partTemplate = sw.GetUserPreferenceStringValue(8)

    build_unit_cell(sw, partTemplate)
    build_modular_panel(sw, partTemplate)
    build_air_domain(sw, partTemplate)
    print("\n==================================================")
    print(" ALL 3 CAD MODELS GENERATED WITH REAL VERIFIED CUTS!")
    print("==================================================")

if __name__ == "__main__":
    main()
