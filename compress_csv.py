import pandas as pd

# Load your large CSV file
df = pd.read_csv("cleaned_skincare_products.csv")

# Print dataset info
print("✅ Original Data Loaded")
print(df.info())  # Shows dataset details (rows, columns)

# Save as a compressed GZIP file
df.to_csv("cleaned_skincare_products.csv.gz", index=False, compression="gzip")

print("✅ CSV compressed successfully! New file: cleaned_skincare_products.csv.gz")
