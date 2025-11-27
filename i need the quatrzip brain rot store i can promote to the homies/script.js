document.addEventListener('DOMContentLoaded', () => {
    console.log("BRAIN ROT INITIATED 🧠📉");

    // Brain Rot Meter
    let brainRotLevel = 0;
    const meterDisplay = document.getElementById('rot-level');
    
    function increaseBrainRot(amount) {
        brainRotLevel += amount;
        if (meterDisplay) {
            meterDisplay.innerText = brainRotLevel + "%";
            
            if (brainRotLevel > 100) {
                document.body.style.filter = `hue-rotate(${brainRotLevel}deg)`;
            }
            if (brainRotLevel > 500) {
                document.body.style.transform = `rotate(${Math.random() * 2 - 1}deg)`;
            }
        }
    }

    // Scroll increases brain rot
    window.addEventListener('scroll', () => {
        increaseBrainRot(0.1);
    });

    // Buy Button Evasion (The "Slippery" Button)
    const buyButtons = document.querySelectorAll('.buy-btn');
    
    buyButtons.forEach(btn => {
        btn.addEventListener('mouseover', (e) => {
            // 30% chance to move away
            if (Math.random() > 0.7) {
                const x = (Math.random() - 0.5) * 200;
                const y = (Math.random() - 0.5) * 200;
                btn.style.transform = `translate(${x}px, ${y}px)`;
                increaseBrainRot(5);
            }
        });

        btn.addEventListener('click', () => {
            alert("OUT OF STOCK DUE TO FANUM TAX 📉");
            increaseBrainRot(10);
        });
    });

    // Random Title Flashing
    setInterval(() => {
        const titles = ["QUATRZIP", "QUATRZIP 💀", "QUATRZIP 🤡", "QUATRZIP 🥶", "QUATRZIP 🗿"];
        document.title = titles[Math.floor(Math.random() * titles.length)];
    }, 1000);

    // Konami Code for Ultimate Rot
    let keys = [];
    const konami = "ArrowUpArrowUpArrowDownArrowDownArrowLeftArrowRightArrowLeftArrowRightba";
    
    window.addEventListener('keydown', (e) => {
        keys.push(e.key);
        keys.splice(-konami.length - 1, keys.length - konami.length);
        if (keys.join('').includes(konami)) {
            alert("GOD MODE ACTIVATED: SKIBIDI OVERLOAD");
            document.body.style.animation = "spin 5s infinite linear";
            increaseBrainRot(9000);
        }
    });
});

// Add spin animation dynamically
const styleSheet = document.createElement("style");
styleSheet.innerText = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(styleSheet);
