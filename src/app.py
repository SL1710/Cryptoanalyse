import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import base64
import os
import locale

locale.setlocale(locale.LC_ALL, '')

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Data
df = pd.read_csv('/Users/simonlanger/Sommersemester23/Cryptoanalyse/merged_data_3008.csv')

# Definiere den Pfad zum Ordner mit den Logos
logos_folder = "/Users/simonlanger/Sommersemester23/Cryptoanalyse/Logos"

# Liste der Logos-Dateinamen
logos = [
    "HOME",
    "KONS",
    "BTC",
    "ETH",
    "USDT",
    "BNB",
    "XRP",
    "USDC",
    "STETH",
    "ADA",
    "DOGE",
    "SOL",
    "TRX",
    "TON",
    "DOT",    
    "MATIC",
    "LTC"
]

# Liste der zugehörigen Texte für jedes Logo (ein Wort pro Logo)
logo_texts = [
    "Home",
    "Protocols",
    "Bitcoin",
    "Ethereum",
    "Tether",
    "Binance",
    "Ripple",    
    "USD Coin",
    "Lido Staked Ether",
    "Cardano",
    "Dogecoin",
    "Solana",
    "TRON",
    "Toncoin",
    "Polkadot",    
    "Polygon",
    "Litecoin",
    ]

# Encode die Logos in base64
encoded_logos = {logo: encode_image(os.path.join(logos_folder, f"{logo}.png")) for logo in logos}

def calculate_current_market_cap_percentage(coin_df):
    total_market_cap = df[df['Timestamp'] == latest_date]['Market Cap'].sum()
    coin_market_cap = coin_df['Market Cap'].values[0]
    percentage = (coin_market_cap / total_market_cap) * 100
    return percentage

# Funktion zum Erstellen der KPI Cards
def create_kpi_card(title, value, is_currency=False):
    formatted_value = locale.format_string("%d", value, grouping=True)
    formatted_value_with_commas = formatted_value.replace(",", ".")
    
    if is_currency:
        formatted_value_with_commas = formatted_value_with_commas.replace(".", ",")
    
    card = dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(
                [
                    html.H4(f"${formatted_value_with_commas}" if is_currency else formatted_value_with_commas, className="card-title"),
                ]
            ),
        ],
        style={"width": "20rem", "margin": "0.5rem"},
    )
    return card

def create_percentage_kpi_card(title, value):
    formatted_value = f"{value:.2f}%"  
    card = dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(
                [
                    html.H4(formatted_value, className="card-title"),
                ]
            ),
        ],
        style={"width": "20rem", "margin": "0.5rem"},
    )
    return card

def create_kpi_card_with_thousands(title, value):
    formatted_value = locale.format_string("%d", value, grouping=True)
    card = dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(
                [
                    html.H4(formatted_value, className="card-title"),
                ]
            ),
        ],
        style={"width": "20rem", "margin": "0.5rem"},
    )
    return card


# Funktion zum Erstellen der KPIs
def create_kpis(coin, date):
    coin_df = df[(df['Coin'] == coin) & (df['Timestamp'] == date)]
    if not coin_df.empty:
        coin_market_cap = coin_df['Market Cap'].values[0]
        coin_price = coin_df['Price'].values[0]
        coin_quantity = coin_market_cap / coin_price
        coin_market_cap_percentage = calculate_current_market_cap_percentage(coin_df)
        
        market_cap_card = create_kpi_card("Current Market Cap", coin_market_cap, is_currency=True)
        coin_quantity_card = create_kpi_card("Current Token Quantity", coin_quantity)
        market_cap_percentage_card = create_percentage_kpi_card("Current Market Cap in %", coin_market_cap_percentage)
        
        kpi_content = html.Div([
            html.H3(f"{coin} KPIs"),
            dbc.Row([
                dbc.Col(market_cap_card),
                dbc.Col(market_cap_percentage_card),
                dbc.Col(coin_quantity_card),
            ]),
        ])
        return kpi_content
    else:
        return html.P("Keine Daten für diesen Token verfügbar.")

latest_date = df['Timestamp'].max() 

# Seitenlayout 
page_layouts = {
    "HOME": html.Div([
        html.H1("Willkommen auf der Website der Crypto-Währungs-App!"),
        
        html.Div([
            html.H5("Die Kryptowährungsmärkte sind in ständiger Bewegung. Neue Währungen werden geschaffen, alte Währungen werden gehandelt und die Preise schwanken ständig. Es kann schwierig sein, den Überblick zu behalten und zu wissen, wo man anfangen soll."),
        ], style={"margin-bottom": "40px", "margin-top": "50px"}),

        html.Div([
            html.H5("Diese App wurde entwickelt, um den globalen Markt der Kryptowährungen näher zu bringen. Sie bietet eine umfassende Übersicht über die wichtigsten Konsensmechanismen und die 15 Währungen mit dem höchsten Marktwert."),
        ], style={"margin-bottom": "40px"}),

        html.Div([
            html.H5("Auf der Seite Protocols erfahren Sie mehr über die verschiedenen Arten von Konsensmechanismen, die von Kryptowährungen verwendet werden. Sie erfahren, wie diese Mechanismen funktionieren und welche Vor- und Nachteile sie haben."),
        ], style={"margin-bottom": "40px"}),

        html.Div([
            html.H5("Die Kryptowährungsmärkte sind in ständiger Bewegung. Neue Währungen werden geschaffen, alte Währungen werden gehandelt und die Preise schwanken ständig. Es kann schwierig sein, den Überblick zu behalten und zu wissen, wo man anfangen soll."),
        ], style={"margin-bottom": "40px"}),

        html.Div([
            html.H5("Auf den Seiten der einzelnen Währungen finden Sie detaillierte Informationen zu jeder Währung. Sie erfahren mehr über das Konzept und die Technologie der jeweiligen Währung. Darüber hinaus erhalten Sie eine Visualisierung der Preisentwicklung, aktuelle KPIs und die einzigartigen Merkmale und Probleme jeder Währung."),
        ], style={"margin-bottom": "40px"}),

        html.Div([
            html.H5("Meine Mission ist es, Menschen dabei zu helfen, mehr über Kryptowährungen zu erfahren. Wir glauben, dass diese Technologie das Potenzial hat, die Welt zu verändern, und wir möchten, dass jeder die Möglichkeit hat, sich damit auseinanderzusetzen."),
        ], style={"margin-bottom": "60px"}),

        html.Div([
            html.H4("Viel Spaß beim Erkunden!"),
        ], style={"margin-bottom": "20px"}),

    ]),
    
    "KONS": html.Div([
        html.H1("Konsensmechanismen Page"),
        
        html.Div([
            html.P("Hier sind Informationen zu verschiedenen Konsensmechanismen in der Welt der Kryptowährungen."),
        ], style={"margin-bottom": "20px"}),

        html.Div([
            dbc.Col(html.Div([
                html.H3("Proof-of-Work (PoW):"),
                html.P("Bei diesem Mechanismus lösen Miner komplexe mathematische Rätsel, um Transaktionen zu bestätigen und Blöcke zur Blockchain hinzuzufügen. Die Miner, die das Rätsel zuerst lösen, erhalten Belohnungen in Form von Kryptowährung. PoW ist energieintensiv und erfordert leistungsfähige Hardware."),
            ]), width=6),

            dbc.Col(html.Div([
                html.H3("Proof-of-Stake (PoS):"),
                html.P("Hier setzen Teilnehmer Kryptowährungen (Stake) ein, um Blöcke zu validieren und Belohnungen zu erhalten. Die Wahrscheinlichkeit, einen neuen Block zu erstellen, hängt von der Menge der gestakten Coins ab. Es ist energieeffizienter als PoW."),
            ]), width=6),
        ], className="row"),

        html.Div([
            dbc.Col(html.Div([
                html.H3("Delegated Proof-of-Stake (DPoS):"),
                html.P("In diesem Modell wählen Token-Inhaber Delegierte, die im Namen der Gemeinschaft Blöcke validieren. Die Delegierten erhalten Belohnungen für ihre Dienste. DPoS soll die Skalierbarkeit erhöhen, indem es den Validierungsprozess auf wenige Delegierte beschränkt."),
            ]), width=6),

            dbc.Col(html.Div([
                html.H3("Nominated Proof-of-Stake (NPoS):"),
                html.P("Bei Polkadot wählen Token-Inhaber sogenannte Validator-Nodes aus, die Blöcke validieren. Eine Gruppe von Nominatoren unterstützt die gewählten Validatoren, und diese Kooperation hilft, das Netzwerk sicher und stabil zu halten."),
            ]), width=6),
        ], className="row"),

        html.Div([
            dbc.Col(html.Div([
                html.H3("Proof-of-History (PoH):"),
                html.P("Dieser Mechanismus, von Solana verwendet, dient zur Zeitstempelung von Ereignissen. PoH erzeugt eine historische Aufzeichnung, die Proof-of-Stake und die Validierung von Blöcken unterstützt."),
            ]), width=6),

            dbc.Col(html.Div([
                html.H3("Ripple Protocol Consensus Algorithm (RPCA): "),
                html.P("Ripple verwendet ein eigenes Konsenssystem, bei dem ausgewählte Validatoren Transaktionen bestätigen. Es ist aufgrund der zentralen Kontrolle durch Ripple Labs umstritten."),
            ]), width=6),
        ], className="row"),

        html.Div([
            dbc.Col(html.Div([
                html.H3("Proof-of-Stake Velocity (PoSV): "),
                html.P("Toncoin (TON) verwendet PoSV, bei dem Teilnehmer sowohl Coins halten als auch aktiv nutzen müssen, um neue Coins zu verdienen. Dies soll die Währungsumlaufgeschwindigkeit erhöhen."),
            ]), width=6),

            dbc.Col(html.Div([
                html.H3("Proof-of-Stake (PoS) bei Ethereum 2.0: "),
                html.P("Ähnlich wie bei anderen PoS-Systemen setzen Teilnehmer Ether ein, um Blöcke zu validieren. Ethereum 2.0 zielt darauf ab, die Skalierbarkeit und Energieeffizienz zu verbessern."),
            ]), width=6),
        ], className="row"),

        html.Div([
            dbc.Col(html.Div([
                html.H3("Proof-of-Work (PoW) bei Litecoin: "),
                html.P("Ähnlich wie bei Bitcoin lösen Miner mathematische Rätsel, um Transaktionen zu bestätigen. Litecoin verwendet Scrypt als Hash-Funktion, was ASIC-Mining weniger effizient macht als bei Bitcoin."),
            ]), width=6),

            dbc.Col(html.Div([
                html.H3("Kombination aus Proof-of-Stake und Plasma (MATIC):"),
                html.P("Binance Coin verwendet eine angepasste Version des Tendermint-Konsens, bei dem Validator-Nodes Blöcke validieren und Sicherheit bieten."),
            ]), width=6),
        ], className="row"),

        html.Div([
            dbc.Col(html.Div([
                html.H3("Tendermint-basierter Konsensmechanismus (Binance Chain Tendermint): "),
                html.P("In diesem Modell wählen Token-Inhaber Delegierte, die im Namen der Gemeinschaft Blöcke validieren. Die Delegierten erhalten Belohnungen für ihre Dienste. DPoS soll die Skalierbarkeit erhöhen, indem es den Validierungsprozess auf wenige Delegierte beschränkt."),
            ]), width=6),

            dbc.Col(html.Div([
                html.H3("Proof of Authority (PoA): "),
                html.P("Hier werden Transaktionen von ausgewählten Validierern bestätigt, die als Autoritäten agieren. Dies wird oft in privaten oder konsortialen Blockchains eingesetzt, bei denen Identität und Vertrauen wichtiger sind als Dezentralisierung."),
            ]), width=6),
        ], className="row"),

    ]),
    "BTC": html.Div([
        html.H1("Bitcoin Page"),
    
        dbc.Row([
            dbc.Col(html.Div("Bitcoin (BTC) ist die erste und bekannteste Kryptowährung, die auf der innovativen Blockchain-Technologie aufbaut. Die Blockchain von Bitcoin ist ein dezentrales und transparentes Buchungssystem, das Transaktionen in Blöcken speichert. Der Konsensmechanismus von Bitcoin, Proof-of-Work (PoW), erfordert von Minern das Lösen komplexer Rätsel zur Transaktionsverifizierung und Belohnung. Bitcoin hat die Finanzwelt revolutioniert und den Weg für weitere Kryptowährungen geebnet.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'BTC'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("BTC", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("BTC Unique Selling Point"),
                html.P(" "),
                html.P("• Erste dezentrale Kryptowährung: Pionierstatus als erstes dezentrales digitales Gut."),
                html.P("• Begrenzte Gesamtmenge von 21 Millionen Coins: Schafft Knappheit und Werterhaltung."),
                html.P("• Sicherer Proof-of-Work-Konsensmechanismus: Garantiert Sicherheit und Dezentralisierung."),
                html.P("• Lange Verfolgungsgeschichte und breite Akzeptanz: Etablierte Geschichte und weitreichende Annahme."),
                html.P("• Hohe Liquidität und Handelsvolumen: Bietet lebhafte Handelsmöglichkeiten."),
                html.P("• Etabliertes Ökosystem und Infrastruktur: Verfügt über ein ausgereiftes Unterstützungssystem."),
                html.P("• Einzigartiger Wert und Einfluss auf den Kryptomarkt: Hält eine besondere Position im Kryptomarkt."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("BTC Problems"),
                html.P(" "),
                html.P("• Skalierungsprobleme: Begrenzte Transaktionskapazität führt zu Verzögerungen und höheren Gebühren."),
                html.P("• Energieintensiver Bergbau: Proof-of-Work verbraucht große Mengen Energie, was Umweltbedenken aufwirft."),
                html.P("• Volatile Preisschwankungen: Bitcoin's Wert ist starken Schwankungen unterworfen, was die Nutzung als Währung erschwert."),
                html.P("• Mangelnde Anpassungsfähigkeit: Schwierigkeiten bei der Einführung neuer Funktionen und Upgrades im Protokoll."),
                html.P("• Zentrale Mining-Konzentration: Große Mining-Pools könnten die Dezentralisierung gefährden."),
                html.P("• Begrenzte Smart-Contract-Fähigkeiten: Im Vergleich zu neueren Kryptowährungen hat Bitcoin begrenzte Möglichkeiten für komplexe Smart Contracts."),
                html.P("• Regulatorische Unsicherheit: Wechselnde Regulierungen könnten die Akzeptanz und Nutzung behindern."),
            ]), width=5),
        ]),
    ]),
    "ETH": html.Div([
        html.H1("Ethereum Page"),
    
        dbc.Row([
            dbc.Col(html.Div("Ethereum (ETH) ist eine führende Kryptowährung, die die bahnbrechende Blockchain-Technologie nutzt. Die Ethereum-Blockchain ist ein dezentrales, öffentliches Register für Transaktionen, das in Blöcken organisiert ist. Ethereums Konsensmechanismus, der von Proof-of-Work (PoW) zu Proof-of-Stake (PoS) übergeht, ermöglicht Transaktionsüberprüfung und Netzwerksicherheit. PoS reduziert Energieverbrauch und fördert Teilnahme. Ethereum geht über Finanztransaktionen hinaus und ermöglicht die Erstellung dezentraler Anwendungen und Smart Contracts. ")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'ETH'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("ETH", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("ETH Unique Selling Point"),
                html.P(" "),
                html.P("• Erste dezentrale Plattform: Ermöglicht die Ausführung von Smart Contracts und dezentralen Anwendungen."),
                html.P("• Smart Contract Vielseitigkeit: Bietet umfangreiche Möglichkeiten für programmierbare Verträge."),
                html.P("• Aktive Entwicklergemeinschaft: Unterstützt ständige Innovation und Weiterentwicklung."),
                html.P("• Upgrade auf Proof-of-Stake: Geplante Umstellung auf ETH 2.0 zur Verbesserung der Skalierbarkeit und Energieeffizienz."),
                html.P("• DeFi Vorreiter: Treibende Kraft im boomenden Bereich der dezentralen Finanzen."),
                html.P("• ICO Pionier: Legte den Grundstein für die Finanzierung von Projekten über Initial Coin Offerings."),
                html.P("• Breite Akzeptanz und Nutzung: Findet Anwendung in verschiedenen Branchen und Anwendungsfällen."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("ETH Problems"),
                html.P(" "),
                html.P("• Skalierungsprobleme: Herausforderungen bei der Bewältigung von Netzwerküberlastungen und Gebühren."),
                html.P("• Technische Komplexität: Die Funktionsweise von Smart Contracts kann für Entwickler anspruchsvoll sein."),
                html.P("• Konkurrenz und Kompatibilität: Enorme Anzahl von Blockchain-Konkurrenten und Interoperabilitätsfragen."),
                html.P("• Regulierungsunsicherheit: Unklarheit über die regulatorische Zukunft von Kryptowährungen."),
            ]), width=5),
        ]),
    ]),
    "USDT": html.Div([
        html.H1("Tether Page"),
    
        dbc.Row([
            dbc.Col(html.Div("USDT (Tether) ist eine prominente Stablecoin, die auf verschiedenen Blockchains, darunter Ethereum (ETH), basiert. Die Blockchain von USDT ist ein verteiltes Hauptbuch, das die Bewegung der Tether-Token nachverfolgt. USDT verwendet verschiedene Konsensmechanismen, abhängig von der zugrunde liegenden Blockchain, z. B. PoW für Ethereum. Als Stablecoin ist USDT an den Wert des US-Dollars gebunden, was Stabilität in volatilen Krypto-Märkten bietet. USDT wird oft für Handel, Überweisungen und als Brücke zwischen Krypto- und Fiat-Währungen verwendet, und hat die Akzeptanz von Krypto im Mainstream gefördert.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'USDT'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("USDT", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("USDT Unique Selling Point"),
                html.P(" "),
                html.P("• Stabile Preisbindung: Tether ist an den US-Dollar gekoppelt und bietet Stabilität in volatilen Kryptomärkten."),
                html.P("• Weite Verbreitung: USDT wird weitreichend in Krypto-Handelsplattformen als stabile Handelswährung verwendet."),
                html.P("• Schnelle Transaktionen: USDT-Transaktionen erfolgen in der Regel schnell und ermöglichen effizienten Werttransfer."),
                html.P("• Liquidität und Handelsvolumen: Hohe Liquidität und häufiges Handelsvolumen auf verschiedenen Plattformen."),
                html.P("• Vereinfachte Arbitrage: Ermöglicht einfache Preisarbitrage zwischen Börsen und Märkten."),
                html.P("• Einfache Integration: Ermöglicht einfache Integration in verschiedene Kryptodienste und Anwendungen."),
                html.P("• Globale Akzeptanz: Wird von vielen Nutzern und Dienstleistern auf der ganzen Welt akzeptiert."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("USDT Problems"),
                html.P(" "),
                html.P("• Vertrauensfrage: Abhängigkeit von der Reserve zur Unterstützung des 1:1-Verhältnisses zum US-Dollar."),
                html.P("• Transparenzbedenken: Die Offenlegung der tatsächlichen Reserven und Praktiken von Tether wurde angezweifelt."),
                html.P("• Regulatorische Unsicherheit: Aufgrund der möglichen Einordnung als Wertpapier könnten regulatorische Fragen aufkommen."),
                html.P("• Konkurrenz im Stablecoin-Markt: Zahlreiche Konkurrenz-Stablecoins könnten die Marktstellung von USDT beeinträchtigen."),
                html.P("• Systemisches Risiko: Da USDT in vielen Kryptotrading-Paaren weit verbreitet ist, könnte ein Zusammenbruch von Tether Auswirkungen auf den Kryptomarkt haben."),
                html.P("• Rechtsstreitigkeiten: Das Unternehmen hinter Tether war in rechtliche Kontroversen verwickelt, was das Vertrauen beeinträchtigen könnte."),
                html.P("• Technische Störungen: In der Vergangenheit gab es technische Probleme, die zu Transaktionsverzögerungen führten."),
            ]), width=5),
        ]),
    ]),
    "XRP": html.Div([
        html.H1("Ripple Page"),
    
        dbc.Row([
            dbc.Col(html.Div("XRP ist die native Kryptowährung des Ripple-Netzwerks, das Zahlungsabwicklungen und Währungsaustausch erleichtert. Die XRP-Ledger-Blockchain verfolgt Transaktionen und unterstützt eine breite Palette von Währungen. XRP verwendet den Ripple Consensus Algorithm (RCA), bei dem ausgewählte Validatoren Einigkeit über Transaktionen erzielen. XRP zielt darauf ab, schnelle, kostengünstige und grenzüberschreitende Zahlungen zu ermöglichen. Es wird von Banken und Finanzinstitutionen genutzt, um Liquidität zu optimieren.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'XRP'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("XRP", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("XRP Unique Selling Point"),
                html.P(" "),
                html.P("• Schnelle Transaktionen: Ripple bietet schnelle und kostengünstige grenzüberschreitende Transaktionen."),
                html.P("• Skalierbarkeit: Das Ripple-Netzwerk ist auf hohe Transaktionsvolumina ausgelegt."),
                html.P("• Institutionelle Unterstützung: Ripple wird von verschiedenen Finanzinstituten für internationale Zahlungen genutzt."),
                html.P("• Konsensalgorithmus: Das Ripple-Netzwerk verwendet den einzigartigen Consensus-Algorithmus, der Energieeffizienz und Sicherheit bietet."),
                html.P("• XRP als Brückenwährung: XRP kann als Brückenwährung für den Werttransfer zwischen verschiedenen Währungen dienen."),
                html.P("• Fokus auf Regulierung: Ripple arbeitet aktiv mit Regulierungsbehörden zusammen und betont die Bedeutung der Einhaltung von Vorschriften."),
                html.P("• Partnerschaften: Ripple hat Partnerschaften mit verschiedenen Finanzinstitutionen und Technologieunternehmen geschlossen."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("XRP Problems"),
                html.P(" "),
                html.P("• Zentralisierungskritik: Die Kontrolle über einen Großteil der XRP-Token durch das Unternehmen Ripple hat zu Bedenken hinsichtlich der Dezentralisierung geführt."),
                html.P("• Gerichtsverfahren: Ripple wurde von der SEC wegen möglicher Verletzung von Wertpapiergesetzen verklagt, was Unsicherheit schürt."),
                html.P("• Abhängigkeit von Ripple: Der Erfolg von XRP ist stark mit dem Erfolg und den Handlungen des Unternehmens Ripple verknüpft."),
                html.P("• Mangelnde Adoption: Obwohl Ripple Partnerschaften hat, hat XRP noch nicht in dem Maße wie andere Kryptowährungen in der Realwirtschaft Fuß gefasst."),
                html.P("• Konkurrenz im Zahlungssektor: Ripple konkurriert mit traditionellen internationalen Zahlungsnetzwerken sowie anderen Kryptowährungen."),
                html.P("• Technische Kritik: Einige Krypto-Enthusiasten kritisieren XRP's Konsensalgorithmus und den Grad der Zentralisierung."),
                html.P("• Regulatorische Unsicherheit: Die rechtliche Einstufung von XRP ist unsicher und könnte zukünftige Nutzungsmöglichkeiten beeinflussen."),
            ]), width=5),
        ]),
    ]),
    "BNB": html.Div([
        html.H1("Binance Coin Page"),
    
        dbc.Row([
            dbc.Col(html.Div("BNB (Binance Coin) ist die hauseigene Kryptowährung der Binance-Plattform, einer der größten Krypto-Börsen. BNB basiert auf der Binance Chain und der Binance Smart Chain (BSC), die beide eigene Blockchains sind. Die Binance Chain verwendet den Tendermint-Konsensmechanismus, während die BSC eine Kombination aus PoW und PoS nutzt. BNB hat vielfältige Verwendungszwecke, einschließlich Handelsgebühren auf Binance, Teilnahme am BSC-Ökosystem und Zugang zu Launchpad-Veranstaltungen. Als Treibstoff der Binance-Plattform trägt BNB zur Effizienz des Börsenbetriebs und zur Förderung von Krypto-Innovationen bei.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'BNB'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("BNB", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("BNB Unique Selling Point"),
                html.P(" "),
                html.P("• Binance Exchange Integration: BNB ist die native Kryptowährung der Binance-Börse, was verschiedene Vorteile für den Handel und Gebühren bietet."),
                html.P("• Gebührenreduktion: BNB kann auf der Binance-Börse für den Handel verwendet werden, um Handelsgebühren zu reduzieren."),
                html.P("• Token-Brennen: Binance verbrennt regelmäßig einen Teil der im Umlauf befindlichen BNB-Token, um die Knappheit zu erhöhen."),
                html.P("• Launchpad für ICOs: Binance Launchpad ermöglicht es Projekten, Token Sales durchzuführen und trägt zur Nachfrage nach BNB bei."),
                html.P("• Vielfältige Anwendungen: BNB wird nicht nur auf der Binance-Börse, sondern auch in verschiedenen Anwendungen und Ökosystemen verwendet."),
                html.P("• Binance Smart Chain (BSC): BNB ist auch Teil der Binance Smart Chain, die dezentrale Anwendungen und Smart Contracts unterstützt."),
                html.P("• Schnelle Transaktionen: BNB-Transaktionen sind in der Regel schnell und effizient."),
                html.P("• Binance-Ökosystem: BNB ist in verschiedene Dienste wie Binance Launchpad, Binance Pay und Binance Card integriert."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("BNB Problems"),
                html.P(" "),
                html.P("• Zentralisierung: Die Binance-Börse und das Binance-Ökosystem sind zentralisiert, was Dezentralisierungsanliegen aufwirft."),
                html.P("• Abhängigkeit von Binance: Der Wert von BNB ist eng mit dem Erfolg und den Aktivitäten der Binance-Börse verbunden."),
                html.P("• Regulierungsrisiken: Die Binance-Gruppe steht im Mittelpunkt regulatorischer Prüfungen und Unsicherheiten."),
                html.P("• Konkurrenz im Exchange-Token-Markt: Andere Exchange-Token konkurrieren mit BNB um Nutzer und Anwendungsfälle."),
                html.P("• Wettbewerbsdruck: BNB steht im Wettbewerb mit anderen Plattform-Token wie ETH, die ebenfalls in DeFi-Ökosystemen genutzt werden."),
                html.P("• Eingeschränkte Dezentralisierung: Obwohl auf der Binance Smart Chain aktiv, könnte die Dezentralisierung im Vergleich zu anderen Blockchain-Netzwerken eingeschränkt sein."),
                html.P("• Marktabsorption: Eine begrenzte Anzahl von Verwendungszwecken könnte die Nachfrage und den Wert von BNB beschränken."),
                html.P("• Begrenzte Anwendungsvielfalt: Der Anwendungsfall von BNB ist hauptsächlich auf das Binance-Ökosystem beschränkt."),
            ]), width=5),
        ]),
    ]),
    "USDC": html.Div([
        html.H1("USD Coin Page"),
    
        dbc.Row([
            dbc.Col(html.Div("USDC (USD Coin) ist eine führende Stablecoin, die den Wert des US-Dollars repräsentiert. Die USDC-Blockchain basiert auf verschiedenen Blockchains wie Ethereum (ETH) und Algorand. USDC-Token werden auf diesen Blockchains emittiert und verfolgen Transaktionen transparent. Der Konsensmechanismus variiert je nach verwendeter Blockchain, z. B. PoW für Ethereum. USDC bietet Stabilität in volatilen Kryptomärkten und fungiert als Brücke zwischen Krypto und Fiat. Es wird für den Handel, Zahlungen und DeFi-Anwendungen verwendet. Als vertrauenswürdige Stablecoin fördert USDC die Akzeptanz von Kryptowährungen im Mainstream.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'USDC'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("USDC", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("USDC Unique Selling Point"),
                html.P(" "),
                html.P("• Stabile Preisbindung: USDC ist an den US-Dollar gebunden und bietet Stabilität in volatilen Kryptomärkten."),
                html.P("• Vertrauenswürdiger Emittent: USDC wird von etablierten Unternehmen wie Circle und Coinbase herausgegeben."),
                html.P("• Transparente Reserven: Die Unternehmen hinter USDC geben regelmäßige Berichte über die Reserven heraus, um das Vertrauen zu stärken."),
                html.P("• Weite Akzeptanz: USDC wird auf vielen Krypto-Börsen und Plattformen als handelbare Währung verwendet."),
                html.P("• Schnelle Transaktionen: USDC-Transaktionen erfolgen in der Regel schnell und ermöglichen effizienten Werttransfer."),
                html.P("• Liquidität und Handelsvolumen: USDC ist einer der am häufigsten gehandelten Stablecoins auf verschiedenen Plattformen."),
                html.P("• DeFi Integration: USDC wird in vielen dezentralen Finanzanwendungen (DeFi) als Basiswährung verwendet."),
                html.P("• Internationale Verfügbarkeit: USDC kann weltweit genutzt werden, um den US-Dollar zu repräsentieren."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("USDC Problems"),
                html.P(" "),
                html.P("• Vertrauen in die Emittenten: Trotz Transparenz hängt das Vertrauen in USDC von den Emittenten ab."),
                html.P("• Regulatorische Risiken: Die regulatorische Einstufung von Stablecoins wie USDC könnte sich auf die Nutzung auswirken."),
                html.P("• Abhängigkeit von Unternehmen: Der Erfolg von USDC ist an die Stabilität und Integrität der Emittenten gebunden."),
                html.P("• Konkurrenz im Stablecoin-Markt: Zahlreiche andere Stablecoins konkurrieren mit USDC um Nutzer und Akzeptanz."),
                html.P("• Systemisches Risiko: Da USDC in vielen Kryptotrading-Paaren weit verbreitet ist, könnte ein Zusammenbruch von USDC Auswirkungen auf den Kryptomarkt haben."),
                html.P("• Datenschutzbedenken: Die Nutzung von USDC kann potenziell Benutzerdaten exponieren."),
                html.P("• Zentralisierung: Obwohl USDC weit verbreitet ist, bleibt die Ausgabe und Verwaltung in den Händen weniger Unternehmen."),
                html.P("• Technische Störungen: In der Vergangenheit gab es technische Probleme, die zu Transaktionsverzögerungen führten."),
            ]), width=5),
        ]),
    ]),
    "STETH": html.Div([
        html.H1("Lido Staked Ether Page"),
    
        dbc.Row([
            dbc.Col(html.Div("STETH (Staked Ether) ist ein Token, das im Ethereum 2.0-Netzwerk erstellt wird, um die Staking-Funktionalität zu nutzen. Ethereum 2.0 zielt darauf ab, Skalierbarkeit und Effizienz durch Proof-of-Stake (PoS) anstelle von Proof-of-Work (PoW) zu erreichen. STETH repräsentiert gestakete Ether und wird auf der Beacon Chain verfolgt, die als Hauptbuch dient. PoS ermöglicht Validatoren, Transaktionen zu verifizieren und das Netzwerk zu sichern. STETH ermöglicht ETH-Inhabern, am Staking teilzunehmen, Belohnungen zu verdienen und gleichzeitig die Liquidität zu nutzen. Ethereum 2.0 und STETH sind wichtige Schritte zur Verbesserung der Ethereum-Blockchain und zur Bewältigung von Skalierungsproblemen.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'STETH'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("STETH", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("STETH Unique Selling Point"),
                html.P(" "),
                html.P("• Staking-Belohnungen: STETH ermöglicht es Ethereum-Besitzern, ihre Ether im Ethereum 2.0 Staking-Netzwerk zu staken und Belohnungen zu verdienen."),
                html.P("• Einfacher Zugang: Ermöglicht nicht-technischen Benutzern die Teilnahme am Ethereum 2.0 Staking ohne komplizierte Technik."),
                html.P("• Liquide Staking: STETH ermöglicht es den Nutzern, ihre gestakten Ether auf dem Markt zu handeln und zu transferieren."),
                html.P("• Dezentrale Sicherheit: Trägt zur Sicherheit und Dezentralisierung des Ethereum-Netzwerks bei, indem es mehr Ether stakt."),
                html.P("• Langfristige Belohnungen: Ethereum 2.0 soll über die Jahre hinweg belohnt werden, was potenziell stabile Erträge bieten kann."),
                html.P("• Beitrag zur Netzwerkskalierung: Durch das Staken von Ether trägt STETH zur Skalierung des Ethereum-Netzwerks bei."),
                html.P("• Einfache Integration: STETH kann in verschiedene DeFi-Protokolle und Anwendungen integriert werden."),
                html.P("• Geringere Notwendigkeit für Mining: Staking reduziert die Abhängigkeit von energieintensivem Mining und fördert Energieeffizienz."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("STETH Problems"),
                html.P(" "),
                html.P("• Unstaked-Verfügbarkeit: Staked Ether ist für einen festen Zeitraum gesperrt, was zu mangelnder Liquidität führen kann."),
                html.P("• Staking-Risiken: Staking ist mit Risiken verbunden, einschließlich der Möglichkeit von Verlusten bei Netzwerkfehlern oder Angriffen."),
                html.P("• Technische Kenntnisse: Obwohl einfacher als das traditionelle Staking, erfordert STETH immer noch grundlegende Kenntnisse in Bezug auf Krypto und Ethereum."),
                html.P("• Staking-Verluste: Staker können ihre ETH-Beiträge verlieren, wenn sie gegen die Netzwerkregeln verstoßen."),
                html.P("• ETH 2.0 Unsicherheiten: STETH hängt von der reibungslosen Umstellung auf Ethereum 2.0 ab, was Unsicherheit birgt."),
                html.P("• Abhängigkeit vom Ethereum-Ökosystem: STETH's Erfolg hängt von der allgemeinen Akzeptanz und Nutzung des Ethereum-Netzwerks ab."),
                html.P("• Zentralisierungsbedenken: Wie bei anderen Staking-Netzwerken könnten Konzentrationen von großen Stakern die Dezentralisierung beeinträchtigen."),
                html.P("• Regulatorische Unsicherheiten: Wie andere Kryptowährungen könnte auch STETH regulatorischen Veränderungen unterliegen."),
            ]), width=5),
        ]),
    ]),
    "ADA": html.Div([
        html.H1("Cardano Page"),
    
        dbc.Row([
            dbc.Col(html.Div("ADA (Cardano) ist die Kryptowährung des Cardano-Netzwerks, das auf wissenschaftlicher Forschung und Peer-Review basiert. Die Cardano-Blockchain implementiert den Ouroboros-Konsensmechanismus, ein Proof-of-Stake (PoS)-Protokoll, das Energieeffizienz und Sicherheit gewährleistet. ADA zielt darauf ab, Skalierbarkeit, Interoperabilität und Nachhaltigkeit zu erreichen. ADA wird für Transaktionen, DeFi und Staking verwendet, wodurch Benutzer Belohnungen verdienen können. Cardano setzt auf rigorose Forschung und zielt darauf ab, die Blockchain-Technologie weiter voranzutreiben.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'ADA'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("ADA", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("ADA Unique Selling Point"),
                html.P(" "),
                html.P("• Wissenschaftliche Grundlage: Cardano basiert auf Forschung und wissenschaftlichen Ansätzen, um technische Lösungen zu entwickeln."),
                html.P("• Proof-of-Stake-Konsens: Verwendet Ouroboros, einen Proof-of-Stake-Konsensalgorithmus, der Energieeffizienz und Sicherheit bietet."),
                html.P("• Skalierbarkeit: Das Cardano-Protokoll ist darauf ausgelegt, skalierbar zu sein und eine große Anzahl von Transaktionen zu verarbeiten."),
                html.P("• Interoperabilität: Strebt an, mit verschiedenen Blockchains und Systemen zu interagieren und die Kommunikation zu erleichtern."),
                html.P("• Nachhaltigkeit: Das Cardano-Ökosystem fördert die langfristige Nachhaltigkeit und die Beteiligung der Community."),
                html.P("• Governance-Modell: Integriert ein dezentrales Governance-Modell, das die Community in Entscheidungsprozesse einbezieht."),
                html.P("• Smart Contracts und dApps: Ermöglicht die Entwicklung von Smart Contracts und dezentralen Anwendungen auf seiner Plattform."),
                html.P("• Schwerpunkt auf Compliance: Cardano betont die Bedeutung der Einhaltung von Vorschriften und der Zusammenarbeit mit Regulierungsbehörden."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("ADA Problems"),
                html.P(" "),
                html.P("• Entwicklungszeit: Obwohl durchdacht, hat Cardano mehr Zeit für die Entwicklung benötigt, was zu Verzögerungen führte."),
                html.P("• Wettbewerbsdruck: Cardano konkurriert mit anderen Smart-Contract-Plattformen wie Ethereum und Binance Smart Chain."),
                html.P("• Noch nicht vollständig umgesetzt: Einige der geplanten Funktionen und Verbesserungen sind noch nicht vollständig implementiert."),
                html.P("• Konnektivität zu Legacy-Systemen: Die Interoperabilität mit bestehenden Finanzsystemen könnte Herausforderungen mit sich bringen."),
                html.P("• Regulierungsunsicherheit: Wie andere Kryptowährungen könnte auch ADA durch wechselnde Regulierungen beeinflusst werden."),
                html.P("• Technische Komplexität: Entwickeln von dApps auf der Cardano-Plattform erfordert technisches Verständnis."),
                html.P("• Abhängigkeit von Forschung: Der wissenschaftliche Ansatz von Cardano birgt das Risiko, dass Forschungsergebnisse nicht in der Praxis umgesetzt werden können."),
                html.P("• Netzwerkeffekte: Die Etablierung von Cardano im Wettbewerbsumfeld kann aufgrund bestehender Netzwerkeffekte eine Herausforderung sein."),
            ]), width=5),
        ]),
    ]),
    "SOL": html.Div([
        html.H1("Solana Page"),
    
        dbc.Row([
            dbc.Col(html.Div("SOL (Solana) ist die Kryptowährung des Solana-Netzwerks, das auf innovativer Technologie zur Bewältigung von Skalierungsproblemen setzt. Die Solana-Blockchain verwendet den Proof-of-History (PoH)-Konsensmechanismus, der Transaktionsreihenfolge und Zeitstempel sicher festlegt. Mit Proof-of-Stake (PoS) validiert Solana Transaktionen und sichert das Netzwerk. Solana zielt darauf ab, hohe Geschwindigkeiten und geringe Transaktionskosten zu bieten, was es für dezentrale Anwendungen (dApps) attraktiv macht. Die Solana-Blockchain ermöglicht tausende Transaktionen pro Sekunde und hat das Potenzial, Skalierungsprobleme in der Krypto-Welt zu lösen.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'SOL'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("SOL", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("SOL Unique Selling Point"),
                html.P(" "),
                html.P("• Hochleistungsnetzwerk: Solana zeichnet sich durch seine hohe Skalierbarkeit und schnelle Transaktionsverarbeitung aus."),
                html.P("• Hohe Transaktionsgeschwindigkeit: Solana kann Tausende von Transaktionen pro Sekunde verarbeiten, was zu schnellen Netzwerkinteraktionen führt."),
                html.P("• Geringe Transaktionskosten: Die Kosten für Transaktionen auf Solana sind im Vergleich zu anderen Netzwerken niedrig."),
                html.P("• Dezentralisiertes Konsensmodell: Verwendet Proof-of-History (PoH) in Kombination mit Proof-of-Stake für Sicherheit und Effizienz."),
                html.P("• Benutzerfreundliche Erfahrung: Die schnellen Transaktionen und niedrigen Gebühren bieten eine nahtlose Benutzererfahrung."),
                html.P("• Einfache Tokenisierung: Solana unterstützt die einfache Erstellung von benutzerdefinierten Tokens und dezentralen Anwendungen."),
                html.P("• Wachsendes Ökosystem: Solana hat ein zunehmend breites Angebot an Projekten und Anwendungen."),
                html.P("• Interoperabilität: Strebt an, mit anderen Blockchains und Netzwerken zu interagieren und Daten auszutauschen."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("SOL Problems"),
                html.P(" "),
                html.P("• Dezentralisierungsbedenken: Obwohl ein dezentralisiertes Modell verwendet wird, könnte die Konzentration von Staking-Guthaben Auswirkungen auf die Dezentralisierung haben."),
                html.P("• Technische Herausforderungen: Die Komplexität des Netzwerks könnte für Entwickler und Nutzer eine Herausforderung darstellen."),
                html.P("• Wettbewerbsdruck: Solana konkurriert mit anderen leistungsfähigen Netzwerken wie Ethereum, Avalanche und Binance Smart Chain."),
                html.P("• Netzwerkausfälle: Da Solana von einer kleinen Anzahl von Validatoren betrieben wird, könnte ein Ausfall eines Validators das Netzwerk beeinträchtigen."),
                html.P("• Abhängigkeit von Solana Labs: Die Entwicklung und Verbesserung des Netzwerks hängt von Solana Labs ab."),
                html.P("• Regulierungsunsicherheit: Wie andere Kryptowährungen könnte auch SOL regulatorischen Veränderungen unterliegen."),
                html.P("• Technische Störungen: In der Vergangenheit gab es technische Probleme, die zu Netzwerkunterbrechungen führten."),
                html.P("• Längerfristige Akzeptanz: Die langfristige Akzeptanz und Nutzung des Netzwerks müssen sich noch bewähren."),
            ]), width=5),
        ]),
    ]),
    "DOGE": html.Div([
        html.H1("Dogecoin Page"),
    
        dbc.Row([
            dbc.Col(html.Div("DOGE (Dogecoin) ist eine spaßorientierte Kryptowährung, die als Fork von Litecoin entstanden ist. Die DOGE-Blockchain verfolgt Transaktionen und verwendet den Scrypt-Konsensmechanismus, der auf Proof-of-Work (PoW) basiert. Ursprünglich als Scherz gestartet, hat sich DOGE zu einer beliebten und weitverbreiteten Kryptowährung entwickelt. DOGE hebt sich durch sein Maskottchen, den Shiba Inu-Hund, hervor und hat eine engagierte Community. Trotz seiner informellen Herkunft wird DOGE für Trinkgelder, Spenden und sogar für einige Transaktionen verwendet. ")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'DOGE'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("DOGE", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("DOGE Unique Selling Point"),
                html.P(" "),
                html.P("• Gemeinschaft und Kultur: DOGE hat eine starke und enthusiastische Online-Community, die für Spaß und Engagement steht."),
                html.P("• Meme-Kultur: Entstand aus einem Internet-Meme, was zu einer einzigartigen und zugänglichen Identität führte."),
                html.P("• Einfache Nutzung: DOGE ist einfach zu erwerben, zu halten und zu verwenden, was es zu einer beliebten Einstiegskryptowährung macht."),
                html.P("• Schnelle Transaktionen: DOGE bietet schnelle Transaktionsbestätigungen, was für den täglichen Gebrauch nützlich sein kann."),
                html.P("• Niedrige Gebühren: Die Transaktionsgebühren von DOGE sind in der Regel sehr niedrig."),
                html.P("• Trinkgeldkultur: Dogecoin wird oft für Trinkgelder und Spenden in sozialen Medien verwendet."),
                html.P("• Einfache Integration: Aufgrund der Popularität ist DOGE in verschiedenen Krypto-Diensten und Börsen weit verbreitet."),
                html.P("• Markterfahrung: DOGE hat eine lange Geschichte auf dem Kryptomarkt, was zu einer gewissen Stabilität führen kann."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("DOGE Problems"),
                html.P(" "),
                html.P("• Mangelnde technische Weiterentwicklung: Dogecoin hat im Vergleich zu anderen Projekten weniger technische Innovationen."),
                html.P("• Geringe Anwendbarkeit: Dogecoin hat im Vergleich zu anderen Kryptowährungen begrenzte praktische Anwendungsfälle."),
                html.P("• Mangelnde Skalierbarkeit: Dogecoin hat in der Vergangenheit Schwierigkeiten bei der Bewältigung von Netzwerküberlastungen gehabt."),
                html.P("• Konkurrenz im Meme-Space: Andere Meme-basierte Kryptowährungen könnten die Aufmerksamkeit von DOGE ablenken."),
                html.P("• Abhängigkeit von Popularität: Der Wert und die Akzeptanz von DOGE können stark von der aktuellen Internetkultur und Hype abhängen."),
                html.P("• Mangelnde Dezentralisierung: Die Entwicklung und Wartung von Dogecoin hängt von einer kleinen Entwicklergruppe ab."),
                html.P("• Regulierungsunsicherheit: Wie andere Kryptowährungen könnte auch DOGE regulatorischen Veränderungen unterliegen."),
                html.P("• Volatile Preisschwankungen: Dogecoin ist wie andere Kryptowährungen anfällig für starke Preisschwankungen."),
            ]), width=5),
        ]),
    ]),
    "MATIC": html.Div([
        html.H1("Polygon Page"),
    
        dbc.Row([
            dbc.Col(html.Div("MATIC (Polygon) ist die Kryptowährung des Polygon-Netzwerks, das Skalierungs- und Interoperabilitätslösungen für Ethereum bietet. Die MATIC-Blockchain verfolgt Transaktionen und verwendet den Proof-of-Stake (PoS)-Konsensmechanismus. Polygon zielt darauf ab, die Leistung von Ethereum zu steigern, indem es schnelle und kostengünstige Transaktionen ermöglicht. Als Layer-2-Lösung unterstützt Polygon verschiedene dApps und DeFi-Protokolle. MATIC wird für Transaktionsgebühren, Staking und Governance verwendet. Polygon bietet eine Brücke zwischen Ethereum und der Mainstream-Adoption von Kryptowährungen durch verbesserte Skalierbarkeit und Benutzerfreundlichkeit.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'MATIC'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("MATIC", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("MATIC Unique Selling Point"),
                html.P(" "),
                html.P("• Skalierungslösung: Polygon bietet eine Skalierungsschicht für Ethereum, die schnellere und kostengünstigere Transaktionen ermöglicht."),
                html.P("• Interoperabilität: Bietet Interoperabilität zwischen verschiedenen Blockchains und ermöglicht den nahtlosen Austausch von Vermögenswerten."),
                html.P("• Vielseitige Anwendungen: Polygon unterstützt eine breite Palette von Anwendungsfällen, von DeFi über Spiele bis hin zu NFTs."),
                html.P("• Einfache Integration: Das Polygon-Netzwerk kann von Entwicklern einfach in bestehende Ethereum-basierte Projekte integriert werden."),
                html.P("• Effiziente Tokenisierung: Ermöglicht die einfache Erstellung von benutzerdefinierten Tokens und NFTs."),
                html.P("• Dezentralisiertes Staking: Bietet Staking-Möglichkeiten für MATIC-Inhaber, um am Netzwerk teilzunehmen und Belohnungen zu verdienen."),
                html.P("• Energieeffizienz: Polygon verwendet Proof-of-Stake- und Proof-of-Work-Technologien, um Energieeffizienz zu erreichen."),
                html.P("• Skalierbarkeit für DeFi: Bietet eine Lösung für die Überlastung und hohen Gebühren im DeFi-Sektor auf Ethereum."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("MATIC Problems"),
                html.P(" "),
                html.P("• Netzwerksicherheit: Die Abhängigkeit von Ethereum zur Netzwerksicherheit könnte Herausforderungen mit sich bringen."),
                html.P("• Konkurrenz im Layer-2-Raum: Andere Layer-2-Lösungen konkurrieren mit Polygon um Nutzer und Projekte."),
                html.P("• Zentralisierung der Validatoren: Die Validatoren des Polygon-Netzwerks könnten sich in den Händen weniger großer Akteure konzentrieren."),
                html.P("• Technische Herausforderungen: Die technische Komplexität von Layer-2-Lösungen könnte für Entwickler eine Hürde darstellen."),
                html.P("• Regulierungsunsicherheit: Wie andere Kryptowährungen könnte auch MATIC regulatorischen Veränderungen unterliegen."),
                html.P("• Skalierung der Unterstützung: Obwohl vielseitig, könnte die Unterstützung der wachsenden Zahl von Projekten eine Herausforderung sein."),
                html.P("• Dezentralisierung der Chain: Einige Dezentralisierungsaspekte des Netzwerks könnten hinter anderen Layer-1-Blockchains zurückbleiben."),
                html.P("• Volatile Preisschwankungen: MATIC ist wie andere Kryptowährungen anfällig für starke Preisschwankungen."),
            ]), width=5),
        ]),
    ]),
    "TRX": html.Div([
        html.H1("TRON Page"),
    
        dbc.Row([
            dbc.Col(html.Div("TRX (Tron) ist die Kryptowährung des Tron-Netzwerks, das auf dezentralisierten Anwendungen (dApps) und digitalem Unterhaltungsinhalt basiert. Die TRX-Blockchain verfolgt Transaktionen und verwendet den Delegated Proof-of-Stake (DPoS)-Konsensmechanismus. Tron zielt darauf ab, Inhalte direkt zwischen Künstlern und Nutzern zu verteilen und traditionelle Vermittler zu umgehen. TRX wird für Transaktionen, das Bezahlen von Inhalten und die Unterstützung von dApps verwendet. Tron strebt eine Veränderung der Art und Weise an, wie Inhalte im Internet verteilt werden, indem es die Macht an die Benutzer zurückgibt und die Mittelsmänner reduziert.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'TRX'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("TRX", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("TRX Unique Selling Point"),
                html.P(" "),
                html.P("• Dezentralisiertes Ökosystem: TRON ermöglicht die Erstellung dezentraler Anwendungen (dApps) auf seiner Plattform."),
                html.P("• Hochgeschwindigkeits-Transaktionen: TRON kann eine große Anzahl von Transaktionen pro Sekunde verarbeiten."),
                html.P("• Einfache Tokenisierung: TRON ermöglicht die einfache Erstellung von benutzerdefinierten Tokens und Smart Contracts."),
                html.P("• Inhaltsplattform: TRON bietet Möglichkeiten zur Erstellung, Verteilung und Monetarisierung von digitalen Inhalten."),
                html.P("• Unterstützung für dApps: TRON fördert die Entwicklung und Nutzung dezentraler Anwendungen und Spiele."),
                html.P("• Partnerschaften: TRON hat Partnerschaften mit verschiedenen Unternehmen und Projekten geschlossen."),
                html.P("• Übernahmen: TRON hat bekannte Übernahmen wie BitTorrent getätigt, um das Ökosystem zu erweitern."),
                html.P("• Fokus auf dezentrales Internet: TRON zielt darauf ab, ein dezentralisiertes Internet zu schaffen und Datenkontrolle zurückzugeben."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("TRX Problems"),
                html.P(" "),
                html.P("• Zentralisierungskritik: TRON wurde wegen seiner Zentralisierung und Kontrolle kritisiert."),
                html.P("• Netzwerkkapazität: Hohe Nutzung kann zu Netzwerküberlastung und Skalierungsproblemen führen."),
                html.P("• Technische Kritik: Einige Krypto-Enthusiasten kritisieren TRON's technische Umsetzung und Leistung."),
                html.P("• Abhängigkeit von Justin Sun: Der Gründer Justin Sun spielt eine dominierende Rolle im TRON-Ökosystem."),
                html.P("• Regulierungsunsicherheit: Wie andere Kryptowährungen könnte auch TRX regulatorischen Veränderungen unterliegen."),
                html.P("• Konkurrenz im Smart-Contract-Bereich: TRON konkurriert mit anderen Plattformen wie Ethereum und Binance Smart Chain."),
                html.P("• Mangelnde Dezentralisierung: Die Kontrolle durch wenige große Akteure könnte die Dezentralisierung beeinträchtigen."),
                html.P("• Volatile Preisschwankungen: TRX ist wie andere Kryptowährungen anfällig für starke Preisschwankungen."),
            ]), width=5),
        ]),
    ]),
    "LTC": html.Div([
        html.H1("Litecoin Page"),
    
        dbc.Row([
            dbc.Col(html.Div("LTC (Litecoin) ist eine etablierte Kryptowährung, die auf der Bitcoin-Blockchain-Technologie basiert. Die LTC-Blockchain verfolgt Transaktionen und verwendet ebenfalls den Proof-of-Work (PoW)-Konsensmechanismus. Litecoin wurde als Silber zu Bitcoins Gold konzipiert und bietet schnellere Transaktionsbestätigungen und höhere Transaktionskapazität im Vergleich zu Bitcoin. LTC wird für schnelle Zahlungen und Transfers verwendet und hat sich als Alternative zu traditionellen Zahlungsmethoden etabliert. Obwohl technisch ähnlich wie Bitcoin, bietet Litecoin einige Verbesserungen, die es für den Alltagsgebrauch attraktiv machen.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'LTC'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("LTC", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("LTC Unique Selling Point"),
                html.P(" "),
                html.P("• Frühe Kryptowährung: Als eine der ersten Kryptowährungen genießt Litecoin eine lange Geschichte und breite Anerkennung."),
                html.P("• Schnelle Transaktionen: Litecoin bietet schnellere Transaktionsbestätigungen im Vergleich zu Bitcoin."),
                html.P("• Geringere Gebühren: Die Transaktionsgebühren für Litecoin sind in der Regel niedriger als die von Bitcoin."),
                html.P("• Aktive Entwicklung: Litecoin wird weiterhin aktiv entwickelt und verbessert."),
                html.P("• Liquide Handelspaare: Litecoin ist auf vielen Börsen weit verbreitet und hat hohe Handelsliquidität."),
                html.P("• Einfache Integration: Aufgrund der Ähnlichkeiten mit Bitcoin ist die Integration von Litecoin in bestehende Krypto-Dienste einfach."),
                html.P("• Solider Ruf: Litecoin hat einen stabilen Ruf und wird oft als 'Silber zu Bitcoins Gold' bezeichnet."),
                html.P("• Akzeptanz und Anwendung: Litecoin wird von verschiedenen Händlern und Dienstleistern als Zahlungsmittel akzeptiert."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("LTC Problems"),
                html.P(" "),
                html.P("• Konkurrenz im Zahlungsmittelbereich: Litecoin konkurriert mit anderen Kryptowährungen um die Verwendung als Zahlungsmittel."),
                html.P("• Eingeschränkter Anwendungsfall: Litecoin bietet im Vergleich zu anderen Kryptowährungen begrenztere Anwendungsmöglichkeiten."),
                html.P("• Mangelnde Smart Contract-Fähigkeiten: Im Vergleich zu neueren Plattformen wie Ethereum hat Litecoin begrenzte Smart Contract-Fähigkeiten."),
                html.P("• Abhängigkeit von Bitcoin: Litecoin ist oft an die Preisbewegungen von Bitcoin gekoppelt."),
                html.P("• Technische Weiterentwicklung: Neue technische Entwicklungen könnten dazu führen, dass Litecoin in einigen Aspekten zurückbleibt."),
                html.P("• Regulierungsunsicherheit: Wie andere Kryptowährungen könnte auch LTC regulatorischen Veränderungen unterliegen."),
                html.P("• Volatile Preisschwankungen: Litecoin ist wie andere Kryptowährungen anfällig für starke Preisschwankungen."),
                html.P("• Begrenzter Fokus auf Dezentralisierung: Obwohl dezentralisiert, könnte der Fokus von Litecoin auf praktischen Anwendungsfällen die Dezentralisierung einschränken."),
            ]), width=5),
        ]),
    ]),
    "DOT": html.Div([
        html.H1("Polkadot Page"),
    
        dbc.Row([
            dbc.Col(html.Div("DOT (Polkadot) ist die Kryptowährung des Polkadot-Netzwerks, das Interoperabilität und Skalierbarkeit zwischen verschiedenen Blockchains ermöglicht. Die DOT-Blockchain verfolgt Transaktionen und verwendet den Nominated Proof-of-Stake (NPoS)-Konsensmechanismus. Polkadot zielt darauf ab, verschiedene Ketten miteinander zu verbinden und eine sichere Umgebung für die Entwicklung von Anwendungen zu schaffen. DOT dient als Brücke zwischen verschiedenen Blockchains und ermöglicht den Austausch von Vermögenswerten und Daten. Polkadot fördert Innovation und ermöglicht es Entwicklern, spezialisierte Ketten (Parachains) zu erstellen. Als Multi-Chain-Netzwerk verbessert Polkadot die Flexibilität und Effizienz des Blockchain-Ökosystems.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'DOT'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("DOT", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("DOT Unique Selling Point"),
                html.P(" "),
                html.P("• Interoperabilität: Polkadot ermöglicht die Interaktion verschiedener Blockchains, was den Austausch von Daten und Vermögenswerten erleichtert."),
                html.P("• Parachains und Parathreads: Polkadot verwendet Parachains für spezialisierte Anwendungsfälle und Parathreads für flexible Ressourcennutzung."),
                html.P("• Skalierbarkeit: Polkadot zielt darauf ab, hohe Skalierbarkeit durch die parallele Verarbeitung mehrerer Ketten zu erreichen."),
                html.P("• Sichere Konnektivität: Polkadot nutzt Sicherheitsmechanismen wie Nominated Proof-of-Stake (NPoS) und Cross-Chain-Message Passing (XCMP)."),
                html.P("• Entwicklerfreundlichkeit: Polkadot erleichtert Entwicklern die Erstellung von benutzerdefinierten Ketten und Anwendungen."),
                html.P("• Gemeinschaft und Governance: DOT-Inhaber können an Governance-Entscheidungen teilnehmen und das Netzwerk beeinflussen."),
                html.P("• Innovatives Ökosystem: Polkadot fördert die Schaffung vielfältiger Anwendungen und Projekte durch seine offene Architektur."),
                html.P("• Chain-Upgrades: Das DOT-Netzwerk unterstützt Upgrades ohne harte Gabeln, was eine kontinuierliche Weiterentwicklung ermöglicht."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("DOT Problems"),
                html.P(" "),
                html.P("• Konkurrenz im Interoperabilitätsraum: Polkadot konkurriert mit anderen Plattformen, die Interoperabilität anbieten."),
                html.P("• Technische Komplexität: Die Komplexität von Polkadot könnte für Entwickler und Nutzer eine Hürde sein."),
                html.P("• Frühes Entwicklungsstadium: Obwohl vielversprechend, befindet sich das Polkadot-Netzwerk noch in der Entwicklungsphase."),
                html.P("• Risiko von Parachain-Abhängigkeit: Die Abhängigkeit von spezialisierten Parachains könnte Risiken für das Gesamtnetzwerk darstellen."),
                html.P("• Regulierungsunsicherheit: Wie andere Kryptowährungen könnte auch DOT regulatorischen Veränderungen unterliegen."),
                html.P("• Herausforderungen bei Governance: Die dezentrale Governance von Polkadot könnte Herausforderungen bei Entscheidungsprozessen mit sich bringen."),
                html.P("• Abhängigkeit von Entwickleraktivität: Der Erfolg von Polkadot hängt von der fortlaufenden Entwicklung und Unterstützung ab."),
                html.P("• Volatile Preisschwankungen: DOT ist wie andere Kryptowährungen anfällig für starke Preisschwankungen."),
            ]), width=5),
        ]),
    ]),
    "TON": html.Div([
        html.H1("Toncoin Page"),
    
        dbc.Row([
            dbc.Col(html.Div("Toncoin (TON) ist eine dezentrale Layer-1-Blockchain, die 2018 von der verschlüsselten Messaging-Plattform Telegram entwickelt wurde. Die Blockchain von TON verwendet einen Proof-of-Stake (PoS) Konsensmechanismus, bei dem Validatoren zur Verifizierung von Transaktionen und zum Erhalt von Belohnungen TON Token staken müssen. TON wird für Netzwerkoperationen, Transaktionen, Spiele und Sammlerstücke verwendet, die auf TON basieren. Toncoin hat das Potenzial, eine wichtige Rolle in der DeFi- und NFT-Industrie zu spielen.")),
        ]),
    
    
        dbc.Row([
            dbc.Col(dcc.Graph(figure=px.line(df[df['Coin'] == 'TON'], x='Timestamp', y='Price')), width=12),
        ]),
    
    
        dbc.Row([
            dbc.Col(html.Div([
                create_kpis("TON", latest_date),  
            ]), width=3),
            dbc.Col(html.Div([
                html.H3("TON Unique Selling Point"),
                html.P(" "),
                html.P("• Skalierbarkeit: TON ist eine skalierbare Blockchain, die große Transaktionsvolumina verarbeiten kann."),
                html.P("• Geschwindigkeit: TON-Transaktionen sind schnell und kostengünstig."),
                html.P("• Sicherheit: TON ist eine sichere Blockchain, die durch eine Reihe von Sicherheitsmaßnahmen geschützt ist."),
                html.P("• Privatsphäre: TON bietet Privatsphäreoptionen für Nutzer, die ihre Transaktionen vor Dritten verbergen möchten."),
                html.P("• Interoperabilität: TON ist mit anderen Blockchains und Zahlungssystemen kompatibel."),
                html.P("• Innovation: TON ist eine innovative Blockchain, die neue Funktionen und Anwendungen bietet."),
                html.P("• Community: TON hat eine aktive und engagierte Community von Entwicklern und Nutzern."),
            ]), width=4),
            dbc.Col(html.Div([
                html.H3("TON Problems"),
                html.P(" "),
                html.P("• Konkurrenz: TON konkurriert mit anderen Kryptowährungen und Blockchain-Plattformen."),
                html.P("• Regulation: TON könnte regulatorischen Beschränkungen unterliegen."),
                html.P("• Stabilität: TON ist noch in der Entwicklung und es ist unklar, wie stabil die Plattform sein wird."),
                html.P("• Kompatibilität: Es ist unklar, wie gut TON mit anderen Blockchains und Zahlungssystemen kompatibel sein wird."),
                html.P("• Akzeptanz: Es ist unklar, wie weit TON von Unternehmen und Nutzern akzeptiert wird."),
            ]), width=5),
        ]),
    ]),
  
}

# Styling für die Seitenleiste
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Styling für den Seiteninhalt
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Seitenleisteninhalt
sidebar = html.Div(
    [
        html.H2("Cryptoanalyse", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=encoded_logos[logo], height="30px"), width="auto"),
                            dbc.Col(logo_text, width="auto"),
                        ],
                        align="center",
                    ),
                    href=f"/{logo.lower()}",
                    id=f"{logo.lower()}-link",
                    active="exact",
                )
                for logo, logo_text in zip(logos, logo_texts)
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Seiteninhalt
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# App-Layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    [Output(f"{logo.lower()}-link", "active") for logo in logos] + [Output("page-content", "children")],
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    coin = pathname.strip("/").upper()
    page_layout = page_layouts.get(coin, None)
    
    active_links = [pathname == f"/{logo.lower()}" for logo in logos]
    
    if page_layout is None:
        return active_links + [html.P("Invalid page selected.")]
    
    if coin == "BTC":
        return active_links + [page_layouts["BTC"]]
    
    return active_links + [page_layout]

if __name__ == '__main__':
    app.run_server(debug=True)