from scripts.run_etl import run_etl_pipline

data = None


def main():
    print("App pipeline run successfully")
    try:
        data = run_etl_pipline()
    except Exception as e:
        print(f"An error occurred: {e}")
    return data


# Test driven development to check if it can call the extract function
if __name__ == "__main__":
    main()