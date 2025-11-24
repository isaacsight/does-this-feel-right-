// Support button widget trigger
document.addEventListener('DOMContentLoaded', () => {
    const supportBtn = document.getElementById('bmc-support-btn');
    if (supportBtn) {
        supportBtn.addEventListener('click', () => {
            // The BMC widget auto-initializes, we just need to trigger it
            // The widget listens for clicks on elements with specific data attributes
            // So we'll create a temporary element and click it
            const bmcWidget = document.querySelector('.bmc-btn');
            if (bmcWidget) {
                bmcWidget.click();
            }
        });
    }
});
