# 📥 UNSW-NB15 Dataset Download Guide

## Quick Links

**Official Website:**  
https://research.unsw.edu.au/projects/unsw-nb15-dataset

**Direct Download Links:**  
- Training Set: https://cloudstor.aarnet.edu.au/plus/s/2DhnLGDdEECo4ys/download?path=%2FUNSW-NB15%20-%20CSV%20Files&files=UNSW-NB15_1.csv
- Testing Set: https://cloudstor.aarnet.edu.au/plus/s/2DhnLGDdEECo4ys/download?path=%2FUNSW-NB15%20-%20CSV%20Files&files=UNSW-NB15_2.csv

---

## Step-by-Step Download

### Method 1: Official Website (Recommended)

1. **Visit the official page:**
   ```
   https://research.unsw.edu.au/projects/unsw-nb15-dataset
   ```

2. **Scroll to "Download" section**

3. **Download these files:**
   - `UNSW_NB15_training-set.csv` (~56 MB)
   - `UNSW_NB15_testing-set.csv` (~27 MB)

4. **Place files in:**
   ```
   backend/datasets/UNSW_NB15_training-set.csv
   backend/datasets/UNSW_NB15_testing-set.csv
   ```

### Method 2: CloudStor (Alternative)

If the official site is down, use CloudStor:

1. Visit: https://cloudstor.aarnet.edu.au/plus/s/2DhnLGDdEECo4ys

2. Navigate to: `UNSW-NB15 - CSV Files`

3. Download:
   - `UNSW-NB15_1.csv` → Rename to `UNSW_NB15_training-set.csv`
   - `UNSW-NB15_2.csv` → Rename to `UNSW_NB15_testing-set.csv`

4. Place in `backend/datasets/`

---

## Dataset Information

### Training Set
- **Filename:** `UNSW_NB15_training-set.csv`
- **Size:** ~56 MB
- **Rows:** 175,341 network flows
- **Columns:** 49 features + labels
- **Purpose:** Train ML models

### Testing Set
- **Filename:** `UNSW_NB15_testing-set.csv`
- **Size:** ~27 MB
- **Rows:** 82,332 network flows
- **Columns:** 49 features + labels
- **Purpose:** Real-time streaming simulation

---

## File Structure

After download, your directory should look like:

```
backend/
└── datasets/
    ├── UNSW_NB15_training-set.csv  ✅ (175,341 rows)
    ├── UNSW_NB15_testing-set.csv   ✅ (82,332 rows)
    ├── unsw_loader.py
    ├── generate_datasets.py
    ├── email_dataset.csv
    ├── login_dataset.csv
    ├── malware_dataset.csv
    └── network_dataset.csv
```

---

## Verification

### Check Files Exist

**Windows:**
```bash
dir backend\datasets\UNSW_NB15_*.csv
```

**Linux/Mac:**
```bash
ls -lh backend/datasets/UNSW_NB15_*.csv
```

### Expected Output:
```
UNSW_NB15_training-set.csv  (56 MB)
UNSW_NB15_testing-set.csv   (27 MB)
```

### Verify Content

**Python:**
```python
import pandas as pd

# Check training set
train = pd.read_csv('backend/datasets/UNSW_NB15_training-set.csv')
print(f"Training rows: {len(train)}")
print(f"Columns: {len(train.columns)}")

# Check testing set
test = pd.read_csv('backend/datasets/UNSW_NB15_testing-set.csv')
print(f"Testing rows: {len(test)}")
print(f"Columns: {len(test.columns)}")
```

**Expected Output:**
```
Training rows: 175341
Columns: 49
Testing rows: 82332
Columns: 49
```

---

## Dataset Features (49 total)

### Network Flow Features
1. `srcip` - Source IP address
2. `sport` - Source port
3. `dstip` - Destination IP address
4. `dsport` - Destination port
5. `proto` - Protocol (tcp, udp, etc.)
6. `state` - Connection state
7. `dur` - Duration
8. `sbytes` - Source bytes
9. `dbytes` - Destination bytes
10. `sttl` - Source TTL
11. `dttl` - Destination TTL
12. `sloss` - Source packets lost
13. `dloss` - Destination packets lost
14. `service` - Service type
15. `Sload` - Source load
16. `Dload` - Destination load
17. `Spkts` - Source packets
18. `Dpkts` - Destination packets
19. `swin` - Source window size
20. `dwin` - Destination window size
21. `stcpb` - Source TCP base sequence
22. `dtcpb` - Destination TCP base sequence
23. `smeansz` - Source mean packet size
24. `dmeansz` - Destination mean packet size
25. `trans_depth` - Transaction depth
26. `res_bdy_len` - Response body length

### Behavioral Features
27. `Sjit` - Source jitter
28. `Djit` - Destination jitter
29. `Stime` - Start time
30. `Ltime` - Last time
31. `Sintpkt` - Source inter-packet time
32. `Dintpkt` - Destination inter-packet time
33. `tcprtt` - TCP round-trip time
34. `synack` - SYN-ACK time
35. `ackdat` - ACK-DAT time

### Connection Features
36. `is_sm_ips_ports` - Same IPs and ports
37. `ct_state_ttl` - Connection state TTL
38. `ct_flw_http_mthd` - Flow HTTP method
39. `is_ftp_login` - FTP login
40. `ct_ftp_cmd` - FTP command count
41. `ct_srv_src` - Service connections (source)
42. `ct_srv_dst` - Service connections (dest)
43. `ct_dst_ltm` - Destination lifetime
44. `ct_src_ltm` - Source lifetime
45. `ct_src_dport_ltm` - Source-dest port lifetime
46. `ct_dst_sport_ltm` - Dest-source port lifetime
47. `ct_dst_src_ltm` - Dest-source lifetime

### Labels
48. `attack_cat` - Attack category (Normal, DoS, Exploit, etc.)
49. `Label` - Binary label (0=Normal, 1=Attack)

---

## Attack Categories in Dataset

| Category | Count (approx) | Severity |
|----------|----------------|----------|
| Normal | ~56,000 | - |
| Generic | ~40,000 | Medium |
| Exploits | ~33,000 | High |
| Fuzzers | ~18,000 | Medium |
| DoS | ~12,000 | High |
| Reconnaissance | ~10,000 | Medium |
| Analysis | ~2,000 | Medium |
| Backdoor | ~1,700 | High |
| Shellcode | ~1,100 | High |
| Worms | ~130 | High |

---

## Troubleshooting

### "File not found" Error

**Problem:**
```
FileNotFoundError: Dataset not found: backend/datasets/UNSW_NB15_training-set.csv
```

**Solutions:**
1. Check file is in correct directory
2. Check filename spelling (case-sensitive)
3. Check file extension is `.csv` not `.csv.txt`
4. Re-download if file is corrupted

### "Permission denied" Error

**Problem:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
1. Close Excel/CSV viewers
2. Run terminal as administrator
3. Check file permissions

### "Encoding error" or "UnicodeDecodeError"

**Problem:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solution:**
Re-download the file - it may be corrupted

### File Size Mismatch

**Expected Sizes:**
- Training: ~56 MB (175,341 rows)
- Testing: ~27 MB (82,332 rows)

**If different:**
- Re-download the file
- Check you downloaded the correct version

---

## Alternative Datasets

If UNSW-NB15 is unavailable, you can use:

1. **NSL-KDD** - Classic intrusion detection dataset
2. **CICIDS2017** - Canadian Institute for Cybersecurity
3. **KDD Cup 99** - Original network intrusion dataset

**Note:** Code modifications required for alternative datasets.

---

## Citation

If using UNSW-NB15 in research, cite:

```
Moustafa, Nour, and Jill Slay. "UNSW-NB15: a comprehensive data set for 
network intrusion detection systems (UNSW-NB15 network data set)." 
Military Communications and Information Systems Conference (MilCIS), 2015. 
IEEE, 2015.
```

---

## Next Steps

After downloading:

1. ✅ Verify files are in `backend/datasets/`
2. ✅ Run setup: `python setup_unsw_system.py`
3. ✅ Train models: `python backend/ml/train_unsw_models.py`
4. ✅ Start system: `2_START_UNSW_BACKEND.bat`

---

**Need Help?** Check `UNSW_NB15_GUIDE.md` for complete documentation.
