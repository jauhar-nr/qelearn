from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Center
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from rich.markdown import Markdown

ELECTRONIC_LEARN = {
    "nonmag_insulator": "### Insulator / Semiconductor\n\nStandard non-magnetic systems with a clear band gap (e.g., Silicon for 3D bulk, h-BN for 2D monolayer).\n\n*Occupations are fixed to the lowest energy levels (no smearing needed).* ",
    "nonmag_metal": "### Metal / Semimetal\n\nSystems with zero band gap or overlapping bands at the Fermi level (e.g., Aluminum for 3D, Graphene for 2D Dirac semimetal). To achieve SCF convergence, fractional electron occupancies (smearing) are required.\n\n*Parameters Injected:*\n- `occupations = 'smearing'`\n- `smearing = 'mv'` (Marzari-Vanderbilt cold smearing)\n- `degauss = 0.02` (in Ry, ~0.27 eV)",
    "mag_insulator": "### Magnetic Insulator (AFM / Mott-Hubbard)\n\nMagnetic systems with a band gap (e.g., Antiferromagnetic NiO). Requires spin-polarized calculations (`nspin = 2`) and DFT+U (Hubbard U) to open a Mott gap. For AFM, magnetic atoms are split into 2 species with opposite starting magnetizations.\n\n*Parameters Injected:*\n- `nspin = 2`\n- `starting_magnetization(1) = 0.5`\n- `starting_magnetization(2) = -0.5`\n- `lda_plus_u = .true.`\n- `Hubbard_U(1) = 4.6`\n- `Hubbard_U(2) = 4.6`",
    "mag_metal": "### Magnetic Metal\n\nFerromagnetic or magnetic metallic systems (e.g., Fe, Ni, Co). Requires both smearing (fractional occupancies) and spin-polarization (`nspin = 2`).\n\n*Parameters Injected:*\n- `occupations = 'smearing'`\n- `smearing = 'mv'`\n- `degauss = 0.02` (in Ry, ~0.27 eV)\n- `nspin = 2`\n- `starting_magnetization(1) = 0.5`",
    "blank": "### Leave Blank\n\n*\"I know what I'm doing.\"*\n\nLeaves the template completely clean without any automatic electronic parameter injections."
}

DIMENSIONALITY_LEARN = {
    "bulk_3d": "### 3D Bulk Crystal (Standard)\n\nStandard periodic boundary conditions in x, y, and z directions.\n\n*No special dimensionality parameters injected.*",
    "layered_3d": "### 3D Layered Bulk\n\nBulk materials consisting of stacked 2D layers (e.g., Graphite, Bulk MoS2). Standard DFT fails to bind them, so van der Waals corrections are required.\n\n*Parameters Injected:*\n- `vdw_corr = 'dft-d3'`",
    "monolayer_2d": "### 2D Monolayer\n\nA single isolated layer. Requires a vacuum gap in the z-direction to prevent interaction with its periodic image.\n\n*Parameters Injected:*\n- `assume_isolated = '2D'`\n*(Note: For ibrav=0, set a large z-length in CELL_PARAMETERS, e.g. 15-20 Å, to provide vacuum)*",
    "multilayer_2d": "### 2D Multi-layer (Bilayer, etc)\n\nMultiple isolated layers (e.g., Bilayer Graphene). Requires a vacuum gap in z-direction AND van der Waals corrections to bind the layers.\n\n*Parameters Injected:*\n- `assume_isolated = '2D'`\n- `vdw_corr = 'dft-d3'`\n*(Note: For ibrav=0, set a large z-length in CELL_PARAMETERS, e.g. 15-20 Å, to provide vacuum)*",
    "blank": "### Leave Blank\n\n*\"I know what I'm doing.\"*\n\nLeaves the template completely clean."
}

PRESETS = {
    "graphene": {
        "prefix": "graphene",
        "ibrav": "0",
        "nat": "2",
        "ntyp": "1",
        "ecutwfc": "50.0",
        "ecutrho": "400.0",
        "atomic_species": ["C 12.0107 C.pbe-n-kjpaw_psl.1.0.0.UPF"],
        "cell_parameters": [
            "2.4595000000 0.0000000000 0.0000000000",
            "-1.2297500000 2.1300000000 0.0000000000",
            "0.0000000000 0.0000000000 20.0000000000"
        ],
        "atomic_positions": [
            "C 0.0000000000 0.0000000000 0.0000000000",
            "C 0.3333333333 0.6666666667 0.0000000000"
        ],
        "kpoints": "12 12 1 0 0 0"
    },
    "hbn": {
        "prefix": "hbn",
        "ibrav": "0",
        "nat": "2",
        "ntyp": "2",
        "ecutwfc": "60.0",
        "ecutrho": "480.0",
        "atomic_species": [
            "B 10.811 B.pbe-n-kjpaw_psl.1.0.0.UPF",
            "N 14.007 N.pbe-n-kjpaw_psl.1.0.0.UPF"
        ],
        "cell_parameters": [
            "2.5040000000 0.0000000000 0.0000000000",
            "-1.2520000000 2.1685285334 0.0000000000",
            "0.0000000000 0.0000000000 20.0000000000"
        ],
        "atomic_positions": [
            "B 0.0000000000 0.0000000000 0.0000000000",
            "N 0.3333333333 0.6666666667 0.0000000000"
        ],
        "kpoints": "12 12 1 0 0 0"
    },
    "silicon": {
        "prefix": "silicon",
        "ibrav": "0",
        "nat": "2",
        "ntyp": "1",
        "ecutwfc": "40.0",
        "ecutrho": "320.0",
        "atomic_species": ["Si 28.086 Si.pbe-n-kjpaw_psl.1.0.0.UPF"],
        "cell_parameters": [
            "0.0000000000 2.7150000000 2.7150000000",
            "2.7150000000 0.0000000000 2.7150000000",
            "2.7150000000 2.7150000000 0.0000000000"
        ],
        "atomic_positions": [
            "Si 0.0000000000 0.0000000000 0.0000000000",
            "Si 0.2500000000 0.2500000000 0.2500000000"
        ],
        "kpoints": "4 4 4 0 0 0"
    },
    "aluminum": {
        "prefix": "aluminum",
        "ibrav": "0",
        "nat": "1",
        "ntyp": "1",
        "ecutwfc": "40.0",
        "ecutrho": "320.0",
        "atomic_species": ["Al 26.98 Al.pbe-n-kjpaw_psl.1.0.0.UPF"],
        "cell_parameters": [
            "0.0000000000 2.0250000000 2.0250000000",
            "2.0250000000 0.0000000000 2.0250000000",
            "2.0250000000 2.0250000000 0.0000000000"
        ],
        "atomic_positions": [
            "Al 0.0000000000 0.0000000000 0.0000000000"
        ],
        "kpoints": "8 8 8 0 0 0"
    },
    "iron": {
        "prefix": "iron",
        "ibrav": "0",
        "nat": "1",
        "ntyp": "1",
        "ecutwfc": "80.0",
        "ecutrho": "640.0",
        "atomic_species": ["Fe 55.845 Fe.pbe-spn-kjpaw_psl.1.0.0.UPF"],
        "cell_parameters": [
            "-1.4330000000 1.4330000000 1.4330000000",
            "1.4330000000 -1.4330000000 1.4330000000",
            "1.4330000000 1.4330000000 -1.4330000000"
        ],
        "atomic_positions": [
            "Fe 0.0000000000 0.0000000000 0.0000000000"
        ],
        "kpoints": "8 8 8 0 0 0"
    },
    "nio": {
        "prefix": "nio",
        "ibrav": "0",
        "nat": "4",
        "ntyp": "3",
        "ecutwfc": "60.0",
        "ecutrho": "480.0",
        "atomic_species": [
            "Ni1 58.693 Ni.pbe-n-kjpaw_psl.1.0.0.UPF",
            "Ni2 58.693 Ni.pbe-n-kjpaw_psl.1.0.0.UPF",
            "O   15.999 O.pbe-n-kjpaw_psl.1.0.0.UPF"
        ],
        "cell_parameters": [
            "2.0850000000 2.0850000000 4.1700000000",
            "2.0850000000 4.1700000000 2.0850000000",
            "4.1700000000 2.0850000000 2.0850000000"
        ],
        "atomic_positions": [
            "Ni1 0.0000000000 0.0000000000 0.0000000000",
            "Ni2 0.5000000000 0.5000000000 0.5000000000",
            "O   0.2500000000 0.2500000000 0.2500000000",
            "O   0.7500000000 0.7500000000 0.7500000000"
        ],
        "kpoints": "4 4 4 0 0 0"
    },
    "graphite": {
        "prefix": "graphite",
        "ibrav": "0",
        "nat": "4",
        "ntyp": "1",
        "ecutwfc": "50.0",
        "ecutrho": "400.0",
        "atomic_species": ["C 12.0107 C.pbe-n-kjpaw_psl.1.0.0.UPF"],
        "cell_parameters": [
            "2.4640000000 0.0000000000 0.0000000000",
            "-1.2320000000 2.1338865949 0.0000000000",
            "0.0000000000 0.0000000000 6.7110000000"
        ],
        "atomic_positions": [
            "C 0.0000000000 0.0000000000 0.2500000000",
            "C 0.0000000000 0.0000000000 0.7500000000",
            "C 0.3333333333 0.6666666667 0.2500000000",
            "C 0.6666666667 0.3333333333 0.7500000000"
        ],
        "kpoints": "12 12 4 0 0 0"
    },
    "hbn_bulk": {
        "prefix": "hbn_bulk",
        "ibrav": "0",
        "nat": "4",
        "ntyp": "2",
        "ecutwfc": "60.0",
        "ecutrho": "480.0",
        "atomic_species": [
            "B 10.811 B.pbe-n-kjpaw_psl.1.0.0.UPF",
            "N 14.007 N.pbe-n-kjpaw_psl.1.0.0.UPF"
        ],
        "cell_parameters": [
            "2.5040000000 0.0000000000 0.0000000000",
            "-1.2520000000 2.1685276111 0.0000000000",
            "0.0000000000 0.0000000000 6.6600000000"
        ],
        "atomic_positions": [
            "B 0.0000000000 0.0000000000 0.2500000000",
            "B 0.0000000000 0.0000000000 0.7500000000",
            "N 0.3333333333 0.6666666667 0.2500000000",
            "N 0.6666666667 0.3333333333 0.7500000000"
        ],
        "kpoints": "12 12 4 0 0 0"
    },
    "fe_monolayer": {
        "prefix": "fe_monolayer",
        "ibrav": "0",
        "nat": "1",
        "ntyp": "1",
        "ecutwfc": "80.0",
        "ecutrho": "640.0",
        "atomic_species": ["Fe 55.845 Fe.pbe-spn-kjpaw_psl.1.0.0.UPF"],
        "cell_parameters": [
            "2.8660000000 0.0000000000 0.0000000000",
            "0.0000000000 2.8660000000 0.0000000000",
            "0.0000000000 0.0000000000 20.0000000000"
        ],
        "atomic_positions": [
            "Fe 0.0000000000 0.0000000000 0.0000000000"
        ],
        "kpoints": "12 12 1 0 0 0"
    },
    "nio_2d": {
        "prefix": "nio_2d",
        "ibrav": "0",
        "nat": "4",
        "ntyp": "3",
        "ecutwfc": "60.0",
        "ecutrho": "480.0",
        "atomic_species": [
            "Ni1 58.693 Ni.pbe-n-kjpaw_psl.1.0.0.UPF",
            "Ni2 58.693 Ni.pbe-n-kjpaw_psl.1.0.0.UPF",
            "O   15.999 O.pbe-n-kjpaw_psl.1.0.0.UPF"
        ],
        "cell_parameters": [
            "2.9530000000 0.0000000000 0.0000000000",
            "-1.4765000000 2.5573727974 0.0000000000",
            "0.0000000000 0.0000000000 20.0000000000"
        ],
        "atomic_positions": [
            "Ni1 0.0000000000 0.0000000000 0.5000000000",
            "Ni2 0.3333333333 0.6666666667 0.5000000000",
            "O   0.6666666667 0.3333333333 0.4400000000",
            "O   0.0000000000 0.0000000000 0.5600000000"
        ],
        "kpoints": "12 12 1 0 0 0"
    }
}

class ElectronicNatureScreen(Screen):
    """Step 1 of the Setup Wizard."""
    
    CSS = """
    #setup-main {
        width: 90%;
        max-width: 160;
        height: 32;
        border: round #ffffff;
        padding: 1 2;
        background: #000000;
        margin: 2 0;
    }
    #menu-panel {
        width: 50%;
        height: 100%;
        border-right: solid #ffffff;
        padding-right: 2;
    }
    #learn-panel {
        width: 50%;
        height: 100%;
        padding-left: 2;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Center():
            with Horizontal(id="setup-main"):
                with Vertical(id="menu-panel"):
                    yield Static(" CHOOSE MATERIAL TYPE: ELECTRONIC NATURE ", classes="title")
                    yield OptionList(
                        Option("1. Insulator / Semiconductor", id="nonmag_insulator"),
                        Option("2. Metal", id="nonmag_metal"),
                        Option("3. Magnetic Insulator / Semiconductor", id="mag_insulator"),
                        Option("4. Magnetic Metal", id="mag_metal"),
                        Option("5. Leave Blank", id="blank"),
                        id="electronic_options"
                    )
                with Vertical(id="learn-panel"):
                    yield Static(" LEARN ", classes="title")
                    yield Static(Markdown(ELECTRONIC_LEARN["nonmag_insulator"]), id="wizard-learn-content")
        yield Static("\\[↑/↓] Move   \\[enter] Next   \\[esc] Back", id="nav-hint")

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        option_id = event.option.id
        if option_id in ELECTRONIC_LEARN:
            self.query_one("#wizard-learn-content", Static).update(Markdown(ELECTRONIC_LEARN[option_id]))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if not hasattr(self.app, 'setup_choices'):
            self.app.setup_choices = {}
        self.app.setup_choices['electronic'] = event.option.id
        self.app.push_screen(DimensionalityScreen())

class DimensionalityScreen(Screen):
    """Step 2 of the Setup Wizard."""
    
    CSS = """
    #setup-main {
        width: 90%;
        max-width: 160;
        height: 32;
        border: round #ffffff;
        padding: 1 2;
        background: #000000;
        margin: 2 0;
    }
    #menu-panel {
        width: 50%;
        height: 100%;
        border-right: solid #ffffff;
        padding-right: 2;
    }
    #learn-panel {
        width: 50%;
        height: 100%;
        padding-left: 2;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Center():
            with Horizontal(id="setup-main"):
                with Vertical(id="menu-panel"):
                    yield Static(" CHOOSE MATERIAL TYPE: DIMENSIONALITY ", classes="title")
                    yield OptionList(
                        Option("1. 3D Bulk Crystal", id="bulk_3d"),
                        Option("2. 3D Layered Bulk (Graphite, etc)", id="layered_3d"),
                        Option("3. 2D Monolayer", id="monolayer_2d"),
                        Option("4. 2D Multi-layer (Bilayer/Trilayer)", id="multilayer_2d"),
                        Option("5. Leave Blank", id="blank"),
                        id="dim_options"
                    )
                with Vertical(id="learn-panel"):
                    yield Static(" LEARN ", classes="title")
                    yield Static(Markdown(DIMENSIONALITY_LEARN["bulk_3d"]), id="wizard-learn-content")
        yield Static("\\[↑/↓] Move   \\[enter] Build Template   \\[esc] Back", id="nav-hint")

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        option_id = event.option.id
        if option_id in DIMENSIONALITY_LEARN:
            self.query_one("#wizard-learn-content", Static).update(Markdown(DIMENSIONALITY_LEARN[option_id]))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.app.setup_choices['dimensionality'] = event.option.id
        
        from qelearn.ui.screens import SCF_TEMPLATE, SystemSetupScreen
        import copy
        
        template = copy.deepcopy(SCF_TEMPLATE)
        
        elec = self.app.setup_choices.get('electronic')
        dim = self.app.setup_choices.get('dimensionality')

        # 1. Determine preset to load if not leaving blank
        preset_to_load = None
        if elec != "blank" or dim != "blank":
            if elec == "nonmag_insulator":
                if dim in ["monolayer_2d", "multilayer_2d"]:
                    preset_to_load = "hbn"
                elif dim == "layered_3d":
                    preset_to_load = "hbn_bulk"
                else:
                    preset_to_load = "silicon"
            elif elec == "nonmag_metal":
                if dim in ["monolayer_2d", "multilayer_2d"]:
                    preset_to_load = "graphene"
                elif dim == "layered_3d":
                    preset_to_load = "graphite"
                else:
                    preset_to_load = "aluminum"
            elif elec == "mag_insulator":
                if dim in ["monolayer_2d", "multilayer_2d"]:
                    preset_to_load = "nio_2d"
                else:
                    preset_to_load = "nio"
            elif elec == "mag_metal":
                if dim in ["monolayer_2d", "multilayer_2d"]:
                    preset_to_load = "fe_monolayer"
                else:
                    preset_to_load = "iron"

        # 2. Apply preset values to template
        if preset_to_load:
            preset = PRESETS[preset_to_load]
            for line in template:
                if line.get("type") == "field" and line.get("key") in preset:
                    if isinstance(preset[line["key"]], str):
                        line["value"] = preset[line["key"]]
            
            # Handle multiline fields (atomic_positions, cell_parameters, atomic_species)
            for list_key in ["atomic_positions", "cell_parameters", "atomic_species"]:
                pos_idx = -1
                for i, line in enumerate(template):
                    if line.get("key") == list_key:
                        pos_idx = i
                        break
                
                if pos_idx != -1 and list_key in preset:
                    template[pos_idx]["value"] = preset[list_key][0]
                    for pos in reversed(preset[list_key][1:]):
                        new_line = template[pos_idx].copy()
                        new_line["value"] = pos
                        template.insert(pos_idx + 1, new_line)

        # 3. Inject dynamic parameters
        insert_idx = 0
        for i, line in enumerate(template):
            if line.get("key") == "ecutwfc":
                insert_idx = i
                break
                
        def insert_field(key, label, value):
            nonlocal insert_idx
            template.insert(insert_idx, {"type": "field", "key": key, "label": label, "value": value, "quote": False, "suffix": ","})
            insert_idx += 1
            
        def insert_field_quote(key, label, value):
            nonlocal insert_idx
            template.insert(insert_idx, {"type": "field", "key": key, "label": label, "value": value, "quote": True, "suffix": ","})
            insert_idx += 1

        if elec in ["nonmag_metal", "mag_metal"]:
            insert_field_quote("occupations", "  occupations = ", "smearing")
            insert_field_quote("smearing", "  smearing = ", "mv")
            insert_field("degauss", "  degauss = ", "0.02")
        
        if elec == "mag_metal":
            insert_field("nspin", "  nspin = ", "2")
            insert_field("starting_magnetization(1)", "  starting_magnetization(1) = ", "0.5")

        if elec == "mag_insulator":
            insert_field("nspin", "  nspin = ", "2")
            insert_field("starting_magnetization(1)", "  starting_magnetization(1) = ", "0.5")
            insert_field("starting_magnetization(2)", "  starting_magnetization(2) = ", "-0.5")
            insert_field("lda_plus_u", "  lda_plus_u = ", ".true.")
            insert_field("Hubbard_U(1)", "  Hubbard_U(1) = ", "4.6")
            insert_field("Hubbard_U(2)", "  Hubbard_U(2) = ", "4.6")

        if dim in ["monolayer_2d", "multilayer_2d"]:
            insert_field_quote("assume_isolated", "  assume_isolated = ", "2D")
            
        if dim in ["layered_3d", "multilayer_2d"]:
            insert_field_quote("vdw_corr", "  vdw_corr = ", "dft-d3")
            
        # 4. Enforce 2D rules
        if dim in ["monolayer_2d", "multilayer_2d"]:
            for line in template:
                if line.get("key") == "kpoints":
                    parts = line["value"].split()
                    if len(parts) >= 3:
                        parts[2] = "1"
                    if len(parts) >= 6:
                        parts[5] = "0"
                    line["value"] = " ".join(parts)
            
        # 5. Inject Workflow specific changes
        workflow = getattr(self.app, 'workflow', 'scf')
        if workflow == "relax":
            # Change calculation to a field
            for line in template:
                if line.get("key") == "calculation":
                    line["type"] = "field"
                    line["label"] = "  calculation = "
                    line["value"] = "vc-relax"
                    line["quote"] = True
                    line["suffix"] = ","
                    if "text" in line:
                        del line["text"]
            
            # Inject &IONS and &CELL blocks after &ELECTRONS
            electrons_slash_idx = -1
            in_electrons = False
            for i, line in enumerate(template):
                if line.get("key") == "electrons_block":
                    in_electrons = True
                elif in_electrons and line.get("key") == "slash":
                    electrons_slash_idx = i
                    break
            
            if electrons_slash_idx != -1:
                ions_cell_blocks = [
                    {"type": "static", "key": "empty", "text": ""},
                    {"type": "static", "key": "ions_block", "text": "&IONS"},
                    {"type": "static", "key": "slash", "text": "/"},
                    {"type": "static", "key": "empty", "text": ""},
                    {"type": "static", "key": "cell_block", "text": "&CELL"},
                ]
                if dim in ["monolayer_2d", "multilayer_2d"]:
                    ions_cell_blocks.append({"type": "field", "key": "cell_dofree", "label": "  cell_dofree = ", "value": "2Dxy", "quote": True, "suffix": ","})
                ions_cell_blocks.append({"type": "static", "key": "slash", "text": "/"})
                template[electrons_slash_idx+1:electrons_slash_idx+1] = ions_cell_blocks

        self.app.push_screen(SystemSetupScreen(template=template))
