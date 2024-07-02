from langchain_text_splitters import Language


CODE_DATA_PATH="data"

MIME_TYPE_TO_LANGUAGE = {
    "text/x-python": Language.PYTHON,
    "application/javascript": Language.JS,
    "text/javascript": Language.JS,
    "application/x-php": Language.PHP,
    "text/x-c++src": Language.CPP,
    "text/x-csrc": Language.C,
    "text/x-go": Language.GO,
    "text/x-java-source": Language.JAVA,
    "text/x-kotlin": Language.KOTLIN,
    "application/typescript": Language.TS,
    "application/x-ruby": Language.RUBY,
    "text/x-rustsrc": Language.RUST,
    "text/x-scala": Language.SCALA,
    "text/x-swift": Language.SWIFT,
    "text/x-markdown": Language.MARKDOWN,
    "application/x-latex": Language.LATEX,
    "text/html": Language.HTML,
    "text/x-solidity": Language.SOL,
    "text/x-csharp": Language.CSHARP,
    "text/x-cobol": Language.COBOL,
    "text/x-lua": Language.LUA,
    "text/x-perl": Language.PERL,
    "text/x-haskell": Language.HASKELL,
    "text/x-elixir": Language.ELIXIR,
}