from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from symptoms.terms_utils import MedicalTermProvider


class KnownTermsTestCase(TestCase):
    def setUp(self):
        pass

    def test_known_terms(self):
        """Known test should be recognized by the provider"""

        provider = MedicalTermProvider()
        sentence = "Yes my symptoms are blue cone monochromatism, monochromacy and abetalipoproteinemia, sometimes I feel an alpha-1-antitrypsin deficiency, but my the agenesis of corpus callosum and abnormality of epiphysis morphology are the most annoyingm, abdominal wall muscle weakness."

        terms = provider.find_medical_terms(sentence)

        self.assertIn('monochromacy', terms)
        self.assertIn('cone', terms)
        self.assertIn('corpus callosum', terms)
        self.assertIn('abdominal wall muscle weakness', terms)
        self.assertNotIn('alpha-1-antitrypsin deficiency', terms)
        self.assertNotIn('monochromatism', terms)
        self.assertNotIn('Yes', terms)
        self.assertNotIn('are', terms)
        self.assertNotIn('sometimes', terms)
        self.assertNotIn('callosum', terms)