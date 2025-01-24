class LLM_API:
    def __init__(
        self,
        model: str,
        api_key: str,
        url: str = "",
        is_gemini: bool = False,
        delay_ms: float = 0,
    ):
        self.model = model
        self.api_key = api_key
        self.url = url
        self.is_gemini = is_gemini
        self.delay_ms = delay_ms
