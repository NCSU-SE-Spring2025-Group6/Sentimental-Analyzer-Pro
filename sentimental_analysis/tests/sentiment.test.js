const { JSDOM } = require("jsdom");

describe("Sentiment Analysis - Frontend Tests via JSDOM", () => {
  let window, document, analyzeText;

  beforeAll(() => {
    const html = `
      <html>
        <body>
          <textarea id="input-text"></textarea>
          <button id="analyze-button">Analyze</button>
          <div id="result"></div>
          <script>
            function analyzeText(input) {
              if (typeof input !== 'string') throw new Error('Invalid input');
              const clean = input.trim().toLowerCase();
              if (!clean) return 'neutral';

              const hasPositive = clean.includes('good') || clean.includes('love') || clean.includes('awesome');
              const hasNegative = clean.includes('bad') || clean.includes('terrible');

              if (hasPositive && hasNegative) return 'positive';
              if (hasPositive) return 'positive';
              if (hasNegative) return 'negative';
              return 'neutral';
            }
          </script>
        </body>
      </html>
    `;
    const dom = new JSDOM(html, { runScripts: "dangerously" });
    window = dom.window;
    document = window.document;
    analyzeText = window.analyzeText;
  });

  // Nominal test cases
  test("1. Returns 'positive' for a happy input", () => {
    expect(analyzeText("I love this product!")).toBe("positive");
  });

  test("2. Returns 'negative' for a sad input", () => {
    expect(analyzeText("This is really bad")).toBe("negative");
  });

  test("3. Handles extra spaces in input", () => {
    expect(analyzeText("   good stuff   ")).toBe("positive");
  });

  test("4. Case insensitive match", () => {
    expect(analyzeText("AWESOME")).toBe("positive");
  });

  test("5. Works with emojis in text", () => {
    expect(analyzeText("I love this ❤️")).toBe("positive");
  });

  test("6. Works with mixed sentiments", () => {
    expect(analyzeText("It's bad but I love it")).toBe("positive");
  });

  test("7. Works with slang", () => {
    expect(analyzeText("This is lit")).toBe("neutral");
  });

  test("8. Handles punctuation well", () => {
    expect(analyzeText("good!!!")).toBe("positive");
  });

  test("9. Positive word repeated", () => {
    expect(analyzeText("good good good")).toBe("positive");
  });

  test("10. Negative word repeated", () => {
    expect(analyzeText("bad bad bad")).toBe("negative");
  });

  // Off-nominal test cases
  test("11. Returns neutral for empty string", () => {
    expect(analyzeText("")).toBe("neutral");
  });

  test("12. Returns neutral for whitespace only", () => {
    expect(analyzeText("     ")).toBe("neutral");
  });

  test("13. Throws on null input", () => {
    expect(() => analyzeText(null)).toThrow("Invalid input");
  });

  test("14. Throws on undefined input", () => {
    expect(() => analyzeText(undefined)).toThrow("Invalid input");
  });

  test("15. Throws on numeric input", () => {
    expect(() => analyzeText(123)).toThrow("Invalid input");
  });

  test("16. Neutral on special characters", () => {
    expect(analyzeText("@#$%^&")).toBe("neutral");
  });

  test("17. Neutral on emoji-only string", () => {
    expect(analyzeText("💩")).toBe("neutral");
  });

  test("18. Handles long positive input", () => {
    const input = "good ".repeat(500);
    expect(analyzeText(input)).toBe("positive");
  });

  test("19. Handles long negative input", () => {
    const input = "bad ".repeat(500);
    expect(analyzeText(input)).toBe("negative");
  });

  test("20. Handles mixed long input", () => {
    const input = "bad ".repeat(10) + "love " + "good ".repeat(10);
    expect(analyzeText(input)).toBe("positive");
  });
});
