def count_remaining_values(var, assignment, csp):
    """
    Menghitung jumlah nilai domain yang konsisten (Remaining Values) untuk variabel yang belum ditetapkan (var).
    Memeriksa setiap nilai domain terhadap semua constraint menggunakan fungsi is_consistent().
    """
    count = 0
    # Mengambil daftar nilai domain yang mungkin untuk variabel 'var'
    for value in csp['domain'][var]:
        # Menggunakan is_consistent untuk memverifikasi apakah nilai tersebut valid
        if is_consistent(var, value, assignment, csp):
            count += 1
    return count


def get_degree(var, unassigned_vars, csp):
    """
    Degree Heuristic: Menghitung jumlah constraint BINER ('provinsi_constraint') yang melibatkan 'var'
    dengan variabel lain yang masih berada di dalam list 'unassigned_vars'.
    """
    count = 0
    # Hanya fokus pada constraint biner antar-variabel (Provinsi)
    for constraint in csp['constraints']:
        if constraint[0] == 'provinsi_constraint':
            _, v1, v2, _ = constraint

            # Cek apakah 'var' terlibat dengan variabel lain yang belum ditetapkan
            if var == v1 and v2 in unassigned_vars:
                count += 1
            elif var == v2 and v1 in unassigned_vars:
                count += 1
    return count


def select_unassigned_variable(assignment, csp):
    """
    Selects the next unassigned variable using MRV (Minimum Remaining Values)
    with Degree Heuristic as a tie-breaker.
    """
    unassigned_vars = [var for var in csp['variables'] if var not in assignment]

    if not unassigned_vars:
        return None

    # 1. Hitung dan Cache MRV Counts (Efisiensi)
    mrv_counts = {var: count_remaining_values(var, assignment, csp) for var in unassigned_vars}

    # 2. Terapkan MRV: Cari variabel dengan nilai sisa minimum
    min_mrv = min(mrv_counts.values())
    mrv_candidates = [var for var, count in mrv_counts.items() if count == min_mrv]

    if len(mrv_candidates) == 1:
        # Tidak ada ikatan
        return mrv_candidates[0]

    # 3. Terapkan Degree Heuristic (Pemutus Ikatan)
    # Pilih dari kandidat MRV, variabel dengan degree maksimum.
    return max(mrv_candidates, key=lambda var: get_degree(var, unassigned_vars, csp))

