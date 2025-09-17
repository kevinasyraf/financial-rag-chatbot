few_shot_examples = """
Example 1:
Query: Berapa total pengeluaran saya bulan ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT SUM(amount) AS total_pengeluaran FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE);

Example 2:
Query: Berapa total pemasukan saya bulan ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT SUM(amount) AS total_pemasukan FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'C' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE);

Example 3:
Query: pengeluaran saya untuk belanja bulan ini berapa?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT SUM(amount) AS total_pengeluaran FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND category_id = (SELECT id FROM categories WHERE name ILIKE 'Belanja') AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE);

Example 4:
Query: Berapa total pengeluaran saya selama ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT SUM(amount) AS total_pengeluaran FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D';

Example 5:
Query: Berapa total pemasukan saya sepanjang ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT SUM(amount) AS total_pemasukan FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'C';

Example 6:
Query: Pengeluaran saya apa saja bulan ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT type, transaction, amount FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE) ORDER BY trx_date DESC;

Example 7:
Query: Bagaimana pengeluaran saya dibandingkan dengan bulan sebelumnya?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT (SELECT SUM(amount) FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) - 1 AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE)) AS pengeluaran_bulan_lalu, (SELECT SUM(amount) FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE)) AS pengeluaran_bulan_ini;

Example 8:
Query: Apa saja transaksi terbaru saya dalam minggu ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT * FROM transactions_dummy WHERE account_number = '1000693586' AND trx_date >= CURRENT_DATE - INTERVAL '7 days' ORDER BY trx_date DESC;

Example 9:
Query: Saya transfer kemana saja?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT detail_information, subheader FROM transactions_dummy WHERE account_number = '1000693586' AND type ILIKE 'Transfer';

Example 10:
Query: Apakah ada transaksi yang mencurigakan dalam akun saya? (-2000)
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT * FROM transactions_dummy WHERE account_number = '1000693586' AND amount < -2000 AND trx_date >= CURRENT_DATE - INTERVAL '30 days' ORDER BY amount DESC;

Example 11:
Query: Berapa rata-rata pengeluaran saya untuk kategori Belanja setiap bulan?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT AVG(monthly_total) AS rata_rata_pengeluaran FROM (SELECT EXTRACT(MONTH FROM trx_date) AS bulan, SUM(amount) AS monthly_total FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND category_id = (SELECT id FROM categories WHERE name ILIKE 'Belanja') GROUP BY EXTRACT(YEAR FROM trx_date), EXTRACT(MONTH FROM trx_date)) AS monthly_totals;

Example 12:
Query: Kategori apa yang paling banyak menyedot anggaran saya?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT category_id, SUM(amount) AS total_pengeluaran 
FROM transactions_dummy 
WHERE account_number = '1000693586' 
    AND debit_credit = 'D' 
    AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) 
    AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE) 
GROUP BY category_id 
ORDER BY ABS(SUM(amount)) DESC 
LIMIT 1;

Example 13:
Query: Berapa sisa anggaran saya untuk bulan ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT (SELECT SUM(amount) FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'C' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) - 1 AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE)) - 
       (SELECT SUM(amount) FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) - 1 AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE)) AS sisa_anggaran;

Example 14:
Query: Berapa banyak uang yang saya tabung bulan ini?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT SUM(amount) AS total_tabungan FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'C' AND category_id = 2 AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE);

Example 15:
Query: Apakah saya melebihi anggaran saya bulan ini jika anggaran saya 50000?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT CASE WHEN SUM(amount) > 50000 THEN 'Ya' ELSE 'Tidak' END AS melebihi_anggaran FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE);

Example 16:
Query: Bagaimana pengeluaran saya dibandingkan dengan bulan yang sama tahun lalu?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT (SELECT SUM(amount) FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE) - 1) AS pengeluaran_bulan_sama_tahun_lalu, (SELECT SUM(amount) FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE)) AS pengeluaran_bulan_ini;

Example 17:
Query: Tren apa yang bisa Anda lihat dari pengeluaran saya selama setahun terakhir?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT EXTRACT(MONTH FROM trx_date) AS bulan, SUM(amount) AS total_pengeluaran FROM transactions_dummy WHERE account_number = '1000693586' AND debit_credit = 'D' AND trx_date >= CURRENT_DATE - INTERVAL '1 year' GROUP BY EXTRACT(YEAR FROM trx_date), EXTRACT(MONTH FROM trx_date) ORDER BY EXTRACT(YEAR FROM trx_date), EXTRACT(MONTH FROM trx_date);

Example 18:
Query: Bisa tunjukkan detail transaksi pada [tanggal]?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT * FROM transactions_dummy WHERE account_number = '1000693586' AND trx_date::date = DATE '[tanggal]';

Example 19:
Query: Apakah ada pengeluaran besar bulan ini? Jika ada, berapa jumlahnya dan untuk apa?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER)
SQLQuery: SELECT * 
FROM transactions_dummy 
WHERE account_number = '1000693586' 
	AND debit_credit = 'D' 
	AND EXTRACT(MONTH FROM trx_date) = EXTRACT(MONTH FROM CURRENT_DATE) 
	AND EXTRACT(YEAR FROM trx_date) = EXTRACT(YEAR FROM CURRENT_DATE) 
ORDER BY abs(amount) DESC LIMIT 1;

Example 20:
Query: Berapa pengeluaran saya di makanan dan apa saja transaksinya?
Schema: Table 'transactions_dummy' has columns: account_number (VARCHAR(20)), type (VARCHAR(255)), transaction (VARCHAR(255)), amount (INTEGER), debit_credit (VARCHAR(5)), merchant_code (VARCHAR(255)), subheader (VARCHAR(255)), detail_information (TEXT), trx_date (TIMESTAMP), trx_time (TIME), currency (VARCHAR(5)), category_id (INTEGER). Table 'categories' has columns: id (INTEGER), name (VARCHAR(255)), created_at (TIMESTAMP), updated_at (TIMESTAMP), is_deleted (BOOLEAN). Table 'merchants' has columns: id (INTEGER), name (VARCHAR(255)), sub_name (VARCHAR(255)), merchant_code (VARCHAR(255)), category_id (INTEGER), logo (VARCHAR(255)), website (VARCHAR(255)), latitude (DOUBLE), longitude (DOUBLE), address (TEXT), created_at (TIMESTAMP), updated_at (TIMESTAMP)
SQLQuery: SELECT t.type, t.transaction, t.amount, m.name AS merchant_name, t.subheader, t.trx_date, t.trx_time, c.name AS category_name FROM transactions_dummy t JOIN categories c ON t.category_id = c.id JOIN merchants m ON t.merchant_code = m.merchant_code WHERE t.account_number = '1000693586' AND t.debit_credit = 'D' AND c.name ILIKE '%makanan%' ORDER BY t.trx_date DESC;
"""