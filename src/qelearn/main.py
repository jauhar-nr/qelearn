from textual.app import App, ComposeResult
from textual.widgets import OptionList, Static, Button
from textual.widgets.option_list import Option
from textual.containers import Horizontal, Vertical, Grid, Center
from textual.screen import ModalScreen
from rich.markdown import Markdown

ASCII_LOGO = """
  ██████╗ ███████╗██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗
 ██╔═══██╗██╔════╝██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║
 ██║   ██║█████╗  ██║     █████╗  ███████║██████╔╝██╔██╗ ██║
 ██║▄▄ ██║██╔══╝  ██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║
 ╚██████╔╝███████╗███████╗███████╗██║  ██║██║  ██║██║ ╚████║
  ╚══▀▀═╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

Interactive Quantum ESPRESSO Input Generator & Learning Tool
────────────────────────────────────────────────────────────

Welcome! Choose a calculation workflow to begin:
"""

LEARNING_DATA = {
    "getting_started": "### Getting Started\n\nWelcome to Quantum ESPRESSO & QELearn!\n\n**Topics covered inside:**\n- **Overview:** What is Quantum ESPRESSO & QELearn?\n- **Workflows:** Input requirements for Band, DOS, SCF & Relax\n- **Organization:** How to organize your project files neatly\n- **Execution:** Running `pw.x` in serial and parallel (MPI)\n- **Shortcuts:** Useful keyboard navigation tips\n\n**Press `[Enter]` to open the full Getting Started page!**",
    "band": "### Band Structure\n\nMaps out the allowed 'highways' for electrons to travel across your crystal.\n\nRequires an initial SCF run to converge the ground-state charge density, followed by a non-self-consistent ('bands') calculation along high-symmetry K-paths in the Brillouin zone.\n\n**Generated Files:**\n- `scf.in` (pw.x)\n- `nscfbands.in` (pw.x with nbnd & nosym)\n- `bands.in` (bands.x)",
    "dos": "### Density of States (DOS)\n\nCounts how many electronic energy levels are available at every energy.\n\nRequires an SCF run to converge the charge density, followed by an NSCF run using a dense K-point mesh (strictly 2D mesh for monolayers) to integrate the density of states.\n\n**Generated Files:**\n- `scf.in` (pw.x)\n- `nscf.in` (pw.x with nbnd)\n- `dos.in` (dos.x)",
    "scf": "### Self-Consistent Field (SCF)\n\nThe foundation of all DFT calculations. Finds the absolute ground-state of your material.\n\nIteratively solves the Kohn-Sham equations until the input and output electron densities match (self-consistency), giving you the total energy and converged charge density.\n\n**Generated Files:**\n- `scf.in`",
    "relax": "### Geometry Optimization\n\nOptimizes atomic positions and unit cell parameters to minimize Hellmann-Feynman forces and stresses.\n\n- `relax` : Optimizes only atomic positions inside a fixed box.\n- `vc-relax` : Optimizes both atomic positions and cell volume/shape (automatically uses `cell_dofree = '2Dxy'` for 2D materials to prevent vacuum collapse).\n\n**Generated Files:**\n- `relax.in` (or `vc-relax.in`)"
}

class QuitScreen(ModalScreen):
    """Screen with a dialog to quit."""

    CSS = """
    QuitScreen {
        align: center middle;
        background: rgba(0, 0, 0, 0.8);
    }
    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 60;
        height: 11;
        border: round #ffffff;
        background: #000000;
    }
    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
        color: #ffffff;
    }
    Button {
        width: 100%;
        background: #000000;
        color: #ffffff;
        border: solid #ffffff;
    }
    Button:hover {
        background: #ffffff;
        color: #000000;
    }
    Button#quit {
        color: #cc0000;
    }
    Button#quit:hover {
        color: #ff0000;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Are you sure you want to quit?", id="question"),
            Button("Quit", id="quit"),
            Button("Cancel", id="cancel"),
            id="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()
            
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("left", "focus_previous", "Previous"),
        ("right", "focus_next", "Next")
    ]
    
    def action_cancel(self) -> None:
        self.app.pop_screen()
        
    def on_key(self, event) -> None:
        """Navigate buttons with arrows."""
        if event.key == "right":
            self.focus_next()
        elif event.key == "left":
            self.focus_previous()


class QELearnApp(App):
    """A Textual app to manage Quantum ESPRESSO inputs."""

    CSS = """
    Screen {
        align: center middle;
        background: #000000;
        color: #ffffff;
    }
    #app-wrapper {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    #logo {
        text-align: center;
        width: 100%;
        margin-top: 1;
        margin-bottom: 0;
        color: #ffffff;
    }
    #main-container {
        width: 90%;
        max-width: 160;
        height: 25;
        border: round #ffffff;
        padding: 1 2;
        background: #000000;
        margin: 0;
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
    .title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
        color: #ffffff;
        background: #000000;
    }
    #workflow-menu {
        height: 100%;
        border: none;
        background: #000000;
    }
    OptionList > .option-list--option {
        color: #ffffff;
    }
    OptionList > .option-list--option-highlighted {
        background: #ffffff;
        color: #000000;
        text-style: bold;
    }
    #nav-hint {
        dock: bottom;
        text-align: right;
        color: #aaaaaa;
        padding: 0 2;
        width: 100%;
    }
    
    /* Markdown Styling */
    Markdown {
        color: #ffffff;
    }
    MarkdownH3 {
        color: #cc0000;
        text-style: bold;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("q", "request_quit", "Quit")
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="app-wrapper"):
            yield Static(ASCII_LOGO.strip('\n'), id="logo")
            with Center():
                with Horizontal(id="main-container"):
                    with Vertical(id="menu-panel"):
                        yield Static("Select Workflow", classes="title")
                        yield OptionList(
                            Option("1. Getting Started", id="getting_started"),
                            Option("2. Band Structure", id="band"),
                            Option("3. Density of States (DOS)", id="dos"),
                            Option("4. Self-Consistent Field (SCF)", id="scf"),
                            Option("5. Geometry Optimization (relax/vc-relax)", id="relax"),
                            id="workflow-menu"
                        )
                    with Vertical(id="learn-panel"):
                        yield Static("Learn", classes="title")
                        yield Static(Markdown(LEARNING_DATA["getting_started"]), id="learn-content")
        yield Static("\\[↑/↓] Move  \\[enter] Select  \\[esc] back  \\[q] quit", id="nav-hint")

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        """Update the learning panel based on the highlighted option."""
        if event.option_list.id == "workflow-menu":
            option_id = event.option.id
            if option_id in LEARNING_DATA:
                self.query_one("#learn-content", Static).update(Markdown(LEARNING_DATA[option_id]))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Navigate to the Wizard screen or Getting Started guide."""
        if event.option_list.id == "workflow-menu":
            if event.option.id == "getting_started":
                from qelearn.ui.getting_started import GettingStartedScreen
                self.push_screen(GettingStartedScreen())
            else:
                self.app.workflow = event.option.id
                from qelearn.ui.wizard import ElectronicNatureScreen
                self.push_screen(ElectronicNatureScreen())

    def action_go_back(self) -> None:
        """Go back to previous screen, or quit if on main screen."""
        if len(self.screen_stack) > 1:
            self.pop_screen()
        else:
            self.push_screen(QuitScreen())

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""
        self.push_screen(QuitScreen())


def run():
    app = QELearnApp()
    app.run()

if __name__ == "__main__":
    run()
