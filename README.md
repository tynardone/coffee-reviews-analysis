<img title="coffee-beans" alt="Coffe cup and beans" src="/images/cup-beans.jpeg">

## About
Coffee Review was founded in 1997 by Kenneth Davids and Ron Walters with the goal of providing the first-ever wine-style coffee reviews. The site boasts as much as one million readers per year. Reviews aim to provide consumers with useful information ot identify superior quality coffee while driving increased demand for farmers and roasters who are meticulous and passionate about the craft of coffee production.

## Review Methods

Reviews are produced from blind, expert cuppings of coffees 100-point reviews.


Aroma, acidity, body, flavor and aftertaste are the standard descriptive categories used by Coffee Review and many professionals when evaluating coffee. O
ther evaluative systems use as many as ten descriptive categories, but we prefer to use the traditional set of five. 

We use a rating system of 1 (low) to 10 (high) for each of the five categories, reflecting both quantity (how intense) and quality (how pleasing.) Overall ratings provide a summary assessment of reviewed coffees and are based on a scale of 50 to 100.

For each roasted coffee, we report its roast level in quantitative descriptive terms based on readings from a specially modified spectrophotometer popularly called an Agtron.

### Aroma
How intense and pleasurable is the aroma when the nose first descends over the cup and is enveloped by fragrance? Aroma also provides a subtle introduction to various nuances of acidity, taste and flavor: bitter and sweet tones, fruit, flower or herbal notes, and the like.

### Acidity
Acidity is the bright, dry sensation that enlivens the taste of coffee. Without acidity coffee is dull and lifeless. Acidity is not a sour sensation, which is a taste defect, nor should it be excessively drying or astringent, though it sometimes is. At best it is a sweetly tart vibrancy that lifts the coffee and pleasurably stretches its range and dimension. Acidity can be delicate and crisp, lush and rich, powerfully tart but sweet, or backgrounded but vibrant, to cite only a few positive ways to characterize it. The darker a coffee is roasted, the less overt acidity it will display.

### Body
Body and mouthfeel describe sensations of weight and texture. Body can be light and delicate, heavy and resonant, thin and disappointing; in texture it can be silky, plush, syrupy, lean or thin.

### Flavor and Aftertaste
Flavor and aftertaste include everything not suitably described under the categories aroma, acidity and body. An assessment of flavor includes consideration of the balance of basic tastes – sweet, bitter and sour in particular, and specific aroma and flavor notes, which are many and can be described by associations like floral (honeysuckle, rose, lilac, etc.), nuances of sweetness (honey, molasses, brown sugar), aromatic wood (cedar, pine, sandalwood) and above all fruit (from bright citrus to lusher, rounder fruit like apricot or plum, or pungent fruit like black currant or mango). Descriptors of flavor may also be global – balanced, deep, delicate, etc. Aftertaste or finish describes reflects sensations that linger after the coffee has been swallowed (or spit out). Generally we tend to reward coffees in which pleasing flavor notes continue to saturate the aftertaste long after the coffee is gone, and the sensations left behind are generally sweet-toned rather than excessively bitter or drying and astringent.

### Overall Coffee Rating
The scale for the overall coffee ratings runs from 50 to 100, and reflects the reviewers’ overall subjective assessment of a coffee’s sensory profile as manifest in the five categories aroma, acidity, body and flavor and aftertaste. Overall ratings are interpreted as follows:

 
Rating	 Interpretation
95-100	 Exceptional
90-94	 Very Good to Outstanding
85-89	 Good
80-84	 Fair
<80	 Poor
 

The higher end of our rating system currently calibrates roughly as follows:

97+ =  We have not tasted a coffee of this style as splendid as this one for a long, long time.

95-96 = Perfect in structure, flawless, and shockingly distinctive and beautiful.

93-94 = Exceptional originality, beauty, individuality and distinction, with no significant negative issues whatsoever.

91-92 = An very good to outstanding coffee with excitement and distinction in aroma and flavor – or an exceptional coffee that still perhaps has some issue that some consumers may object to but others will love – a big, slightly imbalanced acidity, for example, or an overly lush fruit.

89-90 = A very good coffee, drinkable, with considerable distinction and interest.

87-88 = An interesting coffee but either 1) distinctive yet mildly flawed, or 2) solid but not exciting.

85/86 = An acceptable, solid coffee, but nothing exceptional — the best high-end supermarket whole bean.

 
# OpenRefine
https://openrefine.org/
"OpenRefine is a powerful free, open source tool for working with messy data: cleaning it; transforming it from one format into another; and extending it with web services and external data."
This was used as a tool to clean the roaster name, roaster location, and coffee origin fields. These were very messy with many different ways of writing the same thing. For example, <<<<the roaster name "Counter Culture Coffee" was written in 10 different>>>> ways. OpenRefine provides a way to clean these fields more efficiently than doing it manually, by using facets to quickly filter data in multiple ways and using the built in clustering feature to run multiple clustering algorithms to find similar values. It also provides a way to reconcile data with other data sources. For example, the roaster location field was reconciled with Wikibase to confirm and standardize location names and to add latitude and longitude coordinates.

NOTES TODO:
Separating price cleaning and analysis from the rest of the data cleaning and analysis. 
Will keep all samples that have all quality variables for analyzing the relationships of those 
variable. When analyzing price then will remove all reviews that do not have price data. 


# NLP
https://towardsdatascience.com/nlp-gaining-insights-from-text-reviews-94ef955c58c0
https://www.analyticsvidhya.com/blog/2021/07/feature-extraction-and-embeddings-in-nlp-a-beginners-guide-to-understand-natural-language-processing/
https://www.geeksforgeeks.org/feature-extraction-techniques-nlp/
https://towardsdatascience.com/understanding-tf-idf-a-traditional-approach-to-feature-extraction-in-nlp-a5bfbe04723f
https://medium.com/analytics-vidhya/automated-keyword-extraction-from-articles-using-nlp-bfd864f41b34
https://kavita-ganesan.com/python-keyword-extraction/#.XpRvAVNKi8U
https://www.nltk.org/book/
https://towardsdatascience.com/a-friendly-introduction-to-text-clustering-fa996bcefd04
https://medium.com/artefact-engineering-and-data-science/customer-reviews-use-nlp-to-gain-insights-from-your-data-4629519b518e
https://www.artefact.com/blog/using-nlp-to-extract-quick-and-valuable-insights-from-your-customers-reviews/
https://towardsdatascience.com/customer-reviews-analysis-using-nlp-the-netflix-use-case-92b3645770e1