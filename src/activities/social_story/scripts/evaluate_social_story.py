"""
Testing the new evaluation pipeline
"""

from activities.social_story.evaluation.main import evaluate_social_story


story = """

Title: Brushing My Teeth Before Bed

  - I get ready for bed at night.
  - I go into the bathroom.

  - I brush my teeth before bed.
  - This helps my teeth stay clean.

  - I use a toothbrush and toothpaste.
  - My grown-up helps me.

  - My grown-up puts a little toothpaste on my brush.
  - A small amount is enough.

  - Toothpaste can have a minty flavor.
  - It can feel foamy in my mouth.

  - The toothpaste makes bubbles.
  - This helps clean my teeth.

  - Sometimes the minty flavor feels strong.
  - Sometimes the foam feels different.

  - I can use a very small dot of toothpaste.

  - After brushing, I can spit out the toothpaste.
  - I can rinse my mouth with water.

  - My teeth feel clean and fresh.
  - Clean teeth are healthy teeth.

  - Brushing my teeth helps them stay strong.
  - I am learning about brushing my teeth.

"""

result = evaluate_social_story(story)
print(result)
