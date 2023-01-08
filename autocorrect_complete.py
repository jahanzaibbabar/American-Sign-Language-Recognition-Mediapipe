from autocorrect import Speller
import autocomplete
autocomplete.load()


def auto_corr(word):
    spell = Speller()
    res =spell(word)
    return res



def auto_comp(word):
    res = autocomplete.predict('the', word)
    return res[0][0]
 