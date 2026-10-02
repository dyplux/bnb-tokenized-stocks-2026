# Scenario screen review, 2 October 2026

## Task and observation

A judge starts from the local app, enters `1 NVDAB` and a `100 USDT` cash target, then looks for the sale and borrow comparison. This was a Chrome session run by the builder, not an eligible holder or a blind judge.

The first cap-aware screen showed a full-width sale card with no proceeds next to 13 borrow metrics. At 375 CSS pixels, the sale-route button began around 2,144 pixels from the top of the document. Long exact token values wrapped inside the borrow card. The page had no horizontal overflow, but the quote action arrived after the densest part of the page.

## Change

- The opening copy and result now say that the comparison is incomplete. The app still has no verified sale proceeds or personal Venus debt and liquidation view.
- The borrow card keeps seven decision inputs visible. Exact cap values, oracle prices, indexed estimates and isolated risk illustrations sit under an expandable disclosure. Rounded display values don't drive any pass/fail calculation; the server compares base units.
- A keyboard-focusable link in the sale card takes the reader to the existing route check. Cards on desktop follow their content height, so the empty sale card no longer stretches to match the longer borrow card.
- Repeated caveat blocks were cut. The remaining banner and detailed disclosure explain the limits without implying that a deposit or loan will execute.

## Local result and limits

Chrome fetched the public Venus scenario at 320, 375, 768, 1024 and 1440 CSS pixels. All five widths displayed the result, `11.4164 NVDAB` approximate contract headroom and a collapsed exact-values section, with no horizontal overflow or JavaScript page error. At 375 pixels, the sale-route link began around 970 pixels down the document and its anchor targeted the route-check section. The unquoted sale stayed explicit. Private QA captures are kept outside this repository on the SSD.

This checks layout and local interaction only. It doesn't prove that a Binance Web3 key authenticates, a sale route exists, a holder understands the result, or a Venus loan can be made. The app still needs those separate gates before submission.
