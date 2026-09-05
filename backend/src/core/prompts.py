Prompt ="""
  Generate one programming challenge.

  Requirements:

  * Create one clear and practical programming question.
  * The question must be related to programming, software development, or computer science.
  * Provide exactly 4 answer options.
  * Only one option must be correct.
  * The options must be ordered in an array from index 0 to index 3.
  * The correct answer must be represented by its zero-based index.
  * `correct_answer` must be a string containing only one digit: `"0"`, `"1"`, `"2"`, or `"3"`.
  * `"0"` means the first option is correct.
  * `"1"` means the second option is correct.
  * `"2"` means the third option is correct.
  * `"3"` means the fourth option is correct.
  * The other 3 options must be plausible but incorrect.
  * Provide a short and simple explanation of why the correct answer is correct.
  * Keep the question concise and easy to understand.
  * Do not create ambiguous questions where multiple options could reasonably be correct.
  * Return only the requested structured data.
  * Do not add any extra text.

  The response must conform exactly to the following schema:

  {
  "question": "string",
  "options": ["string", "string", "string", "string"],
  "correct_answer": "string",
  "explanation": "string"
  }

  Important:

  * `correct_answer` must NOT contain the answer text.
  * `correct_answer` must NOT contain letters, words, or punctuation.
  * `correct_answer` must contain only one of these exact values: `"0"`, `"1"`, `"2"`, or `"3"`.

  Example:

  {
  "question": "Which keyword is used to define a function in Python?",
  "options": [
  "func",
  "def",
  "function",
  "define"
  ],
  "correct_answer": "1",
  "explanation": "The `def` keyword is used to define functions in Python."
  }
"""
