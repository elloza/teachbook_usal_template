// Custom UI Injection (Language Switcher, Book Downloads and Slides)
document.addEventListener("DOMContentLoaded", function () {
    const TEACHBOOK_VERSION = "3.0";
    if (window.TEACHBOOK_LOADED_VERSION === TEACHBOOK_VERSION) return;
    window.TEACHBOOK_LOADED_VERSION = TEACHBOOK_VERSION;

    setupImageViewer();

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

    findLanguagesJson().then(async result => {
        if (!result) {
            debugLog("TeachBook: Language switcher disabled (languages.json not found).");
            setupMobileHeaderTools(debugLog);
            return;
        }

        const { languages, rootPrefix } = result;

        if (languages.length > 1) {
            injectLanguageSwitcher(languages, rootPrefix);
        } else {
            debugLog("TeachBook: Single language detected. Hiding switcher.");
        }

        injectBookDownloads(languages, rootPrefix);

        // Inject contextual Slidev button when a slides manifest is available.
        if (languages.some(language => language.slides !== false)) {
            await injectSlidesButton(languages, rootPrefix, debugLog);
        }
        setupMobileHeaderTools(debugLog);

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
        setupMobileHeaderTools(debugLog);
    })();
});

function setupMobileHeaderTools(debugLog = () => {}) {
    const articleButtons = document.querySelector(".article-header-buttons");
    const headerEnd = document.querySelector("#pst-header .navbar-header-items__end");
    if (!articleButtons || !headerEnd) return;

    const media = window.matchMedia("(max-width: 991.98px)");
    let mobileTools = document.getElementById("teachbook-mobile-header-tools");
    if (!mobileTools) {
        mobileTools = document.createElement("div");
        mobileTools.id = "teachbook-mobile-header-tools";
        mobileTools.className = "teachbook-mobile-header-tools";
    }

    const movableSelectors = [
        "#teachbook-slides-btn",
        ".teachbook-lang-container",
        ".teachbook-a11y-btn",
        ".dropdown-download-buttons",
        ".btn-fullscreen-button",
        ".theme-switch-button"
    ];

    function movableControls() {
        const controls = [];
        movableSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(control => {
                if (!controls.includes(control)) controls.push(control);
            });
        });
        return controls;
    }

    function moveToMobile() {
        if (!headerEnd.contains(mobileTools)) {
            headerEnd.appendChild(mobileTools);
        }

        movableControls().forEach(control => {
            mobileTools.appendChild(control);
        });

        debugLog("TeachBook: mobile header tools moved into #pst-header");
    }

    function moveToArticle() {
        movableControls().slice().reverse().forEach(control => {
            if (!articleButtons.contains(control)) {
                articleButtons.prepend(control);
            }
        });

        if (mobileTools.parentElement) {
            mobileTools.remove();
        }

        debugLog("TeachBook: mobile header tools restored to article header");
    }

    function apply() {
        if (media.matches) {
            moveToMobile();
        } else {
            moveToArticle();
        }
    }

    apply();

    if (!window.TEACHBOOK_MOBILE_HEADER_LISTENER) {
        const onChange = () => setupMobileHeaderTools(debugLog);
        if (media.addEventListener) {
            media.addEventListener("change", onChange);
        } else if (media.addListener) {
            media.addListener(onChange);
        }
        window.TEACHBOOK_MOBILE_HEADER_LISTENER = true;
    }
}

function setupMobileLanguageDropdown(container) {
    const button = container.querySelector(".teachbook-lang-btn");
    const menu = container.querySelector(".teachbook-lang-dropdown");
    if (!button || !menu) return;

    const media = window.matchMedia("(max-width: 991.98px)");
    let isOpen = false;

    function isMobileHeader() {
        return media.matches && Boolean(container.closest("#pst-header"));
    }

    function resetMenuPosition() {
        menu.classList.remove("teachbook-mobile-lang-dropdown");
        menu.style.left = "";
        menu.style.right = "";
        menu.style.top = "";
        menu.style.transform = "";
    }

    function restoreMenu() {
        if (menu.parentElement !== container) {
            container.appendChild(menu);
        }
        resetMenuPosition();
    }

    function positionMobileMenu() {
        const buttonRect = button.getBoundingClientRect();
        const viewportWidth = document.documentElement.clientWidth || window.innerWidth;
        const menuWidth = Math.min(Math.max(menu.offsetWidth || 140, 140), viewportWidth - 16);
        const left = Math.min(
            Math.max(buttonRect.left + (buttonRect.width / 2) - (menuWidth / 2), 8),
            viewportWidth - menuWidth - 8
        );

        menu.style.left = `${left}px`;
        menu.style.right = "auto";
        menu.style.top = `${buttonRect.bottom + 6}px`;
        menu.style.transform = "none";
    }

    function closeMobileMenu() {
        if (!isOpen) return;
        isOpen = false;
        button.classList.remove("show");
        button.setAttribute("aria-expanded", "false");
        container.classList.remove("show");
        menu.classList.remove("show");
        restoreMenu();
        document.removeEventListener("click", onDocumentClick);
        document.removeEventListener("keydown", onKeydown);
        window.removeEventListener("resize", positionMobileMenu);
        window.removeEventListener("scroll", positionMobileMenu, true);
    }

    function openMobileMenu() {
        isOpen = true;
        if (menu.parentElement !== document.body) {
            document.body.appendChild(menu);
        }
        menu.classList.add("teachbook-mobile-lang-dropdown", "show");
        button.classList.add("show");
        button.setAttribute("aria-expanded", "true");
        container.classList.add("show");
        positionMobileMenu();
        document.addEventListener("click", onDocumentClick);
        document.addEventListener("keydown", onKeydown);
        window.addEventListener("resize", positionMobileMenu);
        window.addEventListener("scroll", positionMobileMenu, true);
    }

    function onDocumentClick(event) {
        if (button.contains(event.target) || menu.contains(event.target)) return;
        closeMobileMenu();
    }

    function onKeydown(event) {
        if (event.key === "Escape") {
            closeMobileMenu();
            button.focus();
        }
    }

    button.addEventListener("click", event => {
        if (!isMobileHeader()) return;
        event.preventDefault();
        event.stopPropagation();

        if (isOpen) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });

    menu.addEventListener("click", event => {
        if (event.target.closest("a")) {
            closeMobileMenu();
        }
    });

    const onMediaChange = () => closeMobileMenu();
    if (media.addEventListener) {
        media.addEventListener("change", onMediaChange);
    } else if (media.addListener) {
        media.addListener(onMediaChange);
    }
}

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
        <div class="dropdown teachbook-lang-container">
            <button class="btn btn-sm teachbook-lang-btn dropdown-toggle" 
                    type="button" 
                    id="teachbook-language-menu"
                    data-bs-toggle="dropdown"
                    data-bs-display="static"
                    aria-expanded="false"
                    aria-label="Change Language / Cambiar Idioma">
                <i class="fa-solid fa-language"></i>
                <span class="lang-text">${currentLangCode.toUpperCase()}</span>
            </button>
            <ul class="dropdown-menu teachbook-lang-dropdown" aria-labelledby="teachbook-language-menu">
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
        setupMobileLanguageDropdown(switcherElement);
    }
}

function injectBookDownloads(languages, rootPrefix) {
    const code = getCurrentPageKey(rootPrefix).split("/")[0];
    const language = languages.find(lang => lang.code === code) || languages[0];
    if (!language?.downloads) return;

    const es = language.code === "es";
    const formats = [
        ["pdf", es ? "Libro completo (PDF)" : "Complete book (PDF)"],
        ["epub", es ? "Libro electrónico (EPUB)" : "Ebook (EPUB)"]
    ].filter(([format]) => language.downloads[format]);
    if (!formats.length) return;

    function appendDownloads(menu, linkClass = "") {
        for (const [format, label] of formats) {
            const item = document.createElement("li");
            const link = document.createElement("a");
            link.className = linkClass;
            link.href = `${rootPrefix}_static/${encodeURIComponent(language.downloads[format])}`;
            link.download = "";
            link.textContent = label;
            item.append(link);
            menu.append(item);
        }
    }

    const headerMenu = document.querySelector(".dropdown-download-buttons .dropdown-menu");
    if (headerMenu) {
        const separator = document.createElement("li");
        separator.innerHTML = '<hr class="dropdown-divider">';
        headerMenu.append(separator);
        appendDownloads(headerMenu, "dropdown-item");
        headerMenu.previousElementSibling?.setAttribute("aria-label", es ? "Descargas" : "Downloads");
    }

    const sidebar = document.querySelector(".bd-sidebar-primary");
    if (sidebar) {
        const menu = document.createElement("details");
        menu.className = "sidebar-book-downloads";
        menu.innerHTML = `<summary><i class="fa-solid fa-download" aria-hidden="true"></i>
            ${es ? "Descargar libro" : "Download book"}</summary><ul></ul>`;
        appendDownloads(menu.querySelector("ul"));
        sidebar.append(menu);
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

function setupImageViewer() {
    if (!window.HTMLDialogElement?.prototype.showModal) return;

    const figures = Array.from(document.querySelectorAll(".bd-article img"), source => ({
        source,
        link: source.closest("a")
    })).filter(({ source, link }) => (
        !source.closest("button, [aria-hidden='true']") &&
        (!link || (link.classList.contains("image-reference") && link.href === source.src))
    ));
    if (!figures.length) return;

    const pageLang = getCurrentPageKey(document.documentElement.dataset.content_root).split("/")[0];
    const lang = ["es", "en"].includes(pageLang) ? pageLang : document.documentElement.lang.split("-")[0];
    const labels = lang === "es" ? {
        open: "Ampliar imagen", out: "Reducir", in: "Ampliar", fit: "Ajustar imagen",
        actual: "Tamaño original", close: "Cerrar", error: "No se ha podido cargar la imagen"
    } : {
        open: "Enlarge image", out: "Zoom out", in: "Zoom in", fit: "Fit image",
        actual: "Actual size", close: "Close", error: "Image could not be loaded"
    };

    const dialog = document.createElement("dialog");
    dialog.className = "teachbook-image-viewer";
    dialog.setAttribute("aria-label", labels.open);
    dialog.innerHTML = `
        <div class="image-viewer-toolbar">
            <p class="image-viewer-caption"></p>
            <output class="image-viewer-scale"></output>
        </div>
        <div class="image-viewer-stage" tabindex="0">
            <div class="image-viewer-canvas"><img alt="" draggable="false"></div>
        </div>`;
    document.body.append(dialog);

    const toolbar = dialog.querySelector(".image-viewer-toolbar");
    const stage = dialog.querySelector(".image-viewer-stage");
    const caption = dialog.querySelector(".image-viewer-caption");
    const scaleLabel = dialog.querySelector("output");
    const image = dialog.querySelector("img");
    const maxScale = 8;
    let scale = 1;
    let minScale = 1;
    let isVector = false;
    let drag = null;
    let opener = null;

    function addControl(label, markup, action) {
        const control = document.createElement("button");
        control.type = "button";
        control.title = label;
        control.setAttribute("aria-label", label);
        control.innerHTML = markup;
        control.addEventListener("click", action);
        toolbar.append(control);
        return control;
    }

    function fit() {
        if (!image.naturalWidth || !image.naturalHeight) return;
        // Leave the 16 px padding on either side of the image.
        const fittedScale = Math.min(
            isVector ? maxScale : 1,
            Math.max(1, stage.clientWidth - 32) / image.naturalWidth,
            Math.max(1, stage.clientHeight - 32) / image.naturalHeight
        );
        minScale = Math.min(1, fittedScale);
        fitButton.disabled = false;
        actualButton.disabled = false;
        zoom(fittedScale);
        stage.scrollTo(0, 0);
    }

    function zoom(nextScale) {
        if (!image.complete || !image.naturalWidth) return;
        const stageBounds = stage.getBoundingClientRect();
        const before = image.getBoundingClientRect();
        const midX = stageBounds.left + stage.clientWidth / 2;
        const midY = stageBounds.top + stage.clientHeight / 2;
        const centerX = before.width ? Math.max(0, Math.min(1, (midX - before.left) / before.width)) : 0.5;
        const centerY = before.height ? Math.max(0, Math.min(1, (midY - before.top) / before.height)) : 0.5;

        scale = Math.max(minScale, Math.min(maxScale, nextScale));
        image.style.width = `${image.naturalWidth * scale}px`;
        scaleLabel.textContent = `${Math.round(scale * 100)}%`;
        smaller.disabled = scale <= minScale;
        larger.disabled = scale >= maxScale;

        const after = image.getBoundingClientRect();
        stage.scrollLeft += after.left + centerX * after.width - midX;
        stage.scrollTop += after.top + centerY * after.height - midY;
    }

    const smaller = addControl(labels.out, '<i class="fa-solid fa-minus" aria-hidden="true"></i>', () => zoom(scale / 1.25));
    const larger = addControl(labels.in, '<i class="fa-solid fa-plus" aria-hidden="true"></i>', () => zoom(scale * 1.25));
    const fitButton = addControl(labels.fit, '<i class="fa-solid fa-expand" aria-hidden="true"></i>', fit);
    const actualButton = addControl(labels.actual, "1:1", () => zoom(1));
    const close = addControl(labels.close, '<i class="fa-solid fa-xmark" aria-hidden="true"></i>', () => dialog.close());
    close.autofocus = true;

    function open(source, trigger) {
        if (dialog.open) return;
        const figure = source.closest("figure");
        const figureCaption = figure?.querySelector(".caption-text") || figure?.querySelector("figcaption");
        const url = source.currentSrc || source.src;
        isVector = /\.svg(?:[?#]|$)|^data:image\/svg\+xml[;,]/i.test(url);
        caption.textContent = figureCaption?.textContent.trim() || source.alt;
        image.alt = source.alt;
        image.style.width = "0px";
        scale = 1;
        scaleLabel.textContent = "";
        [smaller, larger, fitButton, actualButton].forEach(control => { control.disabled = true; });

        opener = trigger;
        dialog.showModal();
        document.body.classList.add("teachbook-image-viewer-open");
        image.src = url;
        if (image.complete && image.naturalWidth) fit();
    }

    image.addEventListener("load", () => { if (dialog.open) fit(); });
    image.addEventListener("error", () => { if (dialog.open) caption.textContent = labels.error; });
    figures.forEach(({ source, link }) => {
        const trigger = link || source;
        source.dataset.imageViewer = "";
        if (!trigger.title) trigger.title = labels.open;
        trigger.setAttribute("aria-haspopup", "dialog");
        if (!link) {
            source.tabIndex = 0;
            source.setAttribute("role", "button");
            source.setAttribute("aria-label", source.alt ? `${labels.open} – ${source.alt}` : labels.open);
            source.addEventListener("keydown", event => {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    open(source, trigger);
                }
            });
        }
        trigger.addEventListener("click", event => {
            if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            open(source, trigger);
        });
    });

    dialog.addEventListener("close", () => {
        if (dialog.open) return;
        document.body.classList.remove("teachbook-image-viewer-open");
        image.removeAttribute("src");
        drag = null;
        opener?.focus({ preventScroll: true });
    });
    dialog.addEventListener("click", event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener("keydown", event => {
        if (!["+", "=", "-"].includes(event.key) || event.ctrlKey || event.metaKey || event.altKey) return;
        event.preventDefault();
        zoom(event.key === "-" ? scale / 1.25 : scale * 1.25);
    });
    stage.addEventListener("wheel", event => {
        if (event.ctrlKey || event.metaKey || !event.deltaY) return;
        event.preventDefault();
        zoom(event.deltaY < 0 ? scale * 1.15 : scale / 1.15);
    }, { passive: false });
    stage.addEventListener("dblclick", () => scale === 1 ? fit() : zoom(1));
    stage.addEventListener("pointerdown", event => {
        if (event.pointerType === "touch" || event.button !== 0 || !event.isPrimary) return;
        drag = {
            pointer: event.pointerId, x: event.clientX, y: event.clientY,
            left: stage.scrollLeft, top: stage.scrollTop
        };
        stage.setPointerCapture(event.pointerId);
    });
    stage.addEventListener("pointermove", event => {
        if (drag?.pointer !== event.pointerId) return;
        stage.scrollLeft = drag.left + drag.x - event.clientX;
        stage.scrollTop = drag.top + drag.y - event.clientY;
    });
    stage.addEventListener("lostpointercapture", () => { drag = null; });
    window.addEventListener("resize", () => { if (dialog.open) fit(); });
}
