from scripts.run_etl import return_data


def main():
    print("App pipeline run successfully")

# Test driven development to check if it can call the extract function


try:
    data = return_data()
except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()