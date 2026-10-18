from dotenv import load_dotenv
from google import genai
from google.genai import types
import yfinance

load_dotenv()

client = genai.Client()
def analyse_stock():
    company = input("What company do you want to analyze? ").strip().upper()
    print("Analysing", company)
    try:
        ticker = yfinance.Ticker(company)
        data = ticker.history(period="5d")
    except Exception as e:
        print("Unable to retrieve stock data: ", e)
        return None
    score = 0
    max_score = 0

    if data.empty:
        print("Company not found.")
    else:
        try:
            info = ticker.info
        except Exception as e:
            print("Info Unavailable: ", e)
            return None
        company_name = info.get("longName", company)
        print("Company:", company_name)

        industry = info.get("industry", "Not Available")
        print("Industry:", industry)

        sector = info.get("sector", "Not Available")
        print("Sector:", sector)

        revenue = info.get("totalRevenue")
        if revenue is None:
            print("No Revenue record available")
            revenue_billion = "Not Available"
        else:
            revenue_billion = revenue/1000000000
            print(f"Revenue = ${revenue_billion:.2f}B")

        marketcap = info.get("marketCap")
        if marketcap is None:
            print("No Market Cap record available")
            marketcap_billion = "Not Available"
        else:
            marketcap_billion = marketcap/1000000000
            print(f"Market Cap = ${marketcap_billion:.2f}B")

        trailingPE = info.get("trailingPE")
        if trailingPE is None:
            print("No trailing P/E record available")
            trailingPE = "Not Available"
        else:
            print(f"Trailing P/E = {trailingPE:.2f}")
            max_score += 2
            if trailingPE > 30:
                print("High Trailing P/E")
            elif trailingPE > 15:
                print("Moderate Trailing P/E")
                score += 1 
            else:
                print("Low Trailing P/E")
                score += 2     

        revenue_growth = info.get("revenueGrowth")
        if revenue_growth is None:
            print("No Revenue growth record available")
            revenue_growth_percent = "Not Available"
        else:
            revenue_growth_percent = (revenue_growth)*100
            print(f"Revenue Growth = {revenue_growth_percent:.2f}%")
            max_score += 2
            if revenue_growth_percent > 20:
                print("Revenue Growth is strong")
                score += 2 
            elif revenue_growth_percent > 0:
                print("Revenue Growth is moderate")
                score += 1 
            else:
                print("Revenue Growth is weak")

        profit_margins = info.get("profitMargins")
        if profit_margins is None:
            print("No Profit margins record available")
            profit_margins_percent = "Not Available"
        else:
            profit_margins_percent = (profit_margins)*100
            print(f"Profit Margins = {profit_margins_percent:.2f}%")
            max_score += 2    
            if profit_margins_percent > 20:
                print("Profit Margin is strong")
                score += 2 
            elif profit_margins_percent > 0:
                print("Profit Margin is moderate")
                score +=1 
            else:
                print("Profit Margin is weak")

        free_cash_flow = info.get("freeCashflow")
        if free_cash_flow is None:
            print("No Free Cash Flow record available")
            free_cash_flow_billions = "Not Available"
        else:
            free_cash_flow_billions = free_cash_flow/1000000000
            print(f"Free Cash Flow = ${free_cash_flow_billions:.2f}B")
            max_score += 2
            if free_cash_flow_billions > 0:
                print("Positive FCF")
                score += 2
            elif free_cash_flow_billions == 0:
                print("No Free Cash Flow")
                score += 1
            else:
                print("Negative FCF")

        closing_data = data["Close"].dropna()

        if len(closing_data) >= 2:
            current_price = closing_data.iloc[-1]
            print(f"Current price: ${current_price:.2f}")

            previous_price = closing_data.iloc[-2]
            print(f"Previous price: ${previous_price:.2f}")

            change = current_price - previous_price
            if change >= 0:
                print(f"Change in price: ${abs(change):.2f}")
            else:
                print(f"Change in price: -${abs(change):.2f}")

            percent_change = (change/previous_price)*100
            if percent_change >= 0:
                print(f"Percentage change: {percent_change:.2f}%")

            if change > 0:
                print("The stock went up.")
            elif change < 0:
                print("The stock went down.")
            else:
                print("The stock did not change.")
        else:
            print("Not enough price data available.")
            
        if max_score == 0:
            print("Insufficient financial data to calculate a score.")
            score_display = "Not Available"
        else:
            score_percent = score/max_score
            score_display = f"{score}/{max_score}"
            print(f"Company Score: {score_display}")
            if score_percent > 0.75:
                print(f"{company} has a Strong Financial profile.")
            elif score_percent > 0.5:
                print(f"{company} has a Moderate Financial profile.")
            else:
                print(f"{company} has a Weak Financial profile.")

        prompt = f"""
        Financial Data:
        Company Name: {company_name}
        Revenue Growth: {revenue_growth_percent}%
        Profit Margin: {profit_margins_percent}%
        Free Cash Flow: ${free_cash_flow_billions}B
        Trailing P/E: {trailingPE}
        Overall Company Score: {score_display}
        """
        return prompt
system_instructions = """
You are a financial analysis assistant.

Your job is to analyse the financial data provided by the user and present the results in a clear, structured report.

Instructions:
- Analyse the five metrics provided: Revenue Growth, Profit Margin, Free Cash Flow, Trailing P/E, and Overall Company Score.
- Explain what each metric means and why it is important for financial analysis.
- Identify the company's strengths based only on the data provided.
- Identify potential risks based only on the data provided.
- Do not compare the company to other companies.
- Do not make assumptions about information that is not provided, including the time period, causes of performance, future performance, or business conditions.
- Do not invent company facts or information.
- Do not make a buy, sell, or hold recommendation.
- The Overall Company Score is based on a simplified scoring system and is not a professional valuation.

Format your response exactly like this:

FINANCIAL ANALYSIS

Metric Explanations
- Revenue Growth: Explain the metric and interpret the provided value.
- Profit Margin: Explain the metric and interpret the provided value.
- Free Cash Flow: Explain the metric and interpret the provided value.
- Trailing P/E: Explain the metric and interpret the provided value.
- Overall Company Score: Explain what the score represents.

Strengths
- List only strengths directly supported by the provided financial metrics.
- Do not describe the company score as a strength or weakness.
- Keep each point concise.

Risks
- Keep each point concise.
- List only risks directly supported by the provided financial metrics.
- Do not describe the company score as a risk.

Overall Summary
- Give a short summary of what the provided financial data shows.
- Do not introduce information that was not provided.
"""
config = types.GenerateContentConfig(
    system_instruction=system_instructions
)

continue_analysis = "yes"
while continue_analysis == "yes":
    prompt = analyse_stock()
    if prompt is not None:
        i = 1
        while i <= 3:    
            try: 
                response = client.models.generate_content(
                    model = "gemini-3.8-flash",
                    contents = prompt,
                    config=config
                )
                print(response.text)
                break
            except Exception as e:
                print("Error:", e)
            i += 1
        if i == 4:
            print("AI analysis unavailable. Please try again later.")
    continue_analysis = input("Would you like to analyse another company?").strip().lower()
