# objective

Identificar até três problemas concretos para utilizadores de acções tokenizadas na BNB Chain, comparar alternativas, validar precedentes de hackathons e recomendar um wedge testável. Auditoria read-only, fontes primárias, verificado em 2026-10-01.

# work done

Li o manual local, `REPORT.md`, `PRODUCT-PLAN.md` e o texto do lead Grok. Verifiquei documentação oficial de BNB Chain, Binance, PancakeSwap, Ondo, xStocks/Jupiter, Base, Robinhood Chain, Uniswap e GitHub. Não editei ficheiros, não instalei, não clonei nem executei código terceiro.

# dated primary sources

- Hackathon BNB Hack: Tokenized Stocks Edition, 16-09 a 11-10-2026, BSC mainnet, bStocks/Ondo/xStocks centrais, Binance Web3 API obrigatória, 20 000 USD, score técnico 30%, originalidade 25%, Developer Experience Report 25%, produto/UX 20%: [página oficial](https://www.bnbchain.org/en/hackathons/tokenized-stocks), verificado em 2026-10-01.
- Binance Agentic Wallet documenta pesquisa e negociação de bStock e Ondo por ticker, com resolução de contrato, estado, quote e confirmação: [stock trading](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading), verificado em 2026-10-01.
- PancakeSwap agrega bStocks, Ondo, xStocks e Robinhood no terminal de stocks, com comparação de preços por ticker: [guia oficial](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas), verificado em 2026-10-01.
- Base, Ondo, Robinhood Chain, Jupiter e Uniswap documentam produtos concorrentes: [Base Stocks](https://brand.base.org/stocks), [Ondo Stocks](https://ondo.finance/ondo-stocks), [Robinhood Stock Tokens](https://docs.robinhood.com/chain/stock-tokens/), [Jupiter xStocks](https://academy.jup.ag/lessons/xstocks-on-jupiter), [Uniswap](https://blog.uniswap.org/tokenized-securities-are-live), verificados em 2026-10-01.

# facts

- A Binance já documenta o fluxo completo “resolver ticker, verificar estado, negociar”. O exemplo de compra mostra quote, slippage, confirmação e acompanhamento da ordem. [Binance Docs](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading), verificado em 2026-10-01.
- PancakeSwap já tem terminal multi-emissor. O utilizador pesquisa um ticker, vê opções de preço, escolhe uma, liga a wallet e faz swap. [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas), verificado em 2026-10-01.
- bStocks são tokens BEP-20 com backing 1:1, negociação 24/7, self-custody e uso em Venus, Lista DAO, PancakeSwap e Aster. [BNB Chain](https://www.bnbchain.org/en/blog/introducing-bstocks-on-bnb-chain-trade-24-7-with-zero-fees-deploy-across-defi-protocols-with-full-self-custody), verificado em 2026-10-01.
- Ondo documenta compra directa em três passos e distribuição por wallets, CEX, DEX e agregadores. A página actual também documenta mint e redemption 24/7 para alguns activos, incluindo NVDAon e TSLAon. [Ondo Stocks](https://ondo.finance/ondo-stocks), [Ondo 24/7](https://ondo.finance/blog/real-24-7-trading-for-tokenized-stocks), verificados em 2026-10-01.
- Jupiter acrescenta verificação de autenticidade, limit orders e compras recorrentes para xStocks. [Jupiter Academy](https://academy.jup.ag/lessons/xstocks-on-jupiter), verificado em 2026-10-01.
- Base oferece Coinbase Tokenized Stocks, contratos públicos, trading 24/7 e composição em lending, collateral e DEXs. [Base](https://brand.base.org/stocks), verificado em 2026-10-01.
- Robinhood Chain expõe API pública para preço, bid/ask, multiplicador, corporate actions e capacidades de trading por activo. [Robinhood APIs](https://docs.robinhood.com/chain/stock-token-apis/), verificado em 2026-10-01.
- O relatório local mediu uma diferença grande entre contratos com o mesmo ticker na BNB Chain. A série registou 129 967 swaps para NVDAB e 3 para NVDAX no corte consultado. Isto é actividade indexada, não compradores únicos, pessoas ou liquidez executável. [evidência local](research/bstocks-hackathon-2026/results/2026-09-30-p3-nvda-swaps-five-ecosystems.md).

# inferences

- Descoberta simples, chat de compra e terminal multi-emissor já têm substitutos fortes.
- “24/7” isolado deixou de ser diferenciador. O valor provável está em saber quando a negociação é realmente executável, qual é a representação correcta e qual o custo total.
- O mesmo ticker pode esconder emissores, direitos económicos, multiplicadores, dividendos, contratos e liquidez diferentes. A escolha do contrato tornou-se parte do problema.

# unknowns

- Ainda não há sessão observada com a mesma wallet, jurisdição e montante em bStocks, Ondo e xStocks na BNB Chain.
- Ainda não há quote executável comparável para 20, 50 ou 100 USD, com slippage e confirmação.
- Não foi medida a taxa de erro, recusa ou abandono do fluxo Binance Agentic Wallet.
- A actividade CMC e DEX não prova procura humana, conversão ou intenção de compra.
- Não há resultado oficial do hackathon de 2026, que continua aberto na data desta pesquisa.

# counterevidence

- O utilizador pode resolver tudo na Binance Wallet ou no PancakeSwap. Um produto concorrente precisa de reduzir erro ou custo numa decisão concreta.
- Ondo, Base e Robinhood Chain já tratam parte do problema de horário, preços e corporate actions.
- Uma interface que apenas reempacote dados públicos terá baixa originalidade e pouca razão para mudar.
- O próprio evento aceita agentes, mas não pontua PnL. Um bot especulativo é uma tese fraca para esta edição.

# up to three problem wedges

## 1. Escolher a representação certa do mesmo ticker

**Utilizador:** trader retail cripto-native na BNB Chain.
**Trigger:** quer comprar 100 USD de NVDA durante o fim de semana.
**Workflow actual:** pesquisa “NVDA”, compara PancakeSwap, Binance Wallet, contratos e eventualmente uma folha ou script próprio.
**Falha observável:** o mesmo ticker aparece como NVDAB, NVDAon ou NVDAx, com diferenças de emissor, backing, dividendos, referência, liquidez e elegibilidade. O terminal mostra alternativas, mas a documentação não demonstra uma revisão uniforme desses atributos antes da assinatura.
**Consequência:** compra do contrato errado, preço pior, impossibilidade de negociar ou exposição económica mal compreendida.
**Teste mais barato:** recolher, no mesmo minuto, contrato, emissor, direitos, estado, quote, slippage e liquidez para NVDA em três emissores. Se o melhor caminho for sempre igual e a escolha não alterar o resultado, o wedge cai.

## 2. Saber se uma quote fora do horário normal é executável

**Utilizador:** operador de tesouraria ou trader que só pode agir ao sábado ou domingo.
**Trigger:** quer entrar, sair ou rebalancear quando o mercado tradicional está fechado.
**Workflow actual:** vê preço on-chain ou referência, consulta manualmente market status e tenta swap.
**Falha observável:** preço de referência pode estar desactualizado, enquanto a liquidez e o estado de mint, redemption ou venue diferem por emissor. A página do hackathon identifica este problema, mas os produtos concorrentes já publicam partes da solução. [BNB Hack](https://www.bnbchain.org/en/hackathons/tokenized-stocks), verificado em 2026-10-01.
**Consequência:** quote informativa sem execução, slippage inesperado ou ordem rejeitada.
**Teste mais barato:** durante um fim de semana, comparar preço on-chain, referência, estado e quote real para os dez activos mais líquidos. Se o desvio ficar abaixo dos custos ou se não houver size executável, abandonar.

## 3. Recuperar de elegibilidade, estado ou erro antes de assinar

**Utilizador:** utilizador não institucional a tentar o primeiro trade de stock tokenizado.
**Trigger:** tenta comprar numa wallet ou venue nova.
**Workflow actual:** liga wallet, fornece USDT, pesquisa ticker e assina quando a interface permite.
**Falha observável:** restrições geográficas, KYC, token halted, gas, aprovação ou autorização podem aparecer tarde. Binance documenta verificações de estado, mas não prova que todos os erros sejam compreensíveis para um novo utilizador. [Binance Docs](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading), verificado em 2026-10-01.
**Consequência:** tempo perdido, abandono ou assinatura de uma transacção que falha.
**Teste mais barato:** executar dez cenários, incluindo jurisdição bloqueada, token pausado, saldo insuficiente, gas insuficiente e quote expirada. Medir quantos falham antes da assinatura e se a mensagem indica recuperação.

# competitors/substitutes

- **Binance Agentic Wallet:** chat, resolução de ticker, quote, confirmação e tracking. Melhor substituto para compra simples.
- **PancakeSwap:** terminal multi-emissor, comparação de preços e swap directo. Melhor substituto para descoberta manual.
- **bStocks/Ondo/xStocks:** cada emissor explica backing, horários, direitos e canais de compra. Melhor substituto para utilizadores já fiéis ao emissor.
- **Solana/Jupiter:** verificação, limit orders e recurring orders para xStocks.
- **Base/Coinbase:** contratos canónicos, prospectos, 24/7 e DeFi integrado.
- **Ethereum/Uniswap:** descoberta e negociação de securities em app, wallet e API.
- **Robinhood Chain:** APIs de preços, multiplicadores e corporate actions.
- **Manual:** folha de cálculo com contratos, screenshots, preços e notas de elegibilidade; script RPC para comparar contratos.
- **Do nothing:** manter dinheiro em stablecoins, usar uma corretora Web2 ou esperar pela abertura do mercado. Este substituto tem custo operacional baixo e evita risco de contrato.

# relevant prior winners

- **BNB Hack Bangkok, 2024, 2.º lugar, BNB DeFi Aggregator.** Fluxo oficial: agregação DEX cross-chain e construção, execução e partilha de estratégias. Integração BNB Chain e foco em acessibilidade. Repositório público e estado actual não foram confirmados. Lição: um workflow de decisão e execução é mais concreto que um catálogo. [resultado oficial](https://www.bnbchain.org/en/blog/bnb-hack-bangkok-recap-celebrating-innovation-and-congratulating-the-winners), verificado em 2026-10-01.
- **BNB AI Hack, 2025, vencedor, Bink AI.** Fluxo: BinkOS combina análise DeFi, automação on-chain, MCP, planning agent e trading de stocks tokenizados; a BNB Chain documenta integrações com Lista DAO e KernelDAO. A colocação numérica não foi publicada. Repositório público não confirmado. Lição: integração repetida e produto em evolução contam mais que uma demo isolada. [BNB Chain](https://www.bnbchain.org/en/blog/congratulations-to-the-latest-bnb-ai-hack-winners-may-29-batch), verificado em 2026-10-01.
- **BNB Hack, batch de agosto de 2025, honorable mention, Helix.** Fluxo oficial: agente autónomo de trading na BNB Chain que executa estratégias em tempo real. A colocação entre finalistas não foi publicada. Repositório público não confirmado. Lição: “agente de trading” sozinho já é território concorrido, por isso a proposta precisa de uma falha específica e demonstrada. [BNB Chain](https://www.bnbchain.org/en/blog/congratulations-to-the-latest-bnb-hack-winners-august-4-batch), verificado em 2026-10-01.

# skill options

- **[binance/binance-skills-hub](https://github.com/binance/binance-skills-hub):** 1,0 mil estrelas, 232 forks, 166 commits, licença MIT. O repositório contém `SKILL.md`, incluindo a skill de securities da Binance. A estrutura é compatível com Agent Skills e pode ser lida pelo Codex, embora o README mencione explicitamente OpenClaw e Claude Code, não Codex. Actividade recente existe, mas a página não expôs a data do último commit nesta consulta. Recomendo estudar, não instalar ainda. Verificado em 2026-10-01.
- **[Hongyi-Li-sz/structured-research-workflow](https://github.com/Hongyi-Li-sz/structured-research-workflow):** 0 estrelas, 2 commits, licença MIT. É pequeno, mas declara compatibilidade com Claude Code e OpenAI Codex, usa apenas `SKILL.md` e organiza evidência, baselines, planos e higiene de research. Recomendo-o como referência metodológica, não como dependência. Verificado em 2026-10-01.

# recommendation

Escolher o wedge 1: um pre-trade issuer and quote guard para o mesmo ticker. A primeira demo deve receber ticker, montante e jurisdição, comparar bStocks/Ondo/xStocks, mostrar contrato, emissor, backing, direitos, estado, preço de referência, quote, slippage, gas, liquidez visível e motivo de bloqueio. A ordem só avança após confirmação humana.

O wedge 2 entra como segunda camada apenas se o teste de fim de semana mostrar desvio e size executável relevantes. O wedge 3 deve ser aceite como requisito de segurança, não como produto separado.

# strongest counterargument

PancakeSwap já mostra opções de preço e a Binance já resolve ticker, estado, quote e execução. O novo guard pode ser uma camada cosmética que acrescenta texto sem melhorar a decisão. Esse argumento só cai com uma comparação gravada em que emissores diferentes produzem resultados materiais para o mesmo ticker e montante.

# impact on decision

Não aprovar um dashboard genérico, um chatbot de stocks, um agente “buy NVDA” ou onboarding duplicado. Avançar apenas se houver diferença mensurável em quote, slippage, direitos, elegibilidade ou taxa de falha. O produto deve usar profundamente a Binance Web3 API, porque o evento dá 25% ao relatório de Developer Experience e usa a profundidade da API como desempate. [regras oficiais](https://www.bnbchain.org/en/hackathons/tokenized-stocks), verificado em 2026-10-01.

# next checks

1. Executar uma matriz NVDA, AAPL e TSLA, três emissores, 20/50/100 USD, durante sessão aberta e fim de semana.
2. Registar contratos, preço, quote, slippage, gas, latência, estado, jurisdição e falha.
3. Repetir a mesma tarefa no PancakeSwap e Binance Agentic Wallet.
4. Fazer dez cenários de erro e medir recuperação antes da assinatura.
5. Abandonar o wedge se a escolha não mudar o resultado ou se a API não fornecer dados suficientes.

# limitations

A pesquisa não mediu utilizadores humanos, conversão, intenção de compra, receita, profundidade total ou taxa de abandono. Likes, seguidores e investimentos de YZi Labs não foram usados como procura ou preferência de júri.

O Grok lead sobre CZ e YZi Labs foi auditado apenas onde podia alterar os wedges. Os URLs de CZ sobre interoperabilidade, Trust Wallet, self-custody, AUM de bStocks e o post da BNB Chain foram tentados em 2026-10-01, mas o X devolveu 403 e as páginas não puderam ser lidas: [interoperabilidade](https://x.com/cz_binance/status/2090590687657922579), [Trust Wallet](https://x.com/cz_binance/status/2092184575908970730), [self-custody](https://x.com/cz_binance/status/2084531849515131231), [AUM](https://x.com/cz_binance/status/2070176909162410430), [anúncio BNB](https://x.com/BNBCHAIN/status/2100203524802134150). Os produtos oficiais corroboram a existência do terminal, do agente e das integrações, mas não validam as palavras ou motivações atribuídas a CZ.