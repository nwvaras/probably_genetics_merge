import spacy

from symptoms.terms_utils import MedicalTermProvider

nlp = spacy.load("en_core_web_sm")
doc = nlp("Yes my symptoms are blue cone monochromatism, monochromacy and abetalipoproteinemia, sometimes I feel an alpha-1-antitrypsin deficiency, but my the agenesis of corpus callosum and abnormality of epiphysis morphology are the most annoyingm, abdominal wall muscle weakness.")

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)

sentence = "Yes my symptoms are blue cone monochromatism, monochromacy and abetalipoproteinemia, sometimes I feel an alpha-1-antitrypsin deficiency, but my the agenesis of corpus callosum and abnormality of epiphysis morphology are the most annoyingm, abdominal wall muscle weakness."
provider = MedicalTermProvider()
terms = provider.find_medical_terms(sentence)
print(terms)