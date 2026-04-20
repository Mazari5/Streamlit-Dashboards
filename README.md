# ⚡ Petrol vs Electric Bike — Pakistan Cost Calculator

A Streamlit dashboard that helps Pakistani riders compare the **true total cost** of owning a petrol bike vs an electric bike — including fuel, service, battery replacements, and CO₂ impact.

## Live Demo

Deploy instantly on [streamlit.app](https://streamlit.io/cloud) (free tier works perfectly).

---

## Files

```
ev_petrol_app/
├── app.py            ← main Streamlit application
├── requirements.txt  ← Python dependencies
└── README.md         ← this file
```

---

## Deploy to Streamlit Community Cloud (Free)

1. **Fork / push to GitHub**
   - Create a new GitHub repository (public or private)
   - Upload `app.py`, `requirements.txt`, and `README.md` to the root of the repo

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click **"New app"**
   - Select your repository, branch (`main`), and set **Main file path** to `app.py`
   - Click **Deploy**

3. **Done** — your app will be live at `https://<your-app-name>.streamlit.app`

---

## Run Locally

```bash
# 1. Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Features

- **Custom inputs** — enter your own petrol bike price, mileage, and EV price
- **EV type selector** — picks Wh/km automatically for common Pakistani EV bikes (Jolta, Vlektra, Sazgar, Ravi, etc.) with a plain-language explanation
- **Battery replacement logic** — calculates how many battery swaps fall within your ownership period based on battery chemistry (LFP / Li-ion / Graphene)
- **Service cost slider** — adjustable monthly petrol service & oil change (default Rs 2,000)
- **Climate impact panel** — CO₂ saved converted to tree equivalents (per month, per year, over full ownership)
- **Interactive charts** — cumulative cost over time (with break-even marker) + cost category breakdown
- **Full references** — all data sources cited in an expandable section at the bottom

---

## Data Sources

| Data | Source |
|---|---|
| Petrol price | OGRA — Rs 268.41/L (March 2025) |
| Electricity tariff | NEPRA/LESCO residential slab — ~Rs 52/kWh (2025) |
| CO₂ from petrol | IPCC AR6, 2.31 kg/litre |
| Pakistan grid emissions | NTDC — 0.45 kg CO₂/kWh (2023) |
| Tree absorption | IPCC — 21.77 kg CO₂/tree/year |
| Battery life (LFP) | Battery University — 5–8 years / 2,000+ cycles |
| EV prices & specs | Jolta Electric · Vlektra · Sazgar · PakWheels (April 2025) |
| Petrol bike prices | Honda Atlas · Yamaha Pakistan (April 2025) |

---

## License

MIT — free to use, modify, and share.
