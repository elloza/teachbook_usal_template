// Custom UI Injection (Language Switcher + PDF + Slides Button)
document.addEventListener("DOMContentLoaded", function () {
    const TEACHBOOK_VERSION = "3.0";
    if (window.TEACHBOOK_LOADED_VERSION === TEACHBOOK_VERSION) return;
    window.TEACHBOOK_LOADED_VERSION = TEACHBOOK_VERSION;

    const TEACHBOOK_DEBUG = new URLSearchParams(window.location.search).has("teachbook_debug")
        || localStorage.getItem("teachbook-debug") === "true";
    const debugLog = (...args) => {
        if (TEACHBOOK_DEBUG) console.log(...args);
    };

    // 1. Find languages.json by climbing directories
    // From /repo/es/intro.html:       ../_static/languages.json → found (prefix = "../")
    // From /repo/es/sub/page.html:    ../../_static/languages.json → found (prefix = "../../")
    // From /repo/index.html:          _static/languages.json → found (prefix = "")
    // The prefix that works IS the relative path to the book root.

    async function findLanguagesJson() {
        const candidates = [];
        const addCandidate = (prefix) => {
            if (typeof prefix !== "string") return;
            const normalized = prefix === "." || prefix === "./" ? "" : prefix;
            if (!candidates.includes(normalized)) candidates.push(normalized);
        };

        // Sphinx writes the relative path to the HTML root here. Trying it
        // first avoids a predictable 404 on /<lang>/ pages in GitHub Pages.
        addCandidate(document.documentElement.dataset.content_root);
        if (window.DOCUMENTATION_OPTIONS && window.DOCUMENTATION_OPTIONS.URL_ROOT) {
            addCandidate(window.DOCUMENTATION_OPTIONS.URL_ROOT);
        }

        let prefix = '';
        for (let depth = 0; depth < 10; depth++) {
            addCandidate(prefix);
            prefix = '../' + prefix;
        }

        for (const candidate of candidates) {
            try {
                const url = candidate + '_static/languages.json';
                const res = await fetch(url);
                if (res.ok) {
                    const languages = await res.json();
                    debugLog(`TeachBook: Found languages.json at rootPrefix="${candidate}"`);
                    return { languages, rootPrefix: candidate };
                }
            } catch (e) { /* continue */ }
        }
        return null;
    }

    findLanguagesJson().then(result => {
        if (!result) {
            debugLog("TeachBook: Language switcher disabled (languages.json not found).");
            return;
        }

        const { languages, rootPrefix } = result;

        if (languages.length > 1) {
            injectLanguageSwitcher(languages, rootPrefix);
        } else {
            debugLog("TeachBook: Single language detected. Hiding switcher.");
        }

        // Inject PDF Button
        injectPDFButton(languages, rootPrefix);

        // Inject contextual Slidev button when a slides manifest is available.
        injectSlidesButton(languages, rootPrefix, debugLog);

        // Search page fix: Sphinx search sometimes generates duplicated language prefixes
        // like /es/es/page.html or sidebar links like es/intro.html inside /es/search.html.
        // We normalize those links client-side to keep search usable even if Sphinx emits
        // inconsistent paths in standalone multilingual builds.
        fixSearchPageLinks(rootPrefix, languages, debugLog);
    });

    // 3. Robust Sidebar Toggle (Manual Handler with Polling)
    // The theme's native behavior is unreliable due to ID mismatches.
    // We implement a manual toggle to guarantee functionality.
    // POLLING: We run this check multiple times to catch elements rendered late by theme JS.

    function applySidebarFix() {
        // Find toggles that haven't been fixed yet
        const primaryToggles = document.querySelectorAll('label[for="__primary"]:not([data-fixed]), .primary-toggle:not([data-fixed])');

        primaryToggles.forEach(toggle => {
            toggle.setAttribute('data-fixed', 'true');

            // Do NOT remove 'for' or clone node. Let native/theme behavior persist.
            // Just ADD our listener for the desktop class toggle.
            toggle.addEventListener('click', () => {
                // Do NOT prevent default or stop propagation.
                // Let the theme handle the mobile logic.

                // Toggle custom class for desktop support. This is harmless on
                // mobile because the CSS rule is media-queried.
                document.documentElement.classList.toggle('teachbook-sidebar-hidden');
                debugLog("TeachBook: Toggled 'teachbook-sidebar-hidden'");
            });
        });

        // Secondary sidebar (if needed, same logic)
        const secondaryToggles = document.querySelectorAll('label[for="__secondary"]:not([data-fixed]), .secondary-toggle:not([data-fixed])');

        secondaryToggles.forEach(toggle => {
            toggle.setAttribute('data-fixed', 'true');
            // Do NOT clone or strip. Marking the element prevents duplicated work
            // while preserving the theme's native secondary sidebar behavior.
        });
    }

    // Run immediately
    applySidebarFix();

    // Re-run periodically to catch late-loading elements
    const intervalId = setInterval(applySidebarFix, 500);

    // Stop polling after 5 seconds to save resources
    setTimeout(() => clearInterval(intervalId), 5000);

    // Accessibility: OpenDyslexic Toggle
    (function() {
        // Load OpenDyslexic font from CDN (lazy — only when needed, but preloaded for instant toggle)
        const fontLink = document.createElement("link");
        fontLink.rel = "stylesheet";
        fontLink.href = "https://fonts.cdnfonts.com/css/opendyslexic";
        fontLink.id = "opendyslexic-font-link";
        document.head.appendChild(fontLink);

        // Create toggle button
        const header = document.querySelector(".article-header-buttons");
        if (!header) return;

        const btn = document.createElement("button");
        btn.className = "btn btn-sm teachbook-a11y-btn";
        btn.title = "Modo accesibilidad (OpenDyslexic) / Accessibility mode";
        btn.innerHTML = '<i class="fa-solid fa-universal-access"></i>';
        btn.setAttribute("aria-label", "Toggle accessibility font");

        // Check saved state
        if (localStorage.getItem("teachbook-opendyslexic") === "true") {
            document.documentElement.classList.add("opendyslexic-mode");
            btn.classList.add("active");
        }

        btn.addEventListener("click", function() {
            document.documentElement.classList.toggle("opendyslexic-mode");
            const isActive = document.documentElement.classList.contains("opendyslexic-mode");
            localStorage.setItem("teachbook-opendyslexic", isActive);
            btn.classList.toggle("active", isActive);
        });

        // Insert at the beginning of header buttons (before language switcher)
        header.prepend(btn);
    })();
});

function fixSearchPageLinks(rootPrefix, languages, debugLog = () => {}) {
    if (!window.location.pathname.endsWith('/search.html')) return;

    const langCodes = languages.map(l => l.code);

    function normalizeHref(href) {
        if (!href || href.startsWith('http://') || href.startsWith('https://') || href.startsWith('#')) {
            return href;
        }

        let fixed = href;

        // Fix duplicated lang prefix: es/es/foo.html -> es/foo.html
        langCodes.forEach(code => {
            const doubled = `${code}/${code}/`;
            if (fixed.includes(doubled)) {
                fixed = fixed.replace(doubled, `${code}/`);
            }
        });

        // On /es/search.html, sidebar links may incorrectly be rendered as es/foo.html
        // when they should be just foo.html relative to the language root.
        const currentPath = window.location.pathname;
        const currentLang = langCodes.find(code => currentPath.includes(`/${code}/`));
        if (currentLang && fixed.startsWith(`${currentLang}/`)) {
            fixed = fixed.slice(currentLang.length + 1);
        }

        return fixed;
    }

    function patchLinks(container) {
        const links = container.querySelectorAll('a[href]');
        links.forEach(link => {
            const href = link.getAttribute('href');
            const fixed = normalizeHref(href);
            if (fixed !== href) {
                link.setAttribute('href', fixed);
            }
        });
    }

    // Patch current DOM immediately
    patchLinks(document);

    // Patch search results as they are injected dynamically
    const target = document.getElementById('search-results') || document.body;
    const observer = new MutationObserver(() => patchLinks(document));
    observer.observe(target, { childList: true, subtree: true });

    debugLog('TeachBook: search link fixer enabled');
}

function injectLanguageSwitcher(languages, rootPrefix) {
    const path = window.location.pathname;

    // Detect current language from URL using the codes from languages.json
    let currentLangCode = languages[0].code; // Default to first language
    languages.forEach(lang => {
        if (path.includes(`/${lang.code}/`)) currentLangCode = lang.code;
    });

    const dropdownHtml = `
        <div class="teachbook-lang-container">
            <button class="btn btn-sm teachbook-lang-btn dropdown-toggle" 
                    type="button" 
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    title="Change Language / Cambiar Idioma">
                <i class="fa-solid fa-language"></i>
                <span class="lang-text">${currentLangCode.toUpperCase()}</span>
            </button>
            <ul class="teachbook-lang-dropdown">
                ${languages.map(l => {
        // rootPrefix is the relative path to the book root (e.g., "../" from /es/intro.html)
        // So rootPrefix + "en/intro.html" = "../en/intro.html" which resolves correctly
        const targetUrl = rootPrefix + `${l.code}/intro.html`;

        return `
                    <li>
                        <a href="${targetUrl}" class="dropdown-item ${l.code === currentLangCode ? 'active' : ''}">
                            ${l.name}
                        </a>
                    </li>
                    `;
    }).join('')}
            </ul>
        </div>
    `;

    const header = document.querySelector(".article-header-buttons");
    if (header) {
        const div = document.createElement("div");
        div.innerHTML = dropdownHtml.trim();
        const switcherElement = div.firstChild;
        header.prepend(switcherElement);
    }
}

function injectPDFButton(languages, rootPrefix) {
    const sidebar = document.querySelector(".bd-sidebar-primary");
    if (sidebar) {
        if (document.getElementById("custom-pdf-btn")) return;

        // Detect current language from URL using languages.json codes
        const path = window.location.pathname;
        let lang = languages[0].code;
        languages.forEach(l => {
            if (path.includes(`/${l.code}/`)) lang = l.code;
        });

        const pdfFilenames = {
            "es": "ElaboracionDeLibrosElectronicosMedianteCodigoYAsistentesDeInteligenciaArtificial.pdf",
            "en": "CreatingElectronicBooksWithCodeAndArtificialIntelligenceAssistants.pdf"
        };
        const pdfFilename = pdfFilenames[lang] || `TeachBook_${lang}.pdf`;
        const pdfUrl = rootPrefix + `_static/${pdfFilename}`;

        const langStrings = {
            "es": { "text": "Libro Completo (PDF)", "title": "Descargar PDF completo" },
            "en": { "text": "Complete Book (PDF)", "title": "Download complete PDF" }
        };
        const strings = langStrings[lang] || langStrings["en"];

        const btnHtml = `
            <div class="sidebar-footer-pdf">
                <div class="custom-sidebar-pdf-container">
                    <a href="${pdfUrl}" id="custom-pdf-btn" class="btn btn-sm" download title="${strings.title}">
                        <i class="fa-solid fa-file-pdf"></i>
                        <span>${strings.text}</span>
                    </a>
                </div>
            </div>
        `;

        const div = document.createElement("div");
        div.innerHTML = btnHtml.trim();
        sidebar.appendChild(div.firstChild);
    }
}

async function injectSlidesButton(languages, rootPrefix, debugLog = () => {}) {
    const header = document.querySelector(".article-header-buttons");
    if (!header || document.getElementById("teachbook-slides-btn")) return;

    let manifest;
    try {
        const res = await fetch(rootPrefix + "_static/slides_manifest.json");
        if (!res.ok) {
            debugLog("TeachBook: Slides button disabled (slides_manifest.json not found).");
            return;
        }
        manifest = await res.json();
    } catch (e) {
        debugLog("TeachBook: Slides button disabled (could not load slides manifest).", e);
        return;
    }

    const path = window.location.pathname;
    const langCodes = Array.isArray(manifest.languages) && manifest.languages.length
        ? manifest.languages
        : languages.map(l => l.code);
    let currentLangCode = langCodes[0] || (languages[0] && languages[0].code) || "es";
    langCodes.forEach(code => {
        if (path.includes(`/${code}/`)) currentLangCode = code;
    });

    const currentPage = getCurrentPageKey(rootPrefix);
    const pages = manifest.pages || {};
    const hubs = manifest.hubs || {};
    const targetPath = pages[currentPage] || hubs[currentLangCode];

    if (!targetPath) {
        debugLog(`TeachBook: Slides button disabled (no deck or hub for "${currentPage}").`);
        return;
    }

    const strings = {
        es: { text: "Slides", title: "Abrir diapositivas del tema" },
        en: { text: "Slides", title: "Open chapter slides" }
    };
    const label = strings[currentLangCode] || strings.en;

    const btn = document.createElement("a");
    btn.id = "teachbook-slides-btn";
    btn.className = "btn btn-sm teachbook-slides-btn";
    btn.href = rootPrefix + targetPath;
    btn.title = label.title;
    btn.setAttribute("aria-label", label.title);
    btn.innerHTML = `<i class="fa-solid fa-display"></i><span>${label.text}</span>`;

    header.prepend(btn);
}

function getCurrentPageKey(rootPrefix) {
    const rootUrl = new URL(rootPrefix || ".", window.location.href);
    let rootPath = rootUrl.pathname;
    if (!rootPath.endsWith("/")) rootPath += "/";

    let currentPath = window.location.pathname;
    if (currentPath.startsWith(rootPath)) {
        currentPath = currentPath.slice(rootPath.length);
    } else {
        currentPath = currentPath.replace(/^\/+/, "");
    }

    currentPath = currentPath.replace(/^\/+/, "");
    if (!currentPath || currentPath.endsWith("/")) {
        currentPath += "index.html";
    }

    return decodeURI(currentPath);
}
