from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Static
from rich.markdown import Markdown

GETTING_STARTED_CONTENT = """# Getting Started

Welcome to **Quantum ESPRESSO** and **QELearn**!

### What is Quantum ESPRESSO?
An open-source suite for electronic-structure calculations and materials modeling based on **Density-Functional Theory (DFT)**, plane waves, and pseudopotentials. The core workhorse engine is **`pw.x`** (*Plane-Wave Self-Consistent Field*).

### What is QELearn?
An interactive terminal tool designed to help you learn and generate Quantum ESPRESSO input files. It guides you through setting up calculations, automatically injects proper physical parameters (smearing, spin polarization, cutoffs, 2D vacuum locks), and actively explains what every parameter does.

---

### Workflow & File Organization
It is always recommended to organize your files neatly! While single-step calculations like **SCF** or **Relaxation** only require 1 input file, multi-step workflows like **Band Structure** and **DOS** require 3 input files each (`scf.in` -> `nscf(bands).in` -> post-processing `.in`).

By default, QELearn can generate files directly in your current folder (sharing `outdir = './out'`), but separating them into subfolders keeps everything clean as your project grows:

```text
silicon/
 ├── scf/     (Ground-state: scf.in)
 ├── bands/   (Band structure: scf.in, nscfbands.in, bands.in)
 ├── dos/     (Density of states: scf.in, nscf.in, dos.in)
 ├── relax/   (Geometry relaxation: relax.in)
 └── pseudo/  (Store your .UPF pseudopotential files here)
```
*Note: When using subfolders, ensure `outdir` in your NSCF/Bands files points to your converged SCF folder (e.g. `../scf/out`) and `pseudo_dir` points to `../pseudo/`.*

---

### Running in Terminal
Once your input files are created, run them in your terminal:
```bash
# Serial run (single CPU core)
pw.x -in scf.in > scf.out

# Parallel run with OpenMPI (e.g. 4 cores)
mpirun -np 4 pw.x -in scf.in > scf.out
```

---

### Quick Shortcuts
**Always check the bottom bar!** QELearn dynamically displays available keyboard shortcuts and actions right at the bottom of the screen, and some handy shortcuts only appear on specific pages.

A few universal shortcuts to keep in mind:
- **`[Tab]` / `[Shift+Tab]`**: Navigate between form fields
- **`[Ctrl+S]`**: Save all generated calculation files immediately to disk
- **`[Esc]`**: Return to the previous screen
- **`[q]`**: Open the quit confirmation dialog
"""


class GettingStartedScreen(Screen):
    """Concise Single-Page Getting Started Screen in English."""

    CSS = """
    GettingStartedScreen {
        align: center middle;
        background: #000000;
        color: #ffffff;
    }
    #gs-wrapper {
        width: 90%;
        max-width: 140;
        height: 88%;
        border: round #ffffff;
        padding: 1 2;
        background: #000000;
    }
    #gs-scroll-area {
        width: 100%;
        height: 100%;
        background: #000000;
        padding: 0 1;
    }
    #gs-content {
        width: 100%;
        background: #000000;
    }
    #nav-hint {
        dock: bottom;
        text-align: right;
        color: #aaaaaa;
        padding: 0 2;
        width: 100%;
    }
    MarkdownH1 {
        color: #00ffff;
        text-style: bold;
        margin-top: 0;
        margin-bottom: 1;
    }
    MarkdownH3 {
        color: #cc0000;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 0;
    }
    MarkdownCodeBlock {
        background: #111111;
        border: solid #444444;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("q", "go_back", "Back")
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="gs-wrapper"):
            with VerticalScroll(id="gs-scroll-area"):
                yield Static(Markdown(GETTING_STARTED_CONTENT), id="gs-content")
        yield Static("\\[↑/↓] Scroll  \\[esc] Back", id="nav-hint")

    def on_mount(self) -> None:
        """Focus the scrollable viewport on launch."""
        self.query_one("#gs-scroll-area", VerticalScroll).focus()

    def action_go_back(self) -> None:
        self.app.pop_screen()
