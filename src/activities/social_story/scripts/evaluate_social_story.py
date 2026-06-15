"""
Testing the new evaluation pipeline
"""

from activities.social_story.evaluation.main import evaluate_social_story


story = """
Title: Going to a Restaurant                                                                                                                                                 
                                                                                                                                                                             
  - I go to a restaurant.
  - My family goes with me.

  - We ride in the car.
  - The car stops.
  - We get out.

  - We walk inside.
  - Many people are there.
  - People talk and eat.

  - We wait for a table.
  - I stand with my family.
  - This is okay.

  - A person shows us a table.
  - I sit in my chair.
  - My family sits too.

  - I look at the menu.
  - The menu has food pictures.
  - I pick my food.

  - We wait for our food.
  - I can look around.
  - Waiting is part of eating.

  - My food comes.
  - I eat my food.
  - Eating food is good.

  - Many people are still here.
  - People make sounds.
  - This is normal.

  - I finish my food.
  - We get ready to leave.
  - We walk out.

  - Going to a restaurant is fun.
  - I am safe with my family.
  - I did a good job.
"""

result = evaluate_social_story(story)
print(result)
