import argparse
import duckdb
import os


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", required=True)
    p.add_argument("--out", default="artifacts/bases.duckdb")
    args = p.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    con = duckdb.connect(args.out)
    con.execute("PRAGMA disable_progress_bar;")

    base_products = os.path.join(args.data_dir, "base_products.parquet")

    con.execute(
        f"""
        CREATE OR REPLACE TABLE bases_core AS
        SELECT
          random_key,
          persian_name,
          english_name,
          category_id,
          brand_id
        FROM read_parquet('{base_products}')
        """
    )

    con.close()
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()


