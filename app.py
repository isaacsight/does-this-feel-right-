import webview
import os
import sys

def main():
    # Get the resource path (different when bundled vs development)
    if getattr(sys, 'frozen', False):
        # Running as bundled app
        bundle_dir = os.path.dirname(sys.executable)
        resource_path = os.path.join(bundle_dir, '..', 'Resources')
    else:
        # Running in development
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resource_path = os.path.join(script_dir, 'docs')
    
    # Path to index.html
    html_path = os.path.join(resource_path, 'index.html')
    
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
