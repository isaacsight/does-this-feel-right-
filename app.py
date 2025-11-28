import webview
import os

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the docs/index.html file
    html_path = os.path.join(script_dir, 'docs', 'index.html')
    
    # Convert to file:// URL
    url = f'file://{html_path}'
    
    # Create webview window
    webview.create_window(
        title='Does This Feel Right?',
        url=url,
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False
    )
    
    # Start the webview
    webview.start()

if __name__ == '__main__':
    main()
