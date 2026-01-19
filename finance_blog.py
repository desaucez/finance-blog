import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(page_title="Equity Research Blog", layout="wide", page_icon="📊")

# Custom CSS for editorial/newspaper look (WSJ/Business Times inspired)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #222;
        background-color: #ffffff;
    }

    /* Main title */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #000;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #666;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.6;
        border-bottom: 1px solid #ddd;
        padding-bottom: 1.5rem;
    }

    /* Section headers */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #000;
        margin-top: 4rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #000;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }

    .subsection-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #222;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.1px;
    }

    /* Metrics - clean, minimal boxes */
    .metric-primary {
        background: #fafafa;
        padding: 1.25rem 1rem;
        border: 1px solid #ddd;
        border-radius: 0;
        margin: 1rem 0;
        box-shadow: none;
    }

    .metric-section {
        background: transparent;
        padding: 1rem;
        border: none;
        margin: 1.5rem 0;
    }

    .metric-highlight {
        background: #f8f8f8;
        padding: 1.25rem 1rem;
        border: 1px solid #ccc;
        border-left: 3px solid #000;
        border-radius: 0;
        margin: 1rem 0;
    }

    .metric-container {
        background: transparent;
        padding: 1rem;
        border: none;
        margin: 1.5rem 0;
    }

    /* Analysis blocks - clean spacing, no borders */
    .analysis-template {
        background-color: #ffffff;
        padding: 0;
        border: none;
        margin: 2.5rem 0;
        font-size: 1rem;
        line-height: 1.7;
        color: #333;
    }

    .analysis-insight {
        background-color: #f9f9f9;
        padding: 1.5rem 1.25rem;
        border: none;
        margin: 2.5rem 0;
        font-size: 1rem;
        line-height: 1.7;
        color: #333;
    }

    .analysis-risk {
        background-color: #fff9f9;
        padding: 1.5rem 1.25rem;
        border: none;
        margin: 2.5rem 0;
        font-size: 1rem;
        line-height: 1.7;
        color: #333;
    }

    .template-note {
        color: #777;
        font-style: italic;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        font-weight: 400;
    }

    /* Table of Contents - clean list */
    .toc-container {
        background: #fafafa;
        padding: 1.5rem 1.75rem;
        border-radius: 0;
        border: 1px solid #ddd;
        border-left: 3px solid #000;
        margin: 2.5rem 0;
    }

    .toc-container h3 {
        font-family: 'Inter', sans-serif;
        color: #000;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -0.2px;
    }

    .toc-container a {
        font-family: 'Inter', sans-serif;
        color: #222;
        text-decoration: none;
        font-weight: 400;
        transition: color 0.2s ease;
        display: inline-block;
        padding: 0.25rem 0;
        border-bottom: 1px solid transparent;
    }

    .toc-container a:hover {
        color: #000;
        border-bottom: 1px solid #000;
    }

    .data-source {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid #ddd;
    }

    /* Streamlit metric styling */
    .stMetric {
        background-color: transparent;
    }

    .stMetric label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #666;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stMetric [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-size: 1.75rem;
        font-weight: 600;
        color: #000;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #fafafa;
        border-right: 1px solid #ddd;
    }

    [data-testid="stSidebar"] h1 {
        font-family: 'Inter', sans-serif;
        color: #000;
        font-weight: 700;
        font-size: 1.75rem;
        letter-spacing: -0.3px;
    }

    [data-testid="stSidebar"] h2 {
        font-family: 'Inter', sans-serif;
        color: #222;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="stSidebar"] h3 {
        font-family: 'Inter', sans-serif;
        color: #000;
        font-weight: 600;
        font-size: 1.1rem;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.9rem;
        line-height: 1.65;
        color: #444;
    }

    [data-testid="stSidebar"] .stRadio > label {
        font-weight: 500;
        color: #222;
    }

    /* Warning box - clean style */
    .sidebar-warning {
        background: transparent;
        border: none;
        padding: 0;
        margin: 1rem 0;
        font-size: 0.9rem;
        line-height: 1.65;
        color: #444;
    }

    /* Remove default Streamlit padding for cleaner look */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Fetch data function
@st.cache_data(ttl=3600)
def load_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        info = stock.info
        return df, info
    except Exception as e:
        st.error(f"Error loading data for {ticker}: {str(e)}")
        return None, None

# Stock configuration
STOCKS = {
    "ASTS": {
        "name": "AST SpaceMobile",
        "ticker": "ASTS",
        "sector": "Space Technology / Telecommunications"
    }
    # Add more stocks here as you expand:
    # "NVDA": {
    #     "name": "NVIDIA Corporation",
    #     "ticker": "NVDA",
    #     "sector": "Semiconductors"
    # }
}

# Sidebar navigation
st.sidebar.title("Finance Blog")
st.sidebar.markdown("---")
st.sidebar.subheader("Stock Coverage")

selected_stock = st.sidebar.radio(
    "Select Analysis:",
    options=list(STOCKS.keys()),
    format_func=lambda x: f"{x} - {STOCKS[x]['name']}"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**About This Blog**")
st.sidebar.markdown("I started this blog as a something for me to write about stocks I find interesting. I started investing during National Service, and I didn't really know what I was investing in. I have a little bit of free time now, so I decided to make this blog to understand why I'm even investing in these companies, and to also work on my coding skills. I hope people can read this too, and learn together with me.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Important Disclaimer")
st.sidebar.markdown('<div class="sidebar-warning">', unsafe_allow_html=True)
st.sidebar.markdown("Please take note that anything and everything I'm doing here is the first time I'm doing it, and by no means am I a financial analyst. This is purely for learning, and there might be a few informational and contextual errors.")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main content
stock_info = STOCKS[selected_stock]
ticker = stock_info["ticker"]

# Date range
start_date = "2024-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")

# Load data
with st.spinner(f"Loading {ticker} data..."):
    df, info = load_stock_data(ticker, start_date, end_date)

if df is not None and not df.empty:
    
    # Calculate all metrics upfront
    df['Daily_Return'] = df['Close'].pct_change()
    df['Volatility_20'] = df['Daily_Return'].rolling(window=20).std() * np.sqrt(252) * 100
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    df['Cumulative_Max'] = df['Close'].cummax()
    df['Drawdown'] = (df['Close'] - df['Cumulative_Max']) / df['Cumulative_Max'] * 100
    
    # Header
    st.markdown(f'<div class="main-title">{stock_info["name"]} ({ticker})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Sector: {stock_info["sector"]} | Analysis Period: January 2024 - Present<br><em>Note: This analysis was written on January 10th, 2026, and may be outdated.</em></div>', unsafe_allow_html=True)
    
    # Key metrics row
    # Calculate 52-week metrics (last 252 trading days)
    df_52w = df.tail(252)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Current Price", f"${df['Close'].iloc[-1]:.2f}")
    with col2:
        price_change = df['Close'].iloc[-1] - df['Close'].iloc[0]
        pct_change = (price_change / df['Close'].iloc[0]) * 100
        st.metric("Period Change", f"{pct_change:.2f}%", f"${price_change:.2f}")
    with col3:
        st.metric("52W High", f"${df_52w['High'].max():.2f}")
    with col4:
        st.metric("52W Low", f"${df_52w['Low'].min():.2f}")
    with col5:
        st.metric("Avg Volume", f"{df['Volume'].mean()/1e6:.2f}M")
    
    # Table of Contents
    st.markdown('<div class="toc-container">', unsafe_allow_html=True)
    st.markdown('<h3>Table of Contents</h3>', unsafe_allow_html=True)
    st.markdown("""
    - [I. Stock Overview](#i-stock-overview)
    - [II. Price Action and Technical Analysis](#ii-price-action-and-technical-analysis)
    - [III. Volume and Volatility Analysis](#iii-volume-and-volatility-analysis)
    - [IV. Returns Analysis](#iv-returns-analysis)
    - [V. Risk Assessment and Metrics](#v-risk-assessment-and-metrics)
    - [VI. Investment Conclusion](#vi-investment-conclusion)
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 1: Overview and Investment Thesis
    st.markdown('<div class="section-header" id="i-stock-overview">I. Stock Overview</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="analysis-template">', unsafe_allow_html=True)

    st.markdown("""
    AST SpaceMobile, Inc. (ASTS) is a satellite designer and manufacturer based in the United States. When I started out investing, I would read up about stocks, and ASTS caught my eye as I've always been a guy that likes space.

What ASTS essentially intends to do is build a space-based cellular broadband network that can be accessed by all smartphones. To simplify this, currently when we use our phones, it connects to a cell tower on the ground. This tower then connects to our phones' respective carriers, and routes data via fiber cables, the internet, and so forth. However, a key issue that all of us face is that when we're in certain locations, there is no signal at all. In the case of Singapore, Tekong or HTA. This is because cell towers generally only cover a small area, and they're blocked by physical obstacles, or are just too expensive to build in some places. 

In Singapore, cell connection is generally pretty good, as most cell towers are integrated into HDBs and other buildings on rooftops. However, the same cannot be said for other countries, particularly in rural or remote areas where infrastructure deployment is economically challenging.

In contrast, what ASTS does is put up these huge cell towers in space, in the form of satellites. Our existing phones will be able to connect to these satellites directly. AST's satellites are huge and extremely sensitive, allowing them to receive our phones' very weak signals easily. Standard cellular frequencies (5G, 4G) are used by AST, so no new frequencies or additional technology is needed. Your phone doesn't need to switch modes, and signals can be transmitted directly to the satellite.

For the more technical analysis, AST's satellites use a phased-array antenna, which is comprised of thousands of tiny antenna elements. Here comes the interesting bit: if many signals are being transmitted simultaneously (many people are calling or using their phones), shouldn't it be difficult for the array to determine which signal is which? Well, because there are many antenna elements, the array receives the same signal from slightly different positions, and all signals reach each antenna at a slightly different time, with a slightly different phase. This allows the system to distinguish and process multiple signals concurrently. There is of course more in-depth science involved, including considerations like the Doppler effect, but unfortunately this is a finance blog.
""")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Price Action and Technical Analysis
    st.markdown('<div class="section-header" id="ii-price-action-and-technical-analysis">II. Price Action and Technical Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-header">Price Performance</div>', unsafe_allow_html=True)
    
    # Candlestick chart
    fig_candle = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=ticker,
        increasing_line_color='#00897b',
        decreasing_line_color='#c62828',
        increasing_fillcolor='#00897b',
        decreasing_fillcolor='#c62828'
    )])

    fig_candle.update_layout(
        title=dict(
            text=f'{ticker} Stock Price',
            font=dict(size=16, color='#000', family="Inter, sans-serif", weight=700),
            x=0,
            xanchor='left'
        ),
        yaxis=dict(
            title='Price (USD)',
            titlefont=dict(size=11, color='#666', family="Inter, sans-serif"),
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8',
            showline=True,
            linecolor='#ccc',
            linewidth=1
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8',
            showline=True,
            linecolor='#ccc',
            linewidth=1
        ),
        height=520,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        xaxis_rangeslider_visible=False,
        margin=dict(l=70, r=30, t=50, b=40)
    )
    
    st.plotly_chart(fig_candle, use_container_width=True)
    
    # Support and resistance
    recent_data = df.tail(90)
    resistance = recent_data['High'].quantile(0.90)
    support = recent_data['Low'].quantile(0.10)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''
        <div class="metric-container">
            <p><strong>Resistance Level (90th percentile):</strong> \${resistance:.2f}</p>
            <p><strong>Distance from Resistance:</strong> {((df['Close'].iloc[-1] / resistance - 1) * 100):.2f}%</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="metric-container">
            <p><strong>Support Level (10th percentile):</strong> \${support:.2f}</p>
            <p><strong>Distance from Support:</strong> {((df['Close'].iloc[-1] / support - 1) * 100):.2f}%</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div class="analysis-template">', unsafe_allow_html=True)

    st.markdown('''
    **Overall Trend Direction and Strength**

ASTS has experienced extreme volatility over the last 2 years. So, let's break it down.

In 2024, ASTS was declining, hitting rock bottom at \$1.97 on April 2, 2024. This low represented deep investor scepticism. Many doubted if the company could execute its plans and generate revenue. The market was pricing in a high probability of failure.

From there the stock began to reverse its course and rally, albeit in a very volatile manner. From Apr 2024 to Oct 2025, ASTS climbed from \$2 to \$102.79 a gain of over 5000%. This was not due to speculation, but rather the company doing what it promised.

From Apr 2024 to Aug 2024, the stock recovered as the company prepared its first satellite launches. Investors who believed in the potential accumulated shares at depressed prices. The acceleration of the stock began in Sept 2024, when BlueBirds 1-5 successfully deployed. This proved that the satellites could launch and unfold in space, removing a major risk that kept many investors sceptical.

Throughout 2025, upward movement intensified, as the stock gained 270% over the year. Around major milestones, the most explosive moves occurred. For e.g. Sept 2024 satellite deployment and Oct 2025 announcement of BlueBird 6 shipping to India. As each event reduced uncertainty as to whether ASTS could achieve its goals, investor confidence grew.

Since hitting the Oct 2025 peak of \$102.79, ASTS has pulled back to the \$70 to \$100 range. This correction has several causes. Many investors naturally took profits over the incredible rally it's seen from 2024, and analyst downgrades in late 2025 raised concerns of its valuation. Even if the tech works, is the stock price ahead of its business reality? Insider selling in Dec 2025 also indicated that company execs thought the stock might be overvalued. Finally, after such an explosive run, the stock also just needs to consolidate and digest gains before maybe moving higher.

For now, in the last 2 weeks, I've noticed a tighter trading range. Investors are waiting for the next major catalysts, maybe a satellite launch or revenue announcements.

**Key Support and Resistance Levels**

The \$102.79 ATH in Oct 2025 is now a key resistance level, a ceiling where the stock struggles through break through. In a nutshell, when a stock reaches a new high, everyone who bought below this level is profitable, but investors who bought near the peak (all of us have experienced this unfortunately), and watched their positions drop into losses, want to get out and breakeven. This creates a wall of selling pressure every time the stock approaches that level. In late 2025 and early 2025, it's tried to approach that level many times, but failed each time, reinforcing this resistance.

Below current prices, \$70-\$80 represents a support zone. This is a floor where buyers can consistently step in. This makes sense as this price range still represents substantial gains from the Apr 2024 low but offers a potentially attractive entry point for investors who missed the rally or want to add to positions. When the stock dipped toward \$80 in December 2025 after the insider selling news, buyers emerged quickly, preventing further decline. This zone represents where longer-term investors believe the risk-reward remains favourable given the company's progress.

The \$60 level would be the next major support if the stock breaks lower. This level is important because it would represent a deeper correction from the highs; about 40% down from the peak. A drop to this level would likely trigger stop-loss orders (automatic selling orders that many traders set to limit losses) and shake out weaker hands, potentially leading to capitulation selling. Breaking below \$60 would raise serious questions about whether the bullish narrative is still intact.

On the upside, clearing \$100 decisively would be significant (and great for me too) because its close to the ATH. A breakout about this with strong volume would likely attract momentum traders and trigger a new rally as short sellers scramble to cover their positions.

**Chart Patterns**

Let's move on to some shapes and triangles.

Apr 2024 to Oct 2025, ASTS formed a classic parabolic curve. The price rose at an accelerating rate. The angle of ascent got steeper as the rally progressed. Parabolic moves happen when positive feedback loops develop: good news attracts buyers, pushing the price higher, which attracts more attention and more buyers, which pushes the price even higher. This all culminated in the Oct peak with extremely high volume and wide price swings. Classic signs that the buying frenzy was reaching exhaustion, as everyone who wanted to buy, had already bought.

After the Oct high, the stock entered a downward-sloping channel that looks like a bull flag pattern. This is a brief pause in an uptrend where the stock drifts lower on decreasing volume. This occurs as after a sharp rally; some investors take profits while others wait to see if the gains will hold. Lower volume during the decline shows it's not aggressive selling, but just a lack of new buyers. The December 2025 BlueBird 6 launch briefly broke the stock higher, but it couldn't hold the gains. This failed breakout suggests that investors were sceptical. This could be because the news was already anticipated, or concerns about valuation exceeded the positive milestone.

More recently, the stock has been forming higher lows, while testing the resistance zone (\$100 to \$102). This creates an ascending triangle pattern. The lows keep rising (buyers are getting more aggressive), while the highs stay flat (sellers defend that same level of \$100-\$102). This usually resolves with a breakout in the direction of the prior trend (upwards). If the stock breaks above \$100 with strong volume, it signals that buyers have finally overwhelmed the sellers at resistance, often leading to a sharp move higher as shorts cover and momentum traders jump in. However, if it fails and breaks below the rising support line, it will signal that sellers have won, potentially triggering a sharper decline.

The stock has also left several gaps on the chart, which represent days where the opening price was significantly higher or lower than the previous close. This occurs when news breaks after market close or before market opens. As such, a flood of buy orders overwhelms sellers. Most gaps from positive news in 2025 remain unfilled, meaning the stock never traded back down to fill those price levels. This indicates strong underlying demand. However, gaps down in late December and early January 2026 have partially filled, meaning the stock initially dropped sharply but then recovered some of those losses. This indicates some buyers saw the dip as a buying opportunity, but not enough to completely reverse the negative momentum.

**Price Consolidation and Breakout Periods**

Currently, we're in a consolidation phase in the \$70-\$100 range since Oct 2025. ASTS is trading in a relatively tight range despite significant news flow, suggesting investors are waiting for clearer signals about the commercial timeline and revenue generation. Based on past patterns where consolidations lasted 6-12 weeks before the next breakout, we could be approaching a resolution point where the stock either breaks out to new highs or breaks down below support.

**Volume Confirmation**

Volume is the number of shares traded. High volume means many investors are making decisions, low volume means market is mostly uninterested.

The strongest rallies in ASTS came with volume spikes 3-10 times higher than normal. The September 2024 deployment and October 2025 peaks saw exceptional volume because these events attracted attention from investors who had been watching from the sidelines, hedge funds reassessing their positions, and institutions building positions. Heavy volume during upward moves confirms that there is broad-based demand from many participants.

In Dec 2025, the Bluebird 6 launch generated high volume, but still less than the Oct peak. This difference is a warning sign, as it signals fewer participants are willing to chase the price higher. Maybe the launch was anticipated and baked into the share price, or investors were becoming concerned about valuation. The pullback later confirmed what the volume was signalling. The move lacked conviction.

On the downside, the December selloff after insider selling showed above average but not extreme volume. This pattern suggests routine profit-taking rather than panic. When insiders sell, some investors interpret this as a sign to take profits too, but the moderate volume indicated this wasn't creating widespread fear. The early January 2026 weakness from analyst downgrades saw higher volume, indicating more serious selling as institutional investors who follow analyst recommendations adjusted positions. However, volume still didn't reach panic levels, suggesting the selling was orderly rather than a rush for the exits.

Recently, volume has been elevated but declining. This suggests the market is in wait-and-see mode. Neither buyers nor sellers have strong conviction at current levels. Buyers who believe in the story have already built positions and aren't aggressively adding, while sellers aren't panicking to exit. A breakout in either direction would likely need a volume surge to be sustainable, confirming that new participants are entering the market in force.

**Significant Price Catalysts**

The biggest price drivers have been satellite launches.

Sept 2024 deployment of Bluebirds 1-5 sparked a major rally by proving the tech worked in practice. This was further reinforced in Dec 2025, with Bluebird 6 deploying the largest commercial communications array ever.

Partnership announcements have also validated ASTS's commercial module. Oct 2025 agreement with stc Group, included a \$175 million prepayment, showed that major telecom operators are willing to commit meaningful capital.

Regulatory approvals also benefited ASTS. FCC authorizations from 2024 to 2025 for launches and spectrum testing with AT&T and Verizon reduced fears that regulatory barriers could delay commercialization.

However, analyst actions have impacted sentiment and volatility. Bank of America's \$100 valuation target supported the stock, while downgrades from B. Riley and Scotiabank triggered sell-offs. The wide target range of \$40-\$100 indicated uncertainty in valuation of ASTS.

Finally, negative sentiment factors also affected the stock. Insider selling by CTO Huiwen Yao in December 2025 weighed on confidence, while competition from Starlink's direct-to-phone service raised concerns about whether ASTS can scale fast enough to remain competitive.
''')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Volume and Volatility
    st.markdown('<div class="section-header" id="iii-volume-and-volatility-analysis">III. Volume and Volatility Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-header">Trading Volume</div>', unsafe_allow_html=True)
    
    # Volume chart
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(
        x=df.index,
        y=df['Volume'],
        name='Volume',
        marker=dict(
            color=df['Volume'],
            colorscale=[[0, '#bdd7f0'], [0.5, '#5fa3d6'], [1, '#1565c0']],
            showscale=False
        )
    ))

    fig_vol.add_trace(go.Scatter(
        x=df.index,
        y=df['Volume'].rolling(window=20).mean(),
        name='20-Day Average',
        line=dict(color='#c62828', width=2)
    ))

    fig_vol.update_layout(
        title=dict(
            text='Trading Volume',
            font=dict(size=16, color='#000', family="Inter, sans-serif", weight=700),
            x=0,
            xanchor='left'
        ),
        yaxis=dict(
            title='Volume',
            titlefont=dict(size=11, color='#666', family="Inter, sans-serif"),
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        height=380,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, sans-serif"),
        legend=dict(
            font=dict(size=10, color='#444'),
            bgcolor='rgba(255,255,255,0)',
            x=0,
            y=1.1,
            orientation='h'
        ),
        margin=dict(l=70, r=30, t=50, b=40)
    )
    
    st.plotly_chart(fig_vol, use_container_width=True)
    
    st.markdown('<div class="subsection-header">Historical Volatility</div>', unsafe_allow_html=True)
    
    # Volatility chart
    fig_vol2 = go.Figure()
    fig_vol2.add_trace(go.Scatter(
        x=df.index,
        y=df['Volatility_20'],
        fill='tozeroy',
        name='20-Day Volatility',
        line=dict(color='#d4af37', width=2),
        fillcolor='rgba(212, 175, 55, 0.15)'
    ))

    fig_vol2.update_layout(
        title=dict(
            text='Historical Volatility (20-Day Rolling)',
            font=dict(size=16, color='#000', family="Inter, sans-serif", weight=700),
            x=0,
            xanchor='left'
        ),
        yaxis=dict(
            title='Volatility (%)',
            titlefont=dict(size=11, color='#666', family="Inter, sans-serif"),
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        height=380,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        margin=dict(l=70, r=30, t=50, b=40)
    )
    
    st.plotly_chart(fig_vol2, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Daily Volume", f"{df['Volume'].mean():,.0f}")
    with col2:
        st.metric("Current Volatility", f"{df['Volatility_20'].iloc[-1]:.2f}%")
    with col3:
        st.metric("Peak Volatility", f"{df['Volatility_20'].max():.2f}%")
    
    st.markdown('<div class="analysis-template">', unsafe_allow_html=True)
    st.markdown('''
    **Volume Trends and Investor Interest**

Volume shows how much interest a stock is getting. For ASTS, from 2024-2025, avg. daily volume steadily increased as the price rallied from \$1.97 to \$100. This shows ASTS went from a niche stock followed by retail enthusiasts to attracting institutional attention. A greater volume means more liquidity, so it's easier for investors to buy or sell without moving the price dramatically.

**Volume Spikes and Price Movements**

The largest spikes aligned with major price moves. Sept 2024 Bluebirds 1-5 deployment saw volume spike 5-10 times over the normal, as the stock rallied. Oct 2025 ATH also came with massive volume.

More importantly, volume spikes on good news have been much larger than on bad news. This shows that rallies are driven by genuine buying and not panic selling on the way down. However, an exception is the early Jan 2026 analyst downgrades, which triggered elevated selling volumes.

**Volatility Levels**

It's clear to anybody looking at a chart that ASTS is extremely volatile. For the S&P 500, annualized volatility is 15-20%, but for ASTS, it's 80-100%. However, this is expected due to its initial pre-revenue nature. ASTS smaller market cap and high execution risk of successfully launching satellites is the cause of this volatility.

**High and Low Volatility Periods**

Volatility peaked around major catalysts. Sept 2024 deployment, Oct 2025 ATH, Dec 2025 launch saw maddening number of swings (Really felt some of these swings) as news drove this aggressive selling and buying.

However, volatility was much lesser during quiet periods. Before the launches, in 2024, ASTS was relatively calm. Currently, the stock also shows declining volatility as investors wait for the next catalyst. However, this period of compression is usually considered to be healthy, as it precedes the next big move.

**Risk Management Implications**

High volatility means that your position needs to be sized carefully. ASTS can swing 10-20% daily, and it may turn a reasonably sized position into an outsized risk. It should ideally be a small position on most portfolios, but of course, it depends on your risk appetite and investing horizon.

Volume patterns help with timing. High-volume breakouts have worked better than low-volume rallies. High volume at support levels often marks good entry points as panic sellers exit.

Bottom line is that we have to accept that ASTS is incredibly volatile. To put it bluntly, if you're unable to stomach those crazy swings, it would be better to avoid the stock. Try to use volume and volatility to time entries.
    ''')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Returns Analysis
    st.markdown('<div class="section-header" id="iv-returns-analysis">IV. Returns Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-header">Cumulative Returns</div>', unsafe_allow_html=True)
    
    # Cumulative returns chart
    fig_ret = go.Figure()
    fig_ret.add_trace(go.Scatter(
        x=df.index,
        y=df['Cumulative_Return'] * 100,
        fill='tozeroy',
        name='Cumulative Return',
        line=dict(color='#00897b', width=2),
        fillcolor='rgba(0, 137, 123, 0.12)'
    ))

    fig_ret.update_layout(
        title=dict(
            text='Cumulative Returns Since January 2024',
            font=dict(size=16, color='#000', family="Inter, sans-serif", weight=700),
            x=0,
            xanchor='left'
        ),
        yaxis=dict(
            title='Return (%)',
            titlefont=dict(size=11, color='#666', family="Inter, sans-serif"),
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        height=420,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        margin=dict(l=70, r=30, t=50, b=40)
    )
    
    st.plotly_chart(fig_ret, use_container_width=True)
    
    st.markdown('<div class="subsection-header">Monthly Returns Distribution</div>', unsafe_allow_html=True)
    
    # Monthly returns heatmap
    df_monthly = df['Daily_Return'].resample('M').apply(lambda x: (1 + x).prod() - 1)
    monthly_df = pd.DataFrame({
        'Year': df_monthly.index.year,
        'Month': df_monthly.index.month,
        'Return': df_monthly.values * 100
    })
    
    monthly_pivot = monthly_df.pivot(index='Month', columns='Year', values='Return')
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=monthly_pivot.values,
        x=monthly_pivot.columns,
        y=[month_names[i-1] for i in monthly_pivot.index],
        colorscale=[[0, '#c62828'], [0.5, '#ffffff'], [1, '#00897b']],
        zmid=0,
        text=np.round(monthly_pivot.values, 2),
        texttemplate='%{text}%',
        textfont={"size": 10, "color": "#1a2332", "family": "Inter, sans-serif"},
        colorbar=dict(
            title=dict(text="Return (%)", font=dict(size=11, family="Inter, sans-serif")),
            tickfont=dict(size=10, family="Inter, sans-serif")
        )
    ))

    fig_heat.update_layout(
        title=dict(
            text='Monthly Returns Distribution',
            font=dict(size=16, color='#000', family="Inter, sans-serif", weight=700),
            x=0,
            xanchor='left'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=10, color='#444')
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=10, color='#444')
        ),
        height=420,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=60, r=40, t=50, b=40)
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # Return statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Return", f"{df['Cumulative_Return'].iloc[-1] * 100:.2f}%")
    with col2:
        st.metric("Best Single Day", f"{df['Daily_Return'].max() * 100:.2f}%")
    with col3:
        st.metric("Worst Single Day", f"{df['Daily_Return'].min() * 100:.2f}%")
    with col4:
        avg_daily = df['Daily_Return'].mean() * 100
        st.metric("Avg Daily Return", f"{avg_daily:.3f}%")
    
    st.markdown('<div class="analysis-template">', unsafe_allow_html=True)
    st.markdown('''
    **Overall Performance vs Benchmarks**

ASTS has crushed market benchmarks. As mentioned earlier, from the low of \$1.97 to the ATH, that's about a 5000% increase. For the same period, S&P 500 was 25-30% (albeit still great returns over the last few years). This outperformance generally extends to other space sector stocks, like RKLB.

However, these huge returns come with massive volatility, so the question is, does the return justify the risk?

**Consistency of Returns vs Volatility**

ASTS returns have been anything but consistent. The heatmap shows crazy variation, some months 270%, some 20-30% and some drawdowns too. It's not a steady grower at all.

While the returns are spectacular, there is a massive drawback with such risk. Investors had to endure multiple drawdowns (relatable…), even with the overall uptrend.

I did a little bit of research on some financial math when I was trying to figure out how to explain the risk-reward ratio, and I came across this thing called the Sharpe ratio: return per unit of risk). Obviously, this is beyond my knowledge level, so with a little bit of googling and reading how people quantify it, for ASTS, the Sharpe ratio (1.0-1.5) is positive but not good, when you factor in the crazy swings. Essentially, great returns, but you couldn't really sleep at night, as the stock was just so unpredictable.

**Best and Worst Performing Periods**

As mentioned in the above sections, the best periods all coincided with operational milestones.

The worst periods came during gaps of uncertainty. Early 2024 saw a steady decline, and the stock was bottoming. Late 2025 to 2026 hasn't been the best either, with 20-30% decreases due to analyst downgrades and insider selling.

However, single best day returns exceeded 20%, and worst single days saw 15-20% drops. This asymmetry favours upside, so this is considered encouraging.

**Return Drivers and Catalysts**

Returns are almost largely catalyst driven. By catalyst I mean successful satellite launches, partnership announcements (like the \$175 million stc Group prepayment). All these milestones prove that the tech in fact works, and it reduces the associated risk of launch failures.

But on the flip side, analyst downgrades, insider selling and competitive developments from Starlink also triggered sharp selloffs. Looking back on the stock and its associated prices, delays and execution concerns punished its price way more than good news rewarded it. Historically, this is the norm for high-risk stocks.

**Forward Return Expectations**

Essentially, with all the points we've discussed, ASTS is a stock that tested investors' patience (it tested mine a lot). The journey from its troughs to its peaks has been long.

But given so far that this analysis is mostly about the past, what about the future?

Full disclaimer: The following is mostly my opinion.

Bull Case: Strong forward returns are dependent on successful deployment of remaining 45-60 satellites, commercial service launch generating meaningful revenue and more partnerships. If these materialise, we could see another 2-3x jump in the coming year.

Bear Case: Launches could delay, commercial service disappoints or Starlink proves to be a major competition. It could return to the \$30-40 range.

In conclusion, forward returns will be lower than historical returns, but it will still be high compared to market standards, IF and only IF execution continues. I believe it'll still be a very volatile stock, with it being driven by catalysts rather than a steady growth. To me, this is a high-risk, high-reward profile of a stock.
    ''')
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 5: Risk Metrics
    st.markdown('<div class="section-header" id="v-risk-assessment-and-metrics">V. Risk Assessment and Metrics</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-header">Drawdown Analysis</div>', unsafe_allow_html=True)
    
    # Drawdown chart
    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(
        x=df.index,
        y=df['Drawdown'],
        fill='tozeroy',
        name='Drawdown',
        line=dict(color='#c62828', width=2),
        fillcolor='rgba(198, 40, 40, 0.15)'
    ))

    fig_dd.update_layout(
        title=dict(
            text='Drawdown from Peak',
            font=dict(size=16, color='#000', family="Inter, sans-serif", weight=700),
            x=0,
            xanchor='left'
        ),
        yaxis=dict(
            title='Drawdown (%)',
            titlefont=dict(size=11, color='#666', family="Inter, sans-serif"),
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=10, color='#444'),
            gridcolor='#e8e8e8'
        ),
        height=400,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        margin=dict(l=70, r=30, t=50, b=40)
    )
    
    st.plotly_chart(fig_dd, use_container_width=True)
    
    # Risk metrics calculation
    sharpe_ratio = (df['Daily_Return'].mean() / df['Daily_Return'].std()) * np.sqrt(252) if df['Daily_Return'].std() != 0 else 0
    max_drawdown = df['Drawdown'].min()
    downside_returns = df['Daily_Return'][df['Daily_Return'] < 0]
    downside_std = downside_returns.std() * np.sqrt(252) * 100 if len(downside_returns) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Maximum Drawdown", f"{max_drawdown:.2f}%")
    with col2:
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
    with col3:
        st.metric("Daily Std Dev", f"{df['Daily_Return'].std() * 100:.2f}%")
    with col4:
        st.metric("Downside Deviation", f"{downside_std:.2f}%")
    
    st.markdown('<div class="analysis-template">', unsafe_allow_html=True)
    st.markdown('''
    **Drawdown Analysis**

The maximum drawdown from Oct 2025 ATH to recent lows around \$70-80 represent roughly 25-30% decrease. This isn't the worst in its history, but it is relatively recent, so most investors may have faced this.

A key consideration for investors is how long drawdowns last. That drawdown persisted for 3 months, until recently where it's started to come close to the resistance zone. This tests patience.

The key takeaway is that if you own ASTS, you need to be prepared for it to drop 30-40% any time, and this is something I learnt the hard way too. Before I invested in it, I had no idea it was so volatile.

**Execution Risk**

Execution risk is the biggest risk ASTS faces. Currently it has ambitious plans to launch 45-60 satellites by end of 2026. That means 1-2 launces a month. Any delays would mean a severe punishment by the market.

Zooming into execution, I also think manufacturing scale-up (can they produce in time? launch availability (do SpaceX, Blue Origin and ISRO have slots?) and satellite performance are all important factors. Dec 2026 Bluebird 6 launch was smooth, but 45-60 satellites is a big jump. No one else has done something like this, so this is unproven territory.

Commercial service is also an execution hurdle. ASTS needs to transition from successful launches to generating revenue from their partnerships.

**Competitive Risk**

Starlink represents ASTS competitive threats. T-Mobile has a partnership with Starlink, has already started messaging services, and is expanding to data and voice. Starlink has 660 satellites in space, compared to ASTS's six.

The gap is huge. Even with ASTS's larger and more capable satellites, can they deploy fast enough to compete?

Apple has also begun to enter satellite services, albeit limited so far. This is another long-term concern. If major smartphone manufacturers build satellite connectivity directly into their ecosystems, they could bypass ASTS completely.

**Regulatory Risk**

ASTS operates in a heavily regulated industry. They have received the necessary approvals for current operations, but they still need more authorization. Delays and denials could wreck the company's business model.

International regulations is also another hurdle. Each country has its own set of telecommunications approvals, and this process is slow, bureaucratic and uncertain. Likewise, delays and denials could adversely affect the company.

**Financial Risk**

ASTS is still pre-revenue and cash burning. It needs continuous capital raises to fund its exploits. Each capital raise dilutes existing shareholders.

Should market conditions deteriorate, raising capital becomes harder and more expensive. A failed raising of funds may crater the stock.

**Risk Management**

Given these risks, position sizing is crucial. However, everyone has different risk appetites, and by no means can I give a 100% guaranteed answer to this as I don't have a crystal ball in front of me, and neither am I qualified to tell you what to do.

I do think a fundamental principle here is to diversify. If you're a space sector believer like me, a nice basket of space stocks could reduce the single-company risk. The key fundamental issue of ASTS's risk is that it is so binary. Good news, it goes up like crazy, bad news, it goes down like crazy.
    ''')
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 6: Investment Conclusion
    st.markdown('<div class="section-header" id="vi-investment-conclusion">VI. Investment Conclusion</div>', unsafe_allow_html=True)

    st.markdown('<div class="analysis-template">', unsafe_allow_html=True)
    st.markdown('''
    **Key Things to Monitor Going Forward**

The satellite launch schedule is vital to ASTS's success. 1-2 satellites a month by the end of 2026 are ambitious. It will be vital to monitor for delays and technical issues that could affect this.

Commercial service milestones also matter. AT&T's beta service launch planned for H1 2026 is the first real test of revenue generation. AT&T's beta service launch planned for H1 2026 is the first real test of revenue generation.

Competitive developments need monitoring. Starlink's progress with T-Mobile, particularly the expansion beyond messaging to voice and data, directly impacts ASTS's competitive position. Any setbacks for Starlink or signs that AT&T/Verizon are gaining ground would be positive for ASTS.

**Ideal Investor Profile**

Back when I studied economics in JC, I learnt about rational decision making. However, none of us are rational. Nonetheless, we should try our best to manage emotions when it comes to stocks. As such, the ideal investor for ASTS has a high-risk tolerance and can emotionally handle 30-40% swings. If you're the type to check your portfolio daily(nightly), ASTS will destroy your mental health.

Long-term conviction is key. I think this is a 2–3-year story minimum. You need to believe in the space connectivity thesis, and believe in ASTS ability to execute, and hold fast through the peaks and troughs. Short-term traders will get whipsawed by the chaos.

I also can't give a recommended portfolio sizing guide, as it isn't a story of one size fits all. However, portfolio context matters. An ideal investor (not a gambler) should typically have a portfolio with core holdings in index funds and stable stocks. ASTS to me, is a good fit for investors seeking a small position that can deliver meaningful returns. Obviously, on the flip side, those with high-risk stocks as a majority of their portfolio, should avoid adding even more volatility.

**Final Thoughts**

Whenever I see those finance analysts write strong buy, strong sell etc, I don't really like it. I think you must read to know for yourself whether it's a buy or a sell.

But if you're asking for my opinion… I think ASTS is a buy, but with a lot of caution. Given what we covered, ASTS is clearly a volatile stock, high risk, high reward. But I'm a firm believer that ASTS can do what they've set out to do. To me, ASTS is a long-term play, but depending on your risk appetite, portfolio allocation and diversification is key to weather out those periods of 30-40% drawdowns that may happen.

I can't say for sure how high ASTS is going to go, and neither can I come up with a price target. But I believe that a 2-3x increase in the next 12 months is possible.
    ''')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="data-source">', unsafe_allow_html=True)
    st.markdown(f"**Data Source:** Yahoo Finance | **Analysis Date:** January 10, 2026")
    st.markdown("**Disclaimer:** This analysis is for educational and informational purposes only. It does not constitute financial advice. Please conduct your own research and consult with a qualified financial advisor before making investment decisions.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error(f"Unable to load data for {ticker}. Please check the ticker symbol and try again.")