PDF_FILENAMES = {
    "es": "ElaboracionDeLibrosElectronicosMedianteCodigoYAsistentesDeInteligenciaArtificial.pdf",
    "en": "CreatingElectronicBooksWithCodeAndArtificialIntelligenceAssistants.pdf",
}

DEFAULT_PDF_FILENAME = PDF_FILENAMES["es"]


def pdf_filename_for_lang(lang):
    return PDF_FILENAMES.get(lang, f"TeachBook_{lang}.pdf")


def epub_filename_for_lang(lang):
    pdf_name = DEFAULT_PDF_FILENAME if lang == "default" else pdf_filename_for_lang(lang)
    return pdf_name.removesuffix(".pdf") + ".epub"
