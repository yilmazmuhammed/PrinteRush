from printerush.common.assistant_func import FormPI


class ModelPI(FormPI):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
