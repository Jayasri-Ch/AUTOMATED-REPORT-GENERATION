import csv
import matplotlib.pyplot as plt
from fpdf import FPDF
import os  # For opening the PDF

# Analyze CSV data and prepare summary stats
def analyze_data(file_path):
    data = []
    stats = {
        "credit": 0,
        "debit": 0,
        "chip_yes": 0,
        "chip_no": 0,
        "darkweb_yes": 0,
        "darkweb_no": 0,
        "credit_limit_total": 0,
        "total_cards": 0
    }

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
            stats["total_cards"] += 1

            card_type = row['card_type'].strip().lower()
            if card_type == 'credit':
                stats["credit"] += 1
            elif card_type == 'debit':
                stats["debit"] += 1

            chip = row['has_chip'].strip().lower()
            if chip == 'yes':
                stats["chip_yes"] += 1
            else:
                stats["chip_no"] += 1

            dark_web = row['card_on_dark_web'].strip().lower()
            if dark_web == 'yes':
                stats["darkweb_yes"] += 1
            else:
                stats["darkweb_no"] += 1

            try:
                limit = float(row['credit_limit'].replace('$', '').replace(',', '').strip())
                stats["credit_limit_total"] += limit
            except:
                pass

    if stats["total_cards"]:
        stats["average_credit_limit"] = stats["credit_limit_total"] / stats["total_cards"]
    else:
        stats["average_credit_limit"] = 0

    return data, stats

# Create a bar chart and save it as an image
def create_chart(stats, filename='summary_chart.png'):
    labels = ['Credit Cards', 'Debit Cards', 'With Chip', 'No Chip', 'Dark Web', 'Safe']
    values = [
        stats["credit"], stats["debit"],
        stats["chip_yes"], stats["chip_no"],
        stats["darkweb_yes"], stats["darkweb_no"]
    ]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color='#1f77b4', edgecolor='black')  # Add border
    plt.title('Card Summary Overview')
    plt.ylabel('Number of Cards')
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center')

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Generate PDF report
def generate_pdf_report(stats, chart_image, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Card Summary Report', ln=True, align='C', border=1)
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    # Summary table with borders
    items = [
        ("Total Cards", stats["total_cards"]),
        ("Credit Cards", stats["credit"]),
        ("Debit Cards", stats["debit"]),
        ("Cards With Chip", stats["chip_yes"]),
        ("Cards Without Chip", stats["chip_no"]),
        ("Cards Found on Dark Web", stats["darkweb_yes"]),
        ("Safe Cards", stats["darkweb_no"]),
        ("Average Credit Limit", f"${stats['average_credit_limit']:.2f}")
    ]

    for label, value in items:
        pdf.cell(90, 8, label, border=1)
        pdf.cell(100, 8, str(value), ln=True, border=1)

    # Add more space before the chart (increase the number to adjust space)
    pdf.ln(20)  # Added 20mm space

    # Insert chart image
    pdf.image(chart_image, x=10, y=pdf.get_y(), w=180)

    pdf.output(output_path)

# Main function
def main():
    input_file = 'C:/Users/Sri/Contacts/Downloads/cards_data.csv'
    output_pdf = 'card_summary_report.pdf'
    chart_file = 'summary_chart.png'

    data, stats = analyze_data(input_file)
    create_chart(stats, chart_file)
    generate_pdf_report(stats, chart_file, output_pdf)

    print(f"✅ PDF with chart and summary created: {output_pdf}")

    # Auto-open the PDF file
    try:
        os.startfile(output_pdf)  # Works on Windows
    except AttributeError:
        # For macOS and Linux
        import subprocess
        subprocess.call(['open' if os.name == 'posix' else 'xdg-open', output_pdf])

if __name__ == '__main__':
    main()
