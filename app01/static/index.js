const offset = 69;
const angles = []; //in deg
for (let i = 0; i <= 360; i += 45) {
    angles.push((i * Math.PI) / 180);
}
let nearBy = [];

function clearNearBy() {
    nearBy.splice(0, nearBy.length).forEach((e) => (e.style.borderImage = null));
}


document.querySelectorAll(".win-btn").forEach((b) => {

    b.onmouseleave = (e) => {
        e.target.style.background = "black";
        e.target.style.borderImage = null;
        e.target.border = "1px solid transparent";
    };

    b.onmouseenter = (e) => {
        clearNearBy();
    };

    b.addEventListener("mousemove", (e) => {
        e.target.border = "1px solid transparent";
        const rect = e.target.getBoundingClientRect();
        const x = e.clientX - rect.left; //x position within the element.
        const y = e.clientY - rect.top; //y position within the element.
        e.target.style.background = `radial-gradient(circle at ${x}px ${y}px , rgba(255,255,255,0.25),rgba(255,255,255,0) )`;
        e.target.style.borderImage = `radial-gradient(20% 65% at ${x}px ${y}px ,rgba(255,255,255,0.7),rgba(255,255,255,0.7),rgba(255,255,255,0.1) ) 9 / 2px / 0px stretch `;
    });
});

const body = document.querySelector(".win-grid");

body.addEventListener("mousemove", (e) => {

    const x = e.x; //x position within the element.
    const y = e.y; //y position within the element.

    clearNearBy();
    nearBy = angles.reduce((acc, rad, i, arr) => {
        const cx = Math.floor(x + Math.cos(rad) * offset);
        const cy = Math.floor(y + Math.sin(rad) * offset);
        const element = document.elementFromPoint(cx, cy);

        if (element !== null) {

            if (
                element.className === "win-btn" &&
                acc.findIndex((ae) => ae.id === element.id) < 0
            ) {
                const brect = element.getBoundingClientRect();
                const bx = x - brect.left; // x position within the element.
                const by = y - brect.top;  // y position within the element.
                if (!element.style.borderImage)
                    element.style.borderImage = `radial-gradient(${offset * 2}px ${offset * 2
                        }px at ${bx}px ${by}px ,rgba(255,255,255,0.7),rgba(255,255,255,0.1),transparent ) 9 / 1px / 0px stretch `;
                return [...acc, element];
            }
        }
        return acc;
    }, []);
});

body.onmouseleave = (e) => {
    clearNearBy();
};