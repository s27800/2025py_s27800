from Bio import Entrez, SeqIO
import pandas as pd
import matplotlib.pyplot as plt
import time
class NCBIRetriever:
    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key
        Entrez.email = email
        Entrez.api_key = api_key
        Entrez.tool = 'GenBankRetriever'
    def search_taxid(self, taxid):
        print(f"Searching for records with taxID: {taxid}")
        try:
            handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")
            records = Entrez.read(handle)
            organism_name = records[0]["ScientificName"]
            print(f"Organism: {organism_name} (TaxID: {taxid})")

            search_term = f"txid{taxid}[Organism]"
            handle = Entrez.esearch(db="nucleotide", term=search_term, usehistory="y")
            search_results = Entrez.read(handle)
            count = int(search_results["Count"])

            if count == 0:
                print("No records found.")
                return None

            print(f"Found {count} records")
            self.webenv = search_results["WebEnv"]
            self.query_key = search_results["QueryKey"]
            self.count = count

            return count
        except Exception as e:
            print(f"Error during search: {e}")
            return None

    def fetch_all_records(self, min_len, max_len, batch_size=100):
        print("Fetching and filtering records...")
        all_data = []
        for start in range(0, self.count, batch_size):
            try:
                print(f"Fetching records {start + 1} to {start + batch_size}")
                handle = Entrez.efetch(
                    db="nucleotide",
                    rettype="gb",
                    retmode="text",
                    retstart=start,
                    retmax=batch_size,
                    webenv=self.webenv,
                    query_key=self.query_key
                )
                records = SeqIO.parse(handle, "genbank")
                for record in records:
                    seq_len = len(record.seq)
                    if min_len <= seq_len <= max_len:
                        all_data.append({
                            "accession": record.id,
                            "length": seq_len,
                            "description": record.description
                        })
                time.sleep(0.4)  # avoid overloading NCBI
            except Exception as e:
                print(f"Error fetching batch starting at {start}: {e}")
                continue
        print(f"Total records after filtering: {len(all_data)}")
        return all_data

    def generate_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Saved CSV report to {filename}")

    def generate_plot(self, data, filename):
        df = pd.DataFrame(data)
        df = df.sort_values(by="length", ascending=False)
        plt.figure(figsize=(12, 6))
        plt.plot(df["accession"], df["length"], marker='o')
        plt.xticks(rotation=90, fontsize=6)
        plt.title("Sequence Lengths by Accession Number")
        plt.xlabel("Accession Number")
        plt.ylabel("Sequence Length (bp)")
        plt.tight_layout()
        plt.savefig(filename)
        print(f"Saved plot to {filename}")


def main():
    email = input("Enter your email for NCBI: ").strip()
    api_key = input("Enter your NCBI API key: ").strip()
    taxid = input("Enter the taxonomic ID (taxid) of the organism: ").strip()

    try:
        min_len = int(input("Enter minimum sequence length to include: ").strip())
        max_len = int(input("Enter maximum sequence length to include: ").strip())
    except ValueError:
        print("Invalid length input. Must be integers.")
        return

    retriever = NCBIRetriever(email, api_key)
    count = retriever.search_taxid(taxid)

    if not count:
        return

    records = retriever.fetch_all_records(min_len, max_len)

    if not records:
        print("No records found after filtering by length.")
        return

    csv_filename = f"taxid_{taxid}_filtered_sequences.csv"
    retriever.generate_csv(records, csv_filename)

    plot_filename = f"taxid_{taxid}_length_plot.png"
    retriever.generate_plot(records, plot_filename)

if __name__ == "__main__":
    main()