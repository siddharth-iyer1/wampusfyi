# visualizations.py
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from app.config import TABLE_ID, bigquery_client


def price_over_time(name, beds, baths):
    try:
        beds = int(beds)
        baths = int(baths)
    except:
        return
    # GCP Big Query Client, Pull Data
    apt_rows = bigquery_client.list_rows(TABLE_ID)
    apt_df = apt_rows.to_dataframe()

    # Variables for filtering
    form_apt = "Where_are_you_living_this_year_"
    form_beds = "How_many_bedrooms_in_your_apt"
    form_baths = "How_many_bathrooms_in_your_apt"
    form_sign_date = "When_did_you_sign_your_lease___Approximations_are_cool__P_"
    form_price = "How_much_do_you_pay_monthly_just_for_the_apartment_"

    # X-Axis: Holds dates, Y-Axis: Holds prices
    dates = []
    prices = []

    # Iterate through each row in apt_df
    for index, row in apt_df.iterrows():
        if row[form_apt] == name and row[form_beds] == beds and row[form_baths] == baths:
            dates.append(row[form_sign_date])
            prices.append(row[form_price])

    # Set seaborn style
    sns.set_style("darkgrid")

    # Sorting data based on dates for a chronological plot
    sorted_indices = sorted(range(len(dates)), key=lambda k: dates[k])
    dates = [dates[i] for i in sorted_indices]
    prices = [prices[i] for i in sorted_indices]

    # Create the chart
    plt.figure(figsize=(12,7))

    # Plot data
    sns.lineplot(x=dates, y=prices, marker='o', color='#cc5500', linewidth=2.5, markersize=10)

    # Titles and labels
    plt.xlabel("Lease Sign Date", fontsize=15, labelpad=15)
    plt.ylabel("Monthly Rate", fontsize=15, labelpad=15)

    # Improve x-ticks visibility
    plt.gcf().autofmt_xdate()

    # Return the plot
    return plt