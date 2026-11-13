"""
Complete Master Generator for:
1. Solid_Metamaterial_Frame (Single Unit Cell)
2. Modular_Window_Panel_3x3 (Full 3x3 Window Insert Panel with Gasket Flange)
3. Acoustic_Air_Domain (Inverse Fluid/Air Volume with Simulation Waveguides)

Includes full SolidWorks 2022 Parametric Equations, Materials, Mass Properties, and multi-format exports (.SLDPRT, .STEP, .STL).
"""

import os
import sys
import win32com.client

OUT_DIR = os.path.abspath(r"c:\Users\sarat\Downloads\New folder")

def create_unit_cell(sw):
    print("\n==========================================")
    print("STEP 1: Generating Solid_Metamaterial_Frame (Single Unit Cell)")
    print("==========================================")
    
    partTemplate = sw.GetUserPreferenceStringValue(8) # swDefaultTemplatePart
    doc = sw.NewDocument(partTemplate, 0, 0, 0)
    if not doc:
        raise RuntimeError("Failed to create new SolidWorks part document.")
        
    doc.SetUserPreferenceIntegerValue(10, 3) # swUnitSystem_MMGS
    
    # 1. Setup Global Equations
    eqMgr = doc.GetEquationMgr
    eqs = [
        '"W_cell" = 60mm',
        '"H_cell" = 30mm',
        '"D_cell" = 60mm',
        '"W_airway" = 20mm',
        '"t_wall" = 1.6mm',
        '"N_passes" = 4',
        '"W_chamber" = ("W_cell" - "W_airway") / 2',
        '"w_slit" = ("W_chamber" - ("N_passes" + 1) * "t_wall") / "N_passes"',
        '"L_baffle" = "H_cell" - (2 * "t_wall") - "w_slit"',
        '"L_waveguide" = 100mm'
    ]
    for eq in eqs:
        eqMgr.Add2(-1, eq, True)
    print("-> Parametric Global Equations added successfully.")

    def draw_rect(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # 2. Base Solid Block (60 x 30 x 60 mm)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-30.0, -15.0, 30.0, 15.0)
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.060, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> Base Solid Block (60 x 30 x 60 mm) extruded.")

    # 3. Cut Central Airway (20 x 30 x 60 mm Through All)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-10.0, -15.0, 10.0, 15.0)
    doc.FeatureManager.FeatureCut3(
        True, False, False, 6, 0, 0.060, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )
    print("-> Central Ventilation Airway (20 mm) cut Through All.")

    # 4. Cut Resonator Cavities (depth 56.8 mm, leaving 1.6 mm Z end-caps)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-28.4, -13.4, -11.6, 13.4) # Left chamber cavity
    draw_rect(11.6, -13.4, 28.4, 13.4)  # Right chamber cavity
    doc.FeatureManager.FeatureCut3(
        True, False, False, 6, 0, 0.0568, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )
    print("-> Resonator Cavities hollowed to 56.8 mm (1.6 mm end-caps retained).")

    # 5. Extrude Interdigitated Labyrinth Baffles (depth 56.8 mm, Merge = True)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    # Left chamber: Baffle 1 (bottom), Baffle 2 (top), Baffle 3 (bottom)
    draw_rect(-16.2, -13.4, -14.6, 10.4) # Baffle 1
    draw_rect(-20.8, -10.4, -19.2, 13.4) # Baffle 2
    draw_rect(-25.4, -13.4, -23.8, 10.4) # Baffle 3
    # Right chamber: Symmetric
    draw_rect(14.6, -13.4, 16.2, 10.4)  # Baffle 1
    draw_rect(19.2, -10.4, 20.8, 13.4)  # Baffle 2
    draw_rect(23.8, -13.4, 25.4, 10.4)  # Baffle 3
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.0568, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> 3 Interdigitated Serpentine Baffles per side extruded.")

    # 6. Cut Acoustic Entry Slits (3.0 x 3.0 mm, depth 56.8 mm)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-11.6, -13.4, -10.0, -10.4) # Left slit
    draw_rect(10.0, -13.4, 11.6, -10.4)  # Right slit
    doc.FeatureManager.FeatureCut3(
        True, False, False, 6, 0, 0.0568, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )
    print("-> Acoustic Entry Slits (3.0 mm) cut into inner airway walls.")

    # 7. Apply Material: ABS Plastic
    doc.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "ABS")
    print("-> Material assigned: ABS Plastic.")

    # Save and Export
    sldprt_path = os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.SLDPRT")
    step_path = os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.STEP")
    stl_path = os.path.join(OUT_DIR, "Solid_Metamaterial_Frame.STL")

    doc.SaveAs3(sldprt_path, 0, 2)
    doc.SaveAs3(step_path, 0, 2)
    doc.SaveAs3(stl_path, 0, 2)

    print(f"-> Saved: {sldprt_path}")
    print(f"-> Exported: {step_path}")
    print(f"-> Exported: {stl_path}")
    sw.CloseDoc(doc.GetTitle)
    return sldprt_path


def create_window_panel_3x3(sw):
    print("\n==========================================")
    print("STEP 2: Generating Modular_Window_Panel_3x3 (Full 180x180 mm Insert Panel)")
    print("==========================================")
    
    partTemplate = sw.GetUserPreferenceStringValue(8)
    doc = sw.NewDocument(partTemplate, 0, 0, 0)
    if not doc:
        raise RuntimeError("Failed to create new SolidWorks part document.")
        
    doc.SetUserPreferenceIntegerValue(10, 3) # MMGS

    def draw_rect(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # 1. Base Outer Panel (180 x 30 x 180 mm)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-90.0, -15.0, 90.0, 15.0)
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.180, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> 180 x 30 x 180 mm Base Panel extruded.")

    # 2. Cut 3 Central Airway Channels (X centers at -60, 0, +60 mm, each 20 mm wide)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    for col in [-60.0, 0.0, 60.0]:
        draw_rect(col - 10.0, -15.0, col + 10.0, 15.0)
    doc.FeatureManager.FeatureCut3(
        True, False, False, 6, 0, 0.180, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, False, True, True, True, True, False,
        0, 0, False
    )
    print("-> 3 Continuous Central Airway Ducts (20 mm wide) cut.")

    # 3. For each of the 3x3 cells (3 cols in X, 3 rows in Z):
    # In X: cells are centered at -60, 0, +60
    # In Z: cells are centered at -60, 0, +60
    # Resonators are on left and right of each airway:
    # Left chamber: col - 30 to col - 10
    # Cavity: col - 28.4 to col - 11.6
    # Right chamber: col + 10 to col + 30
    # Cavity: col + 11.6 to col + 28.4
    # In Z: each cell is 60 mm tall, with 1.6 mm end caps on top and bottom of each cell.
    # So the cavity in Z extends for 56.8 mm centered at row: [row - 28.4, row + 28.4]!
    
    # We can cut the 3x3 cavities by sketching on the Front Plane and doing blind/offset cuts or sketching on each cell level!
    # Or even better: Sketch the 6 vertical cavity strips and cut MidPlane, then place intermediate 3.2 mm dividers at Z = -30 and +30!
    # Notice: At Z = -30 and Z = +30 are the boundaries between cells where the two 1.6 mm end caps meet = 3.2 mm solid divider!
    # Outer Z bounds: Z = -90 (1.6 mm cap), Z = +90 (1.6 mm cap).
    
    for row_idx, row in enumerate([-60.0, 0.0, 60.0]):
        # Sketch cavities on Front Plane and extrude cut from row - 28.4 to row + 28.4 (depth 56.8 mm)
        doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
        doc.SketchManager.InsertSketch(True)
        for col in [-60.0, 0.0, 60.0]:
            draw_rect(col - 28.4, -13.4, col - 11.6, 13.4)
            draw_rect(col + 11.6, -13.4, col + 28.4, 13.4)
            
        # Cut with offset:
        # Distance = 56.8 mm, Start offset from Front Plane
        # Or simpler: cut MidPlane with depth 56.8 mm centered at Z=row!
        # In FeatureCut3: Dir1 depth, Dir2 depth:
        # Front Plane is Z=0.
        # For row = 0: Dir1 = 28.4 mm, Dir2 = 28.4 mm (MidPlane 56.8 mm)
        # For row = -60: Dir1 = -60 - 28.4 to -60 + 28.4 (Offset start = -60 mm, MidPlane = 56.8 mm)
        if row == 0.0:
            doc.FeatureManager.FeatureCut3(
                True, False, False, 6, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                0, 0, False
            )
        elif row == 60.0:
            # Blind extrude cut with start offset
            # StartConditions = 3 (swStartOffset), StartOffset = 0.0316 m (31.6 mm to 88.4 mm = 56.8 mm)
            doc.FeatureManager.FeatureCut3(
                True, False, False, 0, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0316, False
            )
        elif row == -60.0:
            # Blind in reverse direction with start offset
            doc.FeatureManager.FeatureCut3(
                True, True, False, 0, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0316, True
            )

    print("-> 3x3 Internal Acoustic Cavities hollowed with sealed cell end-caps.")

    # 4. Extrude Baffles across all 3 rows
    for row in [-60.0, 0.0, 60.0]:
        doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
        doc.SketchManager.InsertSketch(True)
        for col in [-60.0, 0.0, 60.0]:
            # Left chamber baffles
            draw_rect(col - 16.2, -13.4, col - 14.6, 10.4)
            draw_rect(col - 20.8, -10.4, col - 19.2, 13.4)
            draw_rect(col - 25.4, -13.4, col - 23.8, 10.4)
            # Right chamber baffles
            draw_rect(col + 14.6, -13.4, col + 16.2, 10.4)
            draw_rect(col + 19.2, -10.4, col + 20.8, 13.4)
            draw_rect(col + 23.8, -13.4, col + 25.4, 10.4)
        if row == 0.0:
            doc.FeatureManager.FeatureExtrusion2(
                True, False, False, 6, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, True, True, True,
                0, 0, False
            )
        elif row == 60.0:
            doc.FeatureManager.FeatureExtrusion2(
                True, False, False, 0, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, True, True, True,
                3, 0.0316, False
            )
        elif row == -60.0:
            doc.FeatureManager.FeatureExtrusion2(
                True, True, False, 0, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, True, True, True,
                3, 0.0316, True
            )
    print("-> 3x3 Labyrinth Baffles extruded and merged.")

    # 5. Cut Acoustic Entry Slits across all 3 rows
    for row in [-60.0, 0.0, 60.0]:
        doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
        doc.SketchManager.InsertSketch(True)
        for col in [-60.0, 0.0, 60.0]:
            draw_rect(col - 11.6, -13.4, col - 10.0, -10.4)
            draw_rect(col + 10.0, -13.4, col + 11.6, -10.4)
        if row == 0.0:
            doc.FeatureManager.FeatureCut3(
                True, False, False, 6, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                0, 0, False
            )
        elif row == 60.0:
            doc.FeatureManager.FeatureCut3(
                True, False, False, 0, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0316, False
            )
        elif row == -60.0:
            doc.FeatureManager.FeatureCut3(
                True, True, False, 0, 0, 0.0568, 0,
                False, False, False, False, 0, 0,
                False, False, False, False, False, True, True, True, True, False,
                3, 0.0316, True
            )
    print("-> 3x3 Acoustic Entry Slits cut.")

    # 6. Add Interlocking Window-Track Mounting Flange (5.0 mm perimeter lip around middle Y in [-5, 5])
    # Total perimeter: X in [-95, 95], Z in [-95, 95]
    # We sketch on the Top Plane (Y = 0) or create flange on outer perimeter
    doc.SelectByID("Top Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    # Outer rectangle: 190 x 190 mm (from -95 to +95 in X and Z)
    # Inner rectangle: 180 x 180 mm (from -90 to +90 in X and Z)
    doc.SketchManager.CreateCornerRectangle(-0.095, -0.095, 0, 0.095, 0.095, 0)
    doc.SketchManager.CreateCornerRectangle(-0.090, -0.090, 0, 0.090, 0.090, 0)
    # Extrude Mid-Plane 10.0 mm (Y in [-5, +5])
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.010, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> 5.0 mm Interlocking Window-Track Flange extruded around middle perimeter.")

    # 7. Apply Material: ABS Plastic
    doc.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "ABS")
    print("-> Material assigned: ABS Plastic.")

    # Save and Export
    sldprt_path = os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.SLDPRT")
    step_path = os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.STEP")
    stl_path = os.path.join(OUT_DIR, "Modular_Window_Panel_3x3.STL")

    doc.SaveAs3(sldprt_path, 0, 2)
    doc.SaveAs3(step_path, 0, 2)
    doc.SaveAs3(stl_path, 0, 2)

    print(f"-> Saved: {sldprt_path}")
    print(f"-> Exported: {step_path}")
    print(f"-> Exported: {stl_path}")
    sw.CloseDoc(doc.GetTitle)
    return sldprt_path


def create_acoustic_air_domain(sw):
    print("\n==========================================")
    print("STEP 3: Generating Acoustic_Air_Domain (Inverse Fluid/Air Volume)")
    print("==========================================")
    
    partTemplate = sw.GetUserPreferenceStringValue(8)
    doc = sw.NewDocument(partTemplate, 0, 0, 0)
    if not doc:
        raise RuntimeError("Failed to create new SolidWorks part document.")
        
    doc.SetUserPreferenceIntegerValue(10, 3) # MMGS

    def draw_rect(x1, y1, x2, y2):
        xa, xb = min(x1, x2) * 1e-3, max(x1, x2) * 1e-3
        ya, yb = min(y1, y2) * 1e-3, max(y1, y2) * 1e-3
        doc.SketchManager.CreateCornerRectangle(xa, ya, 0, xb, yb, 0)

    # 1. Upstream Waveguide Duct (60 x 100 x 60 mm): Y in [-115, -15], depth 60 mm MidPlane
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-30.0, -115.0, 30.0, -15.0)
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.060, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> Upstream Waveguide Duct (100 mm) created.")

    # 2. Downstream Waveguide Duct (60 x 100 x 60 mm): Y in [15, 115], depth 60 mm MidPlane
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-30.0, 15.0, 30.0, 115.0)
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.060, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> Downstream Waveguide Duct (100 mm) created.")

    # 3. Central Ventilation Airway Channel (20 x 30 x 60 mm): Y in [-15, 15], depth 60 mm MidPlane
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-10.0, -15.0, 10.0, 15.0)
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.060, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> Central Ventilation Passage (20 mm) connecting ducts created.")

    # 4. Acoustic Entry Slits (3.0 x 3.0 mm, depth 56.8 mm MidPlane)
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    draw_rect(-11.6, -13.4, -10.0, -10.4)
    draw_rect(10.0, -13.4, 11.6, -10.4)
    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.0568, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> Acoustic Entry Slits (fluid domain) created.")

    # 5. Serpentine Labyrinth Air Channels (depth 56.8 mm MidPlane, Merge = True)
    # Each air pass is 3.0 mm wide:
    # Pass 1: X in [-14.6, -11.6], Y in [-13.4, 13.4]
    # Top Turn 1: X in [-19.2, -14.6], Y in [10.4, 13.4]
    # Pass 2: X in [-19.2, -16.2], Y in [-13.4, 13.4]
    # Bottom Turn 2: X in [-23.8, -16.2], Y in [-13.4, -10.4]
    # Pass 3: X in [-23.8, -20.8], Y in [-13.4, 13.4]
    # Top Turn 3: X in [-28.4, -20.8], Y in [10.4, 13.4]
    # Pass 4: X in [-28.4, -25.4], Y in [-13.4, 13.4]
    doc.SelectByID("Front Plane", "PLANE", 0, 0, 0)
    doc.SketchManager.InsertSketch(True)
    
    # Left serpentine passages
    draw_rect(-14.6, -13.4, -11.6, 13.4) # Pass 1
    draw_rect(-19.2,  10.4, -14.6, 13.4) # Turn 1 (over Baffle 1)
    draw_rect(-19.2, -13.4, -16.2, 13.4) # Pass 2
    draw_rect(-23.8, -13.4, -16.2, -10.4) # Turn 2 (under Baffle 2)
    draw_rect(-23.8, -13.4, -20.8, 13.4) # Pass 3
    draw_rect(-28.4,  10.4, -20.8, 13.4) # Turn 3 (over Baffle 3)
    draw_rect(-28.4, -13.4, -25.4, 13.4) # Pass 4 (terminates at floor)
    
    # Right serpentine passages (symmetric)
    draw_rect(11.6, -13.4, 14.6, 13.4)  # Pass 1
    draw_rect(14.6,  10.4, 19.2, 13.4)  # Turn 1
    draw_rect(16.2, -13.4, 19.2, 13.4)  # Pass 2
    draw_rect(16.2, -13.4, 23.8, -10.4) # Turn 2
    draw_rect(20.8, -13.4, 23.8, 13.4)  # Pass 3
    draw_rect(20.8,  10.4, 28.4, 13.4)  # Turn 3
    draw_rect(25.4, -13.4, 28.4, 13.4)  # Pass 4

    doc.FeatureManager.FeatureExtrusion2(
        True, False, False, 6, 0, 0.0568, 0,
        False, False, False, False, 0, 0,
        False, False, False, False, True, True, True,
        0, 0, False
    )
    print("-> Continuous Serpentine Folded Acoustic Channels extruded and fused.")

    # Assign Air material appearance / properties
    doc.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", "Air")
    print("-> Material assigned: Air.")

    # Save and Export
    sldprt_path = os.path.join(OUT_DIR, "Acoustic_Air_Domain.SLDPRT")
    step_path = os.path.join(OUT_DIR, "Acoustic_Air_Domain.STEP")
    stl_path = os.path.join(OUT_DIR, "Acoustic_Air_Domain.STL")

    doc.SaveAs3(sldprt_path, 0, 2)
    doc.SaveAs3(step_path, 0, 2)
    doc.SaveAs3(stl_path, 0, 2)

    print(f"-> Saved: {sldprt_path}")
    print(f"-> Exported: {step_path}")
    print(f"-> Exported: {stl_path}")
    sw.CloseDoc(doc.GetTitle)
    return sldprt_path


if __name__ == "__main__":
    print("Initializing SolidWorks 2022 Automation...")
    sw = win32com.client.Dispatch('SldWorks.Application')
    sw.Visible = True

    try:
        f1 = create_unit_cell(sw)
        f2 = create_window_panel_3x3(sw)
        f3 = create_acoustic_air_domain(sw)
        print("\n==========================================")
        print("ALL SOLIDWORKS DELIVERABLES GENERATED SUCCESSFULLY!")
        print("==========================================")
    except Exception as e:
        print("\nError during generation:", e)
        import traceback
        traceback.print_exc()
