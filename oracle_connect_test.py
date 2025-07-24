import oracledb

# Credentials
username = "system"
password = "123456789"
dsn = "localhost/XE"  # Change this if your service name is different

# Connect
try:
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()

    # Run a test query
    cursor.execute("SELECT * FROM publications_by_year")
    for row in cursor:
        print(row)

    cursor.close()
    connection.close()
except Exception as e:
    print("❌ Error:", e)


import pandas as pd
import matplotlib.pyplot as plt
import oracledb

conn = oracledb.connect(user="system", password="123456789", dsn="localhost/XE")

#Bar chart 

df4 = pd.read_sql("SELECT * FROM publications_by_year", con=conn)
print("Publications by Year Data:\n", df4)
if not df4.empty:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(df4['PUBLICATION_YEAR'], df4['PUBLICATION_COUNT'], color=['#FF9999', '#66B2FF', '#99FF99'], edgecolor='black')
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            int(bar.get_height()), ha='center', fontsize=10)
        plt.xlabel("Year")
        plt.ylabel("Number of Publications")
        plt.title("Publications by Year (2021-2023)")
        plt.xticks(df4['PUBLICATION_YEAR'])  # Ensure all years are labeled
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
else:
        print("No publications found by year.")


#Faculty-wise Total Publications
df2 = pd.read_sql("SELECT * FROM top_contributing_faculty", con=conn)
print(df2.columns)
plt.figure(figsize=(10,6))
plt.barh(df2['FACULTY_NAME'], df2['TOTAL_PUBLICATIONS'], color=['#FF9999', '#66B2FF', '#99FF99'])
plt.xlabel("Total Publications")
plt.ylabel("Faculty Name")
plt.title("Top Contributing Faculty")
plt.tight_layout()
plt.show()

# Publications by Category (Top 5 Approach)
df = pd.read_sql("""
    SELECT category, COUNT(*) AS count
    FROM publication
    GROUP BY category
    ORDER BY count DESC
    FETCH FIRST 5 ROWS WITH TIES
""", con=conn)
print(df.columns)
plt.figure(figsize=(8, 8))
plt.pie(df['COUNT'], labels=df['CATEGORY'], autopct='%1.1f%%', startangle=140)
plt.title("Publications by Category")
plt.axis('equal')
plt.show()

# Donut Chart – Publications by Type (Journal/Conference/Workshop)

df3 = pd.read_sql("""
    SELECT publication_type, COUNT(*) AS count 
    FROM publication 
    GROUP BY publication_type
""", con=conn)

labels = df3['PUBLICATION_TYPE']
sizes = df3['COUNT']
colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974']

fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops=dict(width=0.4),
    textprops={'fontsize': 12},
    colors=colors[:len(sizes)],
    pctdistance=0.75,      
    labeldistance=1.1     
)


for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_weight('bold')
    autotext.set_fontsize(11)

total = sum(sizes)
ax.text(0, 0, f'Total\n{total}', ha='center', va='center', fontsize=14, weight='bold')
ax.set_title("Publication Type Distribution (Journal vs Conference etc.)", fontsize=14, pad=20)
ax.axis('equal')

plt.tight_layout()
plt.show()

conn.close()
