import spacy

from ml.models import HPOToDisorder


class MedicalTermProvider:
    """
    This class allows to retrieve medical terms from a sentence/document using the terms in HPO-Disorder Database.
    """

    def __init__(self, symtoms=None) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        if symtoms:
            known_terms = HPOToDisorder.objects.filter(id_hp__in=symtoms).values_list('term', flat=True)
        else:
            known_terms = HPOToDisorder.objects.all().values_list('term', flat=True)
        self.known_terms = known_terms

    def find_medical_terms(self, sentence):
        """
        Find medical terms in the given sentence.
        :param sentence: String. NPL sentence
        :return: Array of medical terms.
        """
        # Build the doc
        doc = self.nlp(sentence)

        # Get nouns
        nouns = self.get_compound_nouns(doc)
        print(nouns)
        return self.filter_known_nouns(nouns)

    def get_nouns(self, doc):
        """
        Given a doc, get all nouns.
        :param doc: Spacy document
        :return: Array of found nouns.
        """
        return list(map(lambda noun: noun, filter(lambda word: str(word.pos_) in ['NOUN', 'PROPN'], doc)))

    def get_compound_nouns(self, doc):
        nouns = []
        prev = ''
        for word in reversed(doc):
            # Skip non-interest words
            if word.pos_ not in ['NOUN', 'PROPN', 'ADJ']:
                prev = ''
                continue
            if word.pos_ in ['NOUN', 'PROPN']:
                nouns.insert(0, str(word.text))

            if prev:
                compound = '%s %s' % (str(word.text), prev)
                nouns.insert(0, compound)
                prev = str(compound)
            else:
                prev = str(word.text)
        return nouns


    def is_known_term(self, term):
        """
        Returns True if the specified term is a known term.
        """
        found_terms = list(filter(lambda know_term: term.lower() in know_term.lower(), self.known_terms))
        print('%d found for %s' % (len(found_terms), term))
        return len(found_terms) > 0

    def filter_known_nouns(self, nouns):
        knowns = []
        prev_known = ''
        for noun in nouns:
            if prev_known and noun in prev_known:
                continue
            is_known = self.is_known_term(noun)
            if is_known:
                knowns.append(noun.lower())
                prev_known = noun
            else:
                prev_known = ''
        return knowns





