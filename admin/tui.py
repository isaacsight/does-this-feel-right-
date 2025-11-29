from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, ListView, ListItem, Label, Input, TextArea, Markdown, Select
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Button, Static, ListView, ListItem, Label, Input, TextArea, Markdown, Select, Log, TabbedContent, TabPane
from textual.binding import Binding
import core
import os

class PostListItem(ListItem):
    def __init__(self, post):
        super().__init__()
        self.post = post

    def compose(self) -> ComposeResult:
        title = self.post.get('title', 'Untitled')
        date = self.post.get('date', 'No Date')
        yield Label(f"{title} ({date})")

class EditorScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Cancel"), ("ctrl+s", "save_post", "Save")]

    def __init__(self, post=None):
        super().__init__()
        self.post = post or {}
        self.filename = self.post.get('filename')

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Input(placeholder="Title", value=self.post.get('title', ''), id="title"),
            Input(placeholder="Date (YYYY-MM-DD)", value=str(self.post.get('date', '')), id="date"),
            Input(placeholder="Category", value=self.post.get('category', ''), id="category"),
            Input(placeholder="Tags (comma separated)", value=str(self.post.get('tags', '')), id="tags"),
            TextArea(self.post.get('content', ''), id="content", show_line_numbers=True),
            id="editor-container"
        )
        yield Footer()

    def action_save_post(self):
        title = self.query_one("#title", Input).value
        date = self.query_one("#date", Input).value
        category = self.query_one("#category", Input).value
        tags = self.query_one("#tags", Input).value
        content = self.query_one("#content", TextArea).text
        
        core.save_post(self.filename, title, date, category, tags, content)
        self.app.pop_screen()
        self.app.notify("Post saved!")

class AIGenerationModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Enter topic for AI Post:"),
            Input(placeholder="Topic...", id="topic"),
            Label("Select Provider:"),
            Select([("Gemini", "gemini"), ("ChatGPT", "openai"), ("Claude", "anthropic")], value="gemini", id="provider"),
            Button("Generate", variant="primary", id="generate"),
            Button("Cancel", variant="error", id="cancel"),
            id="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate":
            topic = self.query_one("#topic", Input).value
            provider = self.query_one("#provider", Select).value
            if topic:
                try:
                    filename = core.generate_ai_post(topic, provider=provider)
                    self.app.notify(f"Generated {filename} with {provider}")
                    self.dismiss(True)
                except Exception as e:
                    self.app.notify(f"Error: {e}", severity="error")
        elif event.button.id == "cancel":
            self.dismiss(False)

class BlogTUI(App):
    CSS = """
    Screen {
        layout: horizontal;
    }
    #sidebar {
        width: 30;
        background: $panel;
        border-right: vkey $accent;
    }
    #main {
        width: 1fr;
        padding: 1;
    }
    PostListItem {
        padding: 1;
        border-bottom: solid $primary-background-lighten-1;
    }
    PostListItem:hover {
        background: $accent;
    }
    #editor-container {
        padding: 1;
    }
    TextArea {
        height: 1fr;
        margin-top: 1;
    }
    #dialog {
        padding: 2;
        background: $surface;
        border: solid $accent;
        width: 60;
        height: auto;
        align: center middle;
    }
    #dashboard-status {
        height: auto;
        border: solid $accent;
        padding: 1;
        margin-bottom: 1;
    }
    #server-logs {
        height: 1fr;
        border: solid $secondary;
        background: $surface;
    }
    .status-running {
        color: $success;
    }
    .status-stopped {
        color: $error;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("n", "new_post", "New Post"),
        ("r", "refresh_posts", "Refresh"),
        ("g", "generate_ai", "AI Generate"),
        ("p", "publish_git", "Publish (Git)"),
        ("s", "start_server", "Start Server"),
        ("x", "stop_server", "Stop Server"),
        ("1", "show_dashboard", "Dashboard"),
        ("2", "show_posts", "Posts"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="dashboard", id="main-tabs"):
            with TabPane("Dashboard", id="dashboard"):
                yield Container(
                    Label("Server Status: Stopped", id="status-label", classes="status-stopped"),
                    Horizontal(
                        Button("Start Server", variant="success", id="start-server"),
                        Button("Stop Server", variant="error", id="stop-server"),
                        classes="buttons"
                    ),
                    Label("Server Logs:", classes="log-label"),
                    Log(id="server-logs"),
                    id="dashboard-container"
                )
            with TabPane("Posts", id="posts"):
                yield Container(
                    ListView(id="post-list"),
                    id="sidebar"
                )
                yield Container(
                    Markdown("# Select a post to edit or press 'n' to create new."),
                    id="main"
                )
        yield Footer()

    def on_mount(self) -> None:
        self.server_manager = core.ServerManager()
        self.refresh_posts()
        self.set_interval(2, self.update_server_status)

    def update_server_status(self):
        status = self.server_manager.get_status()
        label = self.query_one("#status-label", Label)
        label.update(f"Server Status: {status}")
        
        if status == "Running":
            label.remove_class("status-stopped")
            label.add_class("status-running")
            # Update logs
            logs = self.server_manager.get_logs()
            log_view = self.query_one("#server-logs", Log)
            log_view.clear()
            log_view.write(logs)
        else:
            label.remove_class("status-running")
            label.add_class("status-stopped")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-server":
            msg = self.server_manager.start_server()
            self.notify(msg)
        elif event.button.id == "stop-server":
            msg = self.server_manager.stop_server()
            self.notify(msg)

    def refresh_posts(self):
        posts = core.get_posts()
        list_view = self.query_one("#post-list", ListView)
        list_view.clear()
        for post in posts:
            list_view.append(PostListItem(post))

    def on_list_view_selected(self, event: ListView.Selected):
        post = event.item.post
        self.push_screen(EditorScreen(post))

    def action_start_server(self):
        msg = self.server_manager.start_server()
        self.notify(msg)
        self.update_server_status()

    def action_stop_server(self):
        msg = self.server_manager.stop_server()
        self.notify(msg)
        self.update_server_status()

    def action_show_dashboard(self):
        self.query_one("#main-tabs", TabbedContent).active = "dashboard"

    def action_show_posts(self):
        self.query_one("#main-tabs", TabbedContent).active = "posts"

    def action_new_post(self):
        self.push_screen(EditorScreen())

    def action_refresh_posts(self):
        self.refresh_posts()
        self.notify("Posts refreshed")

    def action_generate_ai(self):
        def check_result(result):
            if result:
                self.refresh_posts()
        self.push_screen(AIGenerationModal(), check_result)

    def action_publish_git(self):
        try:
            msg = core.publish_git()
            self.notify(msg)
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")

if __name__ == "__main__":
    app = BlogTUI()
    app.run()
