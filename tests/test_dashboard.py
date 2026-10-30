import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
class DashboardTests(unittest.TestCase):
    def test_pages_and_seeds(self):
        app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=30).run()
        self.assertFalse(app.exception)
        for page in ['📊 Model comparison','📉 Forecast visualization','🌊 Volatility / GJR-GARCH','🧠 Explainable AI','📚 Financial report RAG','🏠 Overview / Home']:
            app.sidebar.radio[0].set_value(page).run()
            self.assertFalse(app.exception,str(app.exception))
        for seed in [123,2026]:
            app.sidebar.selectbox[0].set_value(seed).run()
            self.assertFalse(app.exception)
        app.sidebar.radio[0].set_value('🧠 Explainable AI').run()
        next(w for w in app.selectbox if w.label=='Explain model').set_value('XGBoost').run()
        self.assertFalse(app.exception)
    def test_retrieval_page(self):
        app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=30).run()
        app.sidebar.radio[0].set_value('📚 Financial report RAG').run()
        app.text_input[0].set_value('Ridge direction accuracy')
        app.button[-1].click().run()
        self.assertFalse(app.exception)
        self.assertGreater(len(app.expander),1)

    def test_home_shortcuts(self):
        app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=30).run()
        next(b for b in app.button if b.label=='Explore model performance →').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.sidebar.radio[0].value,'📊 Model comparison')
