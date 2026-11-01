
from database import create_patient, get_all_patients

# Original assessment records
# Keep the original values so validation issues can be demonstrated.
records = [
    {
        "full_name": "Robyn Pears",
        "date_of_birth": "28.01.1960",
        "email": "robyn@gmail.com",
        "glucose": 232,
        "haemoglobin": 13.5,
        "cholesterol": 180
    },
    {
        "full_name": "John Hunter",
        "date_of_birth": "10.12.1990",
        "email": "hunter@gmail",
        "glucose": 94,
        "haemoglobin": 15,
        "cholesterol": 200
    },
    {
        "full_name": "Darryl Tim",
        "date_of_birth": "12.11.1993",
        "email": "timd@smh.com.au",
        "glucose": 240,
        "haemoglobin": 18.6,
        "cholesterol": 326
    },
    {
        "full_name": "Peter Larry",
        "date_of_birth": "31.11.2001",
        "email": "Larry@hotmail.com",
        "glucose": 88,
        "haemoglobin": 11.5,
        "cholesterol": 165
    },
    {
        "full_name": "Sam Kerr",
        "date_of_birth": "09.12.2006",
        "email": "sam@news.com.au",
        "glucose": 198,
        "haemoglobin": 8.9,
        "cholesterol": 192
    },
    {
        "full_name": "Robyn Pears",
        "date_of_birth": "28.01.1960",
        "email": "robyn@gmail.com",
        "glucose": 232,
        "haemoglobin": 13.5,
        "cholesterol": 180
    },
    {
        "full_name": "Madison XI",
        "date_of_birth": "12.09.1998",
        "email": "madison@hotmail.com",
        "glucose": 85,
        "haemoglobin": 7.6,
        "cholesterol": 163
    },
    {
        "full_name": "Kris Wu",
        "date_of_birth": "19.10.2030",
        "email": "Kris.wu.gmail.com",
        "glucose": 79,
        "haemoglobin": 16.5,
        "cholesterol": 197
    },
    {
        "full_name": "Tenille Singh",
        "date_of_birth": "30.11.1991",
        "email": "Tenille@yahoo.com",
        "glucose": 101,
        "haemoglobin": 15,
        "cholesterol": 310
    },
    {
        "full_name": "Prem Kumar",
        "date_of_birth": "28.04.1990",
        "email": "prem@telstra.com",
        "glucose": 155,
        "haemoglobin": 12.5,
        "cholesterol": 265
    }
]

print("Assessment records prepared:", len(records))
print("Original records preserved.")
print("No database records have been inserted yet.")

if __name__ == "__main__":
    existing_patients = get_all_patients()

    if existing_patients:
        print("Import cancelled: the database is not empty.")
        print("Please check existing records before importing.")
    else:
        print("\nStarting assessment data import...\n")

        for record in records:
            patient_id = create_patient(record)
            print(f"Imported: {record['full_name']} (ID: {patient_id})")

        print("\nImport completed!")
        print("Total records imported:", len(records))
