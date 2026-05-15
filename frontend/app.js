const API_URL = "http://127.0.0.1:5000/detect";

// ── Character counter ──
document.getElementById("textInput").addEventListener("input", function () {
    document.getElementById("charCount").textContent = this.value.length;
});

// ── Safe Search toggle ──
document.getElementById("safeSearchToggle").addEventListener("change", function () {
    const label   = document.getElementById("toggleText");
    const warning = document.getElementById("adultWarning");

    if (this.checked) {
        label.textContent = "ON";
        label.className   = "toggle-text on";
        warning.classList.add("hidden");
    } else {
        const confirmed = confirm(
            "⚠️  Turn off Safe Search?\n\n" +
            "Adult and 18+ emoji content may appear in results.\n\n" +
            "Only continue if you are 18 years or older."
        );

        if (!confirmed) {
            this.checked = true; // cancel the toggle
            return;
        }

        label.textContent = "OFF";
        label.className   = "toggle-text off";
        warning.classList.remove("hidden");
    }
});

// ── Fill example text ──
function fillExample(btn) {
    const text = btn.textContent.replace(/[^\w\s!?,.'"-]/g, "").trim();
    const input = document.getElementById("textInput");
    input.value = text;
    document.getElementById("charCount").textContent = text.length;
    input.focus();
}

// ── Main detect function ──
async function detectEmojis() {
    const text       = document.getElementById("textInput").value.trim();
    const safeSearch = document.getElementById("safeSearchToggle").checked;
    const btn        = document.getElementById("detectBtn");

    if (!text) {
        showToast("Please type something first!", "#e96cff");
        return;
    }

    // Show loading
    btn.disabled = true;
    document.getElementById("btnText").textContent = "Detecting...";
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("resultsCard").classList.add("hidden");

    try {
        const response = await fetch(API_URL, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ text, safe_search: safeSearch })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || `Server error ${response.status}`);
        }

        const data = await response.json();

        // Display results — one card per emoji with its name
        const display = document.getElementById("emojiDisplay");
        if (data.emojis && data.emojis.length > 0) {
            display.innerHTML = data.emojis.map(item =>
                `<div class="emoji-card">
                    <span class="emoji-char">${item.emoji}</span>
                    <span class="emoji-name">${item.name}</span>
                </div>`
            ).join("");
        } else {
            display.innerHTML = `<div class="emoji-card"><span class="emoji-char">🤷</span><span class="emoji-name">No Match</span></div>`;
        }

        document.getElementById("explanation").textContent =
            data.explanation || "No explanation provided.";

        document.getElementById("loading").classList.add("hidden");
        document.getElementById("resultsCard").classList.remove("hidden");

    } catch (err) {
        document.getElementById("loading").classList.add("hidden");
        showToast("Error: " + err.message, "#dc3545");
    } finally {
        btn.disabled = false;
        document.getElementById("btnText").textContent = "Detect Emojis";
    }
}

// ── Copy emojis to clipboard (only the emoji characters, not the names) ──
function copyEmojis() {
    const chars = [...document.querySelectorAll(".emoji-char")]
        .map(el => el.textContent).join(" ");
    navigator.clipboard.writeText(chars)
        .then(() => showToast("Copied! " + chars))
        .catch(() => showToast("Copy failed — try selecting manually", "#dc3545"));
}

// ── Reset to input view ──
function tryAgain() {
    document.getElementById("resultsCard").classList.add("hidden");
    document.getElementById("textInput").focus();
}

// ── Toast notification ──
function showToast(message, color = "#28a745") {
    let toast = document.querySelector(".toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.className = "toast";
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.style.background = color;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2800);
}

// ── Ctrl+Enter shortcut ──
document.getElementById("textInput").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.ctrlKey) detectEmojis();
});
