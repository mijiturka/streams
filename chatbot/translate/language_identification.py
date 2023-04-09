"""
Program to identify language of a given string
"""

import fasttext

class LanguageIdentification:
    """
    Class object for Language Identification
    """

    def __init__(self):
        """
        Initializing class objects
        """
        pretrained_lang_model = "lid.176.ftz"
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        """
        Attributes
        text: type str, the sentence for which language is to be identified
        """
        predictions = self.model.predict(text, k=1) # top 1 matching languages
        return predictions

if __name__ == '__main__':
    LANGUAGE = LanguageIdentification()
    LANG = LANGUAGE.predict_lang("むかし、武田信玄(たけだしんげん)の家来(けらい)に、主水頭守清(もんどのかみもりきよ)という医者(いしゃ)がいました。")
    print(LANG)
