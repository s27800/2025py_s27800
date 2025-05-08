# Cel programu: Tworzenie losowej sekwencji w formacie fasta o zadanej długości
# Kontekst zastosowania: edukacja biologiczna, testy bioinformatyczne, demonstracja działania formatu FASTA

import random #importowanie modułu random

def generate_dna_sequence(length): #definicja funkcji generującej losową sekwencje
    return ''.join(random.choices('ACGT', k=length)) #tworzenie losowej sekwencji o długości length i zwrócenie jej

def insert_name(sequence, name): #definicja funkcji wstawiającej imię w losowy miejscu sekwencji
    insert_pos = random.randint(0, len(sequence)) #losowanie liczby z zakresu 0 do długości sekwencji
    return sequence[:insert_pos] + name + sequence[insert_pos:] # wstawienie imienia w miejsce które zostało wylosowane w poprzedniej linii i zwrócenie sekwencji

def calculate_statistics(sequence): #definicja funkcji obliczającej statystyki
    dna_only = ''.join([n for n in sequence if n in 'ACGT']) #przepisanie z sekwencji tylko liter symbolizujących nukleotydy (usunięcie znaków niebędących nukleotydami)
    total = len(dna_only) #zapisanie długości poprawionej sekwencji do zmiennej total
    counts = {nucleotide: dna_only.count(nucleotide) for nucleotide in 'ACGT'} #zapisanie do zmiennej counts ilości nukleotydów występujących w sekwencji gdzie dla znaku nukleotydu przypisana jest ilość jego wystąpień w sekwencji
    percentages = {n: (counts[n] / total * 100) for n in 'ACGT'} # zapisanie procentów wystąpień poszczególnych znaków do zmiennej percentages
    cg = counts['C'] + counts['G'] #wyliczenie sumy wystąpień C i G i zapisanie do zmiennej cg
    at = counts['A'] + counts['T'] #wyliczenie sumy wystąpień A i T i zapisanie do zmiennej at
    cg_ratio = (cg / total * 100) if total > 0 else 0 #wyliczenie proporcji wystąpień C i G do wszystkich nukleotydów
    # ORIGINAL
    # return percentages, round(cg_ratio, 2)
    # MODIFIED (dodanie możliwości wyświetlenia at_ratio)
    at_ratio = (at / total * 100) if total > 0 else 0 #wyliczenie proporcji wystąpień A i T do wszystkich nukleotydów
    return percentages, round(cg_ratio, 2), round(at_ratio, 2) #zwrócenie wyliczonych statystyk

def main(): #definicja głównej funkcji main
    try: #oznaczenie modułu który będzie próbował się wykonać i przejdzie do sekcji exception jak wystąpi w środku błąd
        length = int(input("Podaj długość sekwencji: ")) #zapytanie uzytkownika o podanie długości sekwencji dna
        if length <= 0: #sprawdzenie czy podana przez użytkownika długość sekwencji jest większa niż 0
            raise ValueError #zgłoszenie wyjątku
    except ValueError: #oznaczenie co ma się wydarzyć jak wystąpi błąd
        print("Długość musi być dodatnią liczbą całkowitą.") #wypisanie informacji o wystąpieniu błędu
        return #zakończenie wykonania

    seq_id = input("Podaj ID sekwencji: ").strip() #pytanie użytkownika o id sekwencji i zapis do zmiennej
    description = input("Podaj opis sekwencji: ").strip() #pytanie użytkownika o opis sekwencji i zapis do zmiennej
    name = input("Podaj imię: ").strip() #pytanie użytkownika o imie i zapis do zmiennej

    dna_seq = generate_dna_sequence(length) #przypisanie sekwencji bez imienia do zmiennej
    full_seq = insert_name(dna_seq, name) #przypisanie do zmiennej sekwencje wraz z imieniem

    filename = f"{seq_id}.fasta" #przypisanie do zmiennej ścieżki do pliku do zapisu sekwencji
    with open(filename, 'w') as f: #otworzenie pliku do zapisu sekwencji
        f.write(f">{seq_id} {description}\n") #zapis id i opisu sekwencji do pliku
        # ORIGINAL
        # f.write(full_seq + "\n")
        # MODIFIED (dodanie zawijania tekstu co 50 znaków)
        for i in range(0, len(full_seq), 50): #kursor przechodzący po kolejnych wartościach od znaku 0 do ostatniego znaku sekwencji
            f.write(full_seq[i:i + 50] + '\n') #zapis znaków sekwencji do pliku (po max 50 w linii)

    print(f"\nSekwencja została zapisana do pliku {filename}") #wypisanie informacji o zapisie sekwencji do pliku

    # ORIGINAL
    # percentages, cg_ratio = calculate_statistics(full_seq)
    # MODIFIED (dodanie możliwości wyświetlenia at_ratio)
    percentages, cg_ratio, at_ratio = calculate_statistics(full_seq) #przypisanie wyliczonych statystyk w funkcji do zmiennych

    # ORIGINAL
    #
    # MODIFIED (dodanie zapisu statystyk do pliku)
    filename = f"{seq_id}_statistics.txt" #zapis ścieżki do pliku do zapisu statystyk
    with open(filename, 'w') as f: #otworzenie pliku do zapisu statystyk
        f.write(f"Statystyki: A: {percentages['A']:.1f}%, C: {percentages['C']:.1f}%, "f"G: {percentages['G']:.1f}%, T: {percentages['T']:.1f}%, %CG: {cg_ratio}\n, %AT: {at_ratio}\n") #zapis statystyk do pliku
    print(f"Statystyki sekwencji zostały zapisane do pliku {filename}\n") #wypisanie informacji o zapisie statystyk do pliku

    print("Statystyki sekwencji:") #wypisanie zdania Statystyki sekwencji:
    for n in 'ACGT': #wybór kolejnych znaków nukleotydów spośród ACGT
        print(f"{n}: {percentages[n]:.1f}%") # wypisanie procentu wystąpienia wybranego nukleotydu

    # ORIGINAL
    # print(f"%CG: {cg_ratio}")
    # MODIFIED (dodanie możliwości wyświetlenia at_ratio)
    print(f"%CG: {cg_ratio}") #wypisanie proporcji cg_ratio
    print(f"%AT: {at_ratio}") #wypisanie proporcji at_ratio


if __name__ == "__main__": #start programu
    main() #wywołanie głównej funkcji main
